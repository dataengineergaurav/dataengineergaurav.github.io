---
name: cv-highlight-writer
description: "Turn a week of GitHub activity into CV highlight bullets. Use after progress-analyzer and before cv-editor when the weekly CV refresh proposes updates to data/experience.yaml."
---

# CV Highlight Writer

Propose a small number of achievement bullets for the CV from the analyzer's developments. You are
drafting changes to the source of truth, so restraint matters more than volume.

## Contract

Emit `.progress-generator/<date>/cv-bullets.json`:

```json
{ "bullets": [
  { "engagement_id": "e_ishir", "bullet": "...", "evidence": ["<commit-url>"] },
  { "project_id": "p_x", "bullet": "...", "replaces": 1, "evidence": ["<pr-url>"] }
] }
```

Each bullet targets an `engagement_id` or `project_id` that already exists in
`data/experience.yaml`. Never invent an id. You do not edit `data/experience.yaml`; the orchestrator
applies the bullets `cv-editor` approves.

## Hard rules

1. **Highlights only.** You propose `highlights` bullets. Never a date, role, organization,
   `client_id`, `summary`, or `technologies` change.
2. **At most one bullet per engagement per week.**
3. **The cap is 5 highlights per entry.** When an entry already holds 5, include
   `"replaces": <index>` naming the 0-based highlight you displace. Never exceed the cap.
4. **No em-dashes.** The CV test suite forbids them; they are the strongest "a machine wrote this"
   tell.
5. **Past tense, no first person, at most about 30 words.**
6. **No invented numbers.** A figure must appear in the analyzer evidence.
7. **Evidence required.** Every bullet carries at least one commit, PR, or release URL.
8. **Answer "why it mattered".** If the analyzer could not say what problem the work solved, propose
   nothing for it that week.

## STORIFY

Use the STORIFY arc (Someone, Tension, Obstacle, Risk, Intervene, Future You) only to decide *which*
development is significant. Never write the arc itself into a bullet: a CV bullet is a claim about
delivered work, not a story.

## Guardrails

- Never run git, commit, or push. Deterministic scripts own git.
- Three strong bullets beat ten weak ones. A quiet week may legitimately produce none; say so and
  emit an empty list.
