#!/usr/bin/env bash
# Weekly progress: collect -> blog agent -> CV agent -> guards -> build/test -> two PRs.
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
uv_bin=$(command -v uv) || { printf 'missing executable: uv\n' >&2; exit 1; }

# Fall back to the gh CLI's stored token, so the pipeline never needs a second
# copy of the secret in the environment or /root/.hermes/.env.
if [ -z "${GITHUB_TOKEN:-}" ] && command -v gh >/dev/null 2>&1; then
    GITHUB_TOKEN=$(gh auth token 2>/dev/null || true)
    export GITHUB_TOKEN
fi

cv_root="${CV_ROOT:-/root/CV-Development}"
# The CV scripts need PyYAML and pypdf, which CV-Development already declares.
cv_python="$uv_bin run --project $cv_root --quiet python"
date_utc=$(date -u +%F)
run_dir="$repo_root/.progress-generator/$date_utc"
activity="$repo_root/.progress-generator/activity/$date_utc.json"
mkdir -p "$repo_root/.progress-generator/activity" "$run_dir"
chmod 700 "$repo_root/.progress-generator"

# 1. Activity pack, shared by both stages.
[ -f "$activity" ] || "$python3_bin" "$script_dir/collect.py" --out "$activity"

# 2. Blog stage: the post and the PR body.
blog_prompt="Use the publish-weekly-progress skill for the reporting period ending $date_utc. \
Follow the skill chain: github-progress-collector -> progress-analyzer -> github-project-context \
-> technical-blog-writer -> blog-editor. Read the activity pack at \
.progress-generator/activity/$date_utc.json. Write the post to _posts/$date_utc-weekly-progress.md \
and the PR body to .progress-generator/$date_utc/pr-body.md. Do not run git add, commit, push, or gh."

# Headless runs refuse file writes unless --yolo is passed; permission modes do not
# enable them. Least privilege is preserved by .commandcode/settings.json, because
# deny rules outrank yolo: all Shell is blocked, so the agent can write the post, the
# staging files and the CV highlights but can never run git or any other command.
cmd_flags=(-p --output-format json --no-session --skip-onboarding --no-auto-update
           --trust --yolo --max-turns 40)

# The blog stage is not fatal on its own: if the agent exits non-zero we still run the
# CV stage and the guards, and report it at the end. set -e must not abort the run here.
blog_status=0
"$cmd_bin" "${cmd_flags[@]}" "$blog_prompt" || blog_status=1

relative="_posts/$date_utc-weekly-progress.md"
body_file="$run_dir/pr-body.md"

# 3. CV stage. Independent of the blog PR: any failure here is reported, not fatal to it.
cv_status=0
cv_prompt="Use the cv-highlight-writer skill, then the cv-editor skill, for the week ending $date_utc. \
Read the activity pack at .progress-generator/activity/$date_utc.json and the analysis at \
.progress-generator/$date_utc/analysis.json if it exists, otherwise run progress-analyzer first. \
Write the proposed bullets to .progress-generator/$date_utc/cv-bullets.json, then apply only the \
bullets cv-editor approves to $cv_root/data/experience.yaml: highlights lists only and nothing else. \
If nothing qualifies, change nothing and say so. \
Do not run git add, commit, push, or gh."

cv_status=0
cv_changed=0
if ! "$cmd_bin" "${cmd_flags[@]}" "$cv_prompt"; then
    cv_status=1
elif ! $cv_python "$script_dir/cv_guard.py" --data "$cv_root/data/experience.yaml"; then
    cv_status=1
elif "$git_bin" -C "$cv_root" diff --quiet -- data/experience.yaml; then
    # Nothing qualified this week. Rendering would only churn the PDFs (weasyprint
    # embeds a timestamp), so skip the pull request entirely.
    printf 'no CV highlight changes for %s; skipping the CV pull request\n' "$date_utc"
else
    cv_changed=1
fi

if [ "$cv_status" -eq 0 ] && [ "$cv_changed" -eq 1 ]; then
    if ! (cd "$cv_root" && "$uv_bin" run --quiet pytest -q); then
        cv_status=1
    elif ! $cv_python "$script_dir/cv_sync.py" --cv-root "$cv_root" --site-root "$repo_root"; then
        cv_status=1
    elif ! $cv_python "$script_dir/cv_policy.py" \
            --pdf "$cv_root/Gaurav_Gurjar_CV.pdf" \
            --pdf "$cv_root/Gaurav_Gurjar_CV_extended.pdf"; then
        cv_status=1
    elif ! $cv_python "$script_dir/cv_publish.py" --date "$date_utc" --repo-root "$cv_root" \
            --body-file "$run_dir/cv-body.md" $no_push; then
        cv_status=1
    fi
fi

# 4. Site pull request: the post, plus the refreshed CV when the CV stage got that far.
if [ -f "$relative" ]; then
    script/cibuild
    "$python3_bin" -m unittest scripts.test_weekly_progress scripts.test_cv_refresh -q

    "$python3_bin" "$script_dir/publish.py" --date "$date_utc" --body-file "$body_file" $no_push
else
    printf 'no post produced for %s (quiet week or editor block)\n' "$date_utc"
    [ -f "$body_file" ] && cat "$body_file"
fi

status=0
if [ "$blog_status" -ne 0 ]; then
    printf 'blog agent exited non-zero; published whatever it produced\n' >&2
    status=1
fi
if [ "$cv_status" -ne 0 ]; then
    printf 'CV stage failed; the site pull request is unaffected\n' >&2
    status=1
fi
exit "$status"
