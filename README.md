<div align="center">

<img src="assets/hero.png" alt="Claude Code Godzilla" width="720" />

# Claude Code Godzilla

**進倉。啟動。征服混沌的程式碼戰場。**

[![Version](https://img.shields.io/badge/version-v5.5-blue)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20(WSL2)-lightgrey)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

> 一套開箱即用的 Claude Code 開發配置模板 — Skills、5-Gate Git 品質管線、Tesla StatusLine。
> 複製到新專案，像駕駛員進倉一樣，直接啟動。

---

## 快速開始

```bash
# 1. 複製到新專案
cp -r claude-GUNDAM-zh-tw/.claude your-project/.claude

# 2. 設定 MCP（填入 API keys）
cp .mcp.json.linux.example .mcp.json   # Linux
cp .mcp.json.windows.example .mcp.json # Windows

# 3. 啟動
claude
```

### 全域共用 Skills（選用）

預設 skills 只在當前專案內可用。若想讓**所有專案**都能呼叫某個 skill，可建立全域 symlink：

```bash
# 範例：把 sunnydata-architecture-review 開放給所有專案
ln -s "$(pwd)/.claude/skills/sunnydata-architecture-review" \
      ~/.claude/skills/sunnydata-architecture-review
```

優點：檔案實體只在專案內（git 追得到、可隨專案版控），全域目錄只放捷徑 — 改一處兩邊同步。Windows 使用 `mklink /D`。

---

## 結構

```
.claude/
├── rules/           (11)  # 永遠生效的規則
├── skills/          (41)  # 按需載入的領域知識（sunnydata-* / vibecoding-* / community-*）
├── agents/          (13)  # 專業 Agent
├── commands/        (12)  # Slash Commands
├── output-styles/   (2)   # 產出格式（Vision / Apprentice）
├── settings.json          # 主設定
├── CLAUDE.md              # 專案指令
├── statusline.sh          # StatusLine（Windows）
└── statusline-linux.sh    # StatusLine（Linux/WSL2）
```

---

## Rules（11 個，自動載入）

每次對話自動生效，不需手動觸發。

| 規則 | 核心內容 |
| :--- | :--- |
| **development-workflow** | 先開分支再動 code、研究 → 規劃 → TDD → 審查 → 提交 |
| **git-workflow** | WHY/WHAT/IMPACT commit body、分支保護、PR 前置條件與品質標準、merge 策略 |
| **coding-style** | 不可變性、檔案 < 800 行、函式 < 50 行、命名慣例 |
| **security** | commit 前安全 checklist、秘密管理、依賴安全 |
| **testing** | 80%+ 覆蓋率、TDD 強制（RED-GREEN-IMPROVE） |
| **performance** | 模型選擇策略、Context Window 管理、平行任務 |
| **patterns** | Repository Pattern、API 信封格式、骨架專案策略 |
| **subagent-context** | 子代理產出持久化至 `.claude/context/` |
| **change-governance** | 變更涉及 flow/contract/data/architecture 需先跑 CIA |
| **context-stability** | 6 tier 文件穩定性層級與讀寫規則 |
| **primitive-selection** | command / skill / output-style 選擇決策樹 |

---

## Skills（41 個）

依開發生命週期組織，分 `sunnydata-*`、`vibecoding-*`、`community-*` 三群組。按需載入。

| 階段 | Skill | 用途 |
| :--- | :---- | :--- |
| THINK+PLAN+DO | **sunnydata-design** | 探索意圖 → 撰寫計畫 → 依檢查點執行 |
| BUILD (API) | **sunnydata-api-design** | REST API 設計規範 |
| BUILD (UI) | **sunnydata-shadcn-ui** | shadcn/ui 元件管理 |
| BUILD+TEST | **sunnydata-testing** | TDD + Unit/Integration/E2E (Playwright) |
| VERIFY (安全) | **sunnydata-security** | OWASP 分類 + checklist + 語言特定實踐 |
| VERIFY (審查) | **sunnydata-code-review** | 驗證 → 發起 review → 消化回饋 |
| VERIFY (架構) | **sunnydata-architecture-review** | 三階段 smells → principles → fixes 架構級審查 |
| SHIP (基礎設施) | **sunnydata-infrastructure** | Docker + CI/CD + 部署策略 |
| SHIP (分支) | **sunnydata-branch-lifecycle** | worktree 建立 → commit 審計 → PR/merge 收尾 |
| DEBUG | **sunnydata-debugging** | 四階段結構化除錯 |
| RESEARCH | **sunnydata-deep-research** | 多來源深度研究 |
| ORCHESTRATE | **sunnydata-parallel-agents** | 獨立任務平行派發 |
| META | **sunnydata-skill-authoring** | 撰寫/驗證 SKILL.md |

詳見 [.claude/skills/INDEX.md](.claude/skills/INDEX.md)。

---

## Git 工作流

本模板強制嚴謹的 git 協作流程，適用於開源專案和團隊協作。

### 5 道品質關卡

```
GATE 1  分支確認     在 main 上？停。dirty？停。沒指定分支？停。
   ↓
GATE 2  Commit 品質  WHY/WHAT/IMPACT body、72 字元 subject、一 commit 一事
   ↓
GATE 3  歷史審計     merge 前逐條檢查 commit 品質
   ↓
GATE 4  PR Pre-flight 測試通過、self-review、無 debug 殘留、< 400 行
   ↓
GATE 5  PR 品質      Background/Changes/Impact/Test Plan
   ↓
Merge → 刪除遠端分支 → Done
```

### 分支策略

```
main ──┬── feat/xxx ──── PR ──→ main
       ├── fix/yyy  ──── PR ──→ main
       └── chore/zzz ─── PR ──→ main
```

---

## 開發流程

```
分支確認 → 研究 → 規劃 → TDD → 審查 → 提交 → PR
```

| 入口 | 類型 | 用途 |
| :--- | :--- | :--- |
| `/task-init` | command | 建立 WBS、分析複雜度 |
| `/task-next` | command | 取下一個任務 |
| `sunnydata-design` | skill | 規劃實作步驟 |
| `sunnydata-testing` | skill | Red-Green-Refactor |
| `vibecoding-code-review` / `sunnydata-code-review` | skill | 程式碼審查 |
| `/verify` | command | 全面驗證 |
| `e2e-validation-specialist` | agent | Playwright E2E |
| `/build-fix` | command | 修復建置錯誤 |
| `/task-status` | command | 進度總覽 |
| `/time-log` | command | 開發時間報表 |
| `/save-session` | command | 儲存 session 狀態 |

**Primitive 選擇**：command 限觸碰系統狀態；skill 是預設入口。詳見 `.claude/rules/primitive-selection.md`。

---

## StatusLine

```
🦁 Opus 4.6 │ ❄️ 26% │ project (main*) │ 15m │ $12.50
```

Tesla High-Contrast 主題。Linux 使用 `statusline-linux.sh`。

```jsonc
// settings.json
"statusLine": "bash .claude/statusline-linux.sh"  // Linux/WSL2
"statusLine": "bash .claude/statusline.sh"         // Windows
```

---

## 版本記錄

| 版本 | 日期 | 變更 |
| :--- | :--- | :--- |
| v5.1 | 2026-05-10 | 新增 `sunnydata-architecture-review` skill（三階段 smells/principles/fixes 流程＋100 條行話分類索引）、README 加入全域 symlink 共用說明 |
| v5.0 | 2026-04-06 | MECE 重構 skills (23→12, sunnydata-)、Git 5-gate 工作流、WHY/WHAT/IMPACT commit 標準、PR pre-flight |
| v4.3 | 2026-03-24 | 時間追蹤、`/time-log`、StatusLine 持久化 |
| v4.2 | 2026-03-16 | 跨平台（Windows/Linux）、Agent 全 opus |
| v4.1 | 2026-03-16 | rules(7)、skills(8)、MCP(+2) |
| v4.0 | 2026-03-16 | 13 Agent、16 Commands、StatusLine |

---

## License

MIT
