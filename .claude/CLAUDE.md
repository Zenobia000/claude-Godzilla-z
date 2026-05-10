# Project Instructions

## Skill 使用規則

遇到可能適用的 skill 時，**先透過 Skill tool 載入再行動**。優先序：

1. **使用者明確指示**（CLAUDE.md、直接請求）— 最高
2. **Skills** — 覆蓋預設系統行為
3. **預設系統提示** — 最低

流程類 skill（sunnydata-design、sunnydata-debugging）優先於實作類 skill（sunnydata-api-design、sunnydata-testing）。

## Subagent Context 持久化

Subagent 完成後，主 agent 必須將最終產出總結寫入 `.claude/context/` 對應子目錄。
詳見 `rules/subagent-context.md`。此為 harness 架構的一部分，靜默執行，不需使用者確認。

## Context Stability Tiers

文件分 6 個穩定性層級（`0-principles` ~ `5-views`），每層有不同的更新頻率與 AI 處理規則。
詳見 `rules/context-stability.md`。tier 2 (contracts) 文件需帶 `last-synced-with` frontmatter；
撰寫前可用 `sunnydata-doc-freshness` skill 檢查鮮度。
