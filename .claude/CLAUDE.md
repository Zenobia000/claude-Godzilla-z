# Claude Code Project Instructions

這個專案是一套「文件驅動、證據閉環」的軟體開發生態系。預設工作流是：

`業務來源 → /intake → /specify → /deliver → /verify`（流程唯一權威：[WORKFLOW.md](WORKFLOW.md)）

## 元件責任

- `rules/`：每次工作都成立的規則。`golden-rules.md` 是跨技術棧的底線；`git-workflow.md` 是 Git／push／PR 操作規範；`language-register.md` 定義**文件**的業務／橋接／工程三層語域；`plain-language-answers.md` 定義**對話**的語域——何時該把答案翻到決策層、何時不可以；`thinking-boundary.md` 定義速通/深思模式與「哪些必須使用者親自思考、AI 只 provoke」。
- `skills/`：能力資料庫與可重用方法；四個 Action Skills 是主要入口，路由見 `skills/INDEX.md`。
- `agents/`：需要獨立 context、權限邊界、平行處理或專業驗證時才使用。
- `output-styles/`：只改變回答呈現方式，不承載開發流程。
- `hooks/`：僅容納確定、快速、可重複執行的自動化；不得把專案管理狀態偷偷寫入。
- `VibeCoding_Workflow_Templates/`：工程文件的可填寫模板；三個 `*_tracker.xlsx` 是角色追蹤簿，其中 `requirements_tracker.xlsx` ①需求決策是需求決策權威（見 `docs/document-system/workbook-guide.md`）。文件深度依開發階段（雛型／Pilot／企業級）裁剪，見 `VibeCoding_Workflow_Templates/_meta/workflow_manual.md`。
- `software_development_documentation_guide_zh_tw.docx`：企業文件分類與選用參考（模板已依其九層分類與文件詞彙對齊）。
- `.out-of-scope/`：已審視並拒絕的機制與理由；重新提案前先讀對應檔。

## Skill 使用

遇到適用的 Skill，先載入其指示再行動。使用者直接要求的結果與專案 Golden Rules 優先。入口選擇與 confusable 區辨以 `skills/INDEX.md` 的路由表為準：

- 專案進件與 Excel 來源正規化：`/intake`
- 需求轉 PRD／BDD／SAD／ADR／追溯矩陣：`/specify`
- 依已核准規格交付垂直切片：`/deliver`
- 以測試與證據判定完成：`/verify`
- 除錯、資安、API、測試、前端與架構等細部能力：按任務載入對應 `sunnydata-*` 或 `community-*` Skill。

避免為同一件事同時套用多個流程型 Skill；由 Action Skill 編排必要的能力 Skill。

## 文件權威與追溯

Excel 與 Markdown 都可以是權威來源，但同一欄位只能有一個 owner。以
`docs/document-system/architecture.md` 的權威矩陣為準；任何轉換都保留來源座標與穩定 ID。

原始訪談表、核准紀錄與人工標註不得被生成流程覆寫。工程文件若由來源衍生，必須標示生成時間、來源版本與待確認項目。

## 維護契約（改動本生態系時必須重新滿足的不變量）

1. **單一真相源**：pipeline 流程圖只畫在 `WORKFLOW.md`；`/specify` 硬閘檢查清單只在 `VibeCoding_Workflow_Templates/_meta/workflow_manual.md` §8；追溯 ID 主鏈只在 `docs/document-system/architecture.md` §7.1；版本號只在根目錄 README badge（沿革在 `CHANGELOG.md`）。其他位置一律「一句話＋連結」，不得 paraphrase 內容——paraphrase 就是未來的 drift。
2. **Router 不說謊**：新增、改名、刪除 skill 或改變其定位時，必須同步更新 `skills/INDEX.md` 的目錄與路由段；索引漏列新 skill、或仍導向已刪 skill，視為缺陷而非疏漏。
3. **Frontmatter 與現實一致**：Action Skill 的 `argument-hint` 與說明不得引用已退役的模板或文件名；模板增刪時回查四個 Action Skills。
4. **大型 skill 分層**：SKILL.md 超過約 200 行時拆 `references/`（漸進揭露），不整檔常駐。
5. **來源可追**：新增 community/第三方 skill 必須在 `skills/INDEX.md` 記來源、授權與更新方式。
6. **拒絕有紀錄**：退役或否決一個機制時，在 `.out-of-scope/` 留一檔（概念、理由、先例）；重新提案前先讀它。

## Runtime Context

不把每次對話或 Subagent 摘要寫成專案內的影子文件（本專案已移除舊的 `.claude/context/` 暫存目錄）。Claude Code 的 session/task 機制處理暫態狀態；值得長期保存的內容應進入 PRD、ADR、SAD、測試證據或其他正式文件。
