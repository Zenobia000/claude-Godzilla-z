# Hook 驅動的專案管理狀態（TaskMaster 類）

用 hooks 攔截 prompt、寫 session snapshot／timelog／WBS、維護第二套任務狀態機。

## 為什麼不做

- Hook 適合「確定、快速、低頻、無隱性狀態」的 guardrail；專案管理狀態三項全違反——非確定（要解析語意）、有隱性狀態（影子文件）、且每次對話都跑。
- 第二套狀態機必然與 Claude Code 原生 session/task 機制及正式文件（追蹤簿、PRD、ADR）drift，最後誰都不敢信。
- 值得長期保存的內容應進正式文件；暫態交給原生 task 機制。見 `.claude/hooks/README.md` 的五項准入標準與反清單。

## 先例

- 舊 TaskMaster prompt 攔截、snapshot、timelog、agent-monitor hooks 已於 commits `ab6c93b`、`1bc6776` 刪除。
- `.claude/settings.json` 維持無 `hooks` 鍵；驗證：`jq 'has("hooks")' .claude/settings.json` → `false`。

## 替代出口

需要跨 session 的狀態 → 追蹤簿／PRD／ADR／測試證據；需要事件 guardrail 且滿足五項標準 → 依 `.claude/hooks/README.md` 流程提案。
