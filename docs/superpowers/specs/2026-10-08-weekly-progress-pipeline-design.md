# Weekly Progress Pipeline — Design

Date: 2026-10-08

## Problem

The site publishes research-led authority articles and a second-brain wiki, but there is no
recurring, first-person record of what was actually *built* on GitHub each week. Manually writing
one is the first thing to slip, and a naive automation ("summarize my commits") produces a commit
log, not progress. The site's credibility rests on specifics, so the weekly post must be sourced
from evidence and must never exaggerate.

## Approach

Split the work into a **deterministic layer** and a **reasoning layer**:

- **Deterministic** (scripts, no LLM): gather GitHub activity into a reproducible JSON pack, and
  publish the finished post as a pull request. These parts must be boring and auditable.
- **Reasoning** (Command Code skills): normalize activity, classify changes, write the article,
  and edit it skeptically. These parts need judgment and belong in reusable skills, not code.

The split is a safety boundary: the agent stages cannot touch git or the network beyond the
collector's output, and the scripts never invent prose. Approval is the pull request, so nothing
reaches `master` (and therefore the live site) without review.

## Components

### Deterministic

- `automation/weekly-progress/collect.py` — GitHub REST reads (repos, commits + changed files, PRs
  /merged PRs/issues via search, releases, events) for a 7-day window; normalizes into an activity
  pack; drops merge commits and flags churn (lockfiles, dependency bumps, formatting, docs). Merges
  the `projects.yaml` catalog. `doctor` verifies token scopes. `--from-raw` builds a pack offline.
- `automation/weekly-progress/publish.py` — requires a clean, in-sync worktree; asserts the only
  change is `_posts/<date>-weekly-progress.md`; commits exactly that file on branch
  `weekly-progress/<date>`; pushes; opens a PR via the GitHub API. Idempotent on re-run.
- `automation/weekly-progress/run.sh` — orchestrates collect → agent → single-file guard →
  `script/cibuild` + unit tests → publish. `--no-push` rehearses without publishing.
- `weekly-progress-generator.{service,timer}` — Mondays 04:00 UTC, `Persistent=true`.
- `automation/weekly-progress/setup.sh` — `check|install|remove`, refuses foreign units and
  non-canonical checkouts (mirrors `scripts/setup_article_pipeline.sh`).

### Reasoning (skills, `.commandcode/skills/`)

1. `github-progress-collector` — invoke the collector; normalize; enforce "commits ≠ progress".
2. `progress-analyzer` — classify into `NEW_CAPABILITY | IMPROVEMENT | BUG_FIX | RESEARCH |
   ARCHITECTURE | DATA | AI | DOCUMENTATION | MAINTENANCE | EXPERIMENT`; answer the five questions;
   collapse to 2–5 named developments with evidence links.
3. `technical-blog-writer` — fixed section structure; optional STORIFY; emits the post contract.
4. `github-project-context` — `projects.yaml` catalog; framing + maintenance mode.
5. `blog-editor` — skeptical gate: no invented accomplishments, no unsupported production/scale/
   performance claims, no inflated maintenance, no secrets, no private-repo details.
6. `publish-weekly-progress` — orchestrator; runs the chain and hands off to `publish.py`. Never
   commits or pushes.

## Post contract

`_posts/<date>-weekly-progress.md`, front matter `layout: post`, `title`, `date`,
`topic: Build Log`, `summary`, `description`; body Markdown only, 350–900 words, no H1 (the `post`
layout renders the title), no CTA (the layout injects one), no HTML/Liquid. `Build Log` is picked
up by the existing `/insights/` filters automatically.

## Safety

- Agent never runs git; `publish.py` is the sole writer and never targets `master`.
- `run.sh` guards that exactly one tracked file changed before building or publishing.
- `script/cibuild` runs before publish, so content-policy (client/secret names) and link checks gate
  the PR.
- Collector redacts nothing it shouldn't expose: `private: true` projects are framing-only.
- Secrets come from `/root/.hermes/.env` (`GITHUB_TOKEN`), consistent with the article/wiki lanes.

## Failure modes

- No non-churn activity → no post; a short note is written and the run exits 0.
- Editor `block` → no post; the blocking reasons become the note.
- Dirty worktree / out-of-sync branch / extra changed file → `run.sh` aborts before any PR.
- Missing or under-scoped token → `doctor` fails with an actionable message.

## Alternatives considered

- **Single Python pipeline with LLM stages** (as first drafted): simpler to schedule, but bakes
  editorial judgment into code and hides the reasoning. Rejected in favor of skills.
- **Direct push with a Telegram approve gate** (like the article lane): faster, but the owner
  explicitly preferred PR review and no direct-to-production writes.
- **A new `_progress/` collection**: more separation, but duplicates the archive/filters for no
  benefit; `Build Log` as a topic reuses existing machinery.

## Testing

`scripts/test_weekly_progress.py` (unittest, no network): project-catalog parsing, pack
normalization (merge-drop, churn, flags, stats, PR/issue/release/new-project), truncation, period
math, remote parsing, publish guard accept/reject, skill frontmatter/contract, setup-script
refusal. CI additionally runs `script/cibuild`.
