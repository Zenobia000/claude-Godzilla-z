# Claude Code StatusLine 指南

本專案的 StatusLine 移植自全域 `~/.claude/statusline.sh`（兩份需同步維護）。它解析 Claude Code 傳入 stdin 的官方 JSON 欄位，並額外做三件事：

- 以唯讀 `git symbolic-ref` 與 `git status --porcelain` 補充分支名稱與 dirty 標記。
- 5 小時／7 天 rate-limit **優先讀官方 stdin 的 `rate_limits` 欄位**（每次 API 回應即時更新，與 `/usage` 同源）；stdin 缺該 window 時才以 Claude Code OAuth token 呼叫 `https://api.anthropic.com/api/oauth/usage` 回退。API 結果快取於 `/tmp/claude/statusline-usage-cache.json`（60 秒；API 失敗時 stale 快取最多沿用 10 分鐘，逾期直接省略而不顯示舊數據）。Extra usage（💳）只存在於 usage API。
- 不寫入任何專案狀態檔（全域版的 taskmaster-data session snapshot 區塊在本專案已移除）。

Token 來源依序：`CLAUDE_CODE_OAUTH_TOKEN` 環境變數 → macOS Keychain → `~/.claude/.credentials.json` → `secret-tool`（Linux keyring）。取不到 token 時 rate-limit 行靜默省略，不影響第一行。

## 啟用方式

專案設定先由目前 repo 的任意子目錄解析 Git root，再執行腳本。這避免
Claude Code 從子目錄啟動或 session cwd 改變時，相對路徑找不到 StatusLine：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -lc 'git rev-parse --show-toplevel >/dev/null 2>&1 || exit 0; exec bash \"$(git rev-parse --show-toplevel 2>/dev/null)/.claude/statusline.sh\"'",
    "padding": 0
  }
}
```

Linux 若要使用明確入口，可把最後的檔名改成 `statusline-linux.sh`：

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -lc 'git rev-parse --show-toplevel >/dev/null 2>&1 || exit 0; exec bash \"$(git rev-parse --show-toplevel 2>/dev/null)/.claude/statusline-linux.sh\"'",
    "padding": 0
  }
}
```

`statusline-linux.sh` 只轉交給同目錄的 `statusline.sh`，兩個入口不維護兩份邏輯。此定位方式要求 session 位於 Git worktree 內；無法解析 repo root 時會靜默略過 StatusLine，而不猜測或掃描其他路徑。

## 顯示內容

第一行為 session 概況，之後視 usage API 是否可用附加 1–3 行 rate-limit：

```text
🦁  Claude Opus │ 🌊  42% (84k/200k) │ 📂  my-repo 🌿  feature/a💫 │ ⏱  1h8m │ 💰  $4.27
⚡  ●○○○○○○○○○   7% 🔄  19:10
📅  ●●●●○○○○○○  44% 🔄  07/28 19:59
💳  ●●○○○○○○○○ $3.10/$50.00
```

| 顯示 | 來源 |
| --- | --- |
| Model（🦁 opus／🦅 sonnet／🐦 haiku／🤖 其他） | `model.display_name` |
| Context %（優先 `used_percentage`，否則由 tokens 計算） | `context_window.*` |
| 📂 目錄 | `cwd` 的 basename |
| 🌿 分支＋💫 dirty | 唯讀 `git symbolic-ref` / `git status --porcelain` |
| ⏱ Duration | `cost.total_duration_ms` |
| 💰 Estimated cost（$0.00 時省略） | `cost.total_cost_usd` |
| ⚡ 5 小時 rate limit＋🔄 重置時間 | stdin `rate_limits.five_hour`（缺欄位退 usage API `five_hour`） |
| 📅 7 天 rate limit＋🔄 重置時間 | stdin `rate_limits.seven_day`（缺欄位退 usage API `seven_day`） |
| 💳 Extra usage（啟用時才顯示） | usage API `extra_usage` |

### Token 水位

Context 使用率對應的水位 icon（與腳本 `level_icon_for_pct` 一致）：

| Context % | Icon |
| --- | --- |
| < 30% | ❄️ |
| 30–49% | 🌊 |
| 50–69% | 🌡 |
| 70–84% | ♨️ |
| 85–94% | 🔥 |
| ≥ 95% | 💥 |

百分比顏色（context 與 rate-limit 共用）：< 50% 綠、50–69% 橙、70–89% 黃、≥ 90% 紅。

官方欄位定義：

- [Claude Code StatusLine](https://code.claude.com/docs/en/statusline)

## 依賴

- Bash
- `jq`
- Git（定位 repo root 與分支；沒有 Git 仍可顯示其他欄位）
- `curl`（抓 usage API；失敗時退回快取或省略 rate-limit 行）

安裝 `jq`：

```powershell
winget install jqlang.jq
```

```bash
# Debian / Ubuntu
sudo apt install jq

# Fedora / RHEL
sudo dnf install jq
```

Windows Git Bash 會依序檢查 PATH、WinGet link、Chocolatey 與 `/c/tools/jq.exe`。

## 本機驗證

語法檢查：

```bash
bash -n .claude/statusline.sh
bash -n .claude/statusline-linux.sh
```

Mock stdin：

```bash
printf '%s\n' '{
  "model": {"display_name": "Claude Opus"},
  "context_window": {
    "context_window_size": 200000,
    "used_percentage": 42,
    "current_usage": {"input_tokens": 84000}
  },
  "cost": {"total_duration_ms": 4085000, "total_cost_usd": 4.27},
  "rate_limits": {
    "five_hour": {"used_percentage": 23.5, "resets_at": 1784880000},
    "seven_day": {"used_percentage": 41.2, "resets_at": 1785369600}
  },
  "cwd": "."
}' | bash .claude/statusline.sh
```

也應測試缺少可選欄位：

```bash
printf '%s\n' '{"model":{"display_name":"Claude"},"context_window":{},"cost":{}}' \
  | bash .claude/statusline.sh
```

`statusline-debug.sh` 會把原始 stdin JSON 存到 `/tmp/statusline-debug.json` 再正常執行 StatusLine，用於排查實際 payload。

## 疑難排解

- `jq not found`：確認 `jq --version` 在相同 shell 可執行。
- 沒有 branch：`cwd` 不在 Git repo，或處於 detached HEAD。
- 沒有 rate-limit 行：session 尚未收到 stdin `rate_limits`（Pro/Max 首次 API 回應後才出現），且回退路徑也失敗（取不到 OAuth token，或 usage API 失敗且快取已超過 10 分鐘）；第一行不受影響。
- Rate-limit 數字疑似過舊：stdin 來源每次 API 回應即時更新；若當下走的是 usage API 回退，最多有 60 秒快取延遲，刪除 `/tmp/claude/statusline-usage-cache.json` 可強制刷新。
- StatusLine 未出現：用 `/statusline` 或 `/status` 確認實際載入的 settings 來源與專案信任狀態。
