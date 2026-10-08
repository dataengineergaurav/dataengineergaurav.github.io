---
name: technical-blog-writer
description: "Turn a progress analysis into the weekly Build Log article that matches this site's post contract. Use after progress-analyzer and before blog-editor. Produces front matter plus a Markdown body in a fixed structure, optionally using the STORIFY arc when the material supports it."
---

# Technical Blog Writer

Write the weekly **Build Log** post from the `progress-analyzer` output. The analysis is the only
source you may use — do not re-introduce raw commit counts as achievements.

## Output contract

Emit **two** parts and nothing else:

**Front matter** (exactly these keys, in this order):

```yaml
---
layout: post
title: "Descriptive, specific title — not 'Weekly Update'"
date: YYYY-MM-DD
topic: Build Log
summary: "One sentence, card-ready, <= 300 chars."
description: "Search/social description, <= 300 chars."
---
```

**Body** — Markdown only, **350–900 words**, no H1 (the `post` layout renders the title), no CTA
(the layout injects one), no raw HTML, no Liquid (`{{` / `{%`).

## Body structure

Use these sections, in order. Omit a section only if it would be empty.

```
## The problem
## What changed
## What I built
## Technical decisions
## What I learned
## What didn't work
## What's next
## GitHub projects
```

- **The problem** — the tension that prompted the week's work (from `problem_solved`).
- **What changed** — the named developments, in significance order.
- **What I built** — concrete artifacts: modules, datasets, endpoints, pipelines, tests.
- **Technical decisions** — the trade-offs and why this approach over alternatives.
- **What I learned** — durable insight, not a restatement.
- **What didn't work** — dead ends and negative results. Be honest; this is what makes it credible.
- **What's next** — from `unfinished` / `open_threads`; may include maintenance/churn.
- **GitHub projects** — a short list linking each touched repo, and the specific artifacts
  (commit/PR/release) cited in `evidence`.

## STORIFY — optional, never forced

When the material is genuinely a story (a real obstacle, a decision under constraint, a turn), you
may shape the narrative with the STORIFY arc:

**Someone → Tension → Obstacle → Risk → Intervene → Future You**

Use it only if the week's work has that shape. For ordinary engineering weeks, write the plain
technical report above. Never stretch a routine week into a hero's journey.

## Voice

Match the site: practical, specific, first-person, no hype. Follow `github-project-context` so
"added a DuckDB query layer" is written as progress on a known project, not an isolated change.
See `references/article-structure.md` for a worked example and phrasing guidance.

## Do not

- Invent accomplishments, metrics, or users.
- Claim production usage, scale, or performance without evidence in `evidence`.
- Include a CTA, H1, or HTML.
- Exceed 300 characters in `summary`/`description`, or 900 words in the body.
