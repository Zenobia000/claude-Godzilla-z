# 開發流程使用說明書

> **版本:** v3.0 | **更新:** 2026-08-05
>
> [`00` 護身符](./00_requirements_amulet.md) 過完之後看這份：**決定這個專案要寫哪幾份文件**。
> 怎麼跑一輪 session（探索、切片、收尾）在 [`.claude/PLAYBOOK.md`](../.claude/PLAYBOOK.md)，這裡不重述。

**這條線沒有簽核閘。** 需要 owner 簽核、可稽核追溯與 Excel 追蹤簿 → 見 [§4](#4-什麼時候換-pilot-線)。

---

## 1. 先選深度

照 `PLAYBOOK.md` 的三條路線走，文件跟著路線走，不反過來：

| 你在哪 | 路線 | 這階段通常值得寫 |
| :--- | :--- | :--- |
| 驗證一個想法，講得出「做完長什麼樣」而且很小 | **A 直接做** | 幾乎不寫；回不了頭的決策寫一則 [`04` ADR](./04_architecture_decision_record_template.md) |
| 是一個功能，講得出做完長什麼樣 | **B 規劃一輪** | [`02` PRD](./02_project_brief_and_prd.md)；要交給別人接手才加 [`05` 架構](./05_architecture_and_design_document.md) ＋ [`08` 結構](./08_project_structure_guide.md) |
| **講不出**做完長什麼樣 | **C 先撥霧** | 不產交付物。撥霧只產決策，清楚了再回這張表 |
| 需求由別人拍板、或要對外驗收 | **換 Pilot 線** | [§4](#4-什麼時候換-pilot-線) |

**唯一判準：這份文件現在寫下來，會替誰省掉一次來回？** 答不出來就先不寫。

模板是**選用的，不是待辦清單**——17 份填滿不代表做對事。

---

## 2. 17 份模板什麼時候取用

### 開工前（00–01）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 00 | [requirements_amulet](./00_requirements_amulet.md) | **每個專案／Epic 開工前必過**：角色權責、FR／NFR 必問、開場檢查表 |
| 01 | 本檔 | 00 過完，決定要寫哪幾份 |

### 需求與行為（02–03）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 02 | [project_brief_and_prd](./02_project_brief_and_prd.md) | 有人要接手，或範圍需要對外講清楚 |
| 03 | [behavior_driven_development_guide](./03_behavior_driven_development_guide.md) | 驗收條件要能直接變測試（搭 `sunnydata-testing`） |

### 架構與契約（04–06）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 04 | [architecture_decision_record_template](./04_architecture_decision_record_template.md) | **三條件全中才寫**：難以逆轉 ∧ 沒有背景會困惑 ∧ 真實取捨的結果。ADR 的價值來自稀有 |
| 05 | [architecture_and_design_document](./05_architecture_and_design_document.md) | 系統形狀要交接，或 NFR 目標需要對應實現策略（C4／DDD） |
| 06 | [api_design_specification](./06_api_design_specification.md) | 契約要給別人（別的團隊、前端、外部）開工（搭 `sunnydata-api-design`） |

### 落到工程（07–10）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 07 | [module_specification_and_tests](./07_module_specification_and_tests.md) | 往 production 走，模組行為與測試要固定下來 |
| 08 | [project_structure_guide](./08_project_structure_guide.md) | 有人要接手 codebase |
| 09 | [file_dependencies_template](./09_file_dependencies_template.md) | 依賴開始糾纏、要判斷改動爆炸半徑（搭 `sunnydata-architecture-review`） |
| 10 | [class_relationships_template](./10_class_relationships_template.md) | 領域模型複雜到光讀 code 講不清楚 |

### 審查與前端（11–12、17）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 11 | [code_review_and_refactoring_guide](./11_code_review_and_refactoring_guide.md) | 要固定團隊的 review 標準（單次 review 走 `sunnydata-code-review` 兩軸即可） |
| 12 | [frontend_architecture_specification](./12_frontend_architecture_specification.md) | 前端要定狀態管理、元件分層、樣式策略 |
| 17 | [frontend_information_architecture_template](./17_frontend_information_architecture_template.md) | 前端要定導覽、路由、頁面層級與資訊分群 |

### 上線與維運（13–16）

| # | 模板 | 什麼時候 |
| :---: | :--- | :--- |
| 13 | [security_and_readiness_checklists](./13_security_and_readiness_checklists.md) | 要往 production 走（搭 `sunnydata-security`） |
| 14 | [deployment_and_operations_guide](./14_deployment_and_operations_guide.md) | 要往 production 走（搭 `sunnydata-infrastructure`） |
| 15 | [documentation_and_maintenance_guide](./15_documentation_and_maintenance_guide.md) | 交接給維護團隊 |
| 16 | [wbs_development_plan_template](./16_wbs_development_plan_template.md) | 要對外承諾時程與工作拆解 |

---

## 3. 誰寫哪份

角色定義、決策權與打架邊界在 [`00` §1](./00_requirements_amulet.md#1-四角色分工速查)，這裡只給落點：

| 角色 | 主要產出 | 語域 |
| :--- | :--- | :---: |
| **PM** | 02 | L1 |
| **SA** | 02（需求段）、03、05 的 NFR **目標** | L2 |
| **架構師** | 04、05（含 NFR **實現**）、09 | L2 |
| **SD** | 06、07、10 | L3 |
| **DEV** | 08、11、12、17 | L3 |
| **SEC／OPS** | 13、14、15 | L3 |

一人多角時角色可以合併，**決策權仍要分開記**——改 NFR 目標是需求變更，不是工程決策。語域規則見 [`.claude/rules/language-register.md`](../.claude/rules/language-register.md)。

---

## 4. 什麼時候換 Pilot 線

任一成立就換到 `refactor/document-driven-ecosystem` 分支（判準與 [`PLAYBOOK.md`](../.claude/PLAYBOOK.md) 同一份）：

- 需求由**別人**拍板，要證明某範圍是誰在何時核准
- 對外交付，驗收條件必須逐條可稽核
- 多人多團隊，「這條需求有沒有測到」要查得出來
- 有法規或稽核要求

兩條線共用同一套 harness 與同一批模板，差別只在文件治理的嚴謹度：Pilot 線才有 `SRC-* → REQ-* → ACPT-*` 追溯鏈、owner 簽核硬閘與追蹤簿。

**先雛型 → 打掉 → 重構是正常路徑。** 別用 production 標準卡雛型，也別用雛型標準交付 production。

---

## 5. 這條線用什麼取代 Gate

沒有「準出 ≥ 90%」這種閘。取代它的是三件常駐的事：

| 取代什麼 | 靠什麼 |
| :--- | :--- |
| 產出完成度簽核 | [`golden-rules` §4](../.claude/rules/golden-rules.md)：**以證據宣告完成**——沒跑過的檢查不得寫成通過 |
| 階段審查會 | 收尾的 `sunnydata-code-review` 兩軸（Standards／Spec **分開報、不排名**） |
| 文件齊備度檢查 | [`git-workflow`](../.claude/rules/git-workflow.md)：這次改動讓哪份**已填寫**的模板失真，就同一個 PR 一起改 |

沒填過的模板不需要為了這條去填。

---

## 版本記錄

| 版本 | 日期 | 變更 |
| :--- | :--- | :--- |
| v3.0 | 2026-08-05 | 重新定位為**模板選用路由**：接在 00 之後、操作層交給 `PLAYBOOK.md`。移除與 POC 線衝突的簽核 Gate 與「完整流程 vs MVP」雙模式；改用 PLAYBOOK 的 A／B／C 三路線。修正 7 個不存在的檔名，補齊 09–12、14–17 |
| v2.0 | — | 完整流程 / MVP 雙模式 + Gate 度量（已退役） |
