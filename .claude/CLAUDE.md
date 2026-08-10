# Claude Code Project Instructions

本檔管**元件責任與維護契約**——這套 harness 由哪些元件組成、改動它時不能破壞什麼。

入口敘述（這是什麼、怎麼開始、預設節奏）在根目錄 [`CLAUDE.md`](../CLAUDE.md)，不在這裡重複。沒有 Excel 追蹤簿、沒有需求簽核閘、沒有強制的追溯 ID 主鏈——那些屬於 Pilot／企業級路線（`refactor/document-driven-ecosystem` 分支）。

## 元件責任

- 根目錄 `CLAUDE.md`：**常駐**入口，只放「這是什麼、怎麼開始、預設節奏」與路由連結；細節一律連結不 paraphrase。帶進新專案的起步順序在 `VibeCoding_Workflow_Templates/_meta/new_project_bootstrap.md`（不常駐）。
- `rules/`：**常駐**規則，只放每次工作都成立、而且與模型預設行為不同的約束；條件性細則一律下放到對應 skill 的 `references/`。常駐面的消融紀錄見 [ABLATION.md](ABLATION.md)。
- `skills/`：按需載入的能力資料庫；路由見 `skills/INDEX.md`。
- `agents/`：需要獨立 context、權限邊界、平行處理或專業驗證時才使用。
- `output-styles/`：只改變回答呈現方式，不承載開發流程。
- `hooks/`：零註冊，只留設計指南；不得把專案管理狀態偷偷寫入。
- `VibeCoding_Workflow_Templates/`：18 份工程文件模板。**依需要取用，不強制填滿**——POC 期填 PRD 與 ADR 通常就夠，其餘等真的需要時再補。
- `.out-of-scope/`：已審視並拒絕的機制與理由；重新提案前先讀對應檔。

## 維護契約（改動本 harness 時必須重新滿足的不變量）

1. **Router 不說謊**：新增、改名、刪除 skill 或改變其定位時，必須同步更新 `skills/INDEX.md`；索引漏列新 skill、或仍導向已刪 skill，視為缺陷而非疏漏。
2. **Frontmatter 與現實一致**：Skill 的 `description` 與說明不得引用已退役的模板或文件名。
3. **大型 skill 分層**：SKILL.md 超過約 200 行時拆 `references/`（漸進揭露），不整檔常駐。
4. **來源可追**：新增 community／第三方 skill 必須在 `skills/INDEX.md` 記來源、授權與更新方式。
5. **拒絕有紀錄**：退役或否決一個機制時，在 `.out-of-scope/` 留一檔（概念、理由、先例）；重新提案前先讀它。
6. **常駐面要有證據**：新增任何常駐內容（根目錄 `CLAUDE.md`、本檔或 `rules/*.md`）時，必須在 [ABLATION.md](ABLATION.md) 的分類表新增一列並填「失敗證據」——這條規則是因為模型反覆犯了什麼錯才存在。填不出證據的不該常駐，改寫成 skill 按需載入。

## Runtime Context

不把每次對話或 Subagent 摘要寫成專案內的影子文件（舊的 `.claude/context/`、`coordination/`、`taskmaster-data/` 已移除）。Claude Code 的 session/task 機制處理暫態狀態；值得長期保存的內容進入模板文件、ADR 或測試證據。
