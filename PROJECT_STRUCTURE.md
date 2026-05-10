# 專案結構總覽

> **版本:** v4.3 | **更新:** 2026-03-24

---

## 目錄結構

```
claude_v2026/
├── README.md                           # 系統總覽、快速開始
├── CLAUDE_TEMPLATE.md                  # 新專案初始化範本
├── PROJECT_STRUCTURE.md                # 本檔案
├── MCP_SETUP_GUIDE.md                  # MCP Server 設定指南
├── .mcp.json                           # MCP Server 定義（不入 Git）
├── .mcp.json.windows.example           # MCP 範本（Windows）
├── .mcp.json.linux.example             # MCP 範本（Linux）
│
├── .claude/                            # Claude Code 核心配置
│   ├── settings.json                   # 專案設定（權限、StatusLine、Model）
│   ├── settings.local.json             # 個人設定（MCP 啟用）
│   ├── WORKFLOW.md                     # 開發流程指南
│   ├── statusline.sh                   # StatusLine bash 腳本（Windows）
│   ├── statusline-linux.sh            # StatusLine bash 腳本（Linux）
│   ├── statusline-go.exe              # StatusLine Go 備用
│   ├── SOP.md                          # 設定 SOP
│   │
│   ├── agents/          (13 個)
│   │   ├── general-purpose.md          # 通用問題解決
│   │   ├── planner.md                  # 功能規劃（opus）
│   │   ├── architect.md                # 系統架構（opus）
│   │   ├── code-quality-specialist.md  # 程式碼審查
│   │   ├── security-infrastructure-auditor.md  # 安全稽核
│   │   ├── test-automation-engineer.md # 測試自動化
│   │   ├── tdd-guide.md               # TDD 引導
│   │   ├── e2e-validation-specialist.md # E2E 測試
│   │   ├── build-error-resolver.md     # 建置錯誤修復
│   │   ├── refactor-cleaner.md         # 死碼清理
│   │   ├── documentation-specialist.md # 文檔專家
│   │   ├── deployment-expert.md        # 部署專家
│   │   └── workflow-template-manager.md # 模板管理
│   │
│   ├── commands/        (17 個)
│   │   ├── plan.md                     # 規劃實作步驟
│   │   ├── tdd.md                      # 測試驅動開發
│   │   ├── build-fix.md               # 修復建置錯誤
│   │   ├── e2e.md                      # E2E 測試
│   │   ├── verify.md                   # 全面驗證
│   │   ├── refactor-clean.md          # 死碼清理
│   │   ├── review-code.md             # 程式碼審查
│   │   ├── check-quality.md           # 品質評估
│   │   ├── learn.md                    # 擷取模式
│   │   ├── save-session.md            # 儲存 session
│   │   ├── task-init.md               # 專案初始化
│   │   ├── task-status.md             # 專案狀態（含時間追蹤）
│   │   ├── task-next.md               # 下個任務（自動追蹤時間）
│   │   ├── time-log.md                # 開發時間報表
│   │   ├── hub-delegate.md            # Agent 委派
│   │   ├── suggest-mode.md            # 建議密度
│   │   └── template-check.md          # 模板合規
│   │
│   ├── rules/           (7 個，自動載入)
│   │   ├── coding-style.md            # 編碼風格
│   │   ├── development-workflow.md    # 開發流程
│   │   ├── git-workflow.md            # Git 流程
│   │   ├── security.md               # 安全規範
│   │   ├── testing.md                 # 測試要求
│   │   ├── performance.md            # 效能優化
│   │   └── patterns.md               # 通用模式
│   │
│   ├── skills/          (8 個精選)
│   │   ├── INDEX.md                   # 索引與擴充指南
│   │   ├── tdd-workflow/              # TDD 流程
│   │   ├── api-design/               # API 設計
│   │   ├── security-review/          # 安全審查
│   │   ├── e2e-testing/              # E2E 測試
│   │   ├── coding-standards/         # 編碼標準
│   │   ├── deep-research/            # 深度研究
│   │   ├── deployment-patterns/      # 部署模式
│   │   └── docker-patterns/          # Docker 模式
│   │
│   ├── output-styles/   (15 個)
│   │   ├── 01-prd-product-spec.md    # PRD
│   │   ├── 02-bdd-scenario-spec.md   # BDD
│   │   ├── ...                        # 03-15
│   │   └── README.md                 # 使用指南
│   │
│   ├── mcp-configs/
│   │   └── README.md                  # MCP 推薦清單
│   │
│   ├── hooks/                         # Hook 腳本庫
│   ├── taskmaster-data/               # 持久化資料（自動產生）
│   │   ├── wbs.md                     # WBS 任務清單
│   │   ├── project.json               # 專案元資料
│   │   ├── timelog.jsonl              # 開發時間日誌（每 session 一筆）
│   │   ├── wbs-history.log           # WBS 更新審計軌跡
│   │   ├── .session-start             # 暫存：session 開始時間
│   │   ├── .session-snapshot          # 暫存：最新 session 快照
│   │   └── .current-task              # 暫存：當前進行中的任務編號
│   ├── context/                       # 跨 Agent 上下文共享
│   │   ├── decisions/                 # 技術決策記錄
│   │   ├── quality/                   # 品質報告
│   │   ├── testing/                   # 測試報告
│   │   ├── e2e/                       # E2E 報告
│   │   ├── security/                  # 安全報告
│   │   ├── deployment/               # 部署報告
│   │   ├── docs/                      # 文檔報告
│   │   └── workflow/                  # 工作流報告
│   │
│   └── coordination/                  # Agent 協調
│       └── human_ai_collaboration_config.md
│
├── VibeCoding_Workflow_Templates/     # 工作流模板庫（v4 穩定性分層）
│   ├── INDEX.md                       # 主索引（穩定性視圖）
│   ├── LEGACY-INDEX.md                # 舊 v3 階段視圖（將於 v5 移除）
│   ├── HOW-TO-INSTANTIATE.md          # 給 end user 的 docs/ 配置建議
│   ├── 0-principles/                  # 一年一改：產品原則、技術不變量
│   │   └── product-principles.template.md
│   ├── 1-decisions/                   # Append-only：ADR、架構總覽
│   │   ├── adr.template.md
│   │   └── architecture-overview.template.md
│   ├── 2-contracts/                   # 與 code 同步：API、模組契約
│   │   ├── api-spec.template.md
│   │   └── module-contract.template.md
│   ├── 3-process/                     # 半年級：工作流、檢查清單、運維
│   │   ├── workflow-manual.md
│   │   ├── bdd-guide.md
│   │   ├── code-review-checklist.md
│   │   ├── security-readiness-checklist.md
│   │   ├── deployment-runbook.template.md
│   │   └── docs-maintenance-guide.md
│   ├── 4-exploration/                 # 任務即用即丟：PRD、WBS
│   │   ├── prd.template.md
│   │   └── wbs.template.md
│   ├── 5-views/                       # 衍生自 code，不手寫
│   │   ├── project-structure.template.md
│   │   ├── file-dependencies.template.md
│   │   ├── class-relationships.template.md
│   │   ├── frontend-architecture.template.md
│   │   └── frontend-information-architecture.template.md
│   └── output_style.md                # Output Style 參考
│
├── everything-claude/                 # 參考資源庫（不直接使用）
│   └── everything-claude-code/
│       ├── agents/                    # 更多 agent 參考
│       ├── skills/     (95 個)       # 更多 skill 可按需複製
│       ├── rules/      (45 個)       # 語言特定規則可按需複製
│       ├── commands/                  # 更多 command 參考
│       └── mcp-configs/              # MCP 設定參考
│
└── status-line/                       # StatusLine 原始碼參考
    └── claude-statusline/
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
