# Claude Code StatusLine 指南

本模板的 StatusLine 是**唯讀顯示器**。它只解析 Claude Code 傳入 stdin 的官方 JSON 欄位，並在一般工作樹中以唯讀 `git branch --show-current` 補充分支名稱。

它不會：

- 尋找或讀取 Claude Code credential。
- 呼叫 Anthropic 私有或未公開的 HTTP endpoint。
- 建立 usage cache、session snapshot 或時間日誌。
- 讀寫任何專案狀態檔或 runtime 資料。
- 修改 Git 或工作區內容。

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

輸出保持單行：

```text
Claude Opus | ctx [####------] 42% | branch feature/a | 1h08m | rate 5h 21% 7d 35% | $4.27
```

| 顯示 | 官方 stdin 欄位 |
| --- | --- |
| Model | `model.display_name`，缺少時使用 `model.id` |
| Context | `context_window.used_percentage` |
| Worktree branch | `worktree.branch` |
| Duration | `cost.total_duration_ms` |
| Five-hour rate limit | `rate_limits.five_hour.used_percentage` |
| Seven-day rate limit | `rate_limits.seven_day.used_percentage` |
| Estimated cost | `cost.total_cost_usd` |

一般工作樹的 payload 沒有 branch 欄位，因此腳本會使用 `workspace.current_dir`（舊 payload 回退到 `cwd`）執行唯讀 Git branch lookup。它不執行 `git status`，避免 StatusLine 高頻刷新拖慢大型 repo。

Rate-limit 欄位若尚未提供便不顯示；缺少欄位不視為錯誤。

官方欄位定義：

- [Claude Code StatusLine](https://code.claude.com/docs/en/statusline)

## 依賴

- Bash
- `jq`
- Git（專案設定用它定位 repo root；直接執行腳本時，沒有 Git 仍可顯示其他欄位）

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

Windows Git Bash 會依序檢查 PATH、WinGet link、Chocolatey 與 `/c/tools/jq.exe`。腳本不掃描整個使用者目錄。

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
  "workspace": {"current_dir": "."},
  "worktree": {"branch": "feature/mock"},
  "context_window": {"used_percentage": 42},
  "cost": {"total_duration_ms": 4085000, "total_cost_usd": 4.27},
  "rate_limits": {
    "five_hour": {"used_percentage": 21, "resets_at": 1784880000},
    "seven_day": {"used_percentage": 35, "resets_at": 1785369600}
  }
}' | bash .claude/statusline.sh
```

也應測試缺少可選欄位：

```bash
printf '%s\n' '{"model":{"display_name":"Claude"},"context_window":{},"cost":{}}' \
  | bash .claude/statusline.sh
```

## 疑難排解

- `statusline requires jq`：確認 `jq --version` 在相同 Git Bash／Linux shell 可執行。
- `invalid status input`：stdin 不是合法 JSON；用上方 mock 先隔離腳本問題。
- 沒有 branch：payload 沒有 `worktree.branch`，而 `workspace.current_dir` 也不在 Git repo。
- 沒有 rate：目前 session 尚未收到 `rate_limits`，腳本會正常省略。
- StatusLine 未出現：用 `/statusline` 或 `/status` 確認實際載入的 settings 來源與專案信任狀態。
