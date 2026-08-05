# 開發工作流（結構）

> 這裡定義**誰負責什麼**。實際怎麼跑一輪見 [PLAYBOOK.md](PLAYBOOK.md)。

**這個 harness 不規定流程順序。** 它只保證三件事：常駐約束永遠生效、能力隨叫隨到、需要隔離時有 Agent。

## 兩條要背起來的規則

1. **探索 → 規劃 → 切片，全程不中斷。** 中途 compact，後面每片都建立在摘要過的推導上。
2. **切片之間必須換 session。** 上一片的實作細節對下一片是雜訊。

## 三層

| 層 | 什麼時候作用 | 誰觸發 | 不放什麼 |
|---|---|---|---|
| `rules/` | 永遠 | 自動載入 | 方法論 |
| `skills/` | 任務語意命中 | 模型判斷或 `/skill-name` | 不變的鐵律 |
| `agents/` | 需要隔離 context／權限／平行／第二意見 | 主 Agent 委派 | Skills 的知識 |

## Context 邊界

| 邊界 | 規則 |
|---|---|
| 探索 → 規劃 → 切片 | **不斷開、不 compact** |
| 規劃 → 實作 | **斷開**，每片從全新 context |
| 切片之間 | **斷開** |
| Review 與驗證 | 獨立 context |

**Smart zone ~120k**：規劃沒完成就逼近它，寫進計畫檔、開新 session，**不要硬撐**。

跨 session 靠**落地產出**接續（計畫檔、測試、commit），不靠對話摘要。純過渡的交接筆記寫到 OS 暫存目錄，**不進 repo**。

## 該載哪個 skill

| 你在做什麼 | 載入 |
|---|---|
| 需求還模糊，要探索 | `sunnydata-design` |
| 決定測試接縫、判斷抽象值不值得 | `sunnydata-codebase-design` |
| 想法太大、連要問什麼都不確定 | `sunnydata-wayfind` |
| 答案在**人**身上 | `sunnydata-questionnaire` |
| 寫測試 / TDD | `sunnydata-testing` |
| 寫 API | `sunnydata-api-design` |
| 卡在 bug | `sunnydata-debugging` |
| 前端 UI | `sunnydata-shadcn-ui`、`community-*` |
| 收尾開 PR | `sunnydata-code-review` → `sunnydata-branch-lifecycle` |
| 部署 / 容器化 | `sunnydata-infrastructure` |
| 回答太長太散 | `adhd-dev-mode`、`sunnydata-plain-explain` |

完整路由見 [skills/INDEX.md](skills/INDEX.md)。

## 文件什麼時候寫

`VibeCoding_Workflow_Templates/` 的 18 份是**選用的**，不是待辦清單。

| 階段 | 通常值得寫 |
|---|---|
| POC 驗證中 | 幾乎不寫；反直覺的決策寫一則 ADR（`04`） |
| 要有人接手 | PRD（`02`）＋架構設計（`05`）＋專案結構（`08`） |
| 往 production 走 | 安全（`13`）、部署（`14`）、模組規格與測試（`07`） |

判準一句：**這份文件寫下來，會替誰省掉一次來回？** 答不出來就不寫。

入口是 [`00` 需求護身符](../VibeCoding_Workflow_Templates/00_requirements_amulet.md)（問對問題、不產文件），逐份的取用時機在 [`01` 模板選用路由](../VibeCoding_Workflow_Templates/01_workflow_manual.md)。

## 常駐約束

| 規則 | 管什麼 |
|---|---|
| [golden-rules](rules/golden-rules.md) | 來源優先、可追溯、保護使用者工作、以證據宣告完成、最小變更 |
| [git-workflow](rules/git-workflow.md) | 先開分支、多 session 驗 ref、destructive 先 backup tag、commit→push→PR 連貫 |
| [thinking-boundary](rules/thinking-boundary.md) | 速通／深思；雛型期不前置治理窮舉 |
| [language-register](rules/language-register.md) | 文件的 L1／L2／L3 語域 |
| [plain-language-answers](rules/plain-language-answers.md) | 對話語域：何時翻到決策層 |

**新增常駐規則前先讀 [ABLATION.md](ABLATION.md)**——填不出失敗證據的不該常駐。
