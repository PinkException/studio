---
name: new-project
description: >-
  Scaffold a new non-code project — a writing project, a content channel, a small
  business, a set of guided tours — into a consistent folder skeleton, then interview
  the user to fill the brief (the north star). Use whenever the user invokes
  /studio:new-project, or says "start a new project", "set up my <channel/book/tours>
  project", "scaffold a project for X", "I want to organise a new <creative/writing>
  project", or describes a fresh non-code endeavour they want to manage with Claude
  Code. Creates the same structure every time (README, brief, plan/{roadmap,calendar,
  backlog}, decisions/log, business/{plan,budget,metrics}, content/, reference/,
  assets/) so the user always knows where the plan, the decisions, and the work live.
  Pairs with studio:next-piece (develop a deliverable) and studio:project-desk (run
  the day-to-day). Do NOT scaffold a full parallel skeleton for a code project — but DO
  offer the docked **business-track** mode (only business/ + roadmap + decisions, reusing
  the repo's existing vision doc as the brief) when a code project — managed by jig/servo
  — needs a go-to-market or business plan alongside its code. Full non-code scaffolding
  belongs here; full code scaffolding belongs to jig.
---

# New Project

This is the **scaffolder**. It does for a creative or business project what a code
scaffolder does for a repo: it lays down **the same folder skeleton every time** and
fills the one file everything else depends on — the **brief** (the north star). The
promise to the user is consistency: start any project this way and you never have to
wonder where the plan, the decisions, or the actual work go. They're always in the
same place.

Two things make a project this skill's territory: it's **not code** (a YouTube
channel, a book, a course, guided tours, a newsletter), and the user wants to **run
it over time** — track decisions, keep a schedule, build deliverables on a rhythm. If
it's a code project, don't fork a parallel skeleton: point them at jig to *build* the
product — or, if they want the **business / go-to-market** side, dock a business track
inside the repo (see "Business track inside an existing code project" below). Full
non-code scaffolding is this skill's home turf; the docked mode is its bridge to code
products.

## What you create

The skeleton — copied from this skill's `templates/` directory into the new project
folder, with placeholders filled from the interview:

```
<project>/
  README.md                 one-glance overview + map of where things live
  brief.md                  THE NORTH STAR — audience, tone, voice, goals, rules
  plan/
    roadmap.md              big phases (now / next / later) + milestones
    calendar.md             what ships when — the schedule the desk reads
    backlog.md              ideas not yet scheduled
  decisions/
    log.md                  every meaningful choice, dated, in plain language
  business/
    plan.md                 light business plan
    budget.md               money + time
    metrics.md              what success looks like, tracked
  content/                  the actual work — one folder per deliverable (starts empty)
  reference/                source material & research (starts empty)
  assets/                   exports: images, audio, thumbnails (starts empty)
```

## Business track inside an existing code project (docked mode)

When the project is **already a code repo** (managed by jig/servo) and the user wants
the *business* layer — audience, pricing, channels, budget, metrics, launch — do **not**
create a parallel project folder. That would duplicate the repo's README and north-star
doc and litter it with empty content/reference/assets folders that make no sense for an
already-built product. Instead **dock a business track inside the repo**:

- **Detect and offer.** If you spot signs of a code repo (a `.git`, a `package.json`/
  `pyproject.toml`, jig/servo machinery) while the user is asking for a business or
  go-to-market plan, *offer* docked mode rather than silently scaffolding a parallel
  project — "This is already a code repo; want me to dock a business track inside it
  instead of starting a separate project?"
- **Scaffold the business slice**, under a subfolder (default `docs/business/`):
  `business/{plan,budget,metrics}.md`, `decisions/log.md`, `roadmap.md`, and
  `calendar.md`. **Skip** `reference/` and `assets/` and the second `README.md` (the repo
  has those); reuse the repo's vision doc instead of a rival `brief.md`.
- **Keep the calendar — for marketing, not the product.** The *product* launches once and
  its milestones live on the roadmap (owned by jig/shaper). But the **communication /
  marketing** around it — build-in-public devlogs, social posts, an email list,
  launch-week beats — is a genuine ongoing stream that runs on a cadence. That stream is a
  content channel in its own right, exactly studio's home turf: `calendar.md`,
  `studio:next-piece`, and `studio:project-desk` all apply to it. Give those marketing
  pieces a home (default `docs/business/marketing/`).
- **Reuse the repo's existing vision/brief as the north star** — e.g.
  `docs/product-vision.md`. Don't write a rival `brief.md`; link to the existing one from
  the docked files so there's a single source of truth.
- **Stay out of the code workflow's lane.** jig/servo (and shaper, if present) own the
  *product and code-release* plan; this business track owns the *commercial* plan. Don't
  re-plan features here or duplicate jig specs — reference them.
- **Then shape the first commercial version** with **studio:scope**, writing it to the
  docked `roadmap.md`.

The interview below still applies, but trimmed: you already have audience/tone/goals in
the vision doc, so focus the conversation on the *business* unknowns — who pays, for
what, through which channel, at what cost, and what success looks like in numbers.

## The operating loop

1. **Confirm it's a studio project, and name it.** One plain sentence back to the
   user: "So this is a *<kind>* project — let's set it up." Get a short **folder
   name** (kebab-case, e.g. `grimm-channel`) and where it should live (default: a new
   folder under the current working directory). If it smells like a code project, don't
   scaffold a full parallel skeleton: either point to jig (if they want to *build* the
   product), or — if they want the **business / go-to-market** side — switch to the
   docked business-track mode below.

2. **Interview for the brief — this is the real work.** The folders are mechanical;
   the brief is what makes the project *yours*. Ask in plain language, a few at a
   time, not as a wall of form fields. Cover:
   - **What it is**, in one sentence (the elevator line).
   - **Audience** — who it's for, what they want from it, where they'll find it.
   - **Tone & voice** — how it should *feel*, and how it should *sound* (voice is
     best pinned to a person: "like a grandmother telling a bedtime story"). Get
     words/phrases that fit and ones to avoid.
   - **Goals** — the point of doing this, and what success looks like in a year.
   - **Rules & constraints** — the non-negotiables (language, cadence, format).
   - **Cadence** — how often pieces ship, and any standing rhythm (e.g. "Monday FR,
     Thursday EN").
   - **What one finished piece looks like** — the most important question for avoiding a
     one-size-fits-all default. What's the *unit* this project ships (an episode? a
     chapter? a tour? an issue?), what parts does a finished one have, does it use
     generated images, and what's its "done." This fills the brief's deliverable-shape
     section that studio:next-piece reads — so a book chapter never gets scaffolded like
     a podcast script.

   Don't interrogate. Offer sensible defaults and let the user correct them — "I'm
   guessing the tone is warm and a little mysterious; right?" A half-filled brief
   they'll refine beats a blank one they won't.

3. **Stamp out the skeleton.** Create the folder and copy every file from
   `templates/`, replacing `{{PLACEHOLDERS}}` with the interview answers. Keep the
   directory structure identical to the template — that sameness is the whole point.
   - Use today's date (from the environment) for `{{DATE}}` fields.
   - Fill what you learned; leave honest `{{PLACEHOLDER}}`s or "— to fill —" where
     the user hasn't decided yet, rather than inventing specifics. Empty `content/`,
     `reference/`, and `assets/` folders are expected — add a short `.gitkeep` or a
     one-line `README.md` in each so they're not lost.
   - Seed `decisions/log.md` with the first real decision: the cadence and format
     the user just chose, with the "why."
   - Seed `plan/calendar.md` with the standing rhythm and, if the user named the
     first few pieces, their rows (status `idea`).

4. **Show the user what they've got — in plain English.** A short tour: "Here's your
   project. The brief holds your tone and audience; the calendar has your Monday/
   Thursday rhythm; decisions are logged as you make them." Point out the one or two
   spots still worth filling in. No file-path dumps unless they ask.

5. **Offer the obvious next step.** The usual best move on a fresh project is to shape
   the first version before building anything: "Want to figure out the smallest version
   you can launch fast?" → that's **studio:scope**. After that, **studio:next-piece** to
   build a v1 deliverable, or **studio:project-desk** to schedule them and set reminders.
   Recommend one; don't hand them a menu.

## Judgment

- **The brief earns the time; the folders don't.** If you find yourself rushing the
  interview to get to file-writing, you've got it backwards. The structure is
  identical every time precisely so you can spend your attention on the brief.
- **Adapt the skeleton, don't bloat it.** The template fits most projects. If a
  project genuinely needs something extra (a guided-tours project might want a
  `routes/` folder; a book wants `chapters/` under content), add it — but keep the
  core files so every studio project still feels the same. Note any structural change
  in the decision log so it's deliberate, not drift.
- **Don't overwrite an existing project.** If the target folder already has a brief
  or a calendar, stop — this is a *new*-project skill. Offer project-desk instead.
- **Match the user's language.** If the project is bilingual or French-first, write
  the brief's voice notes and house-style examples in the language they'll actually
  create in.
