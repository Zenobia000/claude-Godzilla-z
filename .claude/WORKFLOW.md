# 開發工作流

這個 harness **不規定流程順序**。POC 的價值在於「想到就能開始驗證」，把工作流寫死成命令序列反而拖慢它。

流程由你決定，harness 只保證三件事：**常駐約束永遠生效、能力隨叫隨到、需要隔離時有 Agent 可用。**

## 三層怎麼一起運作

```
Rules（常駐）   每次對話都在，約束每一步
   ↓
Skills（按需）  遇到對應任務才載入方法與清單
   ↓
Agents（隔離）  需要獨立 context／權限／平行時才派出
```

| 層 | 什麼時候作用 | 由誰觸發 |
|---|---|---|
| `rules/` | 永遠 | 自動載入 |
| `skills/` | 任務語意命中時 | 模型判斷或使用者 `/skill-name` |
| `agents/` | 需要隔離 context、唯讀邊界、平行探索或第二意見 | 主 Agent 委派 |

三層的邊界：Rules 不放方法論，Skills 不放不變的鐵律，Agents 不複製 Skills 的知識。

## 典型 POC 節奏

不是規定，是常見走法：

```
確認分支 → 想清楚要驗證什麼 → 做出最小可動的東西 → 跑起來看 → 決定打掉還是往下
```

對應可用的能力（**按需載入，不必全用**）：

| 你在做什麼 | 載入 |
|---|---|
| 需求還模糊，要先探索 | `sunnydata-design` |
| 要寫 API | `sunnydata-api-design` |
| 要寫測試 / 用 TDD | `sunnydata-testing` |
| 卡在 bug | `sunnydata-debugging` |
| 要決定測試接縫、判斷某個抽象值不值得 | `sunnydata-codebase-design` |
| 想法太大、連要問什麼都還不確定 | `sunnydata-wayfind` |
| 答案在**人**身上，不在任何文件裡 | `sunnydata-questionnaire` |
| 前端 UI | `sunnydata-shadcn-ui`、`community-*` |
| 準備收尾、開 PR | `sunnydata-code-review` → `sunnydata-branch-lifecycle` |
| 要部署 / 容器化 | `sunnydata-infrastructure` |
| 回答太長太散 | `adhd-dev-mode`、`sunnydata-plain-explain` |

完整路由見 [skills/INDEX.md](skills/INDEX.md)。

## Context 衛生（哪些步驟共享 context、哪些必須清空）

上面那條節奏講的是**產出**怎麼接。這一節講**思考**怎麼接——兩者不一樣，搞混會讓工作在髒 context 上繼續推導。

| 邊界 | 規則 |
|---|---|
| 探索 → 規劃 → 切片（`sunnydata-design` Phase 1→2） | **全程不中斷、不 compact。** 這幾步互為前提，中途壓縮會讓後面的切片建立在被摘要過的推導上 |
| 規劃 → 實作 | **斷開。** 每個切片從**全新 context** 開始，只讀它自己的計畫 |
| 切片之間 | **斷開。** 上一片的實作細節對下一片是雜訊 |
| Review 與驗證 | 獨立 context。要判定的是證據，不是重述實作過程 |

**Smart zone**：模型還能銳利推理的窗口約 120k tokens。規劃還沒完成就逼近它，**不要硬撐**——把當前結論寫進計畫檔，開新 session 續作。壓縮著跑完的規劃，錯誤會一路傳到每個切片。

跨 session 靠**落地產出**接續，不靠對話摘要：計畫檔、已寫的測試、commit 就是交接面。真要一份純過渡的交接筆記，寫到作業系統暫存目錄，**不要進 repo**。

## 文件什麼時候該寫

`VibeCoding_Workflow_Templates/` 的 17 份模板是**選用的**，不是待辦清單。

| 階段 | 通常值得寫的 |
|---|---|
| POC 驗證中 | 幾乎不用寫；決策有反直覺的地方寫一則 ADR（`04_architecture_decision_record_template`） |
| POC 通過、要有人接手 | PRD（`02`）＋ 架構設計（`05`）＋ 專案結構（`08`） |
| 要往 production 走 | 安全檢查（`13`）、部署運維（`14`）、模組規格與測試（`07`） |

判準只有一條：**這份文件現在寫下來，會替誰省掉一次來回？** 答不出來就先不寫。

需要可稽核的需求追溯、owner 簽核閘與 Excel 追蹤簿時，換到 Pilot／企業級路線（`refactor/document-driven-ecosystem` 分支）。

## 常駐約束

| 規則 | 管什麼 |
|---|---|
| [golden-rules](rules/golden-rules.md) | 來源優先、可追溯、保護使用者工作、以證據宣告完成、最小必要變更 |
| [git-workflow](rules/git-workflow.md) | 先開分支、多 session ref 驗證、destructive 先 backup tag、commit→push→PR 連貫 |
| [thinking-boundary](rules/thinking-boundary.md) | 速通／深思模式；雛型期不前置治理窮舉 |
| [language-register](rules/language-register.md) | 文件的 L1／L2／L3 語域 |
| [plain-language-answers](rules/plain-language-answers.md) | 對話語域：何時把答案翻到決策層 |

新增常駐規則前先讀 [ABLATION.md](ABLATION.md)——沒有失敗證據的規則不該常駐。
