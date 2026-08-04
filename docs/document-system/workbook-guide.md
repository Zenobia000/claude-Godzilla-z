# 角色追蹤簿（Excel）指南

沒有 Jira／Confluence 時，用「docs + 三個角色 Excel」管理需求、工程與 QA。核心原則：

> **R&R 靠「誰擁有哪個產物」；串連靠「共用 ID 骨幹」。** 產物按角色分開（開會對焦、職責清楚），用 ID 串起來（追溯不斷）。

## 1. 兩層、三檔

| 層 | 產物 | 用途 |
|---|---|---|
| 知識（訂版） | `docs/` Markdown、ADR、code | 版本化的細節、建置真相源；AI 起草、人 review |
| 追蹤（活的） | 三個角色 Excel | 狀態、決策、追溯；人滾動維護，各角色一檔 |

三個角色 Excel（各放在該 owner 的資料夾）：

| 檔 | Owner | 位置 | 主要欄位 |
|---|---|---|---|
| **需求追蹤** | PM／BA | [`01_requirements/requirements_tracker.xlsx`](../../VibeCoding_Workflow_Templates/01_requirements/requirements_tracker.xlsx) | 需求ID、VOC、優先序、範圍、里程碑、業務驗收、狀態、**核准**、PRD連結；③Gate 記里程碑簽核 |
| **工程追蹤** | 架構師 | [`03_architecture/engineering_tracker.xlsx`](../../VibeCoding_Workflow_Templates/03_architecture/engineering_tracker.xlsx) | FR/NFR-ID、**來源需求**、SAD元件、ADR、Code reality、狀態；②模組BOM |
| **測試追蹤** | QA | [`05_qa/qa_tracker.xlsx`](../../VibeCoding_Workflow_Templates/05_qa/qa_tracker.xlsx) | TC/QTM-ID、**來源FR/NFR**、測試設計、狀態；②執行證據 |

## 2. ID 骨幹（串連的關鍵）

```text
REQ/DEC-*  →  FR/NFR-*  →  TC/QTM-*
（需求追蹤）   （工程追蹤）    （測試追蹤）
```

這是完整追溯主鏈（唯一權威：[architecture.md](architecture.md) §7.1）在追蹤層的骨幹投影，不是另一條鏈。

下游檔用**「來源ID」欄**（範本裡標橙色）指向上游：工程追蹤的 `來源需求` 填 `DEC-*`；測試追蹤的 `來源FR/NFR` 填 `FR-*`。要追一條需求的全貌，就用同一個 ID 在三檔間 filter。跨檔沒有自動 join——這是換取「每檔一個 owner、R&R 清楚」的代價。

## 3. 為什麼分三檔（R&R）

- **開會對焦**：需求會看需求追蹤（PM 主導）、架構會看工程追蹤（架構師主導）、測試會看測試追蹤（QA 主導）。各人只碰自己的檔，職責不混。
- **不失串連**：共用 ID + 來源欄，跨檔仍可追溯。
- 一份 doc / 一個 Excel 檔 = 一個 owner，這就是 R&R 的定義來源。

## 4. 狀態與滾動

各檔 `狀態` 欄下拉：`開放 / 進行中 / Pending / 結束 / Deferred`。需求先確定、開發功能導向、里程碑滾動調整，不必一開始填滿；需求追蹤的 `② 決策沿革` 記錄滾動調整（含一句原因；長理由寫 PRD 附註或 ADR）。

**需求追蹤簿 ①需求決策是需求決策的權威**：owner 在此拍板優先序、範圍、里程碑、業務驗收，並以 `核准` 欄（`提案 / 已核准 / 延後 / 取消`）簽核；`③ Gate` 記里程碑放行（`核准 / 保留 / 退回`＋決策者＋日期）。`/specify` 硬閘（Pilot 階段起）檢查的就是這兩張表；檢查清單的唯一權威是 [workflow_manual](../../VibeCoding_Workflow_Templates/_meta/workflow_manual.md) §8，雛型期只需骨架列、不擋迭代。

## 5. 認知負載鐵律（給 AI）

Excel 只放**骨架**（ID＋狀態＋一句話＋連結），細節在 docs。AI 更新結構化欄位與對應 docs，回報只給**短 delta**（「`DEC-003` 進 In Dev、`FR-007` 連到 `sad.md#agt`」），不倒大段文字。人在 Excel 上做決策（優先序、範圍、狀態轉換、Gate），AI 做決策之間的執行。
