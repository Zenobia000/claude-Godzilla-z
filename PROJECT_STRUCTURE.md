# 專案結構

本專案分成三層：Claude Code 執行期、軟體工程能力庫、文件治理範例。

```text
claude-Godzilla-z/
├── .claude/
│   ├── CLAUDE.md                 # 生態系入口與責任邊界
│   ├── settings.json             # 最小設定；內建 Read/Edit 敏感路徑 deny
│   ├── WORKFLOW.md               # 四階段文件驅動流程
│   ├── rules/                    # 4 份常駐規則
│   │   ├── golden-rules.md       # 跨技術棧底線
│   │   ├── git-workflow.md       # Git／push／PR 操作規範
│   │   ├── language-register.md  # L1/L2/L3 三層語域
│   │   └── thinking-boundary.md  # 速通/深思模式與思考邊界
│   ├── skills/
│   │   ├── intake/               # Excel／訪談來源進件
│   │   ├── specify/              # PRD／BDD／SAD／ADR／追溯
│   │   ├── deliver/              # 已核准垂直切片交付
│   │   ├── verify/               # 證據型驗證關卡
│   │   ├── sunnydata-*/          # 軟體工程能力庫
│   │   └── community-*/          # 社群 UI／UX／效能能力
│   ├── agents/                   # 8 個隔離型專業執行角色
│   ├── output-styles/
│   │   └── 15-Vision-output.md   # 唯一呈現樣式
│   └── hooks/                    # Hook 設計指南（零註冊）
│
├── VibeCoding_Workflow_Templates/    # Pilot 核心 15 份模板＋3 本角色追蹤簿（企業級文件依需增建）
│   ├── INDEX.md                  # 文件選用與模板索引
│   ├── _meta/                    # workflow_manual、template_standard
│   ├── 01_requirements/          # requirements_tracker、prd、brd、srs
│   ├── 02_ux_ui/                 # ux_research_and_journey、information_architecture、ui_spec
│   ├── 03_architecture/          # sad、adr、diagrams/（drawio 大圖＋工具）、engineering_tracker
│   ├── 04_design/                # api_spec+openapi、db_design、lld
│   ├── 05_qa/                    # test_plan、uat_plan、qa_tracker
│   └── 06_ops/                   # deployment_and_operations、runbook
│
├── docs/document-system/
│   ├── INDEX.md                  # 文件系統入口與權威矩陣
│   ├── architecture.md           # Excel／Markdown／Word 權威與同步架構
│   ├── workbook-guide.md         # 三個角色追蹤簿的用法與 ID 骨幹
│   └── artifact-map.md           # 企業文件分類對應模板
│
├── .out-of-scope/                # 已拒絕機制的知識庫（概念＋理由＋先例）
├── software_development_documentation_guide_zh_tw.docx
│                                  # 企業文件全景與選用參考
├── CHANGELOG.md                   # 版本沿革（版本號唯一真相源：README badge）
├── CLAUDE_TEMPLATE.md             # 新專案啟動範本
├── README.md
├── MCP_SETUP_GUIDE.md
└── .mcp.json.*.example
```

## 執行期載入

| 元件 | 載入時機 | 設計限制 |
|---|---|---|
| `CLAUDE.md` | 專案啟動 | 只放入口與責任 |
| `rules/*.md` | 每次對話 | 只放恆定規則（golden、git、語域、思考邊界） |
| `skills/*/SKILL.md` | 人工或語意觸發 | 方法與知識可漸進載入 |
| `agents/*.md` | 明確委派 | 隔離 context／工具／權限 |
| `output-styles/*.md` | 人工選擇 | 只改呈現 |
| `hooks` | settings 有註冊才執行 | 基礎模板目前為零 Hook |

`commands/` 已由四個 Action Skills 取代。Claude Code 會把 Skill 暴露成 slash command，避免維護兩套格式。

## 文件層

```text
企業文件指南（要不要有）
          ↓
VibeCoding Templates（怎麼寫）
          ↓
專案實例文件（實際內容）
          ↕ stable IDs
Excel 統控介面（對焦／核准／追蹤）
```

- Word 指南是分類與裁剪依據，不逐章複製到每個專案。
- VibeCoding templates 是工程工作格式，依開發階段（雛型／Pilot／企業級）選取。
- Excel 保存業務語言、顏色、排序、核准與管理視圖。
- Markdown／code-native contracts 保存可 diff、可 review、可讓 AI 與 CI 消化的工程內容。
- 每個欄位只能指定一個 owner；其他格式是 projection 或索引。

## Agent 邊界

保留的 Agents 分成：

- 唯讀第二意見：architecture、code review、security
- 高雜訊執行：test、E2E、build repair
- 大型專門 context：documentation、deployment

一般規劃、通用研究、TDD 方法、模板選擇與重構不另建 Agent，由主 Agent 搭配 Skills 完成。

## Runtime 退役項目

- TaskMaster prompt 攔截、snapshot、timelog 自動寫入
- 每次 Subagent 強制落地 context
- Agent monitor hooks
- PRD／BDD／TDD 等全域 Output Styles
- 17 個重複 Commands

上述退役項目與 `docs/legacy/` 歸檔均已自 repo 刪除，歷史版本在 git history；`hooks/` 只剩設計指南。
