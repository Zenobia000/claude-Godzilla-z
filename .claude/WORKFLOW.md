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

## 四個入口

| 入口 | 何時使用 | 主要輸入 | 完成條件 |
|---|---|---|---|
| `/intake` | 新專案、需求訪談表、Excel、既有資料進件 | 原始來源與權威 owner | 來源座標、穩定 ID、需求決策紀錄已種好待 owner 拍板 |
| `/specify` | 將白話需求工程化 | **已由 owner 核准的需求決策**、驗收、限制 | 只產生當前階段必要的工程契約，ID 互相連接 |
| `/deliver` | 規格已足以實作 | 核准範圍與驗收標準 | 一個可測的垂直切片完成，未偷改範圍 |
| `/verify` | 任務、PR、里程碑或上線前 | 變更、驗收標準、測試環境 | 實際證據支持狀態；未驗證部分清楚標示 |

四個 Skill 設為手動呼叫，是為了保留人類決定工作階段與變更範圍的控制權。它們會視需要載入除錯、測試、安全、API、UI 或架構等能力 Skill。

**需求決策 vs 工程決策的硬邊界**：優先序、範圍、里程碑、Gate、業務驗收屬**需求決策**，由產品 owner 於 Excel B 區／[`18 需求決策紀錄`](../VibeCoding_Workflow_Templates/18_requirement_decision_record.md) 拍板，AI 不得自動衍生。`/specify` 在 owner 簽核前不得把需求工程化。這條線與 [`rules/language-register.md`](rules/language-register.md) 的 L1（業務）→ L2（中介）→ L3（工程）分水嶺是同一條。

## 文件深度

不要一開始生成整套企業文件。依交付風險選擇：

### Fast Track

適合單一 bug、小型功能或短期實驗。

- 來源／問題與影響
- 可驗收行為或重現步驟
- 最小設計說明（需要決策才建 ADR）
- 實作、回歸測試與證據

### Product Track

適合一般產品功能或跨模組變更。

- PRD、BDD／驗收
- 受影響的 SAD／API／資料契約
- 垂直切片與 Traceability
- 整合測試與發布準備

### Governed Track

適合客戶驗收、法規、高風險或企業治理。

- Excel 文件管制與核准
- SRS／NFR、SAD／SDS、ADR、介面與資料契約
- SIT／UAT、RACI、Runbook、變更與證據紀錄
- 權威矩陣與完整追溯

企業文件全景請參考根目錄 Word 指南；可直接填寫的格式請使用 `VibeCoding_Workflow_Templates/`。

## Excel 與 Markdown

Excel 是業務／PM 的視覺治理介面，Markdown 是工程契約與版本差異介面。兩者不是互相取代：

1. 先在 `docs/document-system/architecture.md` 指定欄位 owner。
2. 保留來源檔、sheet、row、cell/range 與來源列 ID。
3. 用穩定的 `SRC-* → REQ-* → FR/NFR → ACPT-* → SCN-* → TC-*` 串接；`AC-*` 保留給既有架構選項，不作驗收 ID。
4. 自動生成只覆寫標示為 generated 的區域，不覆寫人工核准或標註。
5. 同步後執行 ID、連結、驗收與證據完整性檢查。

四本治理活頁簿（規劃書／BOM／驗收控制表／整合測試計畫）是可重用的**視覺治理 pattern**，不是必備清單；欄位 owner、B/E/G/D 分權與需求決策 schema 見 [`docs/document-system/architecture.md`](docs/document-system/architecture.md) 與模板 18。新專案從 owner 拍板的需求決策起手，不必複製任何特定領域的實例規模。

## Subagent

主 Agent 預設完成一般規劃與實作。只有下列情況才委派：

- 大量搜尋或測試輸出需要隔離 context
- 可安全平行的獨立工作
- 需要唯讀架構／安全／Code Review 第二意見
- 需要限制工具或外部操作權限

Agent 是執行邊界，Skill 才是方法與知識；不要在 Agent prompt 再複製一套流程。

## 狀態與證據

至少分開記錄：

- Requirement／Document：Draft、Review、Approved、Deprecated
- Code reality：TO-BE、PARTIAL、AS-BUILT
- Verification：Not run、Failed、Passed、Blocked
- Evidence：命令、報告、檔案或外部紀錄位置

只有最後一項有實際證據，才能宣告驗證通過。
