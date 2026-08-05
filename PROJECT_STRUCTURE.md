# 專案結構總覽

> **定位:** 快速 POC 用的 Claude Code harness | **更新:** 2026-08-05

---

## 目錄結構

```
claude-Godzilla-z/
├── README.md                           # 系統總覽、快速開始
├── CLAUDE_TEMPLATE.md                  # 新專案初始化範本
├── PROJECT_STRUCTURE.md                # 本檔案
├── MCP_SETUP_GUIDE.md                  # MCP Server 設定指南
├── .mcp.json.windows.example           # MCP 範本（Windows）
├── .mcp.json.linux.example             # MCP 範本（Linux）
│
├── .claude/                            # Claude Code 核心配置
│   ├── CLAUDE.md                       # 專案入口、元件責任、維護契約
│   ├── WORKFLOW.md                     # 流程結構：三層協作、context 邊界
│   ├── PLAYBOOK.md                     # 流程用法：三條路線走查、決策點、常見錯誤
│   ├── ABLATION.md                     # 常駐面消融紀錄與失敗證據登記
│   ├── README.md                       # `.claude/` 生態系責任分層
│   ├── OUTPUT_STYLES.md                # Output Style 使用說明
│   ├── STATUSLINE_GUIDE.md             # StatusLine 平台差異與測試
│   ├── settings.json                   # 最小權限基線 + 敏感路徑 deny
│   ├── statusline.sh                   # StatusLine（Windows）
│   ├── statusline-linux.sh             # StatusLine（Linux/WSL2）
│   │
│   ├── rules/           (5 個，自動載入，共 175 行)
│   │   ├── golden-rules.md             # 跨技術棧底線
│   │   ├── git-workflow.md             # Git 常駐鐵律
│   │   ├── thinking-boundary.md        # 速通／深思模式；雛型期不前置治理窮舉
│   │   ├── language-register.md        # 文件的 L1/L2/L3 語域
│   │   └── plain-language-answers.md   # 對話語域：何時翻到決策層
│   │
│   ├── skills/          (27 個，按需載入)
│   │   ├── INDEX.md                    # 情境路由表
│   │   ├── adhd-dev-mode/              # 輸出密度治理
│   │   ├── sunnydata-*/       (17)     # 軟體工程能力庫
│   │   └── community-*/       (9)      # 社群 UI／UX／效能能力
│   │
│   ├── agents/          (8 個，需要隔離時才派出)
│   │   ├── architect.md                # 唯讀架構第二意見
│   │   ├── code-quality-specialist.md  # 唯讀變更審查
│   │   ├── security-infrastructure-auditor.md
│   │   ├── test-automation-engineer.md
│   │   ├── end-to-end-validation-specialist.md
│   │   ├── build-error-resolver.md
│   │   ├── documentation-specialist.md
│   │   └── deployment-expert.md
│   │
│   ├── output-styles/
│   │   └── 15-Vision-output.md         # 唯一呈現樣式
│   │
│   ├── hooks/
│   │   └── README.md                   # Hook 設計指南（零註冊）
│   │
│   └── mcp-configs/
│       └── README.md                   # MCP 推薦清單
│
├── VibeCoding_Workflow_Templates/     # 18 份工程文件模板（選用，不是待辦清單）
│   ├── INDEX.md                       # 模板索引
│   ├── 00_requirements_amulet.md      # 需求護身符（固定入口，不產文件）
│   ├── 01_workflow_manual.md          # 模板選用路由
│   ├── 02_project_brief_and_prd.md    # PRD
│   ├── 03_behavior_driven_development_guide.md  # BDD
│   ├── 04_architecture_decision_record_template.md  # ADR
│   ├── 05_architecture_and_design_document.md  # 架構設計
│   ├── 06_api_design_specification.md # API 規範
│   ├── 07_module_specification_and_tests.md  # 模組規格
│   ├── 08_project_structure_guide.md  # 專案結構
│   ├── 09_file_dependencies_template.md  # 依賴分析
│   ├── 10_class_relationships_template.md  # 類別關係
│   ├── 11_code_review_and_refactoring_guide.md  # Code Review
│   ├── 12_frontend_architecture_specification.md  # 前端架構
│   ├── 13_security_and_readiness_checklists.md  # 安全檢查
│   ├── 14_deployment_and_operations_guide.md  # 部署運維
│   ├── 15_documentation_and_maintenance_guide.md  # 文檔維護
│   ├── 16_wbs_development_plan_template.md  # WBS 計劃
│   └── 17_frontend_information_architecture_template.md  # 前端 IA
│
└── .out-of-scope/                     # 已審視並拒絕的機制與理由
    ├── README.md
    ├── hook-driven-project-state.md   # 為何不用 Hook 存專案狀態
    ├── workflow-output-styles.md      # 為何 output-styles 不承載流程
    └── plugin-packaging.md            # 為何不打包成 plugin
```

### 已移除的目錄（v6.0-poc）

| 目錄 | 為何移除 |
| :--- | :--- |
| `.claude/commands/` (16) | 把工作流寫死成命令序列；前緣模型不需要，反而壓縮解空間 |
| `.claude/output-styles/` 01–14 (18) | 實際上是文件模板與流程，設成全域樣式會污染每個回答 |
| `.claude/hooks/*.sh` (6) | 在 SessionStart／UserPromptSubmit 注入內容、寫入工作樹 |
| `.claude/context/` | 手動維護的 subagent 摘要影子文件 |
| `.claude/coordination/` | 人機協作設定檔，內容已由 rules 承接 |
| `.claude/taskmaster-data/` | session 快照與 timelog，屬暫態狀態 |
| `.claude/rules/` 7 檔 | coding-style／testing／security／performance／patterns／development-workflow／subagent-context——多數是舊模型的補丁或全域規範的重複 |

完整理由與消融方法見 [.claude/ABLATION.md](.claude/ABLATION.md)。

---

## 配置層次

| 層級 | 檔案 | 用途 |
| :--- | :--- | :--- |
| **專案共用** | `.claude/settings.json` | 最小權限基線、敏感路徑 deny、StatusLine |
| **個人設定** | `.claude/settings.local.json` | 個人權限、MCP 啟用清單（不入版控） |
| **MCP 定義** | `.mcp.json` | MCP Server 設定（含 API keys，不入版控） |
| **常駐規則** | `.claude/rules/*.md` | 自動載入，每次對話生效 |
| **按需能力** | `.claude/skills/*/SKILL.md` | 任務語意命中才載入 |
| **漸進揭露** | `.claude/skills/*/references/*.md` | SKILL.md 指示時才讀 |

---

## 兩條路線

| | 本 repo（main） | Pilot／企業級 |
| :--- | :--- | :--- |
| 分支 | `main` | `refactor/document-driven-ecosystem` |
| 定位 | 快速 POC | 文件驅動、證據閉環 |
| 流程入口 | 無，能力按需載入 | `/intake → /specify → /deliver → /verify` |
| 需求權威 | 無 | `requirements_tracker.xlsx` ①需求決策 |
| 硬閘 | 無 | owner 簽核後才可工程化 |
| 追溯 | 不強制 | `SRC-* → REQ-* → ACPT-* → 證據` 主鏈 |
| 文件模板 | 18 份經典模板 | 依九層分類重組版 ＋ 三本追蹤簿 |

兩條線共用同一套 harness（`rules/`、`skills/`、`agents/`、`ABLATION.md`）。哪些檔案必須雙線一致、哪些刻意不一致，見 [.claude/ABLATION.md](.claude/ABLATION.md) 的「與 Pilot 路線的同步」。

---

## 擴充指南

### 新增 MCP Server

見 [MCP_SETUP_GUIDE.md](MCP_SETUP_GUIDE.md)

### 新增 Skill / Rule / Agent

責任判斷表見 [.claude/skills/INDEX.md](.claude/skills/INDEX.md) 的「責任檢查」。
新增常駐規則前必讀 [.claude/ABLATION.md](.claude/ABLATION.md)——填不出失敗證據的不該常駐。
