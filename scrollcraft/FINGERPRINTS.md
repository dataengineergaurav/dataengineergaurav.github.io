# Fingerprints

Every site you build with **scrollcraft** gets one row here, appended after it
ships. The registry exists so your next build can prove it is a different page
rather than a re-skin of one you already made.

This file is **yours**. It starts empty on purpose: the gate is about not
repeating *yourself*, so it has nothing to say until you have built something.

The rules and the gate live in the skill's
`references/uniqueness.md`. Short version:

**A new build must differ from EVERY row below on at least 4 of the 6
dimensions.** Four against each row individually, not four on average across the
table. If a planned build fails, change the plan. Never edit a row to make room
for it.

The six dimensions are: **grammar**, **nav treatment**, **hero device**,
**act-sequence shape**, **close pattern**, **signature move**.

Dimension 6 is free, because a signature move is unique by definition. So the
gate really asks for three more out of the remaining five, and a build that
changes only grammar and world will fail it.

---

## The registry

| Build | Grammar | Nav treatment | Hero device | Act-sequence shape | Close pattern | Signature move | World | Port |
|---|---|---|---|---|---|---|---|---|
| gledger | Chaptered Editorial | Folio margin index (right-fixed, 6 chapters, bar highlight) | Title page on paper (no media, type-first, dot-grid) | 2 pinned acts (pin 3.1 + pan 2.4) + 6 flow chapters; ~12-14vh total; devices: flow+in, count, pin+cues, pan+rail, reveal | Colophon plate (small type, CTA as running element, links as set plate, no magnet/spotlight) | Fixed trace rail: accumulates dot+label per chapter as progress, doubles as navigation; work ledger rows sync to pin --sc-p | Paper ledger / architectural light (warm paper #f5f0e5, forest ink #18372a, mustard #efb34e, hairline rules, dot-grid) | 4501 |

---

## What is taken

Add a bullet here whenever a build claims something a later build should avoid
reusing: a grammar, a nav treatment, a close pattern, a signature move, an
act-count-and-length band. The shared columns are what the next build inherits
as a constraint, so writing them down is the whole point.

- Chaptered Editorial grammar — next build must pick a different grammar.
- Folio margin index nav — next build should use a bar, map, app chrome, or no nav.
- Title-page hero (no-media, type-first) — next build should open with media, surface, or type-at-scale.
- Colophon close — next build should close with pin+spotlight, collapse, abrupt cut, or inquiry plate.
- Trace-rail signature — accumulating progress-as-record concept is taken; next signature must be unrelated (e.g., wordmark physics,SVG draw, receipt, regrade).
- Paper ledger world — next build should rotate world (low-key cinematic, nocturne, macro, architectural, etc.).

---

## Appending a row

After shipping, add one line to the table and one bullet to **What is taken** if
the build claimed something new. Fill every column. Say what the build shares
with existing rows.

Rows are append-only. A build that has been superseded stays in the table,
because the space it occupies is still occupied.

---

## Worked example

The skill's author kept a registry of twelve builds across eight page grammars.
If you want to see what a filled-in table looks like, and which shapes tend to
collide, read `EXAMPLES.md` in the scrollcraft repository. Treat it as
illustration only: those rows are somebody else's builds and they do **not**
constrain yours.
