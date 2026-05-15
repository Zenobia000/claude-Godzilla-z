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

## Primitive Selection (command / skill / output-style)

3 個原始元的選擇規則見 `rules/primitive-selection.md`。三句口訣：

1. **預設用 skill**——任何程序性知識都該走 skill。
2. **command 只給觸碰系統狀態的工作流**（taskmaster, session, time-log, learn）或具獨立程序邏輯（build-fix, verify, refactor-clean, template-check）。
3. **output-style 只給整個 session 的人格切換**（如視覺化模式），不裝任務模板。

不要為了「快捷鍵」做純間接的 `/command` 包裝；讓使用者用自然語言描述意圖，harness 會自動匹配到對的 skill。

## Change Governance (Hard Gate)

需求變更治理規則見 `rules/change-governance.md`。三句口訣：

1. **變更涉及 flow / contract / data / architecture → 先跑 `sunnydata-change-impact-analysis` skill**（硬 gate，不可繞過）。
2. **CIA §8「Human Decisions Required」未填寫 → 不可動 code**。
3. **文件衝突或 status: deprecated/superseded → 停下來回報，引用具體 ID（BF-/UF-/SF-/API-/TC-/SLO-/PIPE-/MODEL-/OBS-/CAP-/DISC-），不腦補**。

Flow ID 命名規範見 `VibeCoding_Workflow_Templates/0-principles/PRIN-0001-flow-id-conventions.md`；Quality Gates 階段門檻見 `VibeCoding_Workflow_Templates/3-process/QG-0000-quality-gates.md`。
