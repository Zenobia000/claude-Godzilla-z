# Hooks 指南

基礎模板預設**不啟用任何 Hook**。目前 `.claude/settings.json` 沒有 `hooks` 設定；Claude Code 的原生工具、Skills、Tasks、sessions 與 permissions 足以處理一般開發流程。

舊 TaskMaster、session 計時、Agent monitor、prompt 建議與 context 注入腳本均已刪除（歷史版本在 git history）。本目錄只保留這份設計指南。

## 何時才應加入 Hook

Hook 只適合下列特性同時成立的事件：

1. **確定性**：輸入能用機器規則判定，不依賴自然語言推理。
2. **低頻**：只在必要事件觸發，不在每個 prompt 或每次檔案讀取時執行。
3. **靜默**：成功不輸出噪音，不向對話注入提醒文字。
4. **有界**：執行時間短、寫入範圍明確、失敗策略可測試。
5. **不可由現有機制取代**：permissions、sandbox、formatter、CI 或 Skill 無法更直接完成。

適合的例子：

- 寫入特定語言檔案後執行該 repo 已固定的 formatter。
- 阻擋可明確比對的受保護路徑或危險操作。
- 在提交或發佈前執行確定性的 schema／policy 檢查。

不適合的例子：

- 維護 WBS、工時、session snapshot 或另一套 task state。
- 每次使用者輸入都分析意圖、建議 Agent 或注入工作流。
- 每次 Read／Write 都輸出 banner、emoji 或專案狀態。
- 複製 transcript、auto memory、Tasks 或 `/resume` 已有能力。
- 以 Hook 保存產品需求、架構決策或驗收結果；這些應寫入專案文件。

## 選擇機制

| 需求 | 機制 |
| --- | --- |
| 穩定的自然語言政策 | `.claude/rules/` |
| 多步驟、按需工作流 | Skill |
| 禁止工具或敏感路徑 | permissions／sandbox |
| 外部資料或工具 | MCP |
| 專案事實與長期決策 | `docs/`／ADR |
| 事件發生時必須執行的確定性 guardrail | Hook |

## 新增 Hook 的最低要求

- 文件化事件、matcher、stdin schema、stdout／stderr 與 exit-code contract。
- 使用官方 Hook JSON contract；不得從 credential store 探索秘密。
- 成功時 stdout 為空；只在需要 Claude Code 或使用者採取行動時回報。
- 設定短 timeout，並明確選擇 fail-open 或 fail-closed。
- Windows Git Bash 與 Linux 都要有測試，或清楚限定支援平台。
- 以 mock JSON 測試成功、拒絕、無關事件與缺少欄位。
- 在啟用前檢查是否造成隱性寫入、網路請求或循環觸發。

## 驗證目前為零 Hook

```bash
jq 'has("hooks")' .claude/settings.json
```

預期輸出：

```text
false
```

若未來確實需要 Hook，請以單一 guardrail、單一 owner 的小變更加入，並同步更新本指南。不要恢復舊 TaskMaster runtime。
