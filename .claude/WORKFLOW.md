# 文件驅動開發工作流

本模板不再用 Hook 維護第二套 TaskMaster 狀態。開發主線由四個可手動觸發的 Action Skills 串接：

```text
Excel／訪談／既有系統
          ↓
       /intake
          ↓
來源登錄＋需求候選＋待確認事項
          ↓
       /specify
          ↓
PRD／BDD／SAD／ADR／Traceability
          ↓
       /deliver
          ↓
可驗收的垂直切片＋程式碼＋測試
          ↓
       /verify
          ↓
證據、缺口與真實完成狀態
```

## 這個 repo 的定位

這是**文件驅動開發的啟動寶（startup kit）**：只放可重用的模板、`rules/` 與 `skills/`，**不放任何專案的 Excel 或需求資料**。每次開新專案把它當基底，實際產出長在你的專案裡。

流程最上游的「Excel／訪談／既有系統」是你**每個專案自己帶進來的輸入**（需求訪談表、業務 Excel、舊系統文件），住在你的實際專案，不在這個 repo。你在專案裡維護的需求決策，權威是 `requirements_tracker.xlsx` ①需求決策（③Gate 簽核、②決策沿革記變更）。先前隨附的 SmartLock 四本 Excel 只是一份「填好的範例」，已抽離；現行追蹤層是三個角色追蹤簿——**移除的是範例，不是 Excel 這個概念**。

## 四個入口

| 入口 | 何時使用 | 主要輸入 | 完成條件 |
|---|---|---|---|
| `/intake` | 新專案、需求訪談表、Excel、既有資料進件 | 原始來源與權威 owner | 來源座標、穩定 ID、①需求決策已種好 `DEC-*` 待 owner 拍板 |
| `/specify` | 將白話需求工程化 | **已由 owner 核准的需求決策**、驗收、限制 | 只產生當前階段必要的工程契約，ID 互相連接 |
| `/deliver` | 規格已足以實作 | 核准範圍與驗收標準 | 一個可測的垂直切片完成，未偷改範圍 |
| `/verify` | 任務、PR、里程碑或上線前 | 變更、驗收標準、測試環境 | 實際證據支持狀態；未驗證部分清楚標示 |

四個 Skill 設為手動呼叫，是為了保留人類決定工作階段與變更範圍的控制權。它們會視需要載入除錯、測試、安全、API、UI 或架構等能力 Skill。

**需求決策 vs 工程決策的硬邊界**：優先序、範圍、里程碑、Gate、業務驗收屬**需求決策**，由產品 owner 於 `requirements_tracker.xlsx` ①需求決策拍板（③Gate 簽核），AI 不得自動衍生。Pilot 階段起，`/specify` 在 owner 簽核前不得把需求工程化；雛型期只需骨架列，不打斷迭代。這條線與 [`rules/language-register.md`](rules/language-register.md) 的 L1（業務）→ L2（中介）→ L3（工程）分水嶺是同一條。

## 文件深度

不要一開始生成整套企業文件。文件深度跟著**開發階段**走——實務上多數專案從模糊需求靠雛型迭代出來，文件在階段升級時才補齊：

### 雛型（Prototype）

模糊需求、快速迭代、可逆實驗。心流優先：允許直接對話迭代，Action Skills 是可選入口、不是關卡。

- 來源／問題與影響
- 可驗收行為或重現步驟
- 需求追蹤簿 ①需求決策留 `DEC-*` 骨架列
- 最小設計說明（回不了頭的決策才建 ADR）
- 實作、回歸測試與證據

### Pilot／客戶驗證

給真實使用者驗、需要對外簽核。`/specify` 硬閘自此生效。依缺口補齊 Pilot 文件組：

- BRD／PRD／SRS、BDD／驗收
- UX Flow／UI Spec
- SAD／ADR、API 契約（openapi.yaml）、DB 設計
- Test Plan／UAT Plan、Deployment、Runbook

### 企業級（Enterprise）

法規、多團隊、高可用、稽核。

- 文件管制與核准
- NFR、SDS、介面與事件契約
- SIT／UAT、RACI、Monitoring、變更與證據紀錄
- 權威矩陣與完整追溯

企業文件全景請參考根目錄 Word 指南；可直接填寫的格式請使用 `VibeCoding_Workflow_Templates/`。

## Excel 與 Markdown

Excel 是業務／PM 的視覺治理介面，Markdown 是工程契約與版本差異介面。兩者不是互相取代：

1. 一檔一個 owner：三個角色追蹤簿的分工見 `docs/document-system/workbook-guide.md`。
2. 保留來源檔、sheet、row、cell/range 與來源列 ID。
3. 用穩定的 `SRC-* → REQ-* → FR/NFR → ACPT-* → SCN-* → TC-*` 串接；`AC-*` 保留給既有架構選項，不作驗收 ID。
4. 自動生成只覆寫標示為 generated 的區域，不覆寫人工核准或標註。
5. 同步後執行 ID、連結、驗收與證據完整性檢查。

追蹤層是三個**角色追蹤簿**（需求／工程／測試，各一個 owner），用法與欄位見 [`docs/document-system/workbook-guide.md`](../docs/document-system/workbook-guide.md)；所有權模型與自建生成活頁簿的注意事項見 [`docs/document-system/architecture.md`](../docs/document-system/architecture.md)。新專案從 owner 拍板的需求決策起手，不必複製任何特定領域的實例規模。

## 協作模型：Rules × Skills × Agents

三者不是各自獨立的東西，而是三層疊在一起同時運作：

- **Rules（恆定約束層）**：`rules/` 的 [golden-rules](rules/golden-rules.md)、[git-workflow](rules/git-workflow.md)、[language-register](rules/language-register.md) 約束**每一步**，不因階段或 Skill 改變。任何 Skill 或 Agent 的產出都不得違反；來源與 Rules 衝突時指出並以權威來源為準。
- **Skills（方法／編排層）**：四個 Action Skill（`/intake→/verify`）是入口，決定當前階段做什麼，並依任務語意載入能力 Skill（`sunnydata-*`／`community-*`，如 debugging、testing、security、api-design）。能力 Skill 是「怎麼做」的知識，用完即走、不常駐 context。
- **Agents（執行邊界層）**：由主 Agent（跟著 Skill 跑時）在需要**隔離 context／限制工具權限／安全平行／獨立第二意見**時，透過 Task 委派。Agent 是邊界，不是另一套流程——不在 Agent prompt 複製 Skill 的方法。

一句話：**Skill 決定做什麼、Rule 約束怎麼做才合規、Agent 是需要隔離時的執行容器。**

### 階段 × 該考慮的 Agent

預設由主 Agent 直接做；只有隔離確有價值才委派，不為每件事都開 Agent。

| 階段 | 主要 Skill | 典型可委派的 Agent |
|---|---|---|
| `/intake` | intake | `documentation-specialist`（大型來源正規化）|
| `/specify` | specify | `architect`（架構第二意見）|
| `/deliver` | deliver | `test-automation-engineer`、`build-error-resolver` |
| `/verify` | verify | `code-quality-specialist`、`security-infrastructure-auditor`、`end-to-end-validation-specialist` |
| 部署規劃 | 能力 Skill | `deployment-expert` |

### 一個走查（新增一個付款 API）

1. `/intake` 讀你專案的 Excel／訪談（L1 業務語域；Rules 要求來源可追溯），把需求種進 ①需求決策，等 owner 拍板優先序與範圍。
2. owner 在 ①需求決策簽核 → `/specify` 過硬閘，在 L2 把需求翻成 FR/NFR、ACPT 與 API 契約；架構有疑慮時委派 `architect` 拿第二意見，載入 `sunnydata-api-design`。
3. `/deliver` 實作垂直切片（L3 工程語域），載入 `sunnydata-testing`；build 壞了委派 `build-error-resolver`。
4. `/verify` 跑實際測試與 trace，委派 `code-quality-specialist`、`security-infrastructure-auditor` 做隔離審查，用證據判定。

全程 git-workflow 約束 commit／push／文件同步，language-register 約束每份產出的語域。

## 狀態與證據

至少分開記錄：

- Requirement／Document：Draft、Review、Approved、Deprecated
- Code reality：TO-BE、PARTIAL、AS-BUILT
- Verification：Not run、Failed、Passed、Blocked
- Evidence：命令、報告、檔案或外部紀錄位置

只有最後一項有實際證據，才能宣告驗證通過。
