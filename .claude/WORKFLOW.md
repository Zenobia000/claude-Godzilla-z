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
/task-next                  # command: 從 WBS 取下一個任務（自動開始時間追蹤）
    |
sunnydata-design            # skill: 規劃實作步驟（等待確認）
    |
sunnydata-testing           # skill: TDD（Red → Green → Refactor）
    |
/build-fix                  # command: 修復建置錯誤（如有）
    |
vibecoding-code-review      # skill: 程式碼審查（依 VibeCoding 模板）
   或 sunnydata-code-review
    |
e2e-validation-specialist   # agent (Agent tool): E2E 測試
    |
/verify full                # command: 全面驗證（建置+型別+lint+測試+安全）
    |
/task-status                # command: 確認進度（含預估 vs 實際時間），回到 /task-next
```

### Phase 2: 收尾

```bash
/time-log           # command: 查看今日/累計開發時間
/verify pre-pr      # command: PR 前完整檢查（含安全掃描）
/save-session       # command: 儲存 session 狀態供下次恢復
```

---

## 快速模式（小功能/Bug 修復）

```
[describe task]  →  sunnydata-testing  →  /verify quick
```
讓 AI 自動載入 writing-plans skill；無需顯式 `/plan`。

---

## Primitive 選擇規則（重要）

3 個原始元的決策依 `.claude/rules/primitive-selection.md`：

| 入口類型 | 何時用 | 範例 |
| :--- | :--- | :--- |
| **command** (`/name`) | 觸碰 taskmaster/session/time-log 系統狀態，或有獨立程序邏輯 | `/save-session`, `/task-next`, `/verify`, `/build-fix` |
| **skill** (auto-load 或 Skill tool) | **預設**。任何程序性知識 | `vibecoding-code-review`, `sunnydata-design`, `sunnydata-debugging` |
| **output-style** (`/output-style`) | 整個 session 持續的人格切換 | `/output-style Vision-output`（視覺化模式） |

**口訣**：預設用 skill；command 只給系統狀態工作流；output-style 只給人格切換。

---

## 指令速查

### Commands（12 個，皆觸碰系統狀態或具獨立程序）

| 指令 | 用途 | 常用參數 |
| :--- | :--- | :--- |
| `/task-init` | 專案初始化 | |
| `/task-next` | 取下一個任務（自動追蹤時間） | |
| `/task-status` | 查看專案進度（含時間追蹤） | `--detailed`, `--metrics` |
| `/time-log` | 開發時間報表 | `--today`, `--by-task`, `--week`, `--month` |
| `/build-fix` | 修復建置錯誤（含建置工具偵測） | |
| `/verify` | 全面驗證 | `quick`, `full`, `pre-commit`, `pre-pr` |
| `/refactor-clean` | 死碼清理（含工具偵測） | |
| `/template-check` | VibeCoding 模板合規檢查 | |
| `/suggest-mode` | 調整建議密度 | |
| `/learn` | 擷取可重用模式 | |
| `/save-session` | 儲存 session | |
| `/release` | 自動化發佈（CHANGELOG + tag + push） | `<version>` |

### 已遷移至 skill 的舊 commands（**改用 skill / agent tool**）

| 舊 command | 新入口 |
| :--- | :--- |
| `/plan` | `sunnydata-design` skill |
| `/tdd` | `sunnydata-testing` 或 `vibecoding-write-tdd` skill |
| `/e2e` | `e2e-validation-specialist` agent (via Agent tool) |
| `/review-code` | `vibecoding-code-review` 或 `sunnydata-code-review` skill |
| `/hub-delegate` | Agent tool 本身（已內建路由） |
| `/check-quality` | `sunnydata-code-review` + `sunnydata-architecture-review` skills |

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

| Skill | 觸發時機 |
| :--- | :--- |
| `sunnydata-testing` | TDD Red-Green-Refactor 工作流 |
| `vibecoding-write-tdd` | 撰寫 TDD 單元測試規格 |
| `sunnydata-api-design` | API 設計（搭配 `2-contracts/API-0000-api-spec.template.md`） |
| `vibecoding-code-review` | VibeCoding 模板式 code review |
| `sunnydata-code-review` | 通用 code review 流程 |
| `sunnydata-security` / `vibecoding-security-check` | 安全審查 |
| `e2e-validation-specialist` (agent) | E2E 測試 |
| `sunnydata-design` | 規劃實作步驟 |
| `sunnydata-deep-research` | 複雜問題的多源研究 |
| `sunnydata-infrastructure` | 部署/容器化 |
| `sunnydata-doc-freshness` | 檢查 tier-2 contract 文件鮮度 |

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
