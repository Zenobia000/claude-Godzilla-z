# Document System Index

這是 Action Skills 進入文件系統時的第一個索引。它定義目前資產的定位，不複製其內容。

## Authority

| 資料 | 權威來源 | 可人工維護 | 備註 |
|---|---|---|---|
| 原始訪談、VOC、優先序、範圍與核准 | 經指定的 Excel B 欄位或原始業務文件 | 是，由 business owner | 保留視覺語意與來源座標 |
| PRD、FR/NFR、BDD、SAD/SDS、ADR、API／資料契約 | Git 中核准的工程文件／code-native contract | 是，由文件 owner | Excel G 欄位只是投影 |
| 程式碼現況 | Repository、build 與 deployment artifact | 是，由工程流程 | 不由規格狀態推論 |
| 測試設計 | Git 中測試文件與測試程式 | 是，由 QA/RD | Excel G 欄位只是投影 |
| 測試／UAT／發布結果 | 不可變 evidence 與 Excel E 欄位 | 是，由 QA/UAT/Release owner | 生成時必須無損保留 |
| 彙總、coverage、dashboard | Excel D 欄位或報告 | 否 | 可重算 |

完整 B/E/G/D 定義、round-trip 與狀態軸見 [architecture.md](architecture.md)。

## Current assets

| Asset | Classification | Use |
|---|---|---|
| `software_development_documentation_guide_zh_tw.docx` | Catalog/reference | 決定什麼風險需要哪些文件（模板已依其九層分類與文件詞彙全面對齊）|
| `VibeCoding_Workflow_Templates/` | Authoring templates | 產生／更新工程文件 |
| `VibeCoding_Workflow_Templates/01_requirements/requirement_decision_record.md` | 需求決策紀錄（Excel B 區）| owner 拍板優先序、範圍、Gate；`/specify` 硬閘的檢查對象 |
| `01_requirements/requirements_tracker.xlsx`、`03_architecture/engineering_tracker.xlsx`、`05_qa/qa_tracker.xlsx` | 三個角色追蹤 Excel（PM/BA、架構師、QA）| 以 REQ→FR/NFR→TC 的 ID 骨幹串連；見 workbook-guide |

逐文件、逐工作表與 27 類企業文件對照見 [artifact-map.md](artifact-map.md)。

## Project artifact registry

這個模板本身沒有假裝存在一套核准的專案需求。新專案執行 `/intake` 後，依實際需要建立：

```text
docs/document-system/
├── requirements/
│   └── requirements-register.md
├── specifications/
├── architecture/
│   └── adr/
├── verification/
└── traceability/
```

每份 artifact 至少登錄：

| 欄位 | 說明 |
|---|---|
| Path | 真實檔案位置 |
| Type | source / contract / decision / evidence / projection |
| Owner | 唯一維護角色 |
| Status | Draft / Review / Approved / Deprecated |
| Source IDs | `SRC-*`、`REQ-*` 等上游 ID |
| Revision | commit、版本或日期 |
| Replaces | 被替代 artifact／ID |

沒有建立的文件不應只為補滿目錄而生成。
