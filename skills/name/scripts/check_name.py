#!/usr/bin/env python3
"""
check_name.py — availability snapshot for one or more candidate names.

Pure Python 3.11+ standard library. Checks, per name:

  * domains      RDAP (IANA bootstrap -> registry server, rdap.org fallback), DNS fallback
  * github       user/org name, and optionally ORG/NAME as a repository
  * appstore     Apple's public iTunes Search API — exact and near title matches
  * play         Google Play search page, best effort (no public API exists)
  * package id   an exact Android package id on Google Play (optional)

and prints ready-made links for the checks that must stay manual: trademark registers
and social handles.

Every result is one of  taken / looks free / unknown  plus a note. "looks free" is
evidence as of right now, never a reservation and never a trademark clearance.

Usage:
  python3 check_name.py NAME [NAME ...] [--tld com,app,ch] [--github-org ORG]
                        [--country us,ch] [--package-id ID] [--json] [--dry-run]
  python3 check_name.py --self-test
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import date
from html import unescape

TIMEOUT = 12
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36 studio-name-check/1.0")
IANA_BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

TAKEN, FREE, UNKNOWN = "taken", "looks free", "unknown"


@dataclass
class Result:
    check: str
    target: str
    status: str
    note: str = ""
    link: str = ""


@dataclass
class NameReport:
    name: str
    slug: str
    results: list[Result] = field(default_factory=list)
    links: dict[str, str] = field(default_factory=dict)


# ----------------------------------------------------------------------------- helpers

def slugify(name: str) -> str:
    """Lowercase, letters/digits only — what you'd type into a domain or handle."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def http(url: str, accept: str = "*/*") -> tuple[int, bytes, str]:
    """Return (status, body, error). Never raises; status 0 means no HTTP answer."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept,
                                               "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status, resp.read(), ""
    except urllib.error.HTTPError as e:
        try:
            body = e.read()
        except Exception:  # noqa: BLE001
            body = b""
        return e.code, body, ""
    except Exception as e:  # noqa: BLE001 — network, TLS, proxy, timeout
        return 0, b"", f"{type(e).__name__}: {e}"[:120]


# ----------------------------------------------------------------------------- classifiers
# Kept free of I/O so --self-test can exercise them with canned responses.

def classify_rdap(status: int, err: str) -> tuple[str, str]:
    if status == 404:
        return FREE, "no RDAP registration"
    if status == 200:
        return TAKEN, "registered (RDAP)"
    if status == 429:
        return UNKNOWN, "RDAP rate-limited, retry later"
    if status == 0:
        return UNKNOWN, f"no answer ({err or 'network'})"
    return UNKNOWN, f"RDAP HTTP {status}"


def classify_dns(resolved: bool | None) -> tuple[str, str]:
    if resolved is True:
        return TAKEN, "resolves in DNS"
    if resolved is False:
        return UNKNOWN, "no DNS record (unresolved is not unregistered)"
    return UNKNOWN, "DNS lookup failed"


def classify_github(status: int, err: str, body: bytes = b"") -> tuple[str, str]:
    if status == 404:
        return FREE, "no such user/org/repo"
    if status == 200:
        return TAKEN, "exists on GitHub"
    if status in (403, 429):
        if b"rate limit" in body.lower():
            return UNKNOWN, "GitHub API rate limit (60/h unauthenticated) — check the link by hand"
        return UNKNOWN, f"GitHub HTTP {status} (blocked or proxied) — check the link by hand"
    if status == 0:
        return UNKNOWN, f"no answer ({err or 'network'})"
    return UNKNOWN, f"GitHub HTTP {status}"


def classify_appstore(name: str, payload: dict | None, status: int, err: str) -> tuple[str, str]:
    if payload is None:
        if status == 0:
            return UNKNOWN, f"no answer ({err or 'network'})"
        return UNKNOWN, f"iTunes Search HTTP {status}"
    want = normalize_title(name)
    word = re.compile(r"\b" + re.escape(name.lower()) + r"\b")
    exact, near = [], []
    for app in payload.get("results", []):
        title = str(app.get("trackName", ""))
        seller = str(app.get("sellerName", ""))
        label = f"{title} ({seller})" if seller else title
        if normalize_title(title) == want:
            exact.append(label)
        elif word.search(title.lower()):
            near.append(label)
    if exact:
        return TAKEN, "exact title: " + "; ".join(exact[:3])
    if near:
        return UNKNOWN, "no exact title, near: " + "; ".join(near[:3])
    return FREE, "no published app with this title (unpublished records are invisible)"


PLAY_TITLE_RES = (
    re.compile(r'href="/store/apps/details\?id=[^"]*"[^>]*?aria-label="([^"]*)"'),  # top hit
    re.compile(r'class="DdYX5">([^<]*)<'),                                            # list cards
)


def play_titles(html: str) -> list[str]:
    """App titles on the rendered result cards, deduplicated, in page order.

    Only the cards count: the page also echoes the query into <title>, og: tags and its
    data payload, so matching the raw page sees the name on every search."""
    seen: dict[str, None] = {}
    for rx in PLAY_TITLE_RES:
        for t in rx.findall(html):
            seen.setdefault(unescape(t).strip(), None)
    return [t for t in seen if t]


def classify_play(name: str, status: int, html: str, err: str) -> tuple[str, str]:
    if status == 0:
        return UNKNOWN, f"no answer ({err or 'network'})"
    if status != 200:
        return UNKNOWN, f"Play HTTP {status} — open the link and look"
    if len(html) < 2000:
        return UNKNOWN, "Play returned an empty/JS-only page — open the link and look"
    titles = play_titles(html)
    if not titles:
        return UNKNOWN, "no result cards found (Play layout may have changed) — open the link and look"
    want = normalize_title(name)
    prefix = re.compile(re.escape(name) + r"[\s:\-–—|]", re.IGNORECASE)
    exact = [t for t in titles if normalize_title(t) == want]
    near = [t for t in titles if t not in exact and prefix.match(t)]
    if exact:
        return TAKEN, "exact title in Play results: " + "; ".join(exact[:3]) + " (best effort — verify)"
    if near:
        return UNKNOWN, "no exact title, near: " + "; ".join(near[:3]) + " (best effort — verify)"
    return FREE, "name not seen in Play search results (best effort; Play titles need not be unique)"


def classify_package(status: int, err: str) -> tuple[str, str]:
    if status == 404:
        return FREE, "no app with this package id"
    if status == 200:
        return TAKEN, "an app uses this package id"
    if status == 0:
        return UNKNOWN, f"no answer ({err or 'network'})"
    return UNKNOWN, f"Play HTTP {status}"


# ----------------------------------------------------------------------------- checks

_bootstrap_cache: dict[str, str] | None = None


def rdap_servers() -> dict[str, str]:
    """tld -> RDAP base URL from IANA's bootstrap file; empty dict when unreachable."""
    global _bootstrap_cache
    if _bootstrap_cache is not None:
        return _bootstrap_cache
    servers: dict[str, str] = {}
    status, body, _ = http(IANA_BOOTSTRAP, "application/json")
    if status == 200:
        try:
            for tlds, urls in json.loads(body).get("services", []):
                for tld in tlds:
                    servers[tld.lower()] = urls[0].rstrip("/") + "/"
        except Exception:  # noqa: BLE001
            servers = {}
    _bootstrap_cache = servers
    return servers


def check_domain(slug: str, tld: str) -> Result:
    domain = f"{slug}.{tld}"
    link = f"https://{domain}"
    base = rdap_servers().get(tld)
    tried = []
    for url in ([f"{base}domain/{domain}"] if base else []) + [f"https://rdap.org/domain/{domain}"]:
        status, _, err = http(url, "application/rdap+json")
        st, note = classify_rdap(status, err)
        tried.append(f"{urllib.parse.urlparse(url).netloc}:{status or 'x'}")
        if st != UNKNOWN:
            return Result("domain", domain, st, note, link)
    # DNS fallback — only ever confirms "taken".
    try:
        socket.getaddrinfo(domain, 443)
        resolved: bool | None = True
    except socket.gaierror:
        resolved = False
    except Exception:  # noqa: BLE001
        resolved = None
    st, note = classify_dns(resolved)
    return Result("domain", domain, st, f"{note}; RDAP tried {', '.join(tried)}", link)


def check_github_user(slug: str) -> Result:
    status, body, err = http(f"https://api.github.com/users/{slug}", "application/vnd.github+json")
    st, note = classify_github(status, err, body)
    return Result("github", slug, st, note, f"https://github.com/{slug}")


def check_github_repo(org: str, slug: str) -> Result:
    status, body, err = http(f"https://api.github.com/repos/{org}/{slug}", "application/vnd.github+json")
    st, note = classify_github(status, err, body)
    return Result("github-repo", f"{org}/{slug}", st, note, f"https://github.com/{org}/{slug}")


def check_appstore(name: str, country: str) -> Result:
    q = urllib.parse.urlencode({"term": name, "entity": "software", "limit": 50, "country": country})
    url = f"https://itunes.apple.com/search?{q}"
    status, body, err = http(url, "application/json")
    payload = None
    if status == 200:
        try:
            payload = json.loads(body)
        except Exception:  # noqa: BLE001
            payload = None
    st, note = classify_appstore(name, payload, status, err)
    return Result("appstore", f"{name} [{country}]", st, note, url)


def check_play(name: str) -> Result:
    url = "https://play.google.com/store/search?" + urllib.parse.urlencode({"q": name, "c": "apps", "hl": "en"})
    status, body, err = http(url, "text/html")
    st, note = classify_play(name, status, body.decode("utf-8", "replace"), err)
    return Result("play", name, st, note, url)


def check_package(package_id: str) -> Result:
    url = "https://play.google.com/store/apps/details?" + urllib.parse.urlencode({"id": package_id})
    status, _, err = http(url, "text/html")
    st, note = classify_package(status, err)
    return Result("play-package", package_id, st, note, url)


def manual_links(name: str, slug: str) -> dict[str, str]:
    q = urllib.parse.quote(name)
    return {
        "Web search (companies, brands)": f"https://www.google.com/search?q=%22{q}%22",
        "USPTO trademark search (US)": "https://tmsearch.uspto.gov/search/search-information",
        "TMview (EU + national registers)": "https://www.tmdn.org/tmview/",
        "EUIPO eSearch": f"https://euipo.europa.eu/eSearch/#basic/1+1+1+1/100+100+100+100/{q}",
        "WIPO Global Brand Database": "https://branddb.wipo.int/",
        "Swissreg (CH)": "https://www.swissreg.ch/",
        "Google Play search": f"https://play.google.com/store/search?q={q}&c=apps",
        "App Store via web search": f"https://www.google.com/search?q=site%3Aapps.apple.com+%22{q}%22",
        "Instagram": f"https://www.instagram.com/{slug}/",
        "X": f"https://x.com/{slug}",
        "TikTok": f"https://www.tiktok.com/@{slug}",
        "YouTube": f"https://www.youtube.com/@{slug}",
        "Bluesky": f"https://bsky.app/profile/{slug}.bsky.social",
        "Mastodon (mastodon.social)": f"https://mastodon.social/@{slug}",
    }


# ----------------------------------------------------------------------------- runner

def plan(name: str, args: argparse.Namespace) -> list[tuple[str, callable, tuple]]:
    slug = slugify(name)
    jobs: list[tuple[str, callable, tuple]] = []
    for tld in args.tlds:
        jobs.append((f"domain {slug}.{tld}", check_domain, (slug, tld)))
    jobs.append((f"github user/org {slug}", check_github_user, (slug,)))
    if args.github_org:
        jobs.append((f"github repo {args.github_org}/{slug}", check_github_repo, (args.github_org, slug)))
    for cc in args.countries:
        jobs.append((f"app store [{cc}] {name}", check_appstore, (name, cc)))
    jobs.append((f"google play {name}", check_play, (name,)))
    return jobs


def run(names: list[str], args: argparse.Namespace) -> list[NameReport]:
    reports = []
    all_jobs: list[tuple[int, str, callable, tuple]] = []
    for i, name in enumerate(names):
        rep = NameReport(name=name, slug=slugify(name), links=manual_links(name, slugify(name)))
        reports.append(rep)
        for label, fn, fargs in plan(name, args):
            all_jobs.append((i, label, fn, fargs))
    if args.package_id:
        all_jobs.append((0, f"package {args.package_id}", check_package, (args.package_id,)))

    if args.dry_run:
        for i, label, _, _ in all_jobs:
            reports[i].results.append(Result("plan", label, UNKNOWN, "dry run — not checked"))
        return reports

    rdap_servers()  # warm the bootstrap once, before the threads start
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(fn, *fargs): i for i, _, fn, fargs in all_jobs}
        for fut in cf.as_completed(futs):
            i = futs[fut]
            try:
                reports[i].results.append(fut.result())
            except Exception as e:  # noqa: BLE001
                reports[i].results.append(Result("error", "", UNKNOWN, f"{type(e).__name__}: {e}"[:120]))
    for rep in reports:
        rep.results.sort(key=lambda r: (r.check, r.target))
    return reports


def render(reports: list[NameReport], dry_run: bool) -> str:
    out = [f"# Name availability snapshot — {date.today().isoformat()}", ""]
    out.append("Evidence, not clearance: 'looks free' is what is visible right now. "
               "Trademarks and handles need a human look (links below).")
    out.append("")
    out.append("Not covered: companies or brands with no store listing, and sound-alike names. "
               "Search the web for those before trusting any 'looks free'.")
    for rep in reports:
        out += ["", f"## {rep.name}  (slug: `{rep.slug}`)", ""]
        if dry_run:
            out.append("Planned checks:")
            out += [f"- {r.target}" for r in rep.results]
        else:
            out += ["| Check | Target | Status | Note |", "| --- | --- | --- | --- |"]
            for r in rep.results:
                tgt = f"[{r.target}]({r.link})" if r.link else r.target
                out.append(f"| {r.check} | {tgt} | **{r.status}** | {r.note} |")
            counts = {s: sum(1 for r in rep.results if r.status == s) for s in (TAKEN, FREE, UNKNOWN)}
            out.append("")
            out.append(f"Summary: {counts[TAKEN]} taken · {counts[FREE]} look free · {counts[UNKNOWN]} unknown")
        out += ["", "Manual checks (open and look):"]
        out += [f"- {k}: {v}" for k, v in rep.links.items()]
    return "\n".join(out)


# ----------------------------------------------------------------------------- self-test

def self_test() -> int:
    failures = []

    def expect(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got!r}, want {want!r}")

    expect("slugify", slugify("Moss Ling!"), "mossling")
    expect("rdap 404", classify_rdap(404, "")[0], FREE)
    expect("rdap 200", classify_rdap(200, "")[0], TAKEN)
    expect("rdap 0", classify_rdap(0, "timeout")[0], UNKNOWN)
    expect("rdap 429", classify_rdap(429, "")[0], UNKNOWN)
    expect("dns true", classify_dns(True)[0], TAKEN)
    expect("dns false", classify_dns(False)[0], UNKNOWN)
    expect("gh 404", classify_github(404, "")[0], FREE)
    expect("gh 403 blocked", classify_github(403, "")[0], UNKNOWN)
    expect("gh 403 ratelimit", "rate limit" in classify_github(403, "", b'{"message":"API rate limit exceeded"}')[1], True)
    expect("gh 403 proxy", "blocked" in classify_github(403, "", b"forbidden")[1], True)
    payload = {"results": [
        {"trackName": "Mossling: Plant Care", "sellerName": "Someone"},
        {"trackName": "Plant Buddy", "sellerName": "X"},
    ]}
    expect("appstore near", classify_appstore("Mossling", payload, 200, "")[0], UNKNOWN)
    payload["results"].append({"trackName": "MossLing", "sellerName": "Y"})
    expect("appstore exact", classify_appstore("Mossling", payload, 200, "")[0], TAKEN)
    expect("appstore free", classify_appstore("Zorblat", payload, 200, "")[0], FREE)
    expect("appstore nohit", classify_appstore("Mossling", None, 0, "x")[0], UNKNOWN)
    # Every real Play page echoes the query back (title, og: tags, data payload); only the
    # result cards may decide the verdict.
    echo = ('<title id="main-title">Mossling - Android Apps on Google Play</title>'
            "request:[\"Mossling\",4,[1]]},[\"Mossling\"],4" + "x" * 2500)
    top = '<a href="/store/apps/details?id=com.a.b" aria-label="{}">'
    card = '<span class="DdYX5">{}</span>'
    html_exact = echo + top.format("MossLing") + card.format("Plant Buddy")
    html_pref = echo + card.format("Mossling: Water &amp; Light")
    html_none = echo + top.format("AI Symposium") + card.format("My SequelCare")
    html_nocards = echo
    expect("play exact", classify_play("Mossling", 200, html_exact, "")[0], TAKEN)
    expect("play prefix", classify_play("Mossling", 200, html_pref, "")[0], UNKNOWN)
    expect("play prefix unescaped", "Water & Light" in classify_play("Mossling", 200, html_pref, "")[1], True)
    expect("play none despite echo", classify_play("Mossling", 200, html_none, "")[0], FREE)
    expect("play no cards", classify_play("Mossling", 200, html_nocards, "")[0], UNKNOWN)
    expect("play short", classify_play("Mossling", 200, "<html></html>", "")[0], UNKNOWN)
    expect("play 429", classify_play("Mossling", 429, "", "")[0], UNKNOWN)
    expect("package 404", classify_package(404, "")[0], FREE)
    links = manual_links("Mossling", "mossling")
    expect("links instagram", links["Instagram"], "https://www.instagram.com/mossling/")

    if failures:
        print("SELF-TEST FAILED")
        print("\n".join(failures))
        return 1
    print("self-test ok")
    return 0


# ----------------------------------------------------------------------------- main

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("names", nargs="*", help="candidate names (quote names with spaces)")
    p.add_argument("--tld", default="com,app", help="comma-separated TLDs (default: com,app)")
    p.add_argument("--github-org", default="", help="also check ORG/NAME as a repository")
    p.add_argument("--country", default="us", help="comma-separated App Store storefronts (default: us)")
    p.add_argument("--package-id", default="", help="exact Android package id to check on Google Play")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    p.add_argument("--dry-run", action="store_true", help="print the plan and links, no network")
    p.add_argument("--self-test", action="store_true", help="run the built-in parser tests")
    a = p.parse_args(argv)
    a.tlds = [t.strip().lower().lstrip(".") for t in a.tld.split(",") if t.strip()]
    a.countries = [c.strip().lower() for c in a.country.split(",") if c.strip()]
    return a


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.self_test:
        return self_test()
    if not args.names:
        print("give at least one name (or --self-test)", file=sys.stderr)
        return 2
    reports = run(args.names, args)
    if args.json:
        print(json.dumps({"date": date.today().isoformat(),
                          "reports": [asdict(r) for r in reports]}, indent=2, ensure_ascii=False))
    else:
        print(render(reports, args.dry_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
