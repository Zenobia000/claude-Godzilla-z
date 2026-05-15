# 專案結構總覽

> **版本:** v5.5 | **更新:** 2026-05-15

---

## 目錄結構

```
claude-Godzilla-z/
├── README.md                           # 系統總覽、快速開始
├── CHANGELOG.md                        # 版本記錄
├── CLAUDE_TEMPLATE.md                  # 新專案初始化範本
├── PROJECT_STRUCTURE.md                # 本檔案
├── MCP_SETUP_GUIDE.md                  # MCP Server 設定指南
├── LICENSE
├── .mcp.json                           # MCP Server 定義（不入 Git）
├── .mcp.json.windows.example           # MCP 範本（Windows）
├── .mcp.json.linux.example             # MCP 範本（Linux）
├── assets/
│   └── hero.png
│
├── docs/                               # 專案文件（依穩定性分層）
│   └── 4-exploration/                  # 任務級文件（CIA、PRD）
│
├── .claude/                            # Claude Code 核心配置
│   ├── settings.json                   # 專案設定（權限、StatusLine、Model、Hooks）
│   ├── settings.local.json             # 個人設定（MCP 啟用）— 不入 Git
│   ├── CLAUDE.md                       # 專案指令
│   ├── WORKFLOW.md                     # 開發流程指南
│   ├── README.md                       # 配置目錄說明
│   ├── statusline.sh                   # StatusLine（Windows）
│   ├── statusline-linux.sh             # StatusLine（Linux/WSL2）
│   │
│   ├── agents/          (13 個)
│   │   ├── general-purpose.md
│   │   ├── planner.md                  # opus
│   │   ├── architect.md                # opus
│   │   ├── code-quality-specialist.md
│   │   ├── security-infrastructure-auditor.md
│   │   ├── test-automation-engineer.md
│   │   ├── tdd-guide.md
│   │   ├── e2e-validation-specialist.md
│   │   ├── build-error-resolver.md
│   │   ├── refactor-cleaner.md
│   │   ├── documentation-specialist.md
│   │   ├── deployment-expert.md
│   │   └── workflow-template-manager.md
│   │
│   ├── commands/        (12 個)
│   │   ├── build-fix.md               # 修復建置錯誤
│   │   ├── verify.md                   # 全面驗證
│   │   ├── refactor-clean.md          # 死碼清理
│   │   ├── template-check.md          # 模板合規
│   │   ├── release.md                  # 自動化發佈
│   │   ├── learn.md                    # 擷取模式
│   │   ├── save-session.md            # 儲存 session
│   │   ├── task-init.md               # 專案初始化
│   │   ├── task-next.md               # 下個任務
│   │   ├── task-status.md             # 專案狀態
│   │   ├── time-log.md                # 開發時間報表
│   │   └── suggest-mode.md            # 建議密度
│   │
│   ├── rules/           (11 個，自動載入)
│   │   ├── coding-style.md
│   │   ├── development-workflow.md
│   │   ├── git-workflow.md
│   │   ├── security.md
│   │   ├── testing.md
│   │   ├── performance.md
│   │   ├── patterns.md
│   │   ├── subagent-context.md
│   │   ├── change-governance.md
│   │   ├── context-stability.md
│   │   └── primitive-selection.md
│   │
│   ├── skills/          (41 個)
│   │   ├── INDEX.md                   # 索引
│   │   ├── sunnydata-*/               # 通用工具（design, testing, code-review, ...）
│   │   ├── vibecoding-*/              # VibeCoding 模板生成（prd, tdd, api-contract, ...）
│   │   └── community-*/              # 社群貢獻（前端、a11y、UI 設計系統）
│   │
│   ├── output-styles/   (2 個)
│   │   ├── Vision-output.md           # 視覺化模式
│   │   ├── Apprentice-output.md       # 學徒模式
│   │   └── README.md
│   │
│   ├── mcp-configs/
│   │   └── README.md                  # MCP 推薦清單
│   │
│   ├── hooks/                         # Hook 腳本庫
│   ├── taskmaster-data/               # 持久化資料（自動產生）
│   ├── context/                       # 跨 Agent 上下文共享
│   └── coordination/                  # Agent 協調
│
└── VibeCoding_Workflow_Templates/     # 工作流模板庫（v5 穩定性分層）
    ├── INDEX.md                       # 主索引
    ├── OWNERSHIP-MATRIX.md            # 人類 vs AI 職責劃分
    ├── HOW-TO-INSTANTIATE.md          # 給 end user 的 docs/ 配置建議
    ├── 0-principles/                  # 一年一改：產品原則、技術不變量
    ├── 1-decisions/                   # Append-only：ADR、架構總覽
    ├── 2-contracts/                   # 與 code 同步：API、模組契約
    ├── 3-process/                     # 半年級：工作流、檢查清單
    ├── 4-exploration/                 # 任務即用即丟：PRD、WBS、CIA
    └── 5-views/                       # 衍生自 code，不手寫
```

---

## 配置層次

| 層級               | 檔案                            | 用途                           |
| :----------------- | :------------------------------ | :----------------------------- |
| **專案共用** | `.claude/settings.json`       | 權限、StatusLine、Model、Hooks |
| **個人設定** | `.claude/settings.local.json` | 個人權限、MCP 啟用清單         |
| **MCP 定義** | `.mcp.json`                   | MCP Server 設定（含 API keys） |
| **規則**     | `.claude/rules/*.md`          | 自動載入，每次對話生效         |
| **技能**     | `.claude/skills/*/SKILL.md`   | 領域知識，按需參考             |

---

## 擴充指南

### 新增 MCP Server

見 [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)
