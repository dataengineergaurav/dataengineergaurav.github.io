#!/usr/bin/env bash
# Install/remove/check the weekly progress blog timer.
# Usage: setup.sh check|install|remove
set -euo pipefail

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
repo_root=$(dirname -- "$(dirname -- "$script_dir")")

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
    [ -x "$path" ] || { printf 'not executable: %s\n' "$path" >&2; exit 1; }
    printf '%s\n' "$path"
}

python3_bin=$(resolve_executable python3)
git_bin=$(resolve_executable git)
systemctl_bin=$(resolve_executable systemctl)
cmd_bin=$(resolve_executable cmd)

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
    ensure_owned_unit weekly-progress-generator.service "$script_dir/weekly-progress-generator.service"
    ensure_owned_unit weekly-progress-generator.timer "$script_dir/weekly-progress-generator.timer"
}

doctor() {
    local status
    if doctor_output=$("$python3_bin" "$script_dir/collect.py" doctor); then
        [ -z "$doctor_output" ] || printf '%s\n' "$doctor_output"
    else
        status=$?
        printf '%s\n' "$doctor_output" >&2
        return "$status"
    fi
}

case "${1:-}" in
    check)
        printf 'python3=%s\ngit=%s\nsystemctl=%s\ncmd=%s\nrepo=%s\n' \
            "$python3_bin" "$git_bin" "$systemctl_bin" "$cmd_bin" "$repo_root"
        doctor
        ;;
    install)
        ensure_owned_units
        mkdir -p "$repo_root/.progress-generator"
        chmod 700 "$repo_root/.progress-generator"
        chmod +x "$script_dir/run.sh"
        "$systemctl_bin" link --force \
            "$script_dir/weekly-progress-generator.service" \
            "$script_dir/weekly-progress-generator.timer"
        "$systemctl_bin" daemon-reload
        "$systemctl_bin" enable --now weekly-progress-generator.timer
        doctor
        ;;
    remove)
        ensure_owned_units
        "$systemctl_bin" disable --now weekly-progress-generator.timer
        "$systemctl_bin" disable weekly-progress-generator.service
        "$systemctl_bin" daemon-reload
        ;;
    *)
        printf 'usage: %s check|install|remove\n' "$0" >&2
        exit 2
        ;;
esac
