# `.claude/` 生態系

這個目錄提供 Claude Code 的專案級能力庫與執行邊界。設計原則是「Skills 厚、Runtime 薄」：保留完整軟體工程能力，但只讓必要內容進入每次對話。

## 責任分層

| 元件 | 責任 | 不該承擔 |
|---|---|---|
| `CLAUDE.md` | 專案入口與元件邊界 | 完整方法論 |
| `rules/` | 1 份 Golden Rules，永遠生效 | 技術棧清單、固定流程 |
| `skills/` | Action Skills 與能力資料庫 | 無條件常駐 context |
| `agents/` | context／工具／權限隔離 | 複製 Skills 的知識 |
| `output-styles/` | 回答呈現方式 | PRD、BDD、TDD 等流程 |
| `hooks/` | 確定、快速、低頻的 guardrail | 專案管理、隱性狀態機 |
| `statusline*.sh` | 唯讀顯示官方 stdin 狀態 | 憑證查找、HTTP、檔案寫入 |

## 主要工作流

```text
/intake → /specify → /deliver → /verify
```

完整說明見 [WORKFLOW.md](./WORKFLOW.md)，Skills 分類見 [skills/INDEX.md](./skills/INDEX.md)，呈現樣式說明見 [OUTPUT_STYLES.md](./OUTPUT_STYLES.md)。

## Active Agents

Subagent 僅在需要隔離時使用，目前保留 8 個互斥度較高的角色：

| Agent | 邊界 |
|---|---|
| `architect` | 唯讀架構第二意見 |
| `code-quality-specialist` | 唯讀變更審查 |
| `security-infrastructure-auditor` | 唯讀安全與基礎設施稽核 |
| `test-automation-engineer` | 委派的單元／整合測試實作 |
| `end-to-end-validation-specialist` | 高雜訊 E2E 旅程與證據 |
| `build-error-resolver` | 最小差異恢復 build |
| `documentation-specialist` | 大型文件正規化與交叉連結 |
| `deployment-expert` | 預設唯讀的部署／回滾規劃 |

一般規劃、通用研究、TDD 方法、重構與模板選擇由主 Agent 搭配 Skills 處理，不再各自註冊一個重疊 Agent。

Rules、Skills 與 Agents 三層怎麼一起運作（含階段 × Agent 對照與走查）見 [WORKFLOW.md 協作模型](./WORKFLOW.md#協作模型rules--skills--agents)。

## Commands 與 Skills

Claude Code 已將自訂 commands 與 skills 統一為 slash-command 入口。本專案以 Skill 為單一格式，避免同名 command 與 Skill 漂移。

核心入口設為 `disable-model-invocation: true`，由人類明確啟動。細部能力 Skills 可由任務語意載入。

## Hooks 與 TaskMaster

基礎模板預設不註冊 Hook。舊 Hook 腳本仍保留在 `hooks/` 供遷移參考，但不會執行。

舊 TaskMaster runtime 已退役：

- 不再由 Hook 解析 prompt 或寫 session/timelog
- StatusLine 不再修改 Git 工作樹
- 原生 Task list 處理暫態工作
- 規格、issue、ADR 與測試證據處理長期狀態

## Settings 與 StatusLine

`settings.json` 使用最小權限基線，並以 deny 保護內建 Read/Edit 不讀寫敏感路徑；個人 MCP 與額外權限應放進不入版控的 `settings.local.json`。

Read/Edit deny 不是作業系統 sandbox，無法攔截 Bash／PowerShell 子程序直接讀檔。macOS、Linux、WSL2 可依專案風險另啟 Claude Code sandbox；Windows 原生環境需搭配 OS／工作區隔離、最小 shell 授權與不把秘密放進 repository。不要把此設定宣稱為完整的秘密防護。

StatusLine 只消費 Claude Code 官方 stdin 與唯讀 Git branch lookup。平台與 mock 測試方式見 [STATUSLINE_GUIDE.md](./STATUSLINE_GUIDE.md)。

## 擴充原則

- 新方法或領域知識：新增／更新 Skill
- 新的人工觸發端到端流程：Action Skill
- 需要隔離 context 或權限：Subagent
- 所有任務都必須遵守：才考慮 Rule
- 純呈現偏好：Output Style
- 可證明確定、快速、低頻：才考慮 Hook
