---
name: publish-weekly-progress
description: "Orchestrate the weekly progress blog end to end: determine the period, collect GitHub activity, analyze it, write the Build Log, run editorial checks, build and test the site, then hand off to the deterministic publisher that opens a PR. Use for scheduled weekly runs and when the owner asks to publish this week's progress."
argument-hint: "[YYYY-MM-DD period end] [--no-push]"
---

# Publish Weekly Progress

Run the weekly Build Log pipeline. Reasoning is yours; **git and publishing are not** — a
deterministic script does those, so this skill never commits, pushes, or opens a PR itself.

## Contract

Write only these paths; never touch git state:

| Path | Written by | Purpose |
|---|---|---|
| `.progress-generator/activity/<date>.json` | collector script | raw activity pack |
| `.progress-generator/<date>/analysis.json` | you (analyzer) | structured progress analysis |
| `.progress-generator/<date>/editor.json` | you (editor) | verdict + revised body |
| `.progress-generator/<date>/pr-body.md` | you | PR description (summary + editor checklist) |
| `_posts/<date>-weekly-progress.md` | you (writer) | the post the PR will contain |

`_posts/<date>-weekly-progress.md` must be the **only** change to tracked files. `automation/weekly-progress/publish.py`
enforces this and is the only thing allowed to create a branch, commit, push, and open the PR.

## Steps

1. **Period.** Use the previous 7 days ending at the run date (or the date argument). Record
   `since`/`until`.
2. **Collect.** `github-progress-collector`:
   `python3 automation/weekly-progress/collect.py --out .progress-generator/activity/<date>.json`.
   If the pack has no non-churn activity, write a short "quiet week" note to
   `.progress-generator/<date>/pr-body.md`, create **no** post, and stop.
3. **Analyze.** `progress-analyzer` → `.progress-generator/<date>/analysis.json`.
   Identify the **2–5 most meaningful developments**.
4. **Write.** `technical-blog-writer` → `_posts/<date>-weekly-progress.md` (front matter + body).
   Use `github-project-context` for framing.
5. **Edit.** `blog-editor` → `.progress-generator/<date>/editor.json`. Apply `revised_body` when the
   verdict is `revise`; if `block`, do not write a post — write the blocking reasons to the PR body
   file instead and stop.
6. **PR body.** Write `.progress-generator/<date>/pr-body.md`: the analyzer headline + development
   list, the editor verdict/checklist, and the evidence links.
7. **Hand off.** Do **not** run git. Return control to `automation/weekly-progress/run.sh`, which
   builds the site, runs tests, guards that exactly one file changed, and calls
   `python3 automation/weekly-progress/publish.py --date <date> --body-file .progress-generator/<date>/pr-body.md`.

## Manual use

```bash
# full scheduled-style run (collect → agent → guard → build/test → PR)
automation/weekly-progress/run.sh

# rehearsal: everything except branch/commit/push/PR
automation/weekly-progress/run.sh --no-push
```

Approval happens on the **pull request** — review the diff, then merge to publish. The agent must
never push to `master`.

## Guardrails

- No `git add`/`commit`/`push`/`gh` from this skill or any skill it calls.
- No secrets, no private-repo details, no client names in the post.
- If analysis or editing is inconclusive, produce a shorter honest note rather than a padded post.
