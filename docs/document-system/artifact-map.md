# 文件分類與模板對照

> 架構原則與治理規則見[文件驅動開發系統架構](architecture.md)。

## 1. 讀法：結構即地圖

不再維護「文件類別 ↔ Excel 視圖 ↔ 模板」的三方對照表。改為**直接採用 [`software_development_documentation_guide_zh_tw.docx`](../../software_development_documentation_guide_zh_tw.docx) 的九層文件分類**，並讓 VibeCoding 模板依同一套分層（`00`–`07`）安置。要用哪份文件、對應哪個模板，看它落在哪一層即可——資料夾結構本身就是對照。

## 2. 九層文件分類 → 模板資料夾

| Word 章 | 文件層 | 這一層的文件（範例）| 模板 |
|---|---|---|---|
| 4 | 產品與商業 | Vision、MRD、PRD、Roadmap | `00_strategy/`（product_vision、roadmap）＋ `01_requirements/prd` |
| 5 | 需求分析 | BRD、SRS、User Story、Use Case、AC | `01_requirements/`（brd、srs、prd、bdd_guide、需求決策紀錄）|
| 6 | UX | Research、Journey、User Flow、IA、Wireframe | `02_ux_ui/`（ux_research_and_journey、information_architecture）|
| 7 | UI／前端設計 | UI Spec、Interaction、Design System、Frontend Tech | `02_ux_ui/`（ui_spec、frontend_technical_design）|
| 8 | 系統架構 | SAD、C4、ADR、NFR | `03_architecture/`（sad、adr、nfr）|
| 9 | 技術設計 | SDS、LLD、API、Event、DB、Sequence、State Machine | `04_design/`（sds、lld、api_spec＋openapi.yaml、event_spec＋asyncapi.yaml、db_design）|
| 10 | QA／測試 | Test Plan、Test Case、UAT、Traceability、QA Report | `05_qa/`（test_plan、uat_plan）＋追蹤簿 |
| 11 | DevOps／維運 | Deployment、Runbook、Monitoring、Incident | `06_ops/`（deployment_and_operations、runbook、monitoring_spec、incident_postmortem）|
| 12 | 專案治理 | Project Plan、RACI、Risk、Change Request、Release Note | `07_governance/`（wbs_development_plan＋RACI、change_request、release_note）|
| — | 安全（跨層）| Security Design、威脅模型、上線關卡 | `05_qa/`（security_and_readiness）|

Sequence 與 State Machine 不另立模板，收在 `sds.md` §2–3（符合 Word 對 SDS 的定義）；專案結構、模組依賴與類別關係合併在 `lld.md`（C4 Code 層）；Wireframe／Prototype／Design System 以 Figma 為載體，交付邊界寫在 `ui_spec` §9。Code review 與文件維護是流程實踐，不設文件模板——由 `.claude/rules/git-workflow.md` 與對應 Skills 承接。

安全類跨系統架構、技術設計與 QA；本套件把它放在 `05_qa/security_and_readiness`，並在架構與部署階段引用。

## 3. 專案文件的建議資料夾（Word §15）

模板產出的正式文件，放進你**專案自己的** `docs/` 樹（不是這個啟動寶）：

```text
docs/
  00_strategy/      product_vision, roadmap
  01_requirements/  prd, brd, srs, user_stories, 需求決策紀錄
  02_ux_ui/         research, journey_map, user_flow, wireframe, ui_spec, design_system
  03_architecture/  sad, c4, adr, nfr
  04_design/        sds, api, db, event, sequence, state_machine
  05_qa/            test_plan, test_cases, uat, qa_report
  06_ops/           deployment, runbook, monitoring, incident
  07_release/       release_notes, change_requests
```

命名規範見 [`_meta/workflow_manual.md`](../../VibeCoding_Workflow_Templates/_meta/workflow_manual.md) §10。

## 4. 三個角色追蹤 Excel（追蹤層）

沒有 Jira／Confluence 時，用三個**角色各自擁有**的 Excel 追蹤狀態與決策，R&R 靠 owner 分開、串連靠 ID 骨幹：

| 檔 | Owner | ID | 接上游 |
|---|---|---|---|
| `01_requirements/requirements_tracker.xlsx` | PM／BA | `REQ/DEC-*` | — |
| `03_architecture/engineering_tracker.xlsx` | 架構師 | `FR/NFR-*` | 來源需求＝`DEC-*` |
| `05_qa/qa_tracker.xlsx` | QA | `TC/QTM-*` | 來源＝`FR/NFR-*` |

Excel 只放骨架＋狀態＋連結，細節在 docs（訂版）。序程、欄位與認知負載原則見 [`workbook-guide.md`](workbook-guide.md)。需求決策欄位的權威定義見 [`01_requirements/requirement_decision_record`](../../VibeCoding_Workflow_Templates/01_requirements/requirement_decision_record.md)。

## 5. Trace ID 模型

跨層以穩定 ID 串接，不靠檔名、列號或標題：

```text
SRC → REQ → BR/PRD → FR/NFR → ACPT → BDD/SCN
    → SAD/SDS/ADR/API/EVT/DB/MOD → TS/QTM → TC/CASE → EV → UAT/REL
```

| 類型 | 格式範例 | 權威來源 |
|---|---|---|
| 來源座標 | `SRC-CRM-2026-R18-C4` | 原始來源 + intake register |
| 進件需求 | `REQ-0001` | intake requirements register |
| 需求決策 | `DEC-001` | 需求決策紀錄（Excel B 區）|
| 商業需求 | `BR-LOCK-001` | BRD/PRD MD + Excel B |
| 功能／非功能 | `FR-AGT-001`、`NFR-SEC-001` | SRS/NFR MD |
| 驗收條件 | `ACPT-LOCK-001` | PRD/SRS MD |
| BDD 場景 | `SCN-LOCK-001` | BDD MD |
| 架構決策 | `ADR-001` | ADR MD |
| 模組／API／事件／資料 | `MOD-*`、`API-*`、`EVT-*`、`DB-*` | SAD/SDS/OpenAPI/AsyncAPI/Schema |
| 測試 | `TS-01`、`QTM-*`、`TC-*`、`CASE-*` | Test Plan/Cases |
| 證據／發布 | `EV-*`、`REL-*`、`CR-*`、`WBS-*` | 證據庫／Release／Change/Plan |

每筆跨文件 trace 至少保存 `id / type / source_artifact / source_locator / upstream_ids[] / downstream_ids[] / status / owner / version / evidence[] / supersedes[]`。驗證器至少檢查：ID 唯一且合法、upstream/downstream 雙向一致、無孤兒 FR/NFR/ACPT/TC/證據、四種狀態（requirement/code reality/verification/release）未混用、B/E 欄位在活頁簿重建前後保留。

## 6. MVP／Pilot／Enterprise 文件量

| 階段 | 對應 profile | 文件量 |
|---|---|---|
| MVP | Fast | ≈ 9 份：需求決策、PRD、BDD、精簡架構、核心測試與證據 |
| Pilot | Product | ≈ 13 份：加 UAT、受影響 SAD/API、部署 |
| Enterprise | Governed | ≈ 27 份：完整 SRS/NFR、SAD/SDS、ADR、契約、SIT/UAT、Ops、稽核追溯 |

升級觸發：敏感資料／法遵、多團隊或外部契約、高可用與 on-call、不可逆遷移、正式 UAT 或稽核。文件深度依風險，不無差別填滿。
