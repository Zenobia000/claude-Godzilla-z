<div align="center">

<img src="assets/hero.png" alt="Claude Code Godzilla" width="720" />

# Claude Code Godzilla

**進倉。啟動。征服混沌的程式碼戰場。**

[![Version](https://img.shields.io/badge/version-v6.1--poc-blue)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20(WSL2)-lightgrey)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

> 一套開箱即用的 Claude Code 開發配置模板 — **28 個按需載入的 Skills、18 份工程文件模板、~237 行常駐面**。
> 為快速 POC 設計：能力全都在，但不帶文件治理的硬邊界。複製到新專案，直接啟動。

---

## 快速開始

```bash
# 1. 複製到新專案
cp -r claude-Godzilla-z/.claude your-project/.claude

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
CLAUDE.md                  # repo 入口：這是什麼、怎麼開始、預設節奏
.claude/
├── CLAUDE.md              # 元件責任與維護契約
├── WORKFLOW.md            # Rules／Skills／Agents 三層怎麼一起運作（結構）
├── PLAYBOOK.md            # 三條路線走查、決策點、常見錯誤（用法）
├── ABLATION.md            # 常駐面消融紀錄（每條規則的失敗證據）
├── rules/           (5)   # 永遠生效的常駐規則，共 175 行
├── skills/          (28)  # 按需載入的能力庫（sunnydata-* / community-*）
├── agents/          (8)   # 需要隔離 context 或權限時才派出
├── output-styles/   (1)   # 只改呈現，不承載流程
├── hooks/                 # 零註冊，只留設計指南
├── settings.json          # 最小權限基線 + 敏感路徑 deny
└── statusline*.sh         # StatusLine（Windows / Linux）
```

**沒有 `commands/`、`context/`、`coordination/`、`taskmaster-data/`** —— 那些是為弱模型寫的鷹架，在前緣模型上壓縮解空間、製造規則間的猶豫。理由與消融方法見 [.claude/ABLATION.md](.claude/ABLATION.md)。

---

## Rules（5 個，自動載入）

常駐面只放**每次工作都成立、而且與模型預設行為不同**的約束；條件性細則下放到對應 skill 的 `references/`，用到才載入。

| 規則 | 核心內容 |
| :--- | :--- |
| **golden-rules** | 來源優先、可追溯、保護使用者工作、以證據宣告完成、最小必要變更 |
| **git-workflow** | 先開分支、多 session ref 驗證、destructive 先 backup tag、commit→push→PR 為單一連貫操作 |
| **thinking-boundary** | 速通／深思模式；**雛型期走 happy path，不前置法規／權限／邊界案的窮舉** |
| **language-register** | 文件的 L1 業務／L2 橋接／L3 工程三層語域 |
| **plain-language-answers** | 對話語域：何時該把答案翻到讀者的決策層、何時不可以 |

新增常駐規則前先讀 [ABLATION.md](.claude/ABLATION.md)——填不出「因為什麼失敗才存在」的規則，不該常駐。

---

## Skills（按需載入）

沒有寫死的流程入口。任務語意命中才載入，或由你 `/skill-name` 明確啟動。

| 你在做什麼 | 載入 |
| :--- | :--- |
| 需求還模糊，要先探索 | `sunnydata-design` |
| API 契約 | `sunnydata-api-design` |
| 測試 / TDD | `sunnydata-testing` |
| 卡在 bug | `sunnydata-debugging` |
| 安全敏感（auth、輸入、秘密） | `sunnydata-security` |
| 變更完成要審查 | `sunnydata-code-review`（行級）／`sunnydata-architecture-review`（架構級） |
| 開分支、收尾開 PR | `sunnydata-branch-lifecycle` |
| 容器化、CI/CD、部署 | `sunnydata-infrastructure` |
| 前端 UI | `sunnydata-shadcn-ui`、`community-*` |
| 多來源查證 | `sunnydata-deep-research` |
| 2+ 個真正獨立的子任務 | `sunnydata-parallel-agents` |
| 決定測試接縫、判斷抽象值不值得 | `sunnydata-codebase-design` |
| 想法太大、連要問什麼都還不確定 | `sunnydata-wayfind` |
| 答案在人身上不在文件裡 | `sunnydata-questionnaire` |
| 要新增／修改 skill 本身 | `sunnydata-skill-authoring` |
| 回答太長太散 | `adhd-dev-mode`、`sunnydata-plain-explain` |

完整路由與 community 能力庫見 [.claude/skills/INDEX.md](.claude/skills/INDEX.md)；實際怎麼跑一輪見 [.claude/PLAYBOOK.md](.claude/PLAYBOOK.md)。

---

## 文件模板

`VibeCoding_Workflow_Templates/` 的 18 份模板是**選用的，不是待辦清單**。

固定的只有入口那一份：

| 檔 | 角色 |
| :--- | :--- |
| [`00` 需求護身符](VibeCoding_Workflow_Templates/00_requirements_amulet.md) | **每個專案／Epic 開工前先過**：角色權責、FR／NFR 各八題、開場檢查表。只管問對問題，**不產文件**，十分鐘跑完 |
| [`01` 模板選用路由](VibeCoding_Workflow_Templates/01_workflow_manual.md) | 00 過完之後：這專案該寫哪幾份、每份各自何時取用、何時換 Pilot 線 |

其餘 15 份按深度補：

| 階段 | 通常值得寫的 |
| :--- | :--- |
| POC 驗證中 | 幾乎不用寫；反直覺的決策寫一則 ADR（`04`） |
| POC 通過、要有人接手 | PRD（`02`）＋ 架構設計（`05`）＋ 專案結構（`08`） |
| 要往 production 走 | 安全檢查（`13`）、部署運維（`14`）、模組規格與測試（`07`） |

判準只有一條：**這份文件現在寫下來，會替誰省掉一次來回？** 答不出來就先不寫。

這條線**沒有簽核閘**。取代它的是 golden-rules 的「以證據宣告完成」、收尾的兩軸 review，以及「改動讓哪份已填寫的文件失真就同一個 PR 一起改」。

> 需要可稽核的需求追溯、owner 簽核硬閘與 Excel 追蹤簿？換到 Pilot／企業級路線：`refactor/document-driven-ecosystem` 分支。兩條線共用同一套 harness，差別只在文件治理的嚴謹度。

---

## Git 工作流

| 常駐鐵律 | 內容 |
| :--- | :--- |
| 先開分支 | 在 main 上？停。dirty？停。沒指定分支？停。 |
| 多 session 協調 | 任何 git 寫操作前先驗證 ref 沒被別的 session 推進 |
| Destructive 先 backup tag | `reset --hard`／`push --force`／`branch -D`／`rebase` 之前 |
| commit → push → PR | 你說「做完了」就一氣呵成，中間不問「要不要 push」 |
| Commit body | **按需寫，不是必填**——diff 已經是 WHAT 的真相源 |

Commit message 細則、PR 前置與 body 四段、tangled history 恢復策略在
`.claude/skills/sunnydata-branch-lifecycle/references/git-conventions.md`，開 PR 時才載入。

```
main ──┬── feat/xxx ──── PR ──→ main
       ├── fix/yyy  ──── PR ──→ main
       └── chore/zzz ─── PR ──→ main
```

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
| v6.1-poc | 2026-08-05 | 從 Pilot 線移植與治理無關的工程紀律：新增 `sunnydata-codebase-design`／`wayfind`／`questionnaire`（skills 23 → 27）、`code-review` 加 Spec 軸與跨軸禁止 rerank、`design` 加垂直切片、ADR 加三條件閘。新增 `PLAYBOOK.md`（A 直接做／B 規劃一輪／C 先撥霧）與 `WORKFLOW.md` 的 context 邊界。模板層新增 `00` 需求護身符為固定入口，`01` 從企業流程手冊改為模板選用路由（移除與 POC 線衝突的簽核 Gate）。常駐面維持 211 行 |
| v6.0-poc | 2026-08-04 | **定位為快速 POC harness**。提示詞消融：刪 16 slash commands、18 output-styles、6 hooks、`context/`／`coordination/`／`taskmaster-data/`；常駐面 443 → 211 行（−52%）。新增 `ABLATION.md` 機制（每條常駐規則登記失敗證據）、`adhd-dev-mode` 與 `sunnydata-plain-explain` 輸出治理、skill 漸進揭露（SKILL.md ≤200 行＋`references/`）。17 份經典模板完整保留 |
| v5.1 | 2026-05-10 | 新增 `sunnydata-architecture-review` skill（三階段 smells/principles/fixes 流程＋100 條行話分類索引）、README 加入全域 symlink 共用說明 |
| v5.0 | 2026-04-06 | MECE 重構 skills (23→12, sunnydata-)、Git 5-gate 工作流、WHY/WHAT/IMPACT commit 標準、PR pre-flight |
| v4.3 | 2026-03-24 | 時間追蹤、`/time-log`、StatusLine 持久化 |
| v4.2 | 2026-03-16 | 跨平台（Windows/Linux）、Agent 全 opus |
| v4.1 | 2026-03-16 | rules(7)、skills(8)、MCP(+2) |
| v4.0 | 2026-03-16 | 13 Agent、16 Commands、StatusLine |

---

## License

MIT
