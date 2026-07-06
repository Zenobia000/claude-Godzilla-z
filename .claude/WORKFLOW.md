# 開發工作流指南

## 完整開發流程

```
專案初始化 → 任務管理循環 → 結束保存
```

### Phase 0: 專案初始化

```bash
/task-init          # 建立 WBS、分析複雜度、配置 Hub 策略
```

產出：WBS 任務清單、專案配置、里程碑規劃

### Phase 1: 任務循環（每個任務重複）

```
/task-next          # 從 WBS 取下一個任務（自動開始時間追蹤）
    |
/plan               # 規劃該任務的實作步驟（等待確認）
    |
/tdd                # 測試驅動開發（Red → Green → Refactor）
    |
/build-fix          # 修復建置錯誤（如有）
    |
/review-code        # 程式碼審查
    |
/e2e                # 端到端測試（關鍵流程）
    |
/verify full        # 全面驗證（建置+型別+lint+測試+安全）
    |
/task-status        # 確認進度（含預估 vs 實際時間），回到 /task-next
```

### Phase 2: 收尾

```bash
/time-log           # 查看今日/累計開發時間
/verify pre-pr      # PR 前完整檢查（含安全掃描）
/save-session       # 儲存 session 狀態供下次恢復
```

---

## 快速模式（小功能/Bug 修復）

```
/plan [描述]  →  /tdd  →  /verify quick
```

---

## 指令速查

### 核心工作流（按使用順序）

| 指令 | 用途 | 常用參數 |
| :--- | :--- | :--- |
| `/task-init` | 專案初始化 | |
| `/task-next` | 取下一個任務（自動追蹤時間） | |
| `/task-status` | 查看專案進度（含時間追蹤） | `--detailed`, `--metrics` |
| `/time-log` | 開發時間報表 | `--today`, `--by-task`, `--week`, `--month` |
| `/plan` | 規劃實作步驟 | [功能描述] |
| `/tdd` | 測試驅動開發 | [功能描述] |
| `/build-fix` | 修復建置錯誤 | |
| `/review-code` | 程式碼審查 | [路徑] |
| `/e2e` | E2E 測試 | [流程描述] |
| `/verify` | 全面驗證 | `quick`, `full`, `pre-commit`, `pre-pr` |

### 輔助指令

| 指令 | 用途 |
| :--- | :--- |
| `/hub-delegate` | 委派 agent 執行任務 |
| `/check-quality` | 品質評估 |
| `/refactor-clean` | 死碼清理 |
| `/template-check` | 模板合規檢查 |
| `/time-log` | 開發時間報表（每日/每任務） |
| `/suggest-mode` | 調整建議密度 |
| `/learn` | 擷取可重用模式 |
| `/save-session` | 儲存 session |

---

## Agent 使用時機

| 場景 | 自動使用的 Agent |
| :--- | :--- |
| 複雜功能需求 | planner (opus) |
| 架構決策 | architect (opus) |
| 寫完程式碼後 | code-quality-specialist |
| Bug 修復/新功能 | tdd-guide |
| 建置失敗 | build-error-resolver |
| 安全敏感程式碼 | security-infrastructure-auditor |
| E2E 測試 | e2e-validation-specialist |
| 死碼清理 | refactor-cleaner |
| 更新文檔 | documentation-specialist |
| 部署上線 | deployment-expert |
| 模板整合 | workflow-template-manager |

---

## Rules 自動載入

`.claude/rules/` 下的規則在每次對話中自動生效：

| 規則 | 強制內容 |
| :--- | :--- |
| coding-style | 不可變性、檔案大小限制、錯誤處理 |
| development-workflow | 研究先行、Plan-TDD-Review 流程 |
| git-workflow | Conventional Commits、PR 流程 |
| security | 每次 commit 前安全檢查清單 |
| testing | 80%+ 覆蓋率、TDD 強制 |
| performance | 模型選擇、context 管理 |
| patterns | Repository Pattern、API 格式 |

---

## Skills 參考

`.claude/skills/` 下的 skill 提供特定領域的深度知識：

| Skill | 搭配指令/時機 |
| :--- | :--- |
| sunnydata-design | `/plan`、多步驟實作前 |
| sunnydata-testing | `/tdd`、`/e2e` |
| sunnydata-api-design | 06_api 模板、API 端點設計 |
| sunnydata-shadcn-ui | 前端 UI 開發 |
| sunnydata-security | `/review-code`（安全面）、auth/輸入處理 |
| sunnydata-code-review | `/review-code`、commit/PR 前 |
| sunnydata-architecture-review | 架構審查、設計債盤點 |
| sunnydata-infrastructure | `/verify pre-pr`、容器化與部署 |
| sunnydata-branch-lifecycle | 分支收尾（merge/PR/cleanup） |
| sunnydata-debugging | `/build-fix`、bug 與測試失敗 |
| sunnydata-deep-research | 複雜問題調查 |
| sunnydata-parallel-agents | 2+ 獨立任務平行派發 |
| sunnydata-skill-authoring | 新增/修改 skill |

完整索引見 `.claude/skills/INDEX.md`。

---

## MCP Server

| Server | 用途 |
| :--- | :--- |
| brave-search | 網路搜尋 |
| context7 | 即時文檔查詢（套件文檔） |
| github | GitHub 操作 |
| playwright | 瀏覽器自動化 |
| sequential-thinking | 鏈式推理 |
| memory | 跨 session 記憶 |

更多可用 server 見 `.claude/mcp-configs/README.md`。

---

## 新專案設定指南

1. 複製本模板目錄到新專案
2. 複製 MCP 範本並填入 API keys:
   - Windows: `cp .mcp.json.windows.example .mcp.json`
   - Linux: `cp .mcp.json.linux.example .mcp.json`
3. 根據專案語言，從 everything-claude 複製對應的語言規則到 `.claude/rules/`
4. 根據專案需求，複製額外的 skills 到 `.claude/skills/`
5. 啟動 Claude Code，執行 `/task-init`
