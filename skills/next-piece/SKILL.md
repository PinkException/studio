---
name: next-piece
description: >-
  Develop the next deliverable in a studio project end to end — whatever that project
  ships as a unit: a video script, a book chapter, a guided-tour route, a newsletter
  issue, a lesson, or a marketing piece (a build-in-public devlog, a social post, a
  trailer/launch script) for a code project's docked business track. Scaffold its folder, then move it from blank page to done: draft the
  main content in the project's voice, plus whatever the deliverable needs (image
  prompts only for visual projects, logistics for a tour, and so on). Use whenever the
  user invokes /studio:next-piece, or says "build the next piece", "write the next
  chapter/script/issue", "let's do this week's <thing>", "help me make <title>", or
  wants to produce one concrete unit of the project. Reads the brief — including its
  "what one finished piece looks like" section — so the piece matches both the project's
  voice and its deliverable shape, and updates the calendar status as it progresses.
  Assumes a studio project exists (from studio:new-project); if none is found, offer to
  create one. Pairs with studio:project-desk, which says which piece is due.
---

# Next Piece

This is the **workhorse**: turning the next item on the calendar into a finished
deliverable, in the project's own voice, without facing a blank page alone.

The thing to get right — and the thing this skill is built around — is that **a "piece"
is not always a podcast episode**. It's whatever *this* project ships as a unit. For a
story channel it's a read-aloud script with images; for a book it's a chapter with no
images at all; for guided tours it's a route with stops, timings, and logistics; for a
newsletter it's an issue; for a code project's **docked business track** it's a marketing
piece (a devlog, a social post, a trailer script) — never the product itself, which stays
with the code workflow. So the very first move is to find out what shape a finished piece
takes here — never assume.

## Before anything: load the north star *and* the deliverable shape

Read `brief.md` — tone, voice, words that fit, words to avoid, house style — **and in
particular its "what one finished piece looks like" section**: what a piece is, its
parts, whether it uses generated images, and its definition of done. Then read
`plan/calendar.md` for what's due. Everything below adapts to that shape. If the brief
doesn't define the piece shape yet, ask the user a couple of quick questions and write
it into the brief before scaffolding — that one answer prevents the podcast-shaped
default.

If there's no studio project here at all, don't improvise one; offer
**studio:new-project** first.

## The operating loop

1. **Settle which piece, and its facts.** Take it from the user, or read the calendar
   for the next `idea`/`drafting` item. Pin the basics: title, slot, date, language,
   source/reference, and a size/length target. Confirm the language if the project is
   multilingual — it changes the writing, not just a label.

2. **Scaffold the piece folder — to the deliverable shape.** Under `content/`, create a
   slugged folder. Copy `draft.md` (the main content) and `notes.md` (checklist),
   filling headers. Then **tailor to the brief's piece shape**:
   - Rename/re-section `draft.md` to fit (a chapter, a route, a script) — don't leave
     it shaped like a video script if it isn't one.
   - Add `image-prompts.md` **only if** the brief says the project uses generated
     images. Skip it for text-only pieces.
   - Build the `notes.md` checklist from the brief's "done when" — record/edit steps
     for video, layout/proofing for a chapter, a walk-through for a tour. Don't carry
     over steps the deliverable doesn't have.
   - Set the calendar status to `drafting`.

3. **Draft the main content — to the brief's voice.** This is the heart, and it's the
   same regardless of format: work *with* the user, in readable chunks, inviting
   steering rather than dumping a finished wall.
   - Start from the source and the brief's tone; propose a structure that fits the
     deliverable (hook→body→close for a script; scene/beat structure for a chapter;
     stop-by-stop for a tour).
   - Write in the project's **voice** — every line should pass the brief's voice test.
     Honour the words-to-avoid list. For spoken pieces, read-aloud the tricky lines.
   - Save into the draft file as it firms up.

4. **Add what the deliverable needs — conditionally.** This is where formats diverge:
   - **Visual projects:** walk the draft's beats and propose image prompts (e.g. for
     Midjourney) into `image-prompts.md`, keeping a consistent look from the brief's
     house style, plus a thumbnail. The user generates the images themselves.
   - **A tour:** stops, timing, walking directions, what to say at each.
   - **A chapter / issue:** maybe none — the draft *is* the deliverable.
   Do only what this project's piece shape calls for; don't bolt on image-brainstorming
   for a project that has no images.

5. **Tie off the loose ends.** Fill `notes.md` — research, piece-specific decisions, and
   tick the checklist. Set the calendar status to `ready` when the piece is fully
   prepared (not when published — be honest). Log any decision that outlives this piece
   (a format change, a new recurring segment) to `decisions/log.md`.

6. **Hand back plainly.** What's done, what's left for the user (record, generate
   images, schedule, rehearse — whatever applies), and what's next on the calendar.

## Judgment

- **Fit the deliverable, not a template.** The single biggest failure here is treating
  every piece like a video script. Read the brief's piece shape first; let it drive the
  files, the structure, and the checklist.
- **Voice over polish.** A piece that sounds unmistakably like the project beats a slick
  generic one. When unsure, re-read the brief's voice notes — they outrank your instinct
  for "better" prose.
- **Consistency is a feature.** Reuse recurring elements (opening/closing lines, visual
  style) on purpose. Evolving them is a decision-log entry applied to future pieces, not
  silent drift.
- **Honest statuses.** `ready` means prepared; `published` means actually out. The desk
  trusts these to tell the user what's due.
- **Respect what only the user can do.** Generating images, recording, rehearsing,
  publishing are theirs. Prepare everything up to that line; don't pretend to have done
  it.
