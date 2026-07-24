# Subagent Context 持久化規則

## 核心原則

每次 subagent 完成任務後，主 agent **必須**將其最終產出總結寫入 `.claude/context/` 對應子目錄。
只保留最終結論與可操作建議，不保留思考過程。

## Agent 對應目錄

| Subagent 類型 | 寫入目錄 |
| :--- | :--- |
| code-quality-specialist | `context/quality/` |
| test-automation-engineer, tdd-guide | `context/testing/` |
| e2e-validation-specialist | `context/e2e/` |
| security-infrastructure-auditor | `context/security/` |
| deployment-expert | `context/deployment/` |
| documentation-specialist | `context/docs/` |
| architect, planner, Plan | `context/decisions/` |
| Explore, general-purpose | `context/decisions/` (僅限產出架構/技術決策時) |

不在上表的 agent（如 build-error-resolver、refactor-cleaner）僅在產出值得留存的結論時寫入 `context/quality/`。

## 檔案命名

格式：`{agent-type}-{YYYY-MM-DD-HHmm}-{簡要主題}.md`

範例：
- `code-quality-specialist-2026-04-06-1045-auth-module-review.md`
- `architect-2026-04-06-1100-api-redesign.md`

## 報告範本

```markdown
# {Agent 類型} 報告

- **日期**: {YYYY-MM-DD HH:mm}
- **任務**: {一句話描述}
- **範圍**: {涉及的檔案/模組}

## 結論

{核心發現，條列式，每條 1-2 句}

## 行動項目

- [ ] {具體可執行的建議}

## 影響評估

- **嚴重度**: CRITICAL / HIGH / MEDIUM / LOW
- **影響範圍**: {哪些模組/功能受影響}
```

## 執行時機

1. subagent 回傳結果後，主 agent 立即摘要寫入
2. 如果同一任務多次呼叫同類型 agent，只保留最終版本
3. 寫入後不需要通知使用者（靜默執行）

## 不寫入的情況

- subagent 僅回答簡單問題（如「這個函式在哪裡？」）
- subagent 執行失敗且無有用產出
- 產出內容與既有報告完全重複
