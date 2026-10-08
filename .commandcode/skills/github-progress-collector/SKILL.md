---
name: github-progress-collector
description: "Turn raw GitHub activity for a period into a normalized activity model for the weekly progress blog. Use when starting a weekly progress run, or when asked what actually changed in your repositories this week. Applies the rule that commits are not progress."
---

# GitHub Progress Collector

Collect and **normalize** GitHub activity for a reporting period. The output is a substrate for
`progress-analyzer` — not a summary, and not a commit list.

## Run the collector

Never call the GitHub API yourself. Use the deterministic collector so the run is reproducible
and secret-safe:

```bash
# write the raw pack (feed this to the analyzer)
python3 automation/weekly-progress/collect.py --out .progress-generator/activity/<YYYY-MM-DD>.json

# inspect without writing
python3 automation/weekly-progress/collect.py --dry-run

# build a pack from a saved raw snapshot (offline / tests)
python3 automation/weekly-progress/collect.py --from-raw .progress-generator/activity/raw-<date>.json --out .progress-generator/activity/<date>.json
```

Reporting window defaults to the previous 7 days (`PROGRESS_WINDOW_DAYS`). Override with
`--window-days N` or explicit `--since` / `--until`.

## What the collector returns

A JSON document with these top-level keys:

- `period` — `{since, until, days}`
- `repos[]` — active repos: `{full_name, private, created_at, pushed_at, archived, first_seen, url}`
- `commits[]` — `{repo, sha, date, message, files[], flags{readme,docs,test,churn}}`
- `pull_requests[]` — `{repo, number, title, state, merged, created_at, updated_at, url}`
- `issues[]` — `{repo, number, title, state, created_at, url}`
- `releases[]` — `{repo, tag, name, created_at, url}`
- `new_projects[]` / `deleted_projects[]` / `archived_projects[]`
- `projects_context` — merged from `github-project-context/projects.yaml`
- `stats` — `{commits, files_changed, prs_opened, prs_merged, issues_opened, releases}`

## Normalization rules (the important part)

Commits are evidence, not achievements. Before handing off:

1. **Dedupe** commits by `sha`; drop merge commits (`Merge branch`, `Merge pull request`).
2. **Group** commits by `repo` and then by changed-file cluster (same directory/feature area).
3. **Classify churn and exclude it from "progress"** — mark `churn: true` for:
   - dependency/version bumps (`dependabot`, `bump `, `chore(deps)`)
   - formatting / lint-only commits
   - lockfile-only changes (`package-lock.json`, `Gemfile.lock`, `poetry.lock`, `yarn.lock`,
     `pnpm-lock.yaml`, `Cargo.lock`, `uv.lock`, `go.sum`)
   - pure renames with no content change
   Churn may be mentioned under `## What's next`/maintenance, never counted as an achievement.
4. **Identify**: new projects (first activity in the window), deleted projects, newly archived
   projects, README/docs changes, and release tags — these are high-signal.
5. **Attach context**: join each repo to `projects_context` so downstream stages know the project's
   purpose, audience, stack, and themes.

## Output contract

Hand `progress-analyzer` either the collector JSON path or the normalized model. State the
window, the number of repos touched, and how many commits were discarded as churn. If the window
has no non-churn activity, say so plainly and stop — do **not** manufacture a post.

## Guardrails

- Read-only: never modify repository files, never run `git commit`/`git push`.
- Never print `GITHUB_TOKEN` or any secret. The collector already redacts; do not re-log raw tokens.
- Do not "improve" numbers. Report what the data shows.
