#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(dirname -- "$script_dir")

if [ "${1:-}" = install ] && [ "$repo_root" != /root/dataengineergaurav.github.io ]; then
    printf 'refusing installation outside the canonical checkout: %s\n' "$repo_root" >&2
    exit 1
fi

resolve_executable() {
    local name=$1 path
    path=$(command -v "$name") || {
        printf 'missing executable: %s\n' "$name" >&2
        exit 1
    }
    case "$path" in
        /*) ;;
        *) printf 'executable is not absolute: %s=%s\n' "$name" "$path" >&2; exit 1 ;;
    esac
    [ -x "$path" ] || {
        printf 'not executable: %s\n' "$path" >&2
        exit 1
    }
    printf '%s\n' "$path"
}

python3_bin=$(resolve_executable python3)
codex_bin=$(resolve_executable codex)
hermes_bin=$(resolve_executable hermes)
npm_bin=$(resolve_executable npm)
git_bin=$(resolve_executable git)
systemctl_bin=$(resolve_executable systemctl)
hermes_config=$("$hermes_bin" config path)
case "$hermes_config" in
    /*) ;;
    *) printf 'Hermes config path is not absolute: %s\n' "$hermes_config" >&2; exit 1 ;;
esac
hermes_dir=$(dirname -- "$hermes_config")
approval_source="$repo_root/automation/hermes-article-approval"
plugin_destination="$hermes_dir/plugins/personal_article_approval"

install_timer() {
    "$systemctl_bin" link --force \
        "$script_dir/personal-article-generator.service" \
        "$script_dir/personal-article-generator.timer"
    "$systemctl_bin" daemon-reload
    "$systemctl_bin" enable --now personal-article-generator.timer
}

remove_timer() {
    "$systemctl_bin" disable --now personal-article-generator.timer
    "$systemctl_bin" disable personal-article-generator.service
    "$systemctl_bin" daemon-reload
}

case "${1:-}" in
    check)
        printf 'python3=%s\ncodex=%s\nhermes=%s\nnpm=%s\ngit=%s\nsystemctl=%s\nhermes-config=%s\n' \
            "$python3_bin" "$codex_bin" "$hermes_bin" "$npm_bin" "$git_bin" \
            "$systemctl_bin" "$hermes_config"
        "$hermes_bin" gateway status
        ;;
    install)
        mkdir -p "$repo_root/.article-generator"
        chmod 700 "$repo_root/.article-generator"
        mkdir -p "$(dirname -- "$plugin_destination")"
        if [ -L "$plugin_destination" ]; then
            resolved_destination=$(CDPATH= cd -- "$plugin_destination" 2>/dev/null && pwd -P) || {
                printf 'refusing conflicting plugin symlink: %s\n' "$plugin_destination" >&2
                exit 1
            }
            [ "$resolved_destination" = "$approval_source" ] || {
                printf 'refusing conflicting plugin symlink: %s\n' "$plugin_destination" >&2
                exit 1
            }
        elif [ -e "$plugin_destination" ]; then
            printf 'refusing existing plugin destination: %s\n' "$plugin_destination" >&2
            exit 1
        fi
        [ -L "$plugin_destination" ] || ln -s "$approval_source" "$plugin_destination"
        "$hermes_bin" plugins enable personal_article_approval
        install_timer
        "$hermes_bin" gateway restart
        if doctor_output=$("$python3_bin" "$repo_root/scripts/article_pipeline.py" doctor); then
            [ -z "$doctor_output" ] || printf '%s\n' "$doctor_output"
        else
            doctor_status=$?
            printf '%s\n' "$doctor_output" >&2
            case "$doctor_output" in
                *"not synchronized with its upstream"*|*"no upstream"*|*"@{upstream}"*)
                    printf 'operational blocker: push the branch, set its upstream, and rerun doctor; installation was left intact\n' >&2
                    ;;
                *) printf 'article pipeline doctor failed; installation was left intact\n' >&2 ;;
            esac
            exit "$doctor_status"
        fi
        ;;
    remove)
        remove_timer
        if [ -L "$plugin_destination" ]; then
            resolved_destination=$(CDPATH= cd -- "$plugin_destination" 2>/dev/null && pwd -P) || resolved_destination=
            if [ "$resolved_destination" = "$approval_source" ]; then
                "$hermes_bin" plugins disable personal_article_approval
                rm "$plugin_destination"
                "$hermes_bin" gateway restart
            else
                printf 'leaving non-matching plugin symlink: %s\n' "$plugin_destination" >&2
            fi
        fi
        ;;
    *)
        printf 'usage: %s check|install|remove\n' "$0" >&2
        exit 2
        ;;
esac
