# Weekly CV Refresh — Design

**Date:** 2026-10-09
**Status:** Implemented (2026-10-09) — see the plan's Outcome section for the deviations found during execution.
**Repos:** `dataengineergaurav.github.io` (pipeline host), `CV-Development` (source of truth)

## Problem

The CV exists in two disconnected places.

`CV-Development` holds the real source of truth: a relational data file
(`data/experience.yaml`) with `organizations`, `engagements` and `projects`, where
achievement bullets are `highlights` string lists, rendered to HTML and PDF by
`render.py` with `weasyprint`. Its tests encode editorial invariants
(no em-dashes, no repeated project/role bullets, every highlight must render, a
years-of-experience claim that may not exceed the union of engagement dates).

The portfolio site holds a **hand-copied snapshot** of the CV PDF at
`Gaurav_Gurjar_CV_AI-Data-Engineer.pdf`, linked once from `index.html`. There is no
programmatic link between the repos: nothing reads `CV-Development`, nothing detects
a stale PDF, and nothing regenerates it.

Two failures follow from that:

1. **Drift.** The site PDF has moved ahead of `experience.yaml` and contains claims
   that do not exist in the source of truth.
2. **A live policy leak.** The site's content policy (`scripts/test_public_content.py`,
   `FORBIDDEN_NAMES`) forbids private organization names, and CI enforces it on the
   built site. But `public_text_files()` only reads `.html`, `.xml` and `.txt`, so
   **PDFs are never scanned**. The currently published CV leaks seven forbidden names:

   ```
   sagesure, ishir, cannaspyglass, petfolk, casepoint, archetypal ai, 6overn.ai
   https://dataengineergaurav.github.io/Gaurav_Gurjar_CV_AI-Data-Engineer.pdf
   ```

   CI passes because the leak is invisible to it.

The weekly-progress pipeline (`automation/weekly-progress/`) already solves the hard
half of the problem for the blog: a deterministic GitHub activity collector, six
Command Code skills that reason over the activity pack, and a publisher that opens a
pull request and never writes to the base branch. This design extends that pipeline
rather than building a second one.

## Goal

Make `CV-Development` the single source of truth for the candidate's work history,
and derive the public CV from it on a weekly cadence, using the existing pipeline's
discipline: deterministic scripts own every git action, an agent owns the prose, and a
pull request is the approval step.

**Success criteria**

- A Monday run reads GitHub activity, proposes CV bullet updates, and opens a PR
  against `CV-Development` — with no timeline mutation and no manual editing.
- The site's CV PDF is regenerated from `CV-Development` and refreshed in the same
  run, so the two can no longer drift.
- No `FORBIDDEN_NAMES` or `RETIRED_CLAIMS` term can reach a published artifact,
  including PDFs.
- A quiet week, a failed guard, or an editor block produces no PR and no damage.

**Non-goals**

- Changing employment dates, roles, organizations or the summary. Highlights only.
- Automatically merging anything. The PR is the human gate, as it is for the blog.
- Building a second scheduler or a second collector.
- Redesigning the CV templates beyond what the public projection requires.

## Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Primary outcome | Single source of truth | The portfolio CV must be derived from `experience.yaml`. |
| Pipeline location | Portfolio repo runs both | Reuses the existing timer, collector and PR machinery; no duplicated tooling. |
| Edit boundary | `highlights` only | Keeps the tests as a guard rail; dates and roles are too destructive to automate. |
| Writer approach | Mirror the blog pipeline | `collect.py` + `progress-analyzer` are reused; only the writer/editor are new. |
| `6overn.ai` | Removed from both | It is a forbidden client identifier, not a claim to preserve. |
| Public CV names | Anonymize clients, keep employers | Matches the site's editorial policy while keeping the CV useful for hiring. |

## Architecture

One Monday run, two pull requests. `run.sh` keeps its blog stage and gains a CV stage.
Both stages produce work *before* any publisher runs, because the refreshed PDF is part
of the site pull request.

```
systemd timer (Mon 04:00 UTC)
  └─ automation/weekly-progress/run.sh
       ├─ blog stage (existing)
       │    collect.py → github-progress-collector → progress-analyzer
       │    → technical-blog-writer → blog-editor
       │    → _posts/<date>-weekly-progress.md
       │
       ├─ cv stage (new)
       │    reruns collect.py only if the pack is absent; reuses the pack written
       │    above, and runs progress-analyzer itself if analysis.json is missing
       │    → cv-highlight-writer → cv-editor
       │    → cv_guard.py        (highlights-only diff allow-list)
       │    → uv run pytest      (CV-Development integration gate)
       │    → cv_policy.py       (PDF text vs FORBIDDEN_NAMES)
       │    → cv_sync.py         (renders CV; writes PDF + version.json into the
       │                          site worktree)
       │    → cv_publish.py ..... CV-Development PR (main)
       │
       └─ site PR (existing publish.py, widened guard)
            commits {post, PDF, version.json} → PR against master
```

New scripts live in `automation/weekly-progress/`; the two new skills live in
`.commandcode/skills/`.

The two stages are **independent**. A blog failure does not block the CV pull request
and vice versa; each writes its outcome to `.progress-generator/<date>/` and the run
reports a combined summary. If the CV stage fails, `cv_sync.py` leaves the site
worktree unchanged and the site PR carries the post alone. `publish.py`'s guard
therefore accepts either `{post}` or `{post, PDF, version.json}`, and nothing else.

### Write contract

Mirrors the existing pipeline's boundary:

- Agent skills may write only `.progress-generator/**`, the blog post, and
  `/root/CV-Development/data/experience.yaml`.
- Deterministic scripts own every git action (branch, add, commit, push, PR) and every
  generated artifact (HTML, PDFs, the synced site PDF, the version marker).
- The agent never runs `git add/commit/push` or `gh`.

## Components

### New skills (`.commandcode/skills/`)

**`cv-highlight-writer`** — consumes `analysis.json` and the current `experience.yaml`;
emits `.progress-generator/<date>/cv-bullets.json`:

```jsonc
{ "bullets": [
  { "engagement_id": "e_ishir", "bullet": "…", "evidence": ["<commit-url>"] },
  { "project_id": "p_x", "bullet": "…", "replaces": 1, "evidence": ["<pr-url>"] }
] }
```

Constraints: past tense, no first person, no em-dashes, at most ~30 words, no invented
metrics, at most one bullet per engagement per week, `replaces` required when an
engagement is at its highlight cap.

**`cv-editor`** — the skeptical gate, modelled on `blog-editor`. Rejects a bullet that
duplicates an existing role bullet, lacks evidence, contradicts the Build Log, or
contains a forbidden name. Returns
`{verdict: approve|revise|block, violations, notes, revised_bullets}`. Never commits.

### Promotion bar (anti-bloat)

A CV is not a changelog. A development earns a bullet only if it survives the
collector's churn filtering **and** `progress-analyzer` answers "what problem did it
solve / what is now possible". Churn-only weeks produce nothing. The number of
highlights per engagement is capped at `MAX_HIGHLIGHTS_PER_ENGAGEMENT` (default 5),
enforced deterministically; at the cap the writer must displace an existing bullet via
`replaces`. This bounds the one-page render instead of letting it grow.

### Public projection

`experience.yaml` `organizations[*]` gains two optional fields:

```yaml
organizations:
  sagesure:
    name: SageSure
    public_name: "US residential property insurer"   # optional
    public_about: "…"                                 # optional
```

The render prefers `public_name` / `public_about` when present and falls back to
`name` / `about`. Employers-of-record (Ishir, CannaSpyglass, AI Squared, Casepoint)
carry no `public_name` and render unchanged; clients carry one. The private source of
truth keeps full detail. `6overn.ai` / Archetypal AI is deleted outright.

Employer names are themselves on the site's `FORBIDDEN_NAMES`, so the published CV is
governed by a **client-scoped** denylist: a `CV_ALLOWED_NAMES` tuple records the
employers-of-record permitted on the CV, and the effective CV denylist is
`FORBIDDEN_NAMES` minus that set (plus `RETIRED_CLAIMS`). The site's own prose keeps
the full list. The pipeline's policy check asserts that no client-scoped forbidden
term reaches either rendered PDF.

### Policy gate (closes the CI hole)

Two layers, because the hole is in CI, not just this pipeline:

1. `cv_policy.py` extracts text from every rendered PDF (`pypdf`, already a
   CV-Development dependency) and fails the run if any client-scoped forbidden term or
   `RETIRED_CLAIMS` term appears. This is the check that would have caught today's leak.
2. `scripts/test_public_content.py` is extended so committed PDFs are scanned in CI,
   not only `.html` / `.xml` / `.txt` — PDFs against the client-scoped list, source and
   HTML against the full `FORBIDDEN_NAMES`. The portfolio CI installs `pypdf`. This
   protects any artifact, however it is added.

### Association and sync

`cv_sync.py` (deterministic): in a clean, origin-synchronized `/root/CV-Development`,
run `render.py` and `render.py --expanded`, then copy the **one-pager** render
(`Gaurav_Gurjar_CV.pdf`, a single A4 page) into the site root under the site's existing
name `Gaurav_Gurjar_CV_AI-Data-Engineer.pdf`, so `index.html` is untouched. The
expanded render is committed to `CV-Development` only. Alongside the PDF, write
`Gaurav_Gurjar_CV_AI-Data-Engineer.version.json`:

```json
{ "cv_commit": "<sha>", "rendered_at": "<iso8601>", "sha256": "<hash of the pdf>" }
```

A small CI check asserts the marker's `sha256` matches the committed PDF, so a
hand-swapped or stale PDF fails the build. CI cannot see the upstream repository, so
this detects tampering and desync within the site, not upstream drift — the pipeline
being the only writer is what guarantees freshness.

### Publishers

- `cv_publish.py` mirrors `publish.py`: never targets the base branch, hashes the
  reviewed files, verifies the staged blobs match, is idempotent via a PR lookup, and
  cleans up on failure. Differences: `--repo-root /root/CV-Development`, base `main`,
  branch `cv-refresh/<date>`, and a multi-file allow-list
  (`data/experience.yaml` plus the four regenerated artifacts).
- The site's `publish.py` guard widens from "exactly the post" to the allow-list
  `{_posts/<date>-weekly-progress.md, Gaurav_Gurjar_CV_AI-Data-Engineer.pdf,
  Gaurav_Gurjar_CV_AI-Data-Engineer.version.json}`.

## Failure modes

| Condition | Behaviour |
| --- | --- |
| No non-churn activity, or no development clears the promotion bar | No CV PR; note written; exit 0 |
| `cv-editor` returns `block` | No CV PR; blocking reasons become the note |
| `cv_guard.py` sees a non-highlight change | Abort before any branch or push |
| `experience.yaml` cap exceeded without `replaces` | Abort before any branch or push |
| `pytest` (render suite) fails | Abort; branch deleted |
| `cv_policy.py` finds a forbidden term | Abort; branch deleted |
| `CV-Development` dirty or out of sync with origin | Abort with an actionable message |
| PDF sync fails | Site PR is not opened; CV PR unaffected |
| Blog stage fails | CV stage still runs; combined summary records both |

## Testing

`scripts/test_cv_refresh.py` (unittest, no network), following the existing
`test_weekly_progress.py` pattern:

- `cv_guard` accepts a highlights-only diff and rejects edits to dates, roles,
  `organization_id`, `summary` or `technologies`.
- Highlight cap is enforced, and a `replaces` entry is accepted at the cap.
- `cv_policy` flags a PDF whose extracted text contains a forbidden name, and passes a
  clean one.
- The version marker's `sha256` check rejects a mismatched PDF.
- `publish` multi-file allow-list accepts the expected set and rejects extras.
- Skill frontmatter contract for `cv-highlight-writer` and `cv-editor` (matching
  `name:`/`description:`), and that the orchestrator references `cv_publish.py`.

`CV-Development/tests/test_render.py` remains the integration gate, run via
`uv run pytest` before the CV PR is opened. It gains the `public_name` projection test.

## Rollout

1. Reconcile content first: add `public_name` / `public_about` for client
   organizations and delete `6overn.ai` / Archetypal AI, then regenerate the CV and
   confirm `cv_policy.py` is clean against the regenerated PDFs.
2. Land the CI PDF scan in `test_public_content.py` so the existing leak fails the
   build immediately.
3. Add the skills and scripts; run `run.sh --no-push` for a supervised rehearsal.
4. Enable the CV stage in the existing Monday timer only after a clean rehearsal.

## Open questions

- Whether to decouple the site's hardcoded CV filename via `_config.yml` (nice to have,
  not required by this design).
- Whether the private source should record the `6overn.ai` advisor engagement at all,
  hidden from the public projection. Default: removed entirely.
