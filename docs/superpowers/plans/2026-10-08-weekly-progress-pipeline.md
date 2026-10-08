# Weekly Progress Pipeline — Implementation Plan

Date: 2026-10-08
Spec: `docs/superpowers/specs/2026-10-08-weekly-progress-pipeline-design.md`

## Tasks

- [x] `automation/weekly-progress/collect.py` — activity pack + `doctor` + `--from-raw`.
- [x] `automation/weekly-progress/publish.py` — guard + branch + commit + PR (idempotent).
- [x] `automation/weekly-progress/run.sh` — collect → agent → guard → build/test → publish.
- [x] `automation/weekly-progress/weekly-progress-generator.{service,timer}`.
- [x] `automation/weekly-progress/setup.sh` — `check|install|remove`.
- [x] Six skills in `.commandcode/skills/` (+ `github-project-context/projects.yaml`,
      `technical-blog-writer/references/`, `blog-editor/references/`).
- [x] `scripts/test_weekly_progress.py`.
- [x] `.gitignore` — `.progress-generator/`.
- [x] `README.md` — pipeline + skills sections.
- [x] Design spec + this plan.

## Verification performed

- [x] `python3 -m unittest scripts.test_weekly_progress -v` — 17 tests pass.
- [x] `python3 automation/weekly-progress/collect.py --from-raw <fixture>` — pack written + summarized.
- [x] `python3 automation/weekly-progress/collect.py doctor` — reports token/catalog status.
- [x] `automation/weekly-progress/setup.sh bogus` — exit 2; foreign checkout refused.
- [x] `script/cibuild` — build + html-proofer + content policy pass.

## Operator steps (not code)

- [ ] Add `GITHUB_TOKEN` (`repo` + `read:user`) to `/root/.hermes/.env`.
- [ ] Review/confirm `.commandcode/skills/github-project-context/projects.yaml` entries.
- [ ] `automation/weekly-progress/setup.sh install`.
- [ ] First supervised run: `automation/weekly-progress/run.sh --no-push`, inspect the post, then a
      full `automation/weekly-progress/run.sh` to open the first PR.

## Notes / known limits

- Activity-item collection uses the search API (30 req/min); a normal week is well within budget.
- Deletions are inferred from events (public + authed-private); very recent deletions may be missed.
- `_config.yml` intentionally unchanged: `Build Log` is a free-text topic and dot-dirs are ignored
  by Jekyll. Optionally add `automation` to `exclude` to stop publishing tooling into `_site`.
