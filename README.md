<div align="center">

# 🎬 studio

### A project desk for everything that isn't code.

*Writing projects · content channels · small businesses · guided tours*

[![version](https://img.shields.io/badge/version-0.6.0-blue)](https://github.com/PinkException/studio/releases)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-8A63D2)](https://docs.claude.com/en/docs/claude-code)
[![skills](https://img.shields.io/badge/skills-5-orange)](#-the-five-helpers)

</div>

---

**studio** does for a creative or business project what a code scaffolder does for a repo:
it lays down **the same folder skeleton every time**, so you always know where the plan,
the decisions, and the actual work live — then it helps you shape a first version, build
the deliverables, and keep the whole thing moving.

One structure for every project. A YouTube channel this month, a book next year, a set of
city tours after that — **you learn it once.**

```text
new-project  →  name  →  scope  →  next-piece  →  project-desk
  set up      codename   shape       build         run the
  the brief   now, real  the MVP    deliverables   day-to-day
              name later
```

## 🚀 Quick start

1. **Install** — download [`studio-v0.6.0.zip`](https://github.com/PinkException/studio/releases/latest)
   from the latest release and add it as a plugin in Claude Code.
2. **Start a project** — in a fresh folder, just say it in plain words:
   > *"Start a new project for my YouTube channel."*

   `studio:new-project` interviews you for the brief, scaffolds the folders, and hands off
   to `scope` and your first piece.
3. **Come back any time** with *"where am I, what's due this week?"* → `studio:project-desk`.

No commands to memorize — describe what you want and the right helper steps in.

## 🧰 The five helpers

| Helper | What it's for | Say something like |
|---|---|---|
| **`studio:new-project`** | Scaffold a fresh project + interview you for the **brief** (the north star: audience, tone, voice, goals, and what one finished piece looks like). | *"Start a new project for my YouTube channel."* |
| **`studio:name`** | Two moments, two modes. **Placeholder:** a working codename in minutes, fenced out of the places you can't change later (store identifiers, legal pages, bought domains). **Final:** a real naming round before launch — brief, metaphor territories, filtered candidates, live checks (domains, GitHub, App Store, Google Play) plus trademark and handle links, a scored shortlist with origin stories, and a written record of why. | *"Give me a working name for my new budgeting app."* · *"Time to name this for real — is Mossling taken?"* |
| **`studio:scope`** | Shape **any version, one at a time** (the first is the MVP): set a **time budget** (appetite), name the **risky unknowns** (rabbit holes), and triage every item **include / defer / split / risk-first**. Re-run it for v2, v3… | *"What's the smallest thing I can launch?"* |
| **`studio:next-piece`** | Build the next deliverable end to end, **adapted to your format** — a script, a chapter, a tour, an issue, a marketing post — in the project's own voice. | *"Let's build the next one."* |
| **`studio:project-desk`** | The day-to-day: **what's due this week**, the calendar, the backlog, and a plain-language **decision log**. | *"Where am I? What's due?"* |

## 🗂️ The folder skeleton every project gets

```text
your-project/
├── README.md          one-glance overview + map of where things live
├── brief.md           THE NORTH STAR — audience, tone, voice, goals, rules
├── plan/
│   ├── roadmap.md      the plan in versions — v1 (MVP) first, the rest parked
│   ├── calendar.md     what ships when — the schedule the desk reads
│   └── backlog.md      ideas not yet scheduled
├── decisions/
│   └── log.md          every meaningful choice, dated, in plain language
├── business/
│   ├── plan.md         a light business plan
│   ├── budget.md       money + time
│   └── metrics.md      what success looks like, tracked
├── content/           the actual work — one folder per deliverable
├── reference/         source material & research (naming/ holds the naming records)
└── assets/            exports: images, audio, thumbnails
```

## 🔄 How it fits together

1. **`new-project`** sets up the folders and, more importantly, interviews you to fill the
   **brief** — including what a finished piece looks like, so nothing is assumed to be a
   podcast episode. No name yet? **`name`** hands you a codename on the spot and comes
   back before launch for the real one, with availability checks and a scorecard.
2. **`scope`** shapes the smallest first version worth launching: you set a time budget, it
   fits the work to that budget, flags the risky unknowns, and parks the rest — so you
   **ship instead of planning forever**.
3. **`next-piece`** turns the next item into a finished deliverable, written to the brief's
   voice and shaped to your format (image prompts only when the project uses visuals).
4. **`project-desk`** tells you what's due, captures decisions and ideas, and can set up
   reminders a day or two before each deadline.

## ✨ Example: a weekly story channel

A channel that publishes a Grimm tale read aloud — **French on Mondays, English on Thursdays**:

- **`new-project`** captures the bilingual rhythm, the bedtime-story voice, the audience,
  and that a "piece" here is a read-aloud script + images — seeding the **calendar** with
  the Monday/Thursday slots.
- **`scope`** sets the appetite (say, *"four weekends"*), tackles the rabbit hole up front
  (*"never recorded clean audio — test it this weekend"*), and lands the MVP at *"4 stories
  recorded and the first scheduled"* — subtitles and a Patreon parked for v2.
- **`next-piece`** drafts each week's script in that voice, then (because this project uses
  visuals) brainstorms the scene-by-scene Midjourney prompts and the thumbnail.
- **`project-desk`** answers *"what's due Thursday?"*, logs decisions (*"keep them under 8
  minutes"*), and can remind you before each slot.

The same helpers work for a **book** (a piece is a chapter — no image prompts; `scope` picks
which chapters make v1) or **guided tours** (a piece is a route with stops and timings).
`next-piece` adapts to each — nothing is hardcoded to video.

## 🧩 Code projects: building vs. selling

For *building* software, use a code-focused workflow (e.g. **jig** for specs/implementation,
**shaper** for code-release shaping) — studio doesn't scaffold or build code.

But the **business and marketing layer of a code product** *is* studio's wheelhouse, and the
code workflows don't cover it. So when a code repo needs a go-to-market or marketing plan,
studio offers a **docked business-track mode**: instead of forking a parallel project, it
docks a business-only slice inside the repo (default `docs/business/` —
`business/{plan,budget,metrics}`, `roadmap`, `calendar`, `decisions/log`, and a `marketing/`
folder), and reuses the repo's existing vision doc (e.g. `docs/product-vision.md`) as the
brief rather than writing a rival one.

A docked track runs on **two rhythms**: the **product** launches once (its milestones live on
the roadmap, owned by jig/shaper), while the **marketing** around it — devlogs, social posts,
launch-week beats — ships on an ongoing cadence that `next-piece` and `project-desk` drive
like any other studio channel. `scope` shapes the *commercial* version (audience, pricing,
channels, launch); jig/shaper still own which features ship in which build.

## 📦 Install

studio is distributed as a plugin zip:

1. Grab [`studio-v0.6.0.zip`](https://github.com/PinkException/studio/releases/latest) from the
   latest release.
2. Add it as a plugin in Claude Code (the desktop app's plugin upload, or your usual
   marketplace flow).
3. Open a project folder and start talking — `studio:new-project` takes it from there.

## 📄 License

[MIT](LICENSE) © Marie-Rose Ramboz

<div align="center"><sub>Built with ❤️ for everyone managing creative work in Claude Code.</sub></div>
