# Human Behavior

Why interfaces fail at the human, not the code. Every entry is a limit or a bias with the design
decision it forces. Cite the name when you justify a fix — "people scan in an F" is an argument;
"this feels cluttered" is not.

---

## Perception and attention

**You do not see the page; you see what stands out.** Pre-attentive processing happens in
~200 ms, before conscious reading, and it is driven by a small set of channels: position, size,
colour/hue, orientation, motion, and enclosure. Two rules fall out:

- A visual difference must map to a *meaningful* difference, or it is noise. Nine accent colours
  for nine equal things means nothing stands out.
- Vary one channel at a time for emphasis. Stacking size + colour + weight + motion on one item
  flattens the rest of the page and burns the strongest tool you have.

**Gestalt grouping** — the eye groups by **proximity** (nearest), **similarity** (alike),
**common region** (shared container/border), **continuity**, and **closure**. Proximity usually
beats similarity, which means: *whitespace is the primary grouping tool, and a border is what you
add when spacing has failed.* Symptom to look for: a form where labels are closer to the previous
field's input than to their own. That is a proximity bug, and users mis-associate fields because
of it.

**Scanning patterns.** People do not read; they forage.

- Dense text and lists get an **F-pattern** — the first two words of each line carry the load.
  Put the distinguishing word first ("Overdue invoices", not "Invoices that are overdue").
- Short, sparse layouts get a **Z-pattern**.
- Mixed content gets **layer-cake** scanning — headings and bold leads are read, paragraphs are
  skipped. Headings are not decoration; they are the actual reading path.
- **Banner blindness**: anything that looks like an ad (right column, bright box, animation)
  is skipped. Sidebars and promo blocks are invisible at a glance.

**Change blindness.** A change outside the current focus is not noticed at all. This is why a
silent background update, a badge that increments, or a chart that re-renders is functionally
invisible — and why an announcement (a live region, a toast the user asked for) is not optional
for anything that changed on its own.

**Figure/ground.** Overlays, scrims, and elevation must read as *above* the page. If the modal
and the page behind it have the same weight, people try to interact with the background.

---

## Memory

**Working memory is small** — Miller's 7 ± 2 is the popular number, but the useful modern figure
is closer to **four chunks**. Consequences:

- Never require recall of a value from a previous screen. Show it (recognition over recall):
  "Renewing **Pro plan — $29/mo**", not "Renewing the plan you selected".
- Chunk long values: `+971 50 123 4567`, `4111 1111 1111 1111`, `2026-10-09`.
- Cap lists you expect someone to hold in mind at ~5–7 items. Past that, they compare rather
  than remember, and comparison needs a table, not a list.

**Serial position.** In a list, the first and last items are remembered best (primacy/recency).
Put the important item at an end, not the middle.

**Von Restorff (isolation effect).** The item that differs is the item remembered. Use it
deliberately for the one thing that must not be missed — and sparingly, because isolation only
works while it is rare.

**Peak–end rule.** People judge an experience by its most intense moment and its ending, not its
average. A 20-step wizard that ends with a clear confirmation is rated better than a 5-step one
that ends ambiguously. Never let the last screen be a blank redirect.

**Zeigarnik.** Unfinished tasks stick in memory and create tension. A visible progress indicator
and a resumable draft convert that tension into engagement instead of abandonment.

---

## Decision and effort

**Hick's law** — decision time rises with the *number of choices* (roughly log₂(n+1)), and rises
further when the choices are hard to tell apart. This is about the *simultaneous* set, not the
total. Fixes:

- Default the common case.
- Stage: reveal the advanced branch only when asked.
- Rename so options are obviously different; two indistinguishable options cost more than ten
  clear ones.
- Use the primary/secondary/tertiary hierarchy — one dominant action per view.

**Fitts's law** — time to acquire a target depends on *distance* and *size*. A small target far
from the pointer/thumb is expensive. Consequences: 44×44 px minimum touch targets (48 comfortable),
the bottom quarter of a phone is the reachable zone, and *destructive* controls belong where they
take deliberate effort while *frequent* ones belong where they are easy. Expanding a small visual
icon with padding to a large hit area is legitimate; a small hit area never is.

**Tesler's law (conservation of complexity).** Complexity cannot be removed, only moved. Move it
from the user to the system (smart defaults, parsing, inference) or to the expert (advanced
settings). Hiding complexity without absorbing it just relocates it to a support ticket.

**Jakob's law.** People expect your interface to work like the other ones they use. Novel
navigation, novel gestures, and novel form behaviour are taxes you pay for originality. Innovate
where the payoff is real; be conventional for the boring parts.

**Choice overload / jam study.** Beyond a modest set, more options *reduce* conversion and
satisfaction even though people say they want more. If a set exceeds ~7 undifferentiated options,
it needs structure, not scroll.

**Goal gradient.** Effort accelerates as a goal gets closer — a progress bar or a "2 of 5 done"
indicator measurably improves completion, often more than shortening the form would.

---

## Mental models, affordance, feedback

Norman's three, which cover most "it doesn't feel right" complaints:

- **Affordance** — what the thing can do. A control that looks tappable must be tappable; a
  heading that looks tappable must not be.
- **Signifier** — how you know. This is the one that fails most: an icon with no label, a
  draggable region with no handle, an editable cell with no cue. The capability exists and nothing
  announces it.
- **Mapping** — does the control's arrangement match the thing it controls? A "sort ascending"
  arrow that sorts descending is a mapping bug, not a labelling bug.
- **Feedback** — every action gets a visible, timely result. No silent success and no silent
  failure; both teach the user that the interface is unreliable.

**Mental model mismatch.** Users arrive with a model from a competing product or from the old
version. When the new one differs, the mismatch shows up as "it's broken". Either match the model
or teach the change explicitly at the point of change.

---

## Perceived latency

Nielsen's three thresholds, still the working standard:

| Delay | Perception | Design response |
|---|---|---|
| ≤ 100 ms | Instant | No indicator. Anything shown here is noise. |
| 100 ms – 1 s | Noticeable, flow retained | No spinner; a subtle state change is enough |
| 1 s – 10 s | Flow broken | Show progress. If duration is known, show a determinate bar |
| > 10 s | Attention lost | Show progress *and* let them leave or work elsewhere |

Perception beats reality:

- A **determinate** bar feels faster than an indeterminate one, even at identical duration.
- Progress that *accelerates near the end* is judged faster than linear (though a bar that
  stalls is worse than no bar).
- **Skeleton screens** that match the final layout feel faster than a centred spinner because the
  layout is already resolved — and they avoid the layout shift a late load would cause.
- The **Doherty threshold** (~400 ms) is the band where responsiveness becomes an
  engagement issue, not just a speed one.
- Optimistic UI (show the change, reconcile after) removes the wait entirely for low-risk,
  high-confidence actions — and needs an honest rollback path when the write fails.

**Never** make the wait look shorter by lying. A bar that reaches 100 % and then waits is worse
than a spinner.

---

## Emotion, trust, and risk

- **Loss aversion** — losses feel roughly twice as large as equivalent gains. Destructive
  actions, overwrites, and "your trial is ending" all land harder than the symmetric version.
  Weight the confirm/undo accordingly.
- **Defaults carry consent.** A pre-checked box is an endorsement the user did not give. Use
  defaults to help, never to enrol.
- **Trust is asymmetric** — one lost draft outweighs ten smooth saves. Preserve input on error,
  keep drafts, and never clear a form because validation failed.
- **Endowed progress** — "you're 20 % done" beats "start now". Give the first step for free.

---

## Individual differences

There is no average user, and accessibility is not a separate track from usability — it is the
same limits under more pressure:

- **Motor**: tremor and limited precision raise the real cost of small or drag-only targets.
  Provide non-drag alternatives.
- **Vision**: colour-vision deficiency (~8 % of men) means colour alone never carries meaning.
  Low vision lives at 200 % zoom, where fixed heights and absolute positions break first.
- **Cognitive**: autism, ADHD, dyslexia affect tolerance for motion, dense text, ambiguity, and
  sudden change. Plain language, calm motion, and predictable structure help everyone.
- **Situation**: one hand, bright sunlight, a slow connection, a screen reader on a train. Design
  constraints are environmental as often as they are personal.
- **Expertise**: a novice needs labels and orientation; an expert needs density and shortcuts.
  Where both share a surface, progressive disclosure is the pattern, not a simpler page.

---

## Using this file

In a review, every finding should name the limit it violates and the observable evidence. In
design, run the list as a check: targets, choice set, memory, latency, feedback, grouping. If a
fix cannot be tied to one of them, it is probably taste — and taste belongs to `design`.
