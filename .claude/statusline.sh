#!/usr/bin/env bash

# Read-only Claude Code status line.
# Session metrics come exclusively from the documented JSON payload on stdin.
# The only subprocess beyond formatting is a read-only git branch lookup when
# the payload does not contain worktree.branch.

set -f

input=$(cat)
if [ -z "$input" ]; then
    printf '%s\n' "Claude"
    exit 0
fi

find_jq() {
    if command -v jq >/dev/null 2>&1; then
        command -v jq
        return 0
    fi

    # Common Windows Git Bash locations. Do not scan the home directory.
    for candidate in \
        "${LOCALAPPDATA:-}/Microsoft/WinGet/Links/jq.exe" \
        "${HOME:-}/AppData/Local/Microsoft/WinGet/Links/jq.exe" \
        "/c/ProgramData/chocolatey/bin/jq.exe" \
        "/c/tools/jq.exe"; do
        if [ -n "$candidate" ] && [ -x "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done

    return 1
}

jq_bin=$(find_jq) || {
    printf '%s\n' "Claude | statusline requires jq"
    exit 0
}

if ! printf '%s' "$input" | "$jq_bin" -e . >/dev/null 2>&1; then
    printf '%s\n' "Claude | invalid status input"
    exit 0
fi

json_value() {
    printf '%s' "$input" | "$jq_bin" -r "$1"
}

integer_or_zero() {
    awk '{
        value = int($1 + 0)
        if (value < 0) value = 0
        print value
    }'
}

format_duration() {
    local milliseconds=$1
    local seconds hours minutes

    seconds=$((milliseconds / 1000))
    hours=$((seconds / 3600))
    minutes=$(((seconds % 3600) / 60))
    seconds=$((seconds % 60))

    if [ "$hours" -gt 0 ]; then
        printf '%dh%02dm' "$hours" "$minutes"
    elif [ "$minutes" -gt 0 ]; then
        printf '%dm%02ds' "$minutes" "$seconds"
    else
        printf '%ds' "$seconds"
    fi
}

build_bar() {
    local percentage=$1
    local width=10
    local filled empty index

    [ "$percentage" -gt 100 ] && percentage=100
    filled=$((percentage * width / 100))
    empty=$((width - filled))

    printf '['
    index=0
    while [ "$index" -lt "$filled" ]; do
        printf '#'
        index=$((index + 1))
    done
    index=0
    while [ "$index" -lt "$empty" ]; do
        printf '-'
        index=$((index + 1))
    done
    printf ']'
}

model=$(json_value '.model.display_name // .model.id // "Claude"')
context_percentage=$(json_value '.context_window.used_percentage // 0' | integer_or_zero)
[ "$context_percentage" -gt 100 ] && context_percentage=100

duration_ms=$(json_value '.cost.total_duration_ms // 0' | integer_or_zero)
duration=$(format_duration "$duration_ms")
cost=$(json_value '.cost.total_cost_usd // 0' | awk '{printf "$%.2f", $1 + 0}')

five_hour=$(json_value '.rate_limits.five_hour.used_percentage // empty' | integer_or_zero)
seven_day=$(json_value '.rate_limits.seven_day.used_percentage // empty' | integer_or_zero)
[ -n "$five_hour" ] && [ "$five_hour" -gt 100 ] && five_hour=100
[ -n "$seven_day" ] && [ "$seven_day" -gt 100 ] && seven_day=100

branch=$(json_value '.worktree.branch // empty')
if [ -z "$branch" ]; then
    cwd=$(json_value '.workspace.current_dir // .cwd // empty')
    if [ -n "$cwd" ] && command -v git >/dev/null 2>&1; then
        branch=$(git -C "$cwd" branch --show-current 2>/dev/null)
    fi
fi

printf '%s | ctx ' "$model"
build_bar "$context_percentage"
printf ' %d%%' "$context_percentage"
[ -n "$branch" ] && printf ' | branch %s' "$branch"
printf ' | %s' "$duration"

if [ -n "$five_hour" ] || [ -n "$seven_day" ]; then
    printf ' | rate'
    [ -n "$five_hour" ] && printf ' 5h %d%%' "$five_hour"
    [ -n "$seven_day" ] && printf ' 7d %d%%' "$seven_day"
fi

printf ' | %s\n' "$cost"
