# Availability checks — what each one proves, and what it doesn't

Read this before interpreting the checker's output or any manual lookup. The single rule:
**these checks produce evidence, not clearance.** Phrase every result as "looks free as of
<date>", and always say what was *not* checked.

## The checker script

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_name.py NAME [NAME ...] [options]

  --tld com,app,ch        TLDs to check (default: com,app)
  --github-org ORG        also check ORG/NAME as a repo
  --country us,ch,fr      App Store storefronts to search (default: us)
  --package-id ID         check an exact Android package id on Google Play
  --json                  machine-readable output
  --dry-run               print the plan and the manual links, no network
  --self-test             run the built-in parser tests
```

Pure Python 3.11+ standard library, nothing to install. Several names in one call run in
parallel. Each result is one of **taken / looks free / unknown**, with a note.

## What each check means

### Domains (RDAP, DNS fallback)

- **How:** the Registration Data Access Protocol — the modern, structured replacement for
  WHOIS. The script reads IANA's bootstrap list to find each TLD's RDAP server and asks
  for the domain. HTTP 404 = no registration = *looks free*; 200 = *taken*. If a TLD has
  no RDAP server (a few country TLDs), it falls back to `rdap.org`, then to a DNS lookup:
  a domain that resolves is taken; one that doesn't is only *unknown* (unresolved is not
  unregistered).
- **Doesn't prove:** that you can buy it. Premium pricing, registry reservations, and
  someone registering it an hour later are all invisible here. **Buy the domain the day
  you decide.**
- **For a mobile app:** the store listing is the front door. A taken `.com` is a
  trade-off, not a kill — `.app` (HTTPS-only, good for apps), `get<name>.com`, or
  `<studio>.com/<name>` are normal. Score it; don't panic.

### GitHub (user/org and repo)

- **How:** the public API. 404 = free; 200 = taken; 403 = rate-limited (60 unauthenticated
  calls per hour per IP) → *unknown*, retry later or check `https://github.com/<name>` by hand.
- **Matters for:** a public repo or org named after the product. Renaming a repo later
  is cheap (GitHub redirects), so this is low-stakes.

### App Store (Apple)

- **How:** Apple's public iTunes Search API, no key needed:
  `https://itunes.apple.com/search?term=<name>&entity=software&country=<cc>`. The script
  reports **exact** title matches (title equals the name, ignoring case, spaces and
  punctuation) and **near** matches (the name is a whole word in the title, e.g.
  "Mossling: Plant Care").
- **The rule that matters:** Apple enforces **unique app names** per storefront — but
  only when you create the app record in App Store Connect, which needs a paid developer
  membership. So "no exact match found" is a good sign, not a guarantee: an app can be
  registered but not yet published, and the search API only sees published apps.
- **Check more than one storefront** when the roadmap has several markets (`--country
  us,ch,fr,de`); an app published only in France won't show in the US search.

### Google Play

- **How:** Google has **no public search API**. The script fetches the Play search page
  for the name and reads the titles on the result cards (exact title → *taken*, "Name: …"
  → *unknown* with the near matches listed). It ignores the rest of the page, which
  echoes the query everywhere. It is *best effort* and says *unknown* when Google serves
  a JavaScript-only page, blocks the request, or the card layout changes.
  Always open the printed link and look with your own eyes, and run the WebSearch
  `"<name>" site:play.google.com` as well.
- **The rule that matters:** Google Play does **not** require unique titles. Two apps can
  share a name. So the question on Play is not "is it free?" but "**will people find mine
  among the others?**" A name shared with an established app with millions of installs
  is a findability problem even though nothing stops you publishing.
- **Package id** (`--package-id com.studio.thing`): the details page returns 404 if no
  app uses that id. Remember the id is **permanent once published** — see the placeholder
  rules in SKILL.md.

### Trademarks — links only, human judgment required

The script prints links; it never queries registers. Open them and search the name as a
word mark, looking at **live** marks in the classes that cover software and apps
(Nice classes **9** software, **42** software services; **44** if health-related,
**41** if education):

- **USPTO Trademark Search** (US federal register).
- **TMview** (EU and many national registers at once) and **EUIPO**.
- **WIPO Global Brand Database** (international).
- The studio's **national register** when outside the US (e.g. Swissreg for Switzerland).

Report what you see: "no live US or EU marks for <name> in class 9/42 on <date>; one
dead mark from 2014; a live mark in class 25 (clothing), different field." Never write
"trademark clear". Similar-sounding or similar-looking marks in the same field matter as
much as identical ones — that assessment is exactly what a trademark attorney's knockout
search is for, and it is cheap compared to a forced rename after launch.

### Social handles — links only

Platforms block automated lookups and rate-limit aggressively, so the script just prints
the profile URLs (Instagram, X, TikTok, YouTube, Bluesky, Mastodon). Open the ones the
brief says matter. A taken handle is a mild negative; `<name>app` or `<studio>.<name>` are
common fallbacks.

## Reading the whole picture

| Signal | Weight in the decision |
| --- | --- |
| Direct competitor with the same name in the same category | **Kill** |
| Company or brand with the name in the same field, even with no store listing | **Kill** |
| Sound-alike or one-letter variant in the same category | Very strong negative |
| Live trademark, same name, same class, same market | **Kill** (or attorney first) |
| Exact App Store title match, same category | Very strong negative |
| Established Play app with the same name | Strong negative (findability) |
| `.com` taken, parked or unrelated | Trade-off; prefer `.app` or a prefix |
| Exact title match in an unrelated category | Mild negative; note it |
| GitHub / handle taken | Mild negative |
| Any check `unknown` | Say so, link it, don't guess |

**What no check here sees:** companies and brands without a live store listing, and
sound-alike names. The checker can report "looks free" everywhere for a name a funded
company already uses. Those come from the web searches in the skill's step 4, which run
*before* the checker.

Availability is a **snapshot**. If the user picks a name, the next step is to buy the
domain and claim the handles the same day, then log the decision with the check date.
