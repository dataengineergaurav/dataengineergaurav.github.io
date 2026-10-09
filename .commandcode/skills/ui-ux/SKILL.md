---
name: ui-ux
description: "Design and review interfaces around the people using them — grounded in perception, cognition and motor limits, usability heuristics, and established interaction patterns. Use when the user asks about UX or usability, information architecture, navigation, forms, empty/loading/error states, onboarding, destructive actions, cognitive load, or user behavior, or asks to review, critique, or fix an interface that feels confusing or hard to use. Complements the `design` skill, which owns visual craft."
argument-hint: "[design|review] [target]"
---

# UI-UX

Interfaces fail for human reasons long before they fail for aesthetic ones: the target was too
small, the choice set was too wide, the label was ambiguous, the error destroyed the work. This
skill is the human layer — perception, cognition, motor limits, decision cost, and the
interaction patterns that respect them.

**Boundary.** This skill owns *the human and the interaction*. It does not own palette, type
scale, layout composition, motion curves, or brand voice — the `design` skill owns those, and
`design`'s own accessibility reference owns the access floor. When a finding is "this is hard to
look at", hand it to `/design`. When it is "this is hard to *do*", it is ours. The two skills
compose: a review that runs both produces one findings table, not two.

**Three references, loaded on demand:**

| File | Owns |
|---|---|
| `references/human-behavior.md` | Perception, attention, memory, decision cost, motor limits, mental models, perceived latency |
| `references/usability.md` | Heuristic evaluation, the nine states, feedback, errors, forms, measurement |
| `references/interface-patterns.md` | Navigation, search, tables, overlays, destructive actions, notifications, onboarding, anti-patterns |

## Step 0 — Name the job, then the pattern

Never start from a component. Start from what the person is trying to do on this surface; that
picks the pattern, not the other way around.

1. **The job** — one of: monitor, operate, compare, configure, learn, decide, explore.
2. **The artifact** — the real object in the user's world (a queue, an invoice, a route, a
   record, a schedule, a roster). If you cannot name the artifact, you do not yet understand
   the surface.
3. **The pressure** — what is the user afraid of or in a hurry about? A first-time visitor needs
   orientation; an operator on their fortieth row needs speed; someone deleting needs safety.
4. **Then** pick the pattern from `interface-patterns.md` and say the reason out loud. A pattern
   with no reason is a habit.

If the composition does not match the job, no amount of polish fixes it. Fix the composition
first.

## Mode A — designing

Run these in order; each points at a reference that goes deeper.

1. **Pick the pattern** from the job above (`interface-patterns.md`). Name the failure mode you
   are avoiding, not just the pattern you are using.
2. **Check the human constraints** (`human-behavior.md`):
   - targets ≥ 44×44 px, and thumb-reachable on touch
   - keep the *simultaneous* choice set small — Hick's law is about decision time, so stage or
     default instead of listing
   - recognition over recall: never make someone remember a value from a previous screen
   - ≤ 100 ms feels instant, ≤ 1 s keeps flow, > 10 s loses them — and a perceived wait is
     shorter than a bare spinner
3. **Design all nine states** (`usability.md`), not just the happy one: idle, hover, active,
   focus, loading, empty, error, disabled, overflow.
4. **Defaults are decisions.** Every default is a claim about the common case. A required field
   with no default is often a design failure, not a neutral choice.
5. **Prevention beats recovery; undo beats confirm.** Confirm only what is irreversible,
   financial, legal, or bulk. Everything else gets an undo.
6. **Write the state copy** — empty, loading, error, no-results (`usability.md`). General voice
   is `design`'s job; the copy inside a state is ours.
7. **Name what you changed** — `path/to/file:line`, or the exact component.

## Mode B — reviewing

A usability review is not a visual review. Run these in order and do not let a prettier surface
jump the queue — a broken keyboard path outranks a dull palette.

1. **Job pass** — can the primary task be completed at all, end to end? Touch it; do not only
   look at it.
2. **Behavior pass** (`human-behavior.md`) — targets, decision cost, memory load, scanning,
   mental model, perceived latency.
3. **Heuristic pass** (`usability.md`) — Nielsen's ten, one line of evidence each.
4. **Pattern pass** (`interface-patterns.md`) — is this even the right pattern for the job, and
   which of its documented failure modes is present?
5. **State pass** — which of the nine states are missing or indistinguishable?
6. **Access pass** — the floor: keyboard reachability, visible focus, accessible names,
   contrast, zoom and reflow. Reuse `design`'s escalation triggers.
7. **Severity and report** — see below.

### Findings

One table, ordered by severity then by reach (a fix in a shared component outranks the same
symptom in one leaf). Reuse the `design` skill's severity scale so both skills feed one report.

| # | Severity | Discipline | Location | Before | After | Why |
|---|---|---|---|---|---|---|
| 1 | HIGH | Usability | `SignupForm.tsx:41` | Submit stays disabled until valid, with no reason shown | Keep it enabled; validate on submit, put the message on the field | A disabled button hides the one thing the user must fix |
| 2 | MEDIUM | Human behavior | `Filters.tsx:12` | 14 checkboxes, ungrouped, no default | Group into three labelled sets, default to the common case | Hick's law: decision time grows with the choice set |

A finding without a severity, a location, and a concrete **After** is an observation, not a
finding.

**Verdict** — exactly one: **Block** (a HIGH still stands), **Needs changes** (MEDIUM/LOW
outstanding), **Ship** (nothing actionable left, and you ran the passes you claim).

## Non-negotiables

HIGH on sight. Do not average them away because the surface is small.

- A control that never says what it is.
- A path the mouse can walk and the keyboard cannot.
- A placeholder doing a label's job.
- A disabled action whose reason is invisible.
- Meaning carried by colour alone.
- A destructive action with neither confirm nor undo.
- Content unreachable at 320 px wide or 200 % zoom.
- Motion that runs regardless of `prefers-reduced-motion`.
- A reachable state — empty, error, loading, overflow — with nothing explaining it.

## Which reference answers which question

| The question | Go to |
|---|---|
| "Why does this feel slow?" | `human-behavior.md` → Perceived latency |
| "Why can't people find it?" | `human-behavior.md` → Attention and scanning; `interface-patterns.md` → Navigation |
| "Why do they keep making mistakes?" | `usability.md` → Error prevention and recovery |
| "Is this the right control?" | `interface-patterns.md` → Selection and controls |
| "What shows when there is no data?" | `usability.md` → The nine states |
| "Modal or a page?" | `interface-patterns.md` → Overlays |
| "How do I evaluate this?" | `usability.md` → Heuristic evaluation |
| "What should I test with users?" | `usability.md` → Measurement |

## Worked example

A settings page lists 30 toggles in one column, alphabetically.

- **Job**: configure. **Artifact**: the account's behaviour. **Pressure**: the user wants one
  specific switch and will read all 30 to find it.
- The configure pattern says group by task or object, never alphabetically — grouping is the
  Gestalt proximity principle doing the work, and it turns 30 simultaneous choices into five
  sets of six.
- Behaviour: each toggle takes effect immediately, so its label must be a statement of fact
  ("Send weekly summary"), not a verb ("Enable").
- States: what does a toggle that failed to save look like? Currently nothing — that is the
  finding.
- Report one table, two findings: the grouping, and the missing save-failed state.

## What this skill refuses

- Restating visual craft that `design` already owns.
- Inventing user research, metrics, or quotes that were never gathered.
- Citing "best practice" without naming the pattern and the reason.
- Declaring a surface usable without having touched the primary task.
