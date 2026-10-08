#!/usr/bin/env bash
# Weekly progress blog: collect -> agent (skills) -> guard -> build/test -> open PR.
# Usage: run.sh [--no-push]
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(dirname -- "$(dirname -- "$script_dir")")
cd "$repo_root"

no_push=""
if [ "${1:-}" = "--no-push" ]; then
    no_push="--no-push"
fi

python3_bin=$(command -v python3) || { printf 'missing executable: python3\n' >&2; exit 1; }
cmd_bin=$(command -v cmd) || { printf 'missing executable: cmd\n' >&2; exit 1; }
git_bin=$(command -v git) || { printf 'missing executable: git\n' >&2; exit 1; }

date_utc=$(date -u +%F)
run_dir="$repo_root/.progress-generator/$date_utc"
mkdir -p "$repo_root/.progress-generator/activity" "$run_dir"
chmod 700 "$repo_root/.progress-generator"

"$python3_bin" "$script_dir/collect.py" --out "$repo_root/.progress-generator/activity/$date_utc.json"

prompt="Use the publish-weekly-progress skill for the reporting period ending $date_utc. \
Follow the skill chain: github-progress-collector -> progress-analyzer -> github-project-context \
-> technical-blog-writer -> blog-editor. Read the activity pack at \
.progress-generator/activity/$date_utc.json. Write the post to _posts/$date_utc-weekly-progress.md \
and the PR body to .progress-generator/$date_utc/pr-body.md. Do not run git add, commit, push, or gh."

"$cmd_bin" -p "$prompt" --output-format json --no-session --skip-onboarding --no-auto-update --max-turns 40

relative="_posts/$date_utc-weekly-progress.md"
body_file="$run_dir/pr-body.md"

if [ ! -f "$relative" ]; then
    printf 'no post produced for %s (quiet week or editor block)\n' "$date_utc"
    [ -f "$body_file" ] && cat "$body_file"
    exit 0
fi

status=$("$git_bin" status --porcelain --untracked-files=all)
if [ "$status" != "?? $relative" ]; then
    printf 'publish guard failed: expected only "?? %s", saw:\n%s\n' "$relative" "${status:-<clean>}" >&2
    exit 1
fi

script/cibuild
"$python3_bin" -m unittest scripts.test_weekly_progress -q

"$python3_bin" "$script_dir/publish.py" --date "$date_utc" --body-file "$body_file" $no_push
