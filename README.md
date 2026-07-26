<div align="center">

<img src="assets/hero.png" alt="Claude Code Godzilla" width="720" />

# Claude Code Godzilla

**文件驅動、能力按需、證據閉環的 Claude Code 軟體工程生態系。**

[![Version](https://img.shields.io/badge/version-v6.0-blue)]()
[![Claude Code](https://img.shields.io/badge/Claude%20Code-2.1.218+-purple)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

這不是一包要求 AI 機械執行的 prompts，而是一個可帶進新專案的工程能力庫：

- Excel 保留業務、PM、QA 熟悉的視覺對焦與簽核表面。
- Markdown／code-native contracts 保留可 diff、可 review、可供 AI 與 CI 使用的工程契約。
- Skills 保存 Superpowers、UI/UX、架構、測試、安全、除錯與交付實務。
- Rules、Agents、Output Styles、Hooks 只承擔各自必要的執行期責任。

## 核心工作流

```text
Excel／訪談／舊系統
        ↓
     /intake
        ↓
     /specify
        ↓
     /deliver
        ↓
     /verify
        ↓
  實際證據與真實狀態
```

| Action Skill | 用途 |
|---|---|
| `/intake` | 唯讀解析 Excel／需求來源，保存 `file → sheet → row/cell → SRC-ID → REQ-ID` |
| `/specify` | 將核准 REQ 映射成 `FR/NFR → ACPT/SCN`，裁剪 PRD、BDD、SAD、ADR 與 Traceability |
| `/deliver` | 交付一個可驗收垂直切片，按需載入專業 Skills |
| `/verify` | 以 build、type、lint、test、security、trace 證據判定狀態 |

完整流程見 [.claude/WORKFLOW.md](.claude/WORKFLOW.md)。

## Word、VibeCoding 與 Excel 怎麼整合

三者不是互相合併成一份巨型文件，而是不同層：

| 層 | 資產 | 回答的問題 |
|---|---|---|
| 文件 catalog | [Software Development Documentation Guide](software_development_documentation_guide_zh_tw.docx) | 這個風險與組織規模需要哪些文件？ |
| 作業模板 | [VibeCoding Workflow Templates](VibeCoding_Workflow_Templates/INDEX.md) | 選中的工程文件要怎麼寫？ |
| 需求決策 | `VibeCoding_Workflow_Templates/01_requirements/requirements_tracker.xlsx` | owner 於 ①需求決策拍板優先序、範圍、核准；③Gate 簽核；②決策沿革記變更與原因 |
| 正式契約 | 目標專案文件、程式碼、測試 | 實際核准與可執行的內容是什麼？ |

詳細整合設計：

- [文件系統架構](docs/document-system/architecture.md)
- [九層文件分類、模板資料夾與 trace ID](docs/document-system/artifact-map.md)
- [文件系統入口與權威矩陣](docs/document-system/INDEX.md)

### Excel 的關鍵結論

不是「Excel 或 Markdown 誰是唯一真相」，而是一檔一個 owner：三個角色追蹤簿由各自的 owner 人工維護，以 `REQ/DEC-* → FR/NFR-* → TC/QTM-*` 的 ID 骨幹串連，細節放 docs 訂版層（見 [workbook-guide](docs/document-system/workbook-guide.md)）：

| 追蹤簿 | Owner | 內容 |
|---|---|---|
| `requirements_tracker.xlsx` | PM／BA | 需求決策、決策沿革 |
| `engineering_tracker.xlsx` | 架構師 | 規格追溯、模組 BOM |
| `qa_tracker.xlsx` | QA | 測試設計、執行證據 |

需求決策由 owner 在 `requirements_tracker.xlsx` ①需求決策拍板；工程契約由 Markdown 與程式碼承載。生成流程不得覆寫人工維護欄位；自建生成活頁簿在 preservation-safe round-trip 完成前只當發布快照。

## Claude Code 元件邊界

```text
.claude/
├── rules/          1 份 Golden Rules
├── skills/         Action Skills + SunnyData + Community 能力庫
├── agents/         8 個隔離型專業角色
├── output-styles/  1 個純呈現樣式
├── hooks/          基礎模板零註冊；僅 Hook 設計指南
└── statusline*     顯示官方 stdin 與 usage API 用量
```

| 元件 | 現行責任 |
|---|---|
| Rules | 來源、追溯、安全、證據、最小變更等 Golden Rules |
| Skills | 方法、清單、模板路由與可重用能力 |
| Agents | 獨立 context、工具／權限隔離、平行或第二意見 |
| Output Style | 只改回答呈現，不承載 PRD／BDD／TDD 流程 |
| Hooks | 只接受確定、快速、低頻、無隱性狀態的 guardrail |

## Skills 能力庫

除了四個 Action Skills，仍保留完整的按需能力：

- SunnyData：設計、API、UI、測試、除錯、安全、Code Review、架構、基礎設施、分支、研究、平行協作、Skill authoring
- Community：前端設計、React／React Native、效能、a11y、UI design system、Web guidelines

詳見 [.claude/skills/INDEX.md](.claude/skills/INDEX.md)。能力庫不是每個 session 的固定 context，只有任務相關部分會載入。

## 快速開始

最簡單的方式是從此模板建立新 repository，再把需求來源放進專案：

```bash
git clone <your-template-repository> my-project
cd my-project
claude
```

有 Excel 訪談表時：

```text
/intake path/to/requirements.xlsx
```

只有口頭構想時也從 `/intake` 開始，讓 AI 先建立來源登錄與待確認事項。新專案啟動提示見 [CLAUDE_TEMPLATE.md](CLAUDE_TEMPLATE.md)。

個人 MCP 與額外權限放在不入 Git 的本機設定；範例見 [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)。

## Runtime 精簡

v6 退役了：

- Hook 驅動的 TaskMaster prompt 攔截、snapshot 與 timelog
- StatusLine 的工作樹寫入與 session snapshot（憑證探索與 usage API 查詢後於全域版移植時恢復）
- 每個 Subagent 強制產生 context 報告
- 17 個與 Skills 重複的 Commands
- 14 個實際上是工作流程的 Output Styles
- 通用、Planner、TDD、Refactor、Template 等重疊 Agents

Claude Code 原生 Task list 處理暫態工作；PRD、ADR、issue、測試與 evidence 處理長期狀態。

## 驗證與安全基線

- `settings.json` 以 deny 阻擋內建 Read/Edit 存取 `.env`、secrets、credentials；這不攔截 Bash 子程序。在 macOS／Linux／WSL2 可另啟 sandbox，Windows 原生環境則需依 OS／工作區隔離與人工授權控管 shell。
- StatusLine 讀官方 stdin（rate-limit 以 stdin `rate_limits` 優先）、唯讀 Git 查詢與 Anthropic usage API 回退；不寫入工作樹或專案狀態。
- Excel intake 工具只讀 OOXML，測試會驗證來源 hash 不變。
- 完成狀態必須區分 Requirement、Code reality、Verification、Release。

## 版本

| 版本 | 日期 | 重點 |
|---|---|---|
| v6.0 | 2026-07-24 | 文件驅動四階段、Excel 欄位級 SSOT、runtime 解耦、Word/Vibe/Excel 整合 |
| v5.1 | 2026-05-10 | 架構 review skill 與 SunnyData 能力庫 |
| v5.0 | 2026-04-06 | Skills MECE 與 Git 品質流程 |
| v4.x | 2026-03 | Agents、Commands、Hooks、StatusLine 生態系 |

## License

[MIT](LICENSE)
