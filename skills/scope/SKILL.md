---
name: scope
description: >-
  Shape a fast first version (MVP) of a studio project and triage everything else into
  later versions — the non-code cousin of release-shaping. Use whenever the user invokes
  /studio:scope, or says "what's the MVP", "help me ship something fast", "what should
  go in version 1 vs later", "triage this scope", "I'm overcomplicating this — cut it
  down", "what's the smallest thing I can launch", "shape the go-to-market for my
  app/product", "what's the smallest commercial version worth selling", "plan the launch
  for this code project", or has a pile of ideas/features for a project and needs to sort
  must-have-now from nice-to-have-later. Also shapes the **go-to-market / commercial**
  version of a code product that's docked a business track (audience, pricing, channels,
  launch) — distinct from jig/shaper, which own code-release shaping. Fixes the **appetite**
  (the time/attention budget) first and fits scope to it; names the **rabbit holes**
  (risky unknowns) and how each is handled; sorts every item four ways (**include /
  defer / split / risk-first**); and pins the point of v1, its definition of done, and
  target launch — writing it all to plan/roadmap.md. Plain-language, creative-project
  cousin of shaper's release-shaping (no JIG, specs, or repo machinery). Reads brief.md
  for the goal and audience. Shapes **any version, one at a time** — the first run produces
  the MVP; re-run it after each launch to shape v2, v3, … from the parked ideas, each with
  a fresh appetite. Naturally follows studio:new-project (set up → shape a version → build)
  and feeds studio:project-desk and studio:next-piece.
---

# Scope

The instinct on a project is to plan the *whole* thing — every feature, every flourish,
the polished end state — and then never ship because the whole thing is too big. This
skill exists to fight that. Its job: help the user shape **one version at a time** —
the smallest next thing worth shipping — get it out fast, and park everything else
honestly so nothing is lost but nothing blocks the launch.

**It shapes any version, not just v1.** The first time you run it, the version it shapes
*is* the MVP — the smallest first launch. After that ships, you run it again to shape v2
from the parked ideas, then v3, and so on. Each pass is a fresh, self-contained shaping:
its own appetite, its own rabbit holes, its own cutline. What it deliberately will *not*
do is shape all future versions up front — fixing the scope of a version you haven't
reached yet is the exact planning-forever trap it exists to kill. Shape the next one
when you're ready to commit to it.

It's the same discipline a good release-shaper brings to code, pointed at a creative or
business project: **fix how much time you'll spend, then fit the work to it** — decide
what's in, what's deliberately out, and why, and retire the scary unknowns before they
blow up. The output isn't a wish-list; it's a cut-list with a time budget and a launch
date.

## Also works for the business side of a code project

This skill isn't only for non-code projects. It also shapes the **commercial / launch**
version of a *code* product that's docked a business track (see new-project's docked
mode). When it does, draw the boundary cleanly:

- **jig / shaper own the code-release shaping** — which features ship in which build.
  Don't re-shape engineering work here; hand it back to them.
- **studio:scope owns the go-to-market shaping** — audience, pricing, channels, launch
  packaging, the smallest *commercial* version worth putting in front of buyers. That's
  what you triage here.
- Read the repo's existing vision doc (e.g. `docs/product-vision.md`) in place of
  `brief.md`, and write the shaped version to the docked `docs/business/roadmap.md`,
  logging the scope decision in `docs/business/decisions/log.md`.

## The north star comes first

Read `brief.md` (or, for a docked code project, the repo's vision doc such as
`docs/product-vision.md`) — especially the **goal** ("the point of doing this") and the
**audience**. The version you're shaping is the shortest next step toward *that* goal in
front of *that* audience — for v1 that's the first launch; for later versions it's the
next most valuable move. A version that's small but pointed at the real goal beats a big
one that drifts.
If the brief has no clear goal yet, pin that down first (or send the user back to
new-project) — you can't triage scope against a goal you don't have.

## The operating loop

1. **Get everything on the table.** Collect the full pile — every idea, feature,
   format, channel, polish item the user is imagining. Pull from the brief, the backlog,
   and just asking. Don't filter yet; you can only cut well once you can see it all.

2. **Set the appetite first — this is the key move.** Before sorting anything, ask the
   single most clarifying question: **how much time and attention is the user willing to
   spend** to get v1 out? ("Three weekends?" "An hour every evening for a month?") The
   appetite is *fixed*; the scope is what flexes to fit it. This flips the usual trap —
   instead of "how long will all this take?" (which never ends), it's "what fits in the
   time I've decided to give it?" Everything below is fitted to this budget. If the user
   resists naming one, gently insist: an MVP without a time budget regrows without limit.

3. **Name the point of this version in one sentence.** What is the *one thing* it has to
   prove or deliver? (For v1: "Publish one story a week that people actually finish and
   come back for." For a later version: "Add the thing that turns watchers into
   subscribers.") Everything triages against this. If two things compete to be "the
   point," it's really two versions — say so, and shape the more valuable one now.

4. **Spot the rabbit holes before committing.** Scan for the unknowns that could quietly
   eat the whole appetite — the things the user has never done, that hide surprise work
   ("I've never recorded clean audio," "I don't know how long editing actually takes").
   Name them out loud. A rabbit hole isn't automatically cut, but it must be **handled
   before the plan is trusted**: shrink it, time-box a test of it, or design around it.
   Unretired rabbit holes are the number-one reason a "small" v1 quietly becomes huge.

5. **Triage each item four ways — out loud.** Walk the pile against the appetite and the
   point, sharing the reasoning so the user can overrule. Sort each into:
   - **Include** — genuinely required to deliver the point, and it fits the appetite. The
     bar is "couldn't launch honestly without it," not "would be nice."
   - **Defer** — useful but outside this appetite. Lands in v2 or someday, with a one-line
     **why** — the why is what stops it sneaking back in.
   - **Split** — too big or really two things. Carve off the smallest version that fits v1
     and defer the rest ("a full back-catalogue" → "the first 4 stories" now, the rest
     later).
   - **Risk-first** — depends on an unretired rabbit hole; don't commit it to this version
     until that unknown is handled (step 4).
   - When genuinely in doubt, **defer it.** A too-big v1 (never ships) costs more than a
     too-small one (ship, then add).

6. **Define "done" and a launch target.** The version needs a finish line: a concrete
   **definition of done / ready to launch** ("4 stories recorded, channel art up, first
   one scheduled") and a **target launch date** — which must be consistent with the
   appetite from step 2. If "done" can't fit the budget, something still has to give;
   loop back and cut more rather than quietly letting the date slip.

7. **Write it to the roadmap.** Fill the **"Now shaping / building"** block in
   `plan/roadmap.md` with the version you just shaped: its number/name, the appetite, the
   point, the rabbit holes and how each is handled, what's included, what's deferred/split
   (with whys), the done-condition and target. Push deferred-but-real ideas down into the
   **parking lot** so they resurface for a future pass. Log the scope decision in
   `decisions/log.md` — the appetite and cut boundary are exactly the choices the user
   shouldn't have to re-argue in three weeks.

8. **Hand back plainly.** The version in a few lines: the time budget, what's in, what's
   intentionally left for later, any risk being tackled first, and when it launches. Then
   the obvious next step — usually **studio:next-piece** to start building one of this
   version's deliverables, or **studio:project-desk** to schedule them.

## Shaping later versions (the re-run loop)

This skill is **re-runnable, one version at a time** — that's how it serves any version,
not just v1. The loop:

1. A version is shaped in the roadmap's **"Now shaping / building"** block and gets built.
2. When it **ships**, move its block down to **"Shipped versions"** (it stays as a record
   of what that version delivered — appetite, what was in, what shipped).
3. Run scope **again** to shape the *next* version into the now-empty "Now shaping" block,
   drawing candidates from the **parking lot** of deferred ideas. Same discipline, fresh
   appetite, fresh rabbit holes.

Only ever **one** version sits in "Now shaping" at a time. Don't pre-shape v3 and v4 into
full blocks while v2 is live — leave them as raw parking-lot ideas until it's their turn.
That's what keeps the roadmap a living plan instead of a frozen multi-year wish-list.

## Judgment

- **Appetite before scope, always.** The defining discipline of this skill: fix the time
  budget first, then fit the work to it. If you find yourself estimating how long the
  wish-list will take, you've inverted it — ask instead what fits the budget the user has
  already decided to spend.
- **Cutting is the value, not a failure.** A skill that says "keep it all" is useless.
  The user is here precisely to be helped to say no. Recommend cuts plainly and kindly,
  and always say *why* and *where it goes* — a cut with a home is easy to accept.
- **Name rabbit holes; don't wave them through.** The unknowns are where appetites die.
  Surface them honestly and insist each is handled (shrunk, tested, or designed around)
  before the plan is trusted — an optimistic plan that ignores a real unknown isn't a
  plan.
- **The boundary is the user's to set.** Triage out loud and recommend, but it's their
  project and their call. Don't quietly drop something they care about; surface the
  trade-off ("this pushes launch ~2 weeks — worth it?") and let them decide.
- **Protect the line after it's drawn.** Once v1 scope is set and logged, treat new
  mid-stream ideas as v2 candidates by default, not silent additions — that's how an MVP
  stays an MVP. (Same spirit as a release scope-audit.)
- **Smallest *real* version, not smallest possible.** The MVP still has to be worth the
  audience's time and true to the brief's voice. "Small" means fewer things, not a
  half-baked thing.
- **Stay in your lane.** Scope shapes and triages; it doesn't build the pieces
  (next-piece) or run the day-to-day (project-desk). Sort the scope, write the roadmap,
  hand off.
