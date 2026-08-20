#!/usr/bin/env bash
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(dirname -- "$script_dir")

case "${1:-}" in
    install|remove)
        if [ "$repo_root" != /root/dataengineergaurav.github.io ]; then
            printf 'refusing operation outside the canonical checkout: %s\n' "$repo_root" >&2
            exit 1
        fi
        ;;
esac

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

ensure_owned_plugin_destination() {
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
}

ensure_owned_unit() {
    local unit=$1 source=$2 fragment
    if fragment=$("$systemctl_bin" show --value --property=FragmentPath "$unit" 2>/dev/null); then
        [ -z "$fragment" ] || [ "$fragment" = "$source" ] || {
            printf 'refusing conflicting systemd unit: %s=%s\n' "$unit" "$fragment" >&2
            exit 1
        }
    fi
}

ensure_owned_units() {
    ensure_owned_unit personal-article-generator.service "$script_dir/personal-article-generator.service"
    ensure_owned_unit personal-article-generator.timer "$script_dir/personal-article-generator.timer"
}

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
        printf 'python3=%s\ncodex=%s\nhermes=%s\ngit=%s\nsystemctl=%s\nhermes-config=%s\n' \
            "$python3_bin" "$codex_bin" "$hermes_bin" "$git_bin" \
            "$systemctl_bin" "$hermes_config"
        "$hermes_bin" gateway status
        ;;
    install)
        ensure_owned_plugin_destination
        ensure_owned_units
        mkdir -p "$repo_root/.article-generator"
        chmod 700 "$repo_root/.article-generator"
        mkdir -p "$(dirname -- "$plugin_destination")"
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
        ensure_owned_plugin_destination
        ensure_owned_units
        remove_timer
        if [ -L "$plugin_destination" ]; then
            "$hermes_bin" plugins disable personal_article_approval
            rm "$plugin_destination"
            "$hermes_bin" gateway restart
        fi
        ;;
    *)
        printf 'usage: %s check|install|remove\n' "$0" >&2
        exit 2
        ;;
esac
