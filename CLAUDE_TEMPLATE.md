<!-- CLAUDE_CODE_PROJECT_TEMPLATE_V6 -->

# Claude Code 專案啟動範本

> **模式：** 人類主導、文件驅動、證據閉環

## 啟動方式

有既有需求訪談表、Excel、合約或舊系統文件時：

```text
/intake [來源檔案或資料夾]
```

只有口頭構想時，先以 `/intake` 進行訪談並建立來源登錄；不要直接生成完整文件套件或開始實作。

## Phase 1：來源與權威

確認：

1. 專案名稱、目的與主要利害關係人
2. 原始來源位置（Excel／Word／會議紀錄／舊系統）
3. 哪些欄位由業務、PM、SA、RD、QA 負責
4. 哪些內容已核准，哪些只是草稿或推論
5. 資料敏感性、不可寫入來源與外部操作限制

Excel 來源必須保留：

```yaml
source_file: path/to/interview.xlsx
sheet: 業務需求
row: 12
cell_range: B12:H12
source_id: SRC-0012
requirement_id: REQ-0042
approval_status: Draft
```

## Phase 2：選擇文件深度

| 階段 | 適用情境 | 最小文件 |
|---|---|---|
| 雛型（Prototype） | 模糊需求、快速迭代、實驗 | 追蹤簿骨架列、驗收或重現、必要決策、測試證據 |
| Pilot／客戶驗證 | 給真實使用者驗、要簽核 | BRD/PRD/SRS、UX/UI、SAD/ADR、API/DB、Test/UAT、Deployment/Runbook（依缺口裁剪） |
| 企業級（Enterprise） | 法規、多團隊、高風險 | 文件管制、NFR、SDS、SIT/UAT、Monitoring、Change Request |

企業文件如何選用：`software_development_documentation_guide_zh_tw.docx`（治理智慧已萃取進 `VibeCoding_Workflow_Templates/_meta/workflow_manual.md`）

工程文件如何填寫：`VibeCoding_Workflow_Templates/`

需求決策：`VibeCoding_Workflow_Templates/01_requirements/requirements_tracker.xlsx` ①需求決策（owner 拍板；③Gate 簽核）

## Phase 3：工程化規格

```text
/specify [範圍或 REQ ID]
```

只建立當前交付需要的文件，並滿足：

- 需求、驗收、設計、測試使用穩定 ID 串接
- 假設與待確認事項不混入核准內容
- AS-BUILT、PARTIAL、TO-BE 分開
- 新決策才新增 ADR，既有決策以連結引用
- 同一欄位只有一個權威 owner

## Phase 4：垂直切片交付

規格可驗收後：

```text
/deliver [FR/NFR/SCN 範圍]
```

一次完成一個可測的垂直切片。細部 API、UI、測試、安全、除錯或架構能力由 `/deliver` 按任務載入對應 Skill；不需要手動串接十幾個 Commands。

## Phase 5：證據關卡

```text
/verify [範圍]
```

完成報告至少包含：

- 實際執行的驗證與結果
- `REQ → FR/NFR → ACPT/SCN → code → test → evidence` 對應
- 未執行項目、阻塞與殘餘風險
- Requirement、Code reality、Verification 三種獨立狀態

## 建議生成的專案指令

目標專案的 `CLAUDE.md` 應短小，只記錄該專案特有資訊：

```markdown
# [PROJECT_NAME]

## Purpose
[產品／系統目的]

## Source authority
- 業務需求與核准：[路徑與 owner]
- 工程契約：[路徑與 owner]
- 程式碼現況：[路徑]
- 測試與證據：[路徑]

## Technical context
- Stack: [LANGUAGE / FRAMEWORK]
- Build: [COMMAND]
- Test: [COMMAND]
- Lint / typecheck: [COMMAND]

## Project constraints
- [只有此專案才成立的限制]

## Workflow
使用 `/intake → /specify → /deliver → /verify`（想法太大時先走 `/wayfind`），並遵循 `.claude/rules/golden-rules.md`。
```

不要把通用 coding style、固定覆蓋率、整套 Git 流程或所有 Skill 內容複製進專案 `CLAUDE.md`。

<!-- CLAUDE_CODE_INIT_END -->
