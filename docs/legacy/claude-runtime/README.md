# Claude Runtime Legacy Archive

此處保存 v5 以前曾直接註冊到 Claude Code runtime 的 prompts。它們不會自動載入，也不會出現在 Agents、Rules、Commands 或 Output Styles 選單。

保留目的：

- 追蹤舊版設計與遷移理由
- 必要時擷取仍有價值的清單或格式
- 避免為了降低 runtime context 而丟失能力資料

目前責任替代：

| 舊 runtime 類型 | 現行替代 |
|---|---|
| 流程型 Commands | `/intake`、`/specify`、`/deliver`、`/verify` Action Skills |
| PRD／BDD／SAD 等 Output Styles | Action Skills + `VibeCoding_Workflow_Templates/` |
| 通用／規劃／TDD／模板 Agents | 主 Agent + 對應 Skills |
| 技術棧與流程 Rules | 按需 Skills；常駐只留 `golden-rules.md` |
| 規則式 Subagent 協作配置 | 原生 Task／Subagent + `.claude/agents/` 的窄角色 |

這些檔案是歷史參考，不應直接複製回 runtime。若要恢復其中一項，先判斷它屬於 Rule、Skill、Agent、Output Style 或 Hook 的哪一種單一責任。
