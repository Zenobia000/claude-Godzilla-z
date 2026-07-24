# 產品開發流程使用說明書

> **版本：** v3.0 | **更新：** 2026-07-24 | **狀態：** 活躍

## 1. 使用原則

- **用問題管理文件：** 文件是降低誤解、支援決策、可驗收的同步工具，不是交付物。不能減少下一次返工的文件就別寫。
- **決策分兩類：** **需求決策**（優先序、範圍、里程碑、Gate、業務驗收）由產品 owner 拍板，落在 Excel B 區 / [`18 需求決策紀錄`](../01_requirements/requirement_decision_record.md)；**工程決策**（架構、契約、測試設計）由工程與 AI 協作。兩者之間是硬邊界，owner 未核准需求決策前不進 `/specify`。
- **來源先行：** 先確認 Excel、訪談、既有文件與程式碼的 owner。
- **欄位級 SSOT：** 同一資訊只有一個人工維護來源；其他載體是投影或索引。
- **風險裁剪：** 建立協作與驗收真正需要的文件，不為了完整而填模板。
- **小步交付：** 以穩定 ID 串接需求、驗收、設計、程式碼、測試與證據。
- **狀態分離：** Requirement、Code reality、Verification、Release 不共用一個狀態。
- **降認知負載：** 看板（角色追蹤 Excel）給眼睛掃、docs 給訂版；AI 更新結構化欄位與 docs，回報只給短 delta，不倒大段說明，減少文件切換與注意力耗散。見 [workbook-guide](../../docs/document-system/workbook-guide.md)。
- **思考模式（速通 vs 深思）：** 低難度/雛形用速通（AI 給推薦選項、你快選）；架構判斷與商業決策這兩個成長標的用深思（AI 只 provoke、你親自判斷並記錄理由）。雛形不前置法規/權限的過度分析，先雛形→打掉→重構迭代。見 [`.claude/rules/thinking-boundary.md`](../../.claude/rules/thinking-boundary.md)。

角色縮寫：Business / PM / Product / BA / ARCH / DEV / QA / SEC / SRE / OPS

## 2. 工作入口

```mermaid
flowchart LR
    A[Excel／訪談／舊系統] --> B[/intake]
    B --> C[/specify]
    C --> D[/deliver]
    D --> E[/verify]
    E -->|規格缺口| C
    E -->|實作缺陷| D
```

| Action | 目的 | 人類控制點 |
|---|---|---|
| `/intake` | 唯讀盤點來源、建立來源座標與需求候選 | 解決衝突、核准需求 |
| `/specify` | 裁剪模板，產生必要的工程契約 | 核准 PRD／BDD／ADR／設計 |
| `/deliver` | 實作一個已核准垂直切片 | 外部操作與 scope change 另行授權 |
| `/verify` | 用實際命令、測試與 trace 證據判定 | 接受風險、退回規格或實作 |

## 3. Profile 選擇

| 條件 | Fast | Product | Governed |
|---|:---:|:---:|:---:|
| 單一 bug、小功能、可逆實驗 | ✓ | | |
| 一般產品功能、跨模組 | | ✓ | |
| 多團隊、外部契約、正式 UAT | | | ✓ |
| 個資、法規、安全或不可逆遷移 | | | ✓ |
| 正式 on-call、高可用、稽核 | | | ✓ |

Profile 可以升級；高風險子範圍不可因整體專案是 MVP 就省略必要設計或證據。

## 4. Fast Track

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

## 5. Product Track

| 階段 | 必要產出 | Gate |
|---|---|---|
| Intake | 來源登錄、REQ、衝突與待確認 | Product/Business 核准範圍 |
| Specify | Lean PRD、BDD、受影響 SAD／API／資料契約 | 行為可驗收、重要決策已處理 |
| Deliver | 一個垂直切片、測試與必要文件更新 | 沒有偷改核准範圍 |
| Verify | build/type/lint/test/security/trace 的適用證據 | 阻擋問題關閉或明確接受 |

## 6. Governed Track

在 Product Track 之上，依 [`artifact-map.md`](../../docs/document-system/artifact-map.md) 選用：

- 文件管制、SRS/NFR、SAD/SDS、ADR、API/Event/DB 契約
- WBS、RACI、Change Request
- Test Plan/Cases、Traceability、SIT/UAT
- Deployment、Runbook、Monitoring、Release evidence
- Excel B/E preservation、完整追溯與稽核

Word 指南是文件 catalog，VibeCoding 是填寫格式，正式專案文件才是工程契約。

## 7. Excel 與工程文件

| 區域 | Owner | 行為 |
|---|---|---|
| B — Business-owned | Business／Product／PM | 人工維護，生成不得覆寫 |
| E — Evidence-owned | QA／UAT／Release | 依穩定 ID 無損合併 |
| G — Generated contract | 工程文件／程式碼 | 由 canonical source 重建 |
| D — Derived | 公式／生成器 | 唯讀、可重算 |

這個啟動寶不隨附 Excel 產生器；B/E/G/D 是你在**專案自己的活頁簿**裡組織欄位所有權的 pattern。需求決策（B 區）以 [`18 需求決策紀錄`](../01_requirements/requirement_decision_record.md) 為權威。若專案自建產生器投影 G/D，生成欄不得覆寫 B/E，且在 preservation-safe round-trip 完成前不當雙向 SSOT。

## 8. Gate 判定

不要用固定「文件完成度 90%」或通用覆蓋率取代專案風險判斷。每個 Gate 應回答：

- 哪些 REQ／AC／Scenario 在範圍內？
- 適用的驗證命令是什麼，是否實際執行？
- 需求、程式碼、驗證與發布狀態各是什麼？
- 證據在哪裡，誰核准？
- 哪些項目未執行、阻擋或接受風險？

只有證據支持的 gate 才能標記 PASS。

## 9. 文件選用矩陣

不是每個專案都建立每一份文件。以「團隊現在缺什麼共識」對應要補的文件：

| 情境／缺口 | 最低必要 | 建議補充 | 一開始先不做 |
|---|---|---|---|
| MVP、可逆、單團隊 | 18 需求決策、02 PRD、03 BDD | 04 ADR（僅重大決策）| SDS、完整 SIT/UAT |
| 前後端分工 | + 12 前端架構、17 前端 IA | 06 API 契約 | Design System 全套 |
| 企業流程／多系統整合 | + 05 SAD、06 API、SRS/NFR | 04 ADR、DB 設計 | — |
| AI／不確定性產品 | + 03 BDD 邊界場景、13 安全 | 評估與回歸集 | — |
| 客戶驗收／正式上線 | + 07 測試、UAT、14 部署 | Runbook、Monitoring | — |

三階段文件組合（對應 Fast/Product/Governed）：**MVP ≈ 9 份、Pilot ≈ 13 份、Enterprise ≈ 27 份**；深度依風險升級，見 [artifact-map.md](../../docs/document-system/artifact-map.md)。

## 10. 命名規範

檔名帶語意與版本，讓人不開檔也能判斷內容與時序：

```
ADR-001-use-kafka-for-event-stream.md
openapi-work-order-v1.yaml
UAT_WorkOrder_Pilot_ClientA_20260701.xlsx
DEC-001-line-intake-reliability.md   # 需求決策可獨立成檔時
```

- 正式 ID 前綴不可重用；取消保留 tombstone。
- 日期用 `YYYYMMDD` 或 `YYYY-MM-DD`；版本用 `vN`。

## 11. 反模式與完成度檢查

上線或提交前，對照常見反模式（表面現象 → 真正問題 → 修正）：

| 表面現象 | 真正問題 | 修正 |
|---|---|---|
| 設計只給 Figma | 缺狀態與互動規格 | 補 UI/Interaction Spec（12/17）|
| 優先序/範圍由 AI 或規則自動判 | 需求決策沒交還 owner | 回 18 需求決策紀錄由 owner 簽核 |
| 一個「狀態」欄想代表全部 | Requirement/Code/Verify/Release 混用 | 拆四個狀態軸 |
| 文件填滿但沒人讀 | 為完整而寫，非為共識 | 依風險裁剪 |
| 決策理由只在對話裡 | 無法回查為什麼 | 寫 ADR 或決策沿革 |

完成度檢查（每個 Gate）：

- [ ] 範圍內的需求決策已由 owner 核准（18 需求決策紀錄）。
- [ ] 適用的驗證命令已實際執行，有證據。
- [ ] 四個狀態軸分別標記，未混用。
- [ ] 追溯鏈無孤兒 ID，B/E 欄位未被生成覆寫。

## 12. 模板選用

完整清單與 profile 對照見 [INDEX.md](../INDEX.md)。使用時只複製必要章節；模板中的範例值不是專案政策。
