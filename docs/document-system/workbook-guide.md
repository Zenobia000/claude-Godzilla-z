# 治理活頁簿指南（Excel 範本）

> 可填的 `.xlsx` 範本：[`VibeCoding_Workflow_Templates/governance_workbook_template.xlsx`](../../VibeCoding_Workflow_Templates/governance_workbook_template.xlsx)

## 1. 為什麼重排工作表序程

原本四本活頁簿（規劃書／BOM／驗收控制表／測試計畫）的工作表是**依文件類型**分的。站在真實研發團隊「從需求對接一路到工程開發」的視角，比較直覺的是**依流程序程**排：需求先進來、owner 拍板、定義驗收、拆模組、設計測試、收證據、看狀態。

因此範本收斂成**一本整合活頁簿**，工作表依這條流排序。每張表標明欄位屬 B/E/G/D 哪一區（見 [architecture.md §4](architecture.md)）。

## 2. 工作表序程（依團隊流）

| # | 工作表 | 回答什麼 | 主要區 | 主要 ID |
|---|---|---|---|---|
| 0 | 封面與圖例 | 版本、使用方式、B/E/G/D 圖例 | — | — |
| 1 | 需求決策 | owner 拍板優先序、範圍、里程碑、Gate、業務驗收 | **B** | `DEC-*` |
| 2 | 需求追溯 | 需求決策映射到 FR/NFR 與上下游 | G | `REQ/FR/NFR` |
| 3 | 業務驗收 | 驗收條件、成功指標、UAT 核准 | B/G | `ACPT/SCN` |
| 4 | 模組 BOM | 子系統→能力→FR→元件→code reality | G/D | `MOD/FR` |
| 5 | 測試計畫 | 風險場景、測試設計、Entry/Exit | G | `TS/QTM/TC` |
| 6 | 執行證據 | 實測結果、pass/fail、缺陷、版本 | **E** | `TC/CASE/EV` |
| 7 | 狀態儀表 | 各里程碑需求/實作/驗證/覆蓋率 | D | — |

序程刻意讓**第 1 張就是 owner 的需求決策**（需求對接的起點），最後才是衍生的狀態儀表。工程生成欄（G）與衍生欄（D）不覆寫人工的 B/E 欄。

## 3. 區域顏色

範本以底色標示欄位所有權，避免誤editing：

- **B（藍）業務決策**：Business／Product／PM 人工維護，生成不得覆寫。
- **E（綠）證據**：QA／UAT／Release 依穩定 ID 無損合併。
- **G（灰）生成契約**：由 Markdown／程式碼投影，可重建、勿手改。
- **D（黃）衍生**：公式或彙總，唯讀可重算。

## 4. 怎麼用

1. 從 `governance_workbook_template.xlsx` 複製一份到你的專案。
2. 只填 B 區（需求決策、業務驗收、UAT 核准）與 E 區（執行證據）。
3. G/D 欄留給後續由工程契約（Markdown）或公式投影；本啟動寶不隨附產生器，若專案自建，須保留 B/E round-trip。
4. 每列帶穩定 ID，跨表用 ID 串接，不靠列號。

需求決策（第 1 張表）的權威定義與欄位說明見模板 [`01_requirements/requirement_decision_record.md`](../../VibeCoding_Workflow_Templates/01_requirements/requirement_decision_record.md)。
