---
name: name
description: >-
  Name an app, product, or project — in two phases. **Placeholder** (a working codename
  so you can start today without baking a name into permanent places), and **final** (a
  real naming round: brief, metaphor territories, candidates, filtering, live availability
  checks for domains / GitHub / App Store / Google Play plus trademark and social-handle
  links, a scored shortlist with origin stories, and a written record). Use whenever the
  user invokes /studio:name, or says "I need a name for <thing>", "give me a working name",
  "codename for my new app", "placeholder name", "it's time to name this for real", "is
  <name> taken", "check if <name> is available", "rename <placeholder> before launch",
  "help me pick between these names", or starts a project and has no name yet. Works for a
  studio project (writes to reference/naming/ and decisions/log.md) and for the docked
  business track of a code repo (writes to docs/business/naming/ and
  docs/business/decisions/log.md). The checks are evidence, never clearance: a name is
  "looks free", never "cleared" — trademark review stays with the user. Pairs with
  studio:new-project (placeholder at kickoff) and studio:scope (final name as a launch
  rabbit hole). Not for naming things inside code — variables, functions, files, specs,
  or branches.
---

# Name

Naming has two moments, and they want opposite things.

At the **start** of a project the name doesn't matter yet and agonising over it is
procrastination. What matters is having *something* to call it, and not letting that
something leak into places you can't change later. That's **placeholder** mode: fast,
cheap, deliberately disposable.

When the project is **on its track** and a launch is in sight, the name suddenly matters a
lot: it goes on the store listing, the domain, the legal pages, the logo, and into
people's mouths. That's **final** mode: a proper round with research, real checks, and a
written record of why — so the choice is never re-argued.

Pick the mode from what the user said. "Working name", "codename", "placeholder", "just
to start" → placeholder. "For real", "before launch", "is X taken", "final name" → final.
Unsure → ask which moment they're in; it's one question.

## Where things live

- **Studio project:** the naming record goes in `reference/naming/<slug>.md`; the chosen
  name (placeholder or final) is logged in `decisions/log.md`.
- **Docked business track in a code repo** (see new-project's docked mode): the record
  goes in `docs/business/naming/<slug>.md` and the decision in
  `docs/business/decisions/log.md`. Read the repo's vision doc (e.g.
  `docs/product-vision.md`) in place of `brief.md`.
- **A studio with several products** (one company name, many apps): the *company's*
  decision log holds the placeholder convention and the list of working names; each
  product's own project holds its naming record.

If there is no studio project or docked track at all, still do the work — just hand the
record back as text and offer **studio:new-project** to give it a home.

---

## Placeholder mode — a working name in five minutes

The goal is a label the user won't mind saying for the next few months, that is clearly
*not* the final name, and that doesn't get welded into anything permanent.

1. **Use the convention if there is one.** Look in the decision log for a "placeholder
   convention" entry. If none exists, offer to set one now — a theme to draw codenames
   from (Swiss mountains, knitting stitches, constellations, spices, whatever makes
   the user smile). One plain word per project, no two alike. A theme makes codenames
   instantly recognisable as codenames. Log the convention once; reuse it forever.
   If the user prefers a plain descriptive working name ("plant watering app"), that's
   fine too — the point is speed, not cleverness.

2. **Pick one, with a 10-second collision check.** Grep the user's existing projects and
   decision logs so no two products share a codename. No web research in this mode —
   that's the whole point. If the user already arrived with a working name (they usually
   have), keep it; just do the next two steps.

3. **Fence it off.** Tell the user the three places a placeholder must *not* go, because
   they are permanent or expensive to change:
   - **Store identifiers:** the Android `applicationId` / package name and the iOS bundle
     ID can never change once an app is published. Either run **final mode before the
     first store upload**, or choose an identifier you can live with forever (the studio's
     reverse domain plus a neutral word, e.g. `com.<studio>.<neutral>`), never the
     codename.
   - **Legal and public text:** privacy policy, terms, store listing copy, the website —
     keep the codename out of anything a customer or a regulator reads.
   - **Bought things:** domains, trademarks, paid handles. Don't spend money on a name
     you intend to drop.
   Everywhere else (repo name, folder, chat, docs) the codename is fine. Note the
   policy "every product name is a working name until a final-mode round says otherwise"
   in the decision log if it isn't there already.

4. **Log it and move on.** One decision-log entry: *"Working name: <codename>, from the
   <theme> convention. Not final. Revisit before the first store upload / launch."*
   Then hand back to whatever the user was doing — usually **studio:new-project** or
   **studio:scope**. Placeholder mode should feel like a two-minute detour, not a
   session.

---

## Final mode — a real naming round

This is a research session. Expect to use WebSearch, the bundled checker script, and a
good hour of the user's attention across a couple of sittings. Load
[reference/naming-craft.md](reference/naming-craft.md) for the craft (what makes a name
stick, what kills one, how to score) and [reference/checks.md](reference/checks.md) for
what each availability check does and doesn't prove.

### 1. The brief — read first, ask only the gaps

Read the north star (`brief.md` or the repo's vision doc) and the product's own brief or
README. Most of the naming brief is already there. Ask only what's missing, a few
questions at a time:

- **What it does**, in one plain sentence, and **who it's for**.
- **How the name should feel** — warm, playful, calm, clinical, clever? Words that fit
  and words to avoid.
- **Family or standalone** — does it carry the studio's name ("<Studio> <Thing>"), echo
  the studio's style, or stand alone? Look at how the studio's existing names feel.
- **Languages that matter** — the markets on the roadmap (e.g. English, French, Spanish,
  German). A name must be sayable in all of them and mean nothing silly or rude in any.
- **Platforms that matter** — which TLDs (`.com`? `.app`? the studio's country TLD?),
  which stores, GitHub, which social handles. This decides which checks are mandatory.
- **Off-limits** — words, styles, competitor echoes, anything already rejected.

### 2. Territories, not thesaurus

Before any names, map two or three **metaphor territories**: what else in the world
works like this product? (A plant-care app is a *gardener*, a *ritual*, a *pocket
greenhouse*, a *weather vane*…) When the brief is clear, pick the territories yourself and
explain them later; only ask the user to choose when two directions are genuinely tied.

### 3. Generate, filter, shortlist — internally

Produce 30+ candidates across the territories (real words, grounded compounds, modified
words, words from the languages that matter, sound-first inventions). Then cut hard with
the anti-pattern checklist in naming-craft.md: no suffix slop, no empty compounds, no
thesaurus words, nothing that fails the phone test, nothing with a bad meaning in a
market language. Keep **six to eight semifinalists**. Don't show the raw list — the user
should meet only vetted names.

### 4. Collisions first, then the checker

For each semifinalist, **search for collisions before anything else** — it's the most
common kill, and it's cheaper than the other checks:

- WebSearch `"<name>" app` and `"<name>" <category>`. A direct competitor in the same
  space kills the name outright.
- WebSearch `"<name>" site:play.google.com` and `"<name>" site:apps.apple.com` to catch
  store listings that the name-matching below might miss.
- WebSearch `"<name>" company` and `"<name>" startup`. A company or brand using the name
  in the same field kills it even with **no store listing**: apps get delisted, and some
  never ship. The checker can't see these.
- Repeat the searches for **sound-alikes and one-letter spellings** (Mossling → Mosling,
  Mossleen, Mozling). Customers say names out loud, so a homophone in the same category is
  the same collision.

Then run the bundled checker on the survivors — several names in one call:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_name.py <name1> <name2> ... \
  --tld com,app,<country-tld> --github-org <studio-org> --country us,<market>
```

It reports, per name: domains (RDAP, with DNS as a fallback), GitHub user/org and a repo
under the studio's org, App Store exact and near matches (Apple's public search API),
Google Play best-effort matches, and ready-made links for the trademark registers and
social handles the script can't query. Add `--json` for machine-readable output,
`--dry-run` to see the plan and links without touching the network. Read
[reference/checks.md](reference/checks.md) for what each result means — in particular,
"looks free" is not "cleared", and a taken `.com` is rarely fatal for a mobile app.

**Trademarks are the user's call.** Open the register links the script prints (USPTO,
TMview/EUIPO, WIPO, the studio's national register) and look for live marks in the same
class (software, class 9/42). Report what you find plainly; never write "trademark
clear". If the name is going on a paid product, say once that a trademark attorney's
knockout search is cheap compared to a forced rename.

If fewer than three candidates survive, go back to step 3 and generate more. Don't lower
the bar to fill the shortlist.

### 5. Score and present three to five finalists

Score the survivors with the rubric in naming-craft.md, run the sentence tests ("Have you
tried ___?", "___ — <tagline>", "the ___ app"), and present the finalists the way a
naming agency would: the name, its 15-second origin story, which territory it came from,
its availability picture in one line, its trade-offs, and your recommendation. Side by
side, so the trade-offs are visible. The user decides.

### 6. Record it

Write the naming record from [templates/scorecard.md](templates/scorecard.md) to
`reference/naming/<slug>.md` (or `docs/business/naming/<slug>.md` when docked): the brief,
the territories, the finalists with scores and availability, the collisions found, the
decision and its why, and the **rename checklist** — every place the placeholder currently
lives (repo name, package identifier if not yet published, website, store listing drafts,
legal pages, logo files, docs, social handles) so the switch is one pass, not a month of
stragglers. When the user picks, add the decision-log entry: *"Final name: <name>.
Why. Alternatives considered. Checked on <date>: <one-line availability summary>."*

Then the obvious next steps, usually: buy the domain today (availability is a snapshot,
not a reservation), claim the handles, and — if a launch is being shaped — hand to
**studio:scope** so the rename lands in the right version.

---

## Judgment

- **Match the mode to the moment.** A full naming round on day one is procrastination
  dressed as diligence; a placeholder on launch day is a liability. Steer gently to the
  right mode when the user is in the wrong one.
- **Protect the permanent things.** The one real danger of a placeholder is that it
  leaks into a store identifier or a legal document. Say so every time, briefly.
- **Metaphor over description, story over vibe.** If you can't tell a 15-second story
  about why it's called that, it isn't ready. A description belongs in the tagline.
- **Evidence, not clearance.** The checker and your searches say what is *visible*
  today. They don't see pending trademarks, unlisted apps, or next week. Phrase results
  as "looks free as of <date>" and name what wasn't checked.
- **A taken .com is a trade-off, not a verdict.** For a mobile app the store listing is
  the front door; `<name>.app`, `get<name>.com` or `<studio>.com/<name>` can be fine.
  Score it; don't auto-kill it. Reserve auto-kills for a direct competitor or a live
  trademark in the same class.
- **Languages are a gate, not a nice-to-have.** If the roadmap says French and German
  are coming, a name that's a giggle in either one fails now, not later.
- **Show the vetted few, not the messy many.** The user's attention goes to deciding
  between good options, not to wading through forty.
- **Don't invent availability.** If the network, a rate limit, or a blocked host stops
  a check, report `unknown` and give the link — never guess from memory which names are
  taken.
- **Stay in your lane.** This skill names things and records why. It doesn't buy
  domains, file trademarks, design logos, or rename code — it hands the user a
  checklist and points at the right helper.
