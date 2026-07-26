#!/bin/bash
# Ported from ~/.claude/statusline.sh (global config). Keep behavior in sync
# when the global script changes. Unlike the global copy, this version does
# NOT write session snapshots (no taskmaster-data persistence in this repo).
set -f

input=$(cat)

if [ -z "$input" ]; then
    printf "Claude"
    exit 0
fi

# ── jq PATH fix (cross-platform) ────────────────────────
if ! command -v jq >/dev/null 2>&1; then
    # Windows Git Bash: jq installed via winget/chocolatey may not be in PATH
    if [ -n "$LOCALAPPDATA" ] || [ -d "/c/Windows" ]; then
        for p in \
            "$LOCALAPPDATA/Microsoft/WinGet/Links/jq.exe" \
            "$HOME/AppData/Local/Microsoft/WinGet/Links/jq.exe" \
            "/c/ProgramData/chocolatey/bin/jq.exe" \
            "/c/tools/jq.exe"; do
            if [ -f "$p" ]; then
                jq() { "$p" "$@"; }
                export -f jq 2>/dev/null
                break
            fi
        done
        if ! command -v jq >/dev/null 2>&1; then
            found=$(find "$HOME/AppData/Local/Microsoft/WinGet/Packages" -name "jq.exe" 2>/dev/null | head -1)
            if [ -n "$found" ]; then
                jq() { "$found" "$@"; }
                export -f jq 2>/dev/null
            fi
        fi
    fi
    # Linux: suggest install
    # Ubuntu/Debian: sudo apt install jq
    # RHEL/CentOS:   sudo yum install jq  or  sudo dnf install jq
fi

if ! command -v jq >/dev/null 2>&1; then
    printf "Claude (jq not found - install: apt/dnf/yum install jq)"
    exit 0
fi

# ── Colors (Tesla High-Contrast) ───────────────────────
red='\033[38;2;232;33;39m'        # Tesla Red #E82127
blue='\033[38;2;56;172;255m'      # Electric Blue #38ACFF
green='\033[38;2;0;230;118m'      # Neon Green #00E676
cyan='\033[38;2;0;229;255m'       # Cyber Cyan #00E5FF
orange='\033[38;2;255;167;38m'    # Amber #FFA726
yellow='\033[38;2;255;234;0m'     # Volt Yellow #FFEA00
white='\033[38;2;245;245;245m'    # Pure White #F5F5F5
silver='\033[38;2;176;190;197m'   # Tesla Silver #B0BEC5（備用）
gray='\033[38;2;120;120;130m'     # Steel Gray #787882（備用）
pink='\033[38;2;255;82;82m'       # Signal Red / dirty #FF5252
dim='\033[2m'
reset='\033[0m'

sep=" ${dim}│${reset} "

# ── Helpers ─────────────────────────────────────────────
format_tokens() {
    local num=$1
    if [ "$num" -ge 1000000 ] 2>/dev/null; then
        awk "BEGIN {printf \"%.1fm\", $num / 1000000}"
    elif [ "$num" -ge 1000 ] 2>/dev/null; then
        awk "BEGIN {printf \"%.0fk\", $num / 1000}"
    else
        printf "%d" "$num"
    fi
}

color_for_pct() {
    local pct=$1
    if [ "$pct" -ge 90 ] 2>/dev/null; then printf "$red"
    elif [ "$pct" -ge 70 ] 2>/dev/null; then printf "$yellow"
    elif [ "$pct" -ge 50 ] 2>/dev/null; then printf "$orange"
    else printf "$green"
    fi
}

# Context % → 水位 icon（與 STATUSLINE_GUIDE「Token 水位」表一致）
level_icon_for_pct() {
    local pct=$1
    if [ "$pct" -lt 30 ] 2>/dev/null; then printf '%s' '❄️'
    elif [ "$pct" -lt 50 ] 2>/dev/null; then printf '%s' '🌊'
    elif [ "$pct" -lt 70 ] 2>/dev/null; then printf '%s' '🌡'
    elif [ "$pct" -lt 85 ] 2>/dev/null; then printf '%s' '♨️'
    elif [ "$pct" -lt 95 ] 2>/dev/null; then printf '%s' '🔥'
    else printf '%s' '💥'
    fi
}

build_bar() {
    local pct=$1
    local width=$2
    [ "$pct" -lt 0 ] 2>/dev/null && pct=0
    [ "$pct" -gt 100 ] 2>/dev/null && pct=100

    local filled=$(( pct * width / 100 ))
    local empty=$(( width - filled ))
    local bar_color
    bar_color=$(color_for_pct "$pct")

    local filled_str="" empty_str=""
    for ((i=0; i<filled; i++)); do filled_str+="●"; done
    for ((i=0; i<empty; i++)); do empty_str+="○"; done

    printf "${bar_color}${filled_str}${dim}${empty_str}${reset}"
}

iso_to_epoch() {
    local iso_str="$1"
    local epoch
    [ -z "$iso_str" ] || [ "$iso_str" = "null" ] && return 1
    epoch=$(date -d "${iso_str}" +%s 2>/dev/null)
    if [ -n "$epoch" ]; then
        echo "$epoch"
        return 0
    fi
    local stripped="${iso_str%%.*}"
    stripped="${stripped%%Z}"
    stripped="${stripped%%+*}"
    stripped="${stripped%%-[0-9][0-9]:[0-9][0-9]}"
    epoch=$(date -j -f "%Y-%m-%dT%H:%M:%S" "$stripped" +%s 2>/dev/null)
    if [ -n "$epoch" ]; then
        echo "$epoch"
        return 0
    fi
    return 1
}

# $1: unix epoch seconds, $2: time|datetime
format_reset_time() {
    local epoch="$1"
    local style="$2"
    [ -z "$epoch" ] || [ "$epoch" = "null" ] && return
    case "$epoch" in *[!0-9]*) return ;; esac

    local result=""
    case "$style" in
        time)
            result=$(date -d "@$epoch" +"%H:%M" 2>/dev/null)
            [ -z "$result" ] && result=$(date -j -r "$epoch" +"%H:%M" 2>/dev/null)
            ;;
        datetime)
            result=$(date -d "@$epoch" +"%m/%d %H:%M" 2>/dev/null)
            [ -z "$result" ] && result=$(date -j -r "$epoch" +"%m/%d %H:%M" 2>/dev/null)
            ;;
    esac
    printf "%s" "$result"
}

# ── Extract JSON data ───────────────────────────────────
model_name=$(echo "$input" | jq -r '.model.display_name // "Claude"')
model_name_lc=$(printf '%s' "$model_name" | tr '[:upper:]' '[:lower:]')
case "$model_name_lc" in
    *opus*)   model_icon='🦁'; model_color=$red ;;
    *sonnet*) model_icon='🦅'; model_color=$blue ;;
    *haiku*)  model_icon='🐦'; model_color=$green ;;
    *)        model_icon='🤖'; model_color=$cyan ;;
esac

size=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
[ "$size" -eq 0 ] 2>/dev/null && size=200000

input_tokens=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
cache_create=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
cache_read=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')
current=$(( input_tokens + cache_create + cache_read ))

used_tokens=$(format_tokens $current)
total_tokens=$(format_tokens $size)

if [ "$size" -gt 0 ] 2>/dev/null; then
    pct_used=$(( current * 100 / size ))
else
    pct_used=0
fi

# ── Session duration from cost.total_duration_ms ────────
session_duration=""
total_duration_ms=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
if [ "$total_duration_ms" -gt 0 ] 2>/dev/null; then
    elapsed=$(( total_duration_ms / 1000 ))
    if [ "$elapsed" -ge 3600 ] 2>/dev/null; then
        session_duration="$(( elapsed / 3600 ))h$(( (elapsed % 3600) / 60 ))m"
    elif [ "$elapsed" -ge 60 ] 2>/dev/null; then
        session_duration="$(( elapsed / 60 ))m"
    else
        session_duration="${elapsed}s"
    fi
fi

# ── Cost ────────────────────────────────────────────────
total_cost=$(echo "$input" | jq -r '.cost.total_cost_usd // 0' | awk '{printf "$%.2f", $1}')

# ── Context used percentage (from API) ──────────────────
pct_used_api=$(echo "$input" | jq -r '.context_window.used_percentage // empty')
if [ -n "$pct_used_api" ] && [ "$pct_used_api" != "null" ]; then
    pct_used=$pct_used_api
fi

# ── LINE 1 ──────────────────────────────────────────────
pct_color=$(color_for_pct "$pct_used")
level_icon=$(level_icon_for_pct "$pct_used")
cwd=$(echo "$input" | jq -r '.cwd // ""')
[ -z "$cwd" ] || [ "$cwd" = "null" ] && cwd=$(pwd)
dirname=$(basename "$cwd")

git_branch=""
git_dirty=""
if git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git_branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null)
    if [ -n "$(git -C "$cwd" status --porcelain 2>/dev/null)" ]; then
        git_dirty="y"
    fi
fi

# Build line 1: icon+Model | 水位+pct% | 📂 dir 🌿 branch💫 | ⏱ | 💰
# 多數終端對 emoji 寬度與游標前進不一致，emoji 後多補一個空格避免與後續文字疊字。
line1="${model_color}${model_icon}  ${model_name}${reset}"
line1+="${sep}"
line1+="${level_icon}${reset}  ${pct_color}${pct_used}%${reset} ${dim}(${used_tokens}/${total_tokens})${reset}"
line1+="${sep}"
line1+="${cyan}📂  ${dirname}${reset}"
if [ -n "$git_branch" ]; then
    line1+=" ${green}🌿  ${git_branch}${reset}"
    [ -n "$git_dirty" ] && line1+="${pink}💫${reset}"
fi
if [ -n "$session_duration" ]; then
    line1+="${sep}"
    line1+="${white}⏱  ${session_duration}${reset}"
fi
if [ "$total_cost" != "\$0.00" ]; then
    line1+="${sep}"
    line1+="${yellow}💰  ${total_cost}${reset}"
fi

# ── OAuth token resolution ──────────────────────────────
get_oauth_token() {
    if [ -n "$CLAUDE_CODE_OAUTH_TOKEN" ]; then
        echo "$CLAUDE_CODE_OAUTH_TOKEN"
        return 0
    fi
    if command -v security >/dev/null 2>&1; then
        local blob
        blob=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null)
        if [ -n "$blob" ]; then
            local token
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then
                echo "$token"; return 0
            fi
        fi
    fi
    local creds_file="${HOME}/.claude/.credentials.json"
    if [ -f "$creds_file" ]; then
        local token
        token=$(jq -r '.claudeAiOauth.accessToken // empty' "$creds_file" 2>/dev/null)
        if [ -n "$token" ] && [ "$token" != "null" ]; then
            echo "$token"; return 0
        fi
    fi
    if command -v secret-tool >/dev/null 2>&1; then
        local blob
        blob=$(timeout 2 secret-tool lookup service "Claude Code-credentials" 2>/dev/null)
        if [ -n "$blob" ]; then
            local token
            token=$(echo "$blob" | jq -r '.claudeAiOauth.accessToken // empty' 2>/dev/null)
            if [ -n "$token" ] && [ "$token" != "null" ]; then
                echo "$token"; return 0
            fi
        fi
    fi
    echo ""
}

# ── Fetch usage data (cached) ──────────────────────────
cache_dir="${TEMP:-/tmp}/claude"
cache_file="${cache_dir}/statusline-usage-cache.json"
cache_max_age=60
mkdir -p "$cache_dir"

needs_refresh=true
usage_data=""

if [ -f "$cache_file" ]; then
    cache_mtime=$(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file" 2>/dev/null)
    now=$(date +%s)
    cache_age=$(( now - cache_mtime ))
    if [ "$cache_age" -lt "$cache_max_age" ] 2>/dev/null; then
        needs_refresh=false
        usage_data=$(cat "$cache_file" 2>/dev/null)
    fi
fi

if $needs_refresh; then
    token=$(get_oauth_token)
    if [ -n "$token" ] && [ "$token" != "null" ]; then
        response=$(curl -s --max-time 5 \
            -H "Accept: application/json" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            -H "anthropic-beta: oauth-2025-04-20" \
            -H "User-Agent: claude-code/2.1.34" \
            "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)
        if [ -n "$response" ] && echo "$response" | jq -e '.five_hour' >/dev/null 2>&1; then
            usage_data="$response"
            echo "$response" > "$cache_file"
        fi
    fi
    if [ -z "$usage_data" ] && [ -f "$cache_file" ]; then
        # Stale fallback capped at 10 minutes; older data is dropped rather
        # than displayed as current.
        cache_mtime=$(stat -c %Y "$cache_file" 2>/dev/null || stat -f %m "$cache_file" 2>/dev/null)
        now=$(date +%s)
        if [ $(( now - cache_mtime )) -le 600 ] 2>/dev/null; then
            usage_data=$(cat "$cache_file" 2>/dev/null)
        fi
    fi
fi

# ── Rate limit lines ────────────────────────────────────
# Source priority per window: official stdin rate_limits (updated on every
# API response — same data as /usage) → OAuth usage endpoint (cached).
# Extra usage (💳) only exists on the endpoint.
rate_lines=""
bar_width=10

usage_valid=false
if [ -n "$usage_data" ] && echo "$usage_data" | jq -e . >/dev/null 2>&1; then
    usage_valid=true
fi

five_hour_pct=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
five_hour_reset=$(echo "$input" | jq -r '.rate_limits.five_hour.resets_at // empty')
seven_day_pct=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
seven_day_reset=$(echo "$input" | jq -r '.rate_limits.seven_day.resets_at // empty')

if [ -z "$five_hour_pct" ] && $usage_valid; then
    five_hour_pct=$(echo "$usage_data" | jq -r '.five_hour.utilization // empty')
    five_hour_reset=$(iso_to_epoch "$(echo "$usage_data" | jq -r '.five_hour.resets_at // empty')")
fi
if [ -z "$seven_day_pct" ] && $usage_valid; then
    seven_day_pct=$(echo "$usage_data" | jq -r '.seven_day.utilization // empty')
    seven_day_reset=$(iso_to_epoch "$(echo "$usage_data" | jq -r '.seven_day.resets_at // empty')")
fi

if [ -n "$five_hour_pct" ]; then
    five_hour_pct=$(printf '%s' "$five_hour_pct" | awk '{printf "%.0f", $1}')
    five_hour_bar=$(build_bar "$five_hour_pct" "$bar_width")
    five_hour_pct_color=$(color_for_pct "$five_hour_pct")
    five_hour_pct_fmt=$(printf "%3d" "$five_hour_pct")
    five_hour_reset_fmt=$(format_reset_time "$five_hour_reset" "time")

    rate_lines+="${white}⚡${reset}  ${five_hour_bar} ${five_hour_pct_color}${five_hour_pct_fmt}%${reset}"
    [ -n "$five_hour_reset_fmt" ] && rate_lines+=" ${dim}🔄${reset}  ${white}${five_hour_reset_fmt}${reset}"
fi

if [ -n "$seven_day_pct" ]; then
    seven_day_pct=$(printf '%s' "$seven_day_pct" | awk '{printf "%.0f", $1}')
    seven_day_bar=$(build_bar "$seven_day_pct" "$bar_width")
    seven_day_pct_color=$(color_for_pct "$seven_day_pct")
    seven_day_pct_fmt=$(printf "%3d" "$seven_day_pct")
    seven_day_reset_fmt=$(format_reset_time "$seven_day_reset" "datetime")

    [ -n "$rate_lines" ] && rate_lines+="\n"
    rate_lines+="${white}📅${reset}  ${seven_day_bar} ${seven_day_pct_color}${seven_day_pct_fmt}%${reset}"
    [ -n "$seven_day_reset_fmt" ] && rate_lines+=" ${dim}🔄${reset}  ${white}${seven_day_reset_fmt}${reset}"
fi

if $usage_valid; then
    extra_enabled=$(echo "$usage_data" | jq -r '.extra_usage.is_enabled // false')
    if [ "$extra_enabled" = "true" ]; then
        extra_pct=$(echo "$usage_data" | jq -r '.extra_usage.utilization // 0' | awk '{printf "%.0f", $1}')
        extra_used=$(echo "$usage_data" | jq -r '.extra_usage.used_credits // 0' | awk '{printf "%.2f", $1/100}')
        extra_limit=$(echo "$usage_data" | jq -r '.extra_usage.monthly_limit // 0' | awk '{printf "%.2f", $1/100}')
        extra_bar=$(build_bar "$extra_pct" "$bar_width")
        extra_pct_color=$(color_for_pct "$extra_pct")

        [ -n "$rate_lines" ] && rate_lines+="\n"
        rate_lines+="${white}💳${reset}  ${extra_bar} ${extra_pct_color}\$${extra_used}${dim}/${reset}${white}\$${extra_limit}${reset}"
    fi
fi

# ── Output ──────────────────────────────────────────────
printf "%b" "$line1"
[ -n "$rate_lines" ] && printf "\n%b" "$rate_lines"

exit 0
