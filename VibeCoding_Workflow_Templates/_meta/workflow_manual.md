# 產品開發流程使用說明書

> **更新：** 2026-07-27 | **狀態：** 活躍 | 版本隨 repo（沿革見 [CHANGELOG](../../CHANGELOG.md)）
> **Owner:** 模板庫維護者
> **語域:** L2（橋接）
> **定位:** 怎麼跑流程、選階段、過 Gate 的手冊；模板格式規範見 [template_standard](./template_standard.md)。

## 目錄

- [1. 使用原則](#1-使用原則)
- [2. 工作入口](#2-工作入口)
- [3. 階段選擇](#3-階段選擇)
- [4. 雛型期（心流優先）](#4-雛型期心流優先)
- [5. Pilot／客戶驗證](#5-pilot客戶驗證)
- [6. 企業級（Enterprise）](#6-企業級enterprise)
- [7. 追蹤簿與欄位所有權](#7-追蹤簿與欄位所有權)
- [8. Gate 判定](#8-gate-判定)
- [9. 文件選用矩陣](#9-文件選用矩陣)
- [10. 命名規範](#10-命名規範)
- [11. 反模式與完成度檢查](#11-反模式與完成度檢查)
- [12. 模板選用](#12-模板選用)
- [13. 追溯](#13-追溯)

## 1. 使用原則

- **用問題管理文件：** 文件是降低誤解、支援決策、可驗收的同步工具，不是交付物。不能減少下一次返工的文件就別寫。
- **決策分兩類：** **需求決策**（優先序、範圍、里程碑、Gate、業務驗收）由產品 owner 拍板，落在需求追蹤簿 `requirements_tracker.xlsx`（①需求決策、③Gate）；**工程決策**（架構、契約、測試設計）由工程與 AI 協作。兩者之間是硬邊界；Pilot 階段起，owner 未核准需求決策前不進 `/specify`（見 §8 硬閘）。
- **來源先行：** 先確認 Excel、訪談、既有文件與程式碼的 owner。
- **欄位級 SSOT：** 同一資訊只有一個人工維護來源；其他載體是投影或索引。
- **風險裁剪：** 建立協作與驗收真正需要的文件，不為了完整而填模板。
- **小步交付：** 以穩定 ID 串接需求、驗收、設計、程式碼、測試與證據。
- **狀態分離：** Requirement、Code reality、Verification、Release 不共用一個狀態。
- **降認知負載：** 看板（三個角色追蹤簿）給眼睛掃、docs 給訂版；AI 更新結構化欄位與 docs，回報只給短 delta，不倒大段說明，減少文件切換與注意力耗散。見 [workbook-guide](../../docs/document-system/workbook-guide.md)。
- **思考模式（速通 vs 深思）：** **預設速通**——AI 給推薦選項、你快選；你喊「深思」才慢下來（架構判斷與商業決策想成長時），AI 改成只 provoke、你親自判斷並記錄理由。雛形不前置法規/權限的過度分析，先雛形→打掉→重構迭代。見 [`.claude/rules/thinking-boundary.md`](../../.claude/rules/thinking-boundary.md)。

角色縮寫：Business / PM / Product / BA / ARCH / DEV / QA / SEC / SRE / OPS

## 2. 工作入口

主線是 `/intake → /specify → /deliver → /verify`（`/verify` 發現規格缺口退回 `/specify`、實作缺陷退回 `/deliver`）；流程圖唯一權威見 [.claude/WORKFLOW.md](../../.claude/WORKFLOW.md)。

| Action | 目的 | 人類控制點 |
|---|---|---|
| `/intake` | 唯讀盤點來源、建立來源座標與需求候選 | 解決衝突、核准需求 |
| `/specify` | 裁剪模板，產生必要的工程契約 | 核准 PRD／BDD／ADR／設計 |
| `/deliver` | 實作一個已核准垂直切片 | 外部操作與 scope change 另行授權 |
| `/verify` | 用實際命令、測試與 trace 證據判定 | 接受風險、退回規格或實作 |

### 使用範例

Action 是**階段性入口**，不是每次互動的必經流程——雛型期直接對話迭代，要「收斂、正規化、簽核、判定」時才呼叫。

```text
# 雛型期：不用 Action，直接聊
幫我做一個派工排程的雛型，先用 SQLite，能排能看就好
在 ①需求決策補一列 DEC-003：工地主任可以拖拉調整派工順序

# /intake：有來源要正規化、或雛型結論要收斂成需求候選
/intake docs/客戶訪談_0712.xlsx
/intake 上禮拜跟客戶聊的三個功能想法，幫我整理成需求候選

# /specify：owner 在 ①核准後，把業務語言翻成工程契約（FR/ACPT/受影響契約）
/specify DEC-003
/specify M1 範圍內所有已核准的 DEC

# /deliver：照已核准規格做一個垂直切片（實作＋測試＋文件同 commit）
/deliver FR-007

# /verify：用證據判定完成；證據進 qa_tracker ②執行證據
/verify FR-007
/verify M1 全範圍        # Gate 前總驗，結果供 ③Gate 簽核
```

典型節奏：雛型期自由迭代 → 客戶要試用 → `/intake` 收斂成 `DEC-*` → owner 在 ① 標「已核准」→ `/specify M1` → 逐條 `/deliver` → `/verify M1` → ③Gate 簽核 → 進 Pilot。

## 3. 階段選擇

文件深度跟著**開發階段**走，不是跟著模板清單走。實務上大多數專案從模糊需求開始，靠雛型一步步迭代出來；文件在階段升級時才補齊，不在起步時前置。

| 階段 | 情境 | 文件姿態 |
|---|---|---|
| **雛型（Prototype）** | 模糊需求、快速迭代、可逆實驗 | 只維護核心骨架；自由對話迭代，Action Skills 是可選入口、不是關卡 |
| **Pilot／客戶驗證** | 給真實使用者驗、要對外簽核 | 補齊 Pilot 文件組（§5）；`/specify` 硬閘生效 |
| **企業級（Enterprise）** | 多團隊、法規、正式 on-call、稽核 | 完整治理（§6）|

階段只升不降；高風險子範圍（個資、法規、不可逆遷移）一出現，就按企業級對待**該子範圍**，不因整體是雛型而豁免。

## 4. 雛型期（心流優先）

雛型期的目標是驗證想法，不是留文件。**允許直接和 AI 對話迭代，不必每一步走 `/intake → /specify`**；先雛型 → 打掉 → 重構是正常路徑（見 [thinking-boundary](../../.claude/rules/thinking-boundary.md)）。唯二不變量：

- **ID 骨架**：每個要保留的方向在需求追蹤簿 ①需求決策留一列 `DEC-*`（一句 VOC＋狀態），之後升級 Pilot 時追溯不用重建。
- **回不了頭的取捨寫 ADR**：只記重大決策，一段話即可。

```mermaid
flowchart LR
    A[問題／來源] --> B[驗收或重現]
    B --> C[必要決策]
    C --> D[最小實作]
    D --> E[回歸證據]
```

最低集合：

- 問題、影響、來源座標或 bug 重現
- 一個可觀察的驗收行為
- 只有在重要取捨時才建立 ADR
- 最小 code/test 變更與實際驗證

## 5. Pilot／客戶驗證

進入給真實使用者驗證、需要對外簽核時，依缺口從 Pilot 文件組補齊（不是 15 份全建）：

> brd、prd、srs、ux_research_and_journey、information_architecture、ui_spec、sad、adr、api_spec＋openapi.yaml、db_design、lld、test_plan、uat_plan、deployment_and_operations、runbook

| 階段 | 必要產出 | Gate |
|---|---|---|
| Intake | 來源登錄、REQ、衝突與待確認 | Product/Business 核准範圍 |
| Specify | Lean PRD、BDD、受影響 SAD／API／資料契約 | 行為可驗收、重要決策已處理 |
| Deliver | 一個垂直切片、測試與必要文件更新 | 沒有偷改核准範圍 |
| Verify | build/type/lint/test/security/trace 的適用證據 | 阻擋問題關閉或明確接受 |

## 6. 企業級（Enterprise）

在 Pilot 之上，依 [`artifact-map.md`](../../docs/document-system/artifact-map.md) 選用：

- 文件管制、SRS／NFR、SAD／SDS、ADR、API／Event／DB 契約
- WBS、RACI、Change Request
- Test Plan／Test Cases、Traceability、SIT／UAT
- Deployment、Runbook、Monitoring、Release evidence
- 追蹤簿人工欄位保存、完整追溯與稽核

Word 指南是文件 catalog，VibeCoding 是填寫格式，正式專案文件才是工程契約。企業級文件多數**未內建模板**（模板庫收斂到 Pilot 核心 15 份）；進企業級時依 Word 指南增建，git 歷史有可回收的舊版。

## 7. 追蹤簿與欄位所有權

追蹤層是三個角色追蹤簿（各放在 owner 的資料夾），以 ID 骨幹 `REQ/DEC-* → FR/NFR-* → TC/QTM-*` 串連；訂版層是 docs 與模板。用法見 [workbook-guide](../../docs/document-system/workbook-guide.md)。

| 追蹤簿 | Owner | 位置 |
|---|---|---|
| 需求追蹤 | PM／BA | `../01_requirements/requirements_tracker.xlsx` |
| 工程追蹤 | 架構師 | `../03_architecture/engineering_tracker.xlsx` |
| 測試追蹤 | QA | `../05_qa/qa_tracker.xlsx` |

所有權以檔為單位：一檔一個 owner，只有 owner 的角色人工維護；AI 只依穩定 ID 更新結構化欄位並回報短 delta。追蹤簿只放骨架（ID＋狀態＋一句話＋連結），細節在 docs 訂版層。

需求決策的權威是 `requirements_tracker.xlsx` **①需求決策**（owner 拍板優先序、範圍、里程碑、業務驗收與核准）；**③Gate** 記里程碑簽核，**②決策沿革** 記變更與原因。深思模式的長決策理由寫 ADR 或 PRD 附註，不塞追蹤簿。本啟動包不隨附 Excel 產生器；若專案自建生成活頁簿，生成流程不得覆寫人工維護欄位，且在 preservation-safe round-trip 完成前只當發布快照、不當雙向 SSOT。

## 8. Gate 判定

不要用固定「文件完成度 90%」或通用覆蓋率取代專案風險判斷。每個 Gate 應回答：

- 哪些 REQ／AC／Scenario 在範圍內？
- 適用的驗證命令是什麼，是否實際執行？
- 需求、程式碼、驗證與發布狀態各是什麼？
- 證據在哪裡，誰核准？
- 哪些項目未執行、阻擋或接受風險？

只有證據支持的 gate 才能標記 PASS。

### `/specify` 放行檢查（硬閘，Pilot 階段起生效）

雛型期此閘退化為「①需求決策有對應 `DEC-*` 骨架列」即可，不打斷迭代。進入 Pilot 後，`/specify` 啟動前逐項確認：

- [ ] 目標需求在 ①需求決策有對應列，且 `核准 = 已核准`。
- [ ] 該列有 Owner 與更新日期（owner 簽核）。
- [ ] 優先序、範圍、里程碑非空，且不是未經接受的系統自動值。
- [ ] 若跨里程碑 Gate，③Gate 對應列的決策為 `核准`。
- [ ] 商業例外／紅線已標記，工程契約需承接。

任一項不成立：**停止，退回 owner 決策**，不得由 AI 代填後續。需求決策不可由規則或 AI 自動衍生；系統建議值必須由 owner 覆寫或明確接受才算數。

## 9. 文件選用矩陣

不是每個專案都建立每一份文件。以「團隊現在缺什麼共識」對應要補的文件（模板見 [INDEX.md](../INDEX.md)）：

| 情境／缺口 | 最低必要 | 建議補充 | 一開始先不做 |
|---|---|---|---|
| 雛型、可逆、單團隊 | 需求追蹤簿骨架、prd 精簡段 | adr（僅重大決策）| 完整 SRS、SIT/UAT |
| 前後端分工 | + ui_spec、openapi.yaml | ux_research_and_journey | Design System 全套 |
| 企業流程／多系統整合 | + brd、srs、sad、api_spec | db_design | — |
| AI／不確定性產品 | + prd 的邊界場景與驗收條件 | 評估與回歸集 | — |
| 客戶驗收／正式上線 | + test_plan、uat_plan、deployment_and_operations、runbook | — | — |

三階段文件組合：**雛型＝追蹤簿骨架＋prd 精簡＋必要 ADR、Pilot ≈ 15 份、企業級依 artifact-map 全量選用**；深度依風險升級，見 [artifact-map.md](../../docs/document-system/artifact-map.md)。

## 10. 命名規範

檔名帶語意與版本，讓人不開檔也能判斷內容與時序：

```
ADR-001-use-kafka-for-event-stream.md
openapi-work-order-v1.yaml
db-schema-work-order-v1.md
runbook-api-latency-high.md
UAT_WorkOrder_Pilot_ClientA_20260701.xlsx
DEC-001-line-intake-reliability.md   # 需求決策可獨立成檔時
```

- 正式 ID 前綴不可重用；取消保留 tombstone。
- 日期用 `YYYYMMDD` 或 `YYYY-MM-DD`；版本用 `vN`。
- 哪些模板可多實例、分支 key 是什麼，見 [INDEX 實例化規則](../INDEX.md) 與 [template_standard §2](./template_standard.md)。

## 11. 反模式與完成度檢查

上線或提交前，對照常見反模式（表面現象 → 真正問題 → 修正）：

| 表面現象 | 真正問題 | 修正 |
|---|---|---|
| 設計只給 Figma | 缺狀態與互動規格 | 補 ui_spec（§5 States、§6 Interaction）與 Design Handoff |
| 優先序/範圍由 AI 或規則自動判 | 需求決策沒交還 owner | 回 ①需求決策由 owner 簽核 |
| 一個「狀態」欄想代表全部 | Requirement/Code/Verify/Release 混用 | 拆四個狀態軸 |
| API 邊做邊改 | 缺契約 | 先定 openapi.yaml，mock 先行 |
| 上線靠英雄 | 部署知識沒沉澱 | 補 deployment_and_operations、runbook |
| 文件填滿但沒人讀 | 為完整而寫，非為共識 | 依風險裁剪 |
| 決策理由只在對話裡 | 無法回查為什麼 | 寫 ADR 或決策沿革 |

完成度檢查（每個 Gate）：

- [ ] 範圍內的需求決策已由 owner 核准（①需求決策 `核准 = 已核准`；雛型期骨架列即可）。
- [ ] 適用的驗證命令已實際執行，有證據。
- [ ] 四個狀態軸分別標記，未混用。
- [ ] 追溯鏈無孤兒 ID，追蹤簿人工欄位未被生成覆寫。

## 12. 模板選用

完整清單與階段對照見 [INDEX.md](../INDEX.md)。使用時只複製必要章節；模板中的範例值不是專案政策。

## 13. 追溯

- 上游：[golden-rules](../../.claude/rules/golden-rules.md)、[thinking-boundary](../../.claude/rules/thinking-boundary.md)、[architecture.md](../../docs/document-system/architecture.md)
- 下游：全部模板（格式由 [template_standard](./template_standard.md) 約束）、四個 Action Skills
