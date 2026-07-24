# 文件、活頁簿與範本對照表

> 架構原則與治理規則見[文件驅動開發系統架構](architecture.md)。

## 1. 對照表的讀法

本表回答四個問題：

1. 這份資料由誰維護、權威來源在哪裡？
2. 它應該出現在哪一本 Excel 視圖？
3. 建立或更新 Markdown 契約時應採用哪個 VibeCoding 範本？
4. 用什麼穩定 ID 串接，而不是依賴檔名、列號或工作表位置？

載體縮寫：

- **B**：Excel business-owned 欄位。
- **E**：Excel evidence-owned 欄位。
- **G**：由工程契約生成到 Excel 的欄位。
- **D**：衍生／彙總欄位。
- **MD**：Git 中的 Markdown 工程契約。
- **EXE**：程式碼、測試、Schema、IaC 等可執行成品。

## 2. 來源資產盤點

### 2.1 四書治理實例（已抽離）

本架構原始的四書治理實例（SmartLock：四本 xlsx、產生器 `_build_enterprise_workbooks.py` / `_spec_data.py` / `_sync_test_canon.py`、健康報告與元件字典）已抽離為外部範例，不再隨附於本 repo。它示範的可重用結構已萃取進本文件與 [architecture.md](architecture.md)。留下的教訓：產生器把需求決策（優先序/範圍/Gate）硬編碼衍生，是需要翻轉的反模式；決策應外部化為 owner 資料（見模板 18）。

### 2.2 其他來源

| 來源 | 結構／內容 | 在目標系統中的定位 |
|---|---|---|
| [大型軟體公司開發文件指南](../../software_development_documentation_guide_zh_tw.docx) | 18 個編號主章、企業文件目錄、MVP/Pilot/Enterprise 文件集合、命名與反模式 | 文件 catalog 與選擇指南，不直接作工程 SSOT |
| [VibeCoding 工作流範本](../../VibeCoding_Workflow_Templates/INDEX.md) | 18 份產品、需求決策、架構、實作、驗證與營運範本 | 建立／更新 MD 契約的操作模板，不是第二份 SSOT |

## 3. 四本治理活頁簿（pattern）

以下工作表分工是可重用的原型，非特定專案實例。

### 3.1 規格統控規劃書

| 工作表 | 內容 | 目標權責 |
|---|---|---|
| 封面 | 版本、範圍、閱讀方式 | G/D；核准欄若新增則 B |
| ⓪ ID 來源指南 | ID 來源與閱讀規則 | G |
| ① 階段矩陣 | 階段、交付、Gate | G/D；Gate 決策、Owner 為 B |
| ② M1 需求 | M1 FR、狀態、驗收摘要 | G；優先序／納入決定為 B |
| ③ M2 需求 | M2 FR、狀態、驗收摘要 | G；優先序／納入決定為 B |
| ④ M3+ 整合範圍 | 後續整合需求 | G；範圍決定為 B |
| ⑤ 實作順序／Gate | WBS 與放行條件 | G/D；核准決定為 B |
| ⑥ 架構選擇 | 架構選項、影響、狀態 | G；業務約束／核准為 B |
| ⑦ 名詞白話 | 名詞與業務解釋 | G |
| ⑧ 完整模組表 | 模組、需求、code reality | G/D |
| ⑨ ADR 決策表 | ADR 摘要與狀態 | G；決策簽核為 B |
| ⑩ 契約／追溯風險 | 缺口、孤兒與風險 | D；風險接受為 B |
| 元件詞彙表 | 101 個 SAD/SDS 元件 | G |

### 3.2 業務邏輯驗收控制表

| 工作表 | 內容 | 目標權責 |
|---|---|---|
| 封面 | 版本、範圍、使用說明 | G；核准為 B |
| 各 FR 領域頁（依專案領域分）| VOC、FR、驗收、成功指標、例外、階段、元件映射 | FR、ACPT、元件映射為 G；VOC、商業例外、優先序、Owner 與 UAT 接受為 B |
| PERF／SEC／OPS 三個 NFR 頁 | 非功能需求與驗收 | NFR、驗證條件為 G；風險接受與 Owner 為 B |
| 技術流程映射 | 業務流程對架構／元件 | G |
| 元件詞彙表 | SAD/SDS 元件定義 | G |

### 3.3 模組功能 BOM

| 工作表 | 內容 | 目標權責 |
|---|---|---|
| 封面 | 版本與閱讀說明 | G |
| BOM 主表 | L1 子系統、L2 能力群、L3 FR、元件、SAD/SDS、code reality、證據 | G/D；責任人或例外接受若需人工維護則 B |
| SAD/SDS 元件視圖 | 元件到能力、規格與實作證據 | G/D |
| 元件詞彙表 | 101 個元件的定義與邊界 | G |

L1/L2 是視覺分組，L3 的正式 FR ID 與元件 ID 才可參與追溯。`AS-BUILT`、`PARTIAL`、`TO-BE` 是 code reality，不得覆寫 requirement status。

### 3.4 整合測試計畫

| 工作表 | 內容 | 目標權責 |
|---|---|---|
| 封面 | 測試版本、範圍、說明 | G；核准為 E/B |
| ① 策略 | 測試目標、範圍與方法 | G |
| ② 測試類型 | 測試層次與責任 | G |
| ③ Bug 等級 | 缺陷分級與處置 | G；風險接受為 B |
| ④ 環境／部署 | 測試環境與部署條件 | G；實際版本／環境為 E |
| ⑤ STLC | 測試生命週期與 Gate | G/D |
| ⑥ SIT／UAT／RC | 階段、入口／出口條件 | G；簽核結果為 E/B |
| ⑦ RD×QA RACI | 角色責任 | G；Owner 任命為 B |
| ⑧ 客需／場景 | 171 筆需求與測試映射 | G |
| ⑨ 測試案例／執行記錄 | 171 筆設計與執行表面 | 設計為 G；actual、pass/fail、evidence、defect、executor、version、date 為 E |
| 附錄 A 追溯 | 隱藏的全鏈關係 | D |
| 附錄 B 規格完整度 | 隱藏的缺口分析 | D |
| 附錄 C 測試分析 | 隱藏的覆蓋與統計 | D |
| 元件詞彙表 | 隱藏的元件字典 | G |

## 4. Word 企業文件目錄映射

以下是 Word 指南中的大型公司文件 catalog 摘要。不是每個專案都要建立每一份；以風險、協作與稽核需要選用。

| # | 文件類別 | 權威載體／Owner | 主要 ID | Excel 視圖 | VibeCoding 範本 |
|---:|---|---|---|---|---|
| 00 | Product Strategy | MD；Product/Business | `BR-*`、目標 ID | 規格統控 B/G | [02 Brief/PRD](../../VibeCoding_Workflow_Templates/02_project_brief_and_prd.md) |
| 01 | MRD | MD；Product Marketing | `BR-*`、市場假設 ID | 規格統控 B/G | [02 Brief/PRD](../../VibeCoding_Workflow_Templates/02_project_brief_and_prd.md) |
| 02 | BRD | MD；Business/BA | `BR-*` | 規格統控、驗收控制 B/G | [02 Brief/PRD](../../VibeCoding_Workflow_Templates/02_project_brief_and_prd.md) |
| 03 | PRD | MD；Product | `PRD-*`、`FR-*` | 規格統控、驗收控制 G | [02 Brief/PRD](../../VibeCoding_Workflow_Templates/02_project_brief_and_prd.md) |
| 04 | SRS | MD；BA/Engineering | `FR-*` | 四本活頁簿 G | [05 Architecture/Design](../../VibeCoding_Workflow_Templates/05_architecture_and_design_document.md) |
| 05 | NFR | MD；Architecture/SRE/Security | `NFR-*` | 驗收控制、規格統控、測試 G | [13 Security/Readiness](../../VibeCoding_Workflow_Templates/13_security_and_readiness_checklists.md) |
| 06 | UX Research Report | MD／研究庫；UX | 研究／洞察 ID | 規格統控摘要 | [17 Frontend IA](../../VibeCoding_Workflow_Templates/17_frontend_information_architecture_template.md) |
| 07 | Journey Map | MD／設計工具；UX | journey/step ID | 驗收控制摘要 | [17 Frontend IA](../../VibeCoding_Workflow_Templates/17_frontend_information_architecture_template.md) |
| 08 | User Flow | MD／設計工具；UX/Product | flow/step、`SCN-*` | 驗收控制、測試 G | [17 Frontend IA](../../VibeCoding_Workflow_Templates/17_frontend_information_architecture_template.md) |
| 09 | IA | MD／設計工具；UX/Frontend | page/route ID | 規格統控摘要 | [17 Frontend IA](../../VibeCoding_Workflow_Templates/17_frontend_information_architecture_template.md) |
| 10 | UI Spec | MD／設計工具；Design/Frontend | screen/component ID | 驗收控制摘要 | [12 Frontend Architecture](../../VibeCoding_Workflow_Templates/12_frontend_architecture_specification.md) |
| 11 | Design System | MD + 元件庫；Design/Frontend | token/component ID | BOM 摘要 | [12 Frontend Architecture](../../VibeCoding_Workflow_Templates/12_frontend_architecture_specification.md) |
| 12 | SAD | MD；Architect | `MOD-*`、component ID | 規格統控、BOM G | [05 Architecture/Design](../../VibeCoding_Workflow_Templates/05_architecture_and_design_document.md) |
| 13 | Security Architecture | MD；Security/Architect | `NFR-SEC-*`、threat ID | 規格統控、驗收、測試 G | [13 Security/Readiness](../../VibeCoding_Workflow_Templates/13_security_and_readiness_checklists.md) |
| 14 | ADR/ | MD；Decision Owner | `ADR-*` | 規格統控 G/B | [04 ADR](../../VibeCoding_Workflow_Templates/04_architecture_decision_record_template.md) |
| 15 | SDS | MD；Tech Lead | `MOD-*`、component ID | BOM G | [05 Architecture/Design](../../VibeCoding_Workflow_Templates/05_architecture_and_design_document.md) |
| 16 | API Spec | OpenAPI + MD；API Owner | `API-*`、operation ID | BOM、測試 G | [06 API Design](../../VibeCoding_Workflow_Templates/06_api_design_specification.md) |
| 17 | AsyncAPI | AsyncAPI + MD；Event Owner | `EVT-*`、message ID | BOM、測試 G | [06 API Design](../../VibeCoding_Workflow_Templates/06_api_design_specification.md) |
| 18 | DB Design | Schema/Migration + MD；Data Owner | `DB-*`、schema object ID | BOM G | [05 Architecture/Design](../../VibeCoding_Workflow_Templates/05_architecture_and_design_document.md) |
| 19 | Test Plan | MD；QA Lead | `TS-*` | 整合測試 G | [07 Module Spec/Tests](../../VibeCoding_Workflow_Templates/07_module_specification_and_tests.md) |
| 20 | Test Cases | MD／測試工具；QA/RD | `QTM-*`、`TC-*`、`CASE-*` | 整合測試 G/E | [03 BDD](../../VibeCoding_Workflow_Templates/03_behavior_driven_development_guide.md)、[07 Module Spec/Tests](../../VibeCoding_Workflow_Templates/07_module_specification_and_tests.md) |
| 21 | Traceability Matrix | 生成 MD/JSON；QA/Governance | 所有正式 ID | 四本 D | [15 Documentation/Maintenance](../../VibeCoding_Workflow_Templates/15_documentation_and_maintenance_guide.md) |
| 22 | UAT Report | 證據庫 + MD；Business/UAT | `EV-*`、UAT ID | 驗收控制、整合測試 E/B | [03 BDD](../../VibeCoding_Workflow_Templates/03_behavior_driven_development_guide.md) |
| 23 | Deployment Guide | MD + IaC；Platform/Release | deploy/`REL-*` | 整合測試／規格統控摘要 | [14 Deployment/Ops](../../VibeCoding_Workflow_Templates/14_deployment_and_operations_guide.md) |
| 24 | Runbook | MD；Ops/SRE | service/runbook ID | 規格統控風險摘要 | [14 Deployment/Ops](../../VibeCoding_Workflow_Templates/14_deployment_and_operations_guide.md) |
| 25 | Monitoring Spec | MD + monitoring-as-code；SRE | SLI/SLO/alert ID | 規格統控、驗收 G/D | [14 Deployment/Ops](../../VibeCoding_Workflow_Templates/14_deployment_and_operations_guide.md) |
| 26 | Incident Postmortem | MD；Incident Owner | incident/action ID | 規格統控風險摘要 | [15 Documentation/Maintenance](../../VibeCoding_Workflow_Templates/15_documentation_and_maintenance_guide.md) |

另外，Project Plan／RACI／Change Request／Release Notes 屬橫向治理工件：

- Project Plan／WBS：使用 `WBS-*`，投影到規格統控規劃書，採用[16 WBS](../../VibeCoding_Workflow_Templates/16_wbs_development_plan_template.md)。
- RACI：角色任命是 B，責任矩陣投影是 G；視需要放在規格統控或整合測試。
- Change Request：使用 `CR-*`，連結受影響 ID、決策與 migration。
- Release Notes：使用 `REL-*`，連結完成的 FR/NFR、修復、證據與部署，採用[15 Documentation/Maintenance](../../VibeCoding_Workflow_Templates/15_documentation_and_maintenance_guide.md)。

## 5. 18 份 VibeCoding 範本的職責

| 範本 | 何時使用 | 主要產物／不能取代的 SSOT |
|---|---|---|
| [01 Workflow Manual](../../VibeCoding_Workflow_Templates/01_workflow_manual.md) | 選模式與確認交付順序 | 流程指南；不作 task database |
| [02 Project Brief & PRD](../../VibeCoding_Workflow_Templates/02_project_brief_and_prd.md) | 定義問題、價值、範圍、需求 | BRD/PRD MD；業務核准仍在 Excel B |
| [03 BDD Guide](../../VibeCoding_Workflow_Templates/03_behavior_driven_development_guide.md) | 把 ACPT 轉成可驗證場景 | `SCN-*`／BDD；執行證據仍在 E |
| [04 ADR](../../VibeCoding_Workflow_Templates/04_architecture_decision_record_template.md) | 有重要、難逆轉或跨團隊決策 | `ADR-*`；不取代 SAD/SDS |
| [05 Architecture & Design](../../VibeCoding_Workflow_Templates/05_architecture_and_design_document.md) | 系統邊界、元件、資料與部署設計 | SAD/SDS/DB MD；不取代可執行 schema |
| [06 API Design](../../VibeCoding_Workflow_Templates/06_api_design_specification.md) | 對外或跨模組同步／非同步介面 | API/EVT MD；OpenAPI/AsyncAPI 為可執行契約 |
| [07 Module Spec & Tests](../../VibeCoding_Workflow_Templates/07_module_specification_and_tests.md) | 單一模組行為、邊界與測試設計 | MOD/TC MD；不宣告實作已完成 |
| [08 Project Structure](../../VibeCoding_Workflow_Templates/08_project_structure_guide.md) | 新專案或重大目錄調整 | repo layout 決策；實際 repo 為準 |
| [09 File Dependencies](../../VibeCoding_Workflow_Templates/09_file_dependencies_template.md) | 複雜依賴、重構或 impact analysis | dependency map；應由掃描工具驗證 |
| [10 Class Relationships](../../VibeCoding_Workflow_Templates/10_class_relationships_template.md) | 複雜領域模型或物件協作 | class/component design；程式碼為實況 |
| [11 Review & Refactoring](../../VibeCoding_Workflow_Templates/11_code_review_and_refactoring_guide.md) | PR review、技術債與重構 | review checklist／change plan |
| [12 Frontend Architecture](../../VibeCoding_Workflow_Templates/12_frontend_architecture_specification.md) | 前端狀態、元件、route、design system | frontend architecture MD |
| [13 Security & Readiness](../../VibeCoding_Workflow_Templates/13_security_and_readiness_checklists.md) | threat、NFR、上線安全閘門 | security/readiness evidence index |
| [14 Deployment & Operations](../../VibeCoding_Workflow_Templates/14_deployment_and_operations_guide.md) | 部署、回滾、監控、on-call | deploy/runbook/monitoring MD；IaC 與監控系統為實況 |
| [15 Documentation & Maintenance](../../VibeCoding_Workflow_Templates/15_documentation_and_maintenance_guide.md) | 文件更新、維護、release、postmortem | doc/release governance |
| [16 WBS Development Plan](../../VibeCoding_Workflow_Templates/16_wbs_development_plan_template.md) | 多階段、跨人員或需要 Gate | `WBS-*`；不取代需求與 issue tracker |
| [17 Frontend IA](../../VibeCoding_Workflow_Templates/17_frontend_information_architecture_template.md) | 頁面、導覽、user flow 與資訊架構 | IA/flow MD／設計資產 |
| [18 Requirement Decision Record](../../VibeCoding_Workflow_Templates/18_requirement_decision_record.md) | owner 拍板優先序／範圍／里程碑／Gate／業務驗收 | Excel B 區的 MD 形態；需求決策權威，非 AI 衍生 |

## 6. Trace ID 字典

| 類型 | 格式範例 | 權威來源 | 典型上游 → 下游 |
|---|---|---|---|
| 來源座標 | `SRC-CRM-2026-CORE-R18-C4` | 原始來源 + intake register | source file/cell → SRC → REQ |
| 進件需求 | `REQ-0001` | intake requirements register | SRC → REQ → BR/FR/NFR |
| 商業需求 | `BR-LOCK-001` | BRD/PRD MD + Excel B 決策 | Strategy → BR → FR |
| 功能需求 | `FR-AGT-LOCK-001` | SRS MD | BR → FR → ACPT/MOD |
| 非功能需求 | `NFR-SEC-001` | NFR MD | BR/FR → NFR → design/test |
| 驗收條件 | `ACPT-LOCK-001` | PRD/SRS MD | FR/NFR → ACPT → SCN/QTM |
| BDD／業務場景 | `SCN-LOCK-001` | BDD MD | ACPT → SCN → CASE |
| 架構決策 | `ADR-001` | ADR MD | requirement/constraint → ADR → MOD/API/DB |
| 模組／元件 | `MOD-AGT-RES-001` | SAD/SDS MD | FR/NFR/ADR → MOD → code/TC |
| API | `API-LOCK-001` | OpenAPI + MD | FR/MOD → API → TC |
| 事件 | `EVT-LOCK-001` | AsyncAPI + MD | FR/MOD → EVT → TC |
| 資料 | `DB-LOCK-001` | Schema/Migration + MD | FR/MOD/ADR → DB → TC |
| 測試策略 | `TS-01` | Test Plan MD | NFR/system risk → TS → QTM |
| 測試映射 | `QTM-LOCK-001` | trace/test MD | ACPT/design → QTM → TC |
| 詳細測試 | `TC-LOCK-001` | Test Cases／測試程式 | QTM → TC → EV |
| Excel 案例 | `CASE-LOCK-001` | 生成／映射層 | TC → CASE → EV |
| 證據 | `EV-REL-001` | 測試／證據庫 | TC/CASE → EV → UAT/REL |
| 變更 | `CR-001` | Change Request MD | affected IDs → CR → superseding IDs |
| 發布 | `REL-2026-07-001` | Release record | FR/TC/EV → REL |
| 工作分解 | `WBS-M1-001` | Project Plan MD | deliverable IDs → WBS |

### 6.1 最小欄位

每筆跨文件 trace 至少保存：

```text
id
type
source_artifact
source_locator
upstream_ids[]
downstream_ids[]
status
owner
version
evidence[]
supersedes[]
```

驗證器至少檢查：

- ID 唯一且格式合法。
- upstream/downstream 雙向一致。
- 沒有 orphan FR/NFR、ACPT、TC 或 release evidence。
- locator 存在，但 locator 不作主鍵。
- requirement、code reality、verification、release 四種狀態未混用。
- B/E 欄位在活頁簿重建前後完全保留。

## 7. MVP／Full 文件選擇矩陣

| 工件 | MVP | Full |
|---|---|---|
| 業務 Excel | 一份 lean register 或四書的必要頁 | 四本活頁簿 + B/E round-trip |
| Brief／PRD／FR/NFR | 一份 lean spec | 分層 PRD、SRS、NFR |
| ACPT／BDD | 核心 happy/edge/failure path | 全需求與 UAT 場景 |
| SAD/SDS | 一份短架構說明 | 系統與模組完整設計 |
| ADR | 僅重大決策 | 完整決策紀錄與索引 |
| API／Event／DB | 有跨界契約才建立 | machine-readable contracts + migration |
| Test | 核心 checklist + automation | Test Plan/Cases、QTM、SIT/UAT/RC |
| Trace | 關鍵 ID 鏈 | 全鏈 matrix、coverage、orphan gate |
| Security/Ops | 基本 readiness；有服務責任則 runbook | threat、NFR、deploy、runbook、monitoring、DR |
| Release | release note + evidence link | 正式核准、change、release、audit evidence |
| Vibe 範本 | 18、01、02、03；04/06/07/13/14/15 視風險選用 | 依工件選用全部相關範本，不要求無差別填滿 18 份 |

MVP 應升級 Full 的典型觸發條件：敏感資料／法遵、多團隊或外部契約、高可用與 on-call、不可逆資料遷移、正式 UAT 或稽核。

## 8. 現況到目標的缺口

| 缺口 | 影響 | 建議處置 |
|---|---|---|
| 產生器期待的 `04_SRS.md`、`05_NFR.md`、`12_SAD.md`、`15_SDS.md`、`14_ADR/00_INDEX.md`、`19_Test_Plan.md`、`20_Test_Cases.md`、`21_Traceability_Matrix.md`、`22_UAT_Report.md`、`27_Product_Roadmap_WBS.md` 未在目前根目錄出現。元件字典 Markdown 有 101 組 SAD＋SDS locator（202 個 dead links）；四本 workbook 的 OOXML 另含 1,958 個同類 hyperlinks：驗收控制 674、BOM 474、規格統控規劃 266、整合測試 544 | 無法在本倉庫可靠重建快照或開啟 locator | 保持來源檔不變；匯入 canonical 或建立 source manifest 後再由生成器更新 locator，不建立假 placeholder |
| 四本 xlsx 是整檔覆寫的生成快照 | 手動欄位可能遺失 | 導入 B/E schema 與 preservation-safe generation |
| 業務輸入與生成內容尚未欄位級分權 | 「Excel 是 SSOT」容易被誤解 | 每欄標記 B/E/G/D，保護 G/D |
| Trace 仍分散在 Markdown、Python data 與 Excel | 容易孤兒與漂移 | 建立 machine-readable trace manifest 與 validator |
| 部分顯示 ID／L2 標籤可能被當成主鍵 | join 不穩定 | 保留正式 ID，顯示標籤只作分組 |
| Requirement status 與 code reality 容易混讀 | 管理決策失真 | 分成四個獨立狀態軸 |
| Word catalog、Vibe 範本與實際契約可能重複 | 文件量膨脹 | catalog 用來選文件、範本用來產生文件、MD 才是契約 |
| 需求決策（優先序/範圍/Gate）由產生器規則自動衍生 | owner 決策被 AI 代拍，人參與度稀釋 | 以 `18 需求決策紀錄` 為 B 區權威，決策外部化為 owner 資料；`/specify` 硬閘擋未核准項 |
| Word 治理智慧（選用矩陣/命名/反模式/三階段組合）可能隨檔案流失 | 刪 Word 後失去 WHEN/WHY 判斷 | 已吸收進 [`01 workflow manual`](../../VibeCoding_Workflow_Templates/01_workflow_manual.md) §9–§11；Word 文件類型目錄與模板重複部分可放棄 |
