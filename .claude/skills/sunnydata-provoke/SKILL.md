---
name: sunnydata-provoke
description: Pressure-test before spending effort. Mode A grades the ambiguity in a request and asks only what would change the deliverable, declaring the rest as assumptions. Mode B attacks a formed idea, plan, selection or business decision along fixed lenses and converges to the missing evidence, today's first step, and a confidence level. Use when a request could be read two ways, or when the user brings an idea for a sanity check rather than for implementation.
---

> **繁中**：在**投入之前**施壓。兩個模式，同一條紀律——產**決策空間**，不產答案。

# Provoke

這是 [`thinking-boundary`](../../rules/thinking-boundary.md) 深思模式「只 provoke，不給答案」的**方法**。那條規則說了要做什麼，沒說怎麼做。

## 先選模式

| 你手上有的 | 模式 | 產出 |
|---|---|---|
| 一個**要求**，但可能有兩種讀法 | **A 攤模糊** | 真的會改變產出的問題 ＋ 已宣告的假設 |
| 一個**已成形的想法／方案／選型／商業決策** | **B 施壓** | 最缺的證據、最大風險、今天第一步、可信度 |

分不清就看**誰會錯**：A 防的是「我做錯東西」，B 防的是「你想錯方向」。

**別載這個 skill 的時候：**

| 情況 | 去哪 |
|---|---|
| 要施壓的對象已經是 code | `sunnydata-code-review`（行級）／`sunnydata-architecture-review`（架構級） |
| 連要問什麼都講不精準 | `sunnydata-wayfind` |
| 答案在**別人**身上 | `sunnydata-questionnaire` |
| 要一整輪 FR／NFR 訪談題庫 | [`00` 需求護身符](../../../VibeCoding_Workflow_Templates/00_requirements_amulet.md) §3.2／§4.2 |

---

## 模式 A：攤模糊

### 分級——唯一重要的一步

每個缺口丟進三格。**格子決定動作，不是你的謹慎程度決定。**

| 級 | 判準 | 動作 |
|---|---|---|
| **1 會改變產出** | 兩種讀法會做出**不同的東西**——不同檔案、不同介面、不同驗收 | **問**。這部分等答案 |
| **2 只改變作法** | 東西一樣、路徑不同（用哪個庫、放哪一層、命名） | **選一個、宣告、繼續** |
| **3 不影響** | 沒問也不會做錯 | **不要問**。這是雜訊，不是嚴謹 |

不知道放哪格，問自己：**猜錯要丟掉多少工作？** 丟得掉的就是第 2 格。

### 預設不阻塞

**問完第 1 格就往下做能做的**，不是全案停等。全域停等會讓 80% 能動的工作陪 20% 的模糊一起卡住。

只有這三種整案停下：

- 猜錯會造成**不可逆**或影響外部系統的動作（刪除、送出、部署、對外通訊）
- 猜錯會讓**整份產出作廢**，不是局部返工
- 涉及金錢、權限、法遵的判斷

### 假設怎麼宣告

不合格：「我假設你要用 Postgres。」——沒說猜錯會怎樣，等於沒宣告。

合格＝**假設 ＋ 錯了會怎樣 ＋ 推翻的成本**：

> 假設：批次一次最多 1000 筆（你沒給上限）。錯了要重寫分頁邏輯，約 20 分鐘。

宣告放在**產出前面或旁邊**，不是塞在結尾。[`golden-rules`](../../rules/golden-rules.md) #1：不得寫成既成事實。

### 與 `adhd-dev-mode` 的仲裁

`adhd-dev-mode` 說「向使用者要資訊只能當 fallback」——不衝突。它禁的是**把你該做的收斂工作丟回去**（「你貼一下架構我再判斷」）。

模式 A 只准問**第 1 格**：證據不在你這裡、猜錯要重做的。第 2、3 格照 `adhd-dev-mode` 的規矩自己決定。

**問題上限 3 個。** 超過 3 個第 1 格缺口，代表這不是模糊、是還沒撥霧 → `sunnydata-wayfind`。

---

## 模式 B：施壓

### 五個檢查軸——不是五個人

「五個顧問互不通氣」在單一 context 裡辦不到：同一個模型換五個名字，只會產生五種語氣，不會產生五份獨立判斷。**要真獨立就開 subagent**（見下）；不開就誠實當成五個**檢查軸**跑，並在輸出裡承認它們共用同一個前提。

| 軸 | 它問什麼 | 不合格的產出 |
|---|---|---|
| **反例** | 誰做過這件事、怎麼死的？有沒有反例？ | 泛泛的「可能有風險」 |
| **前提** | 哪一條被當成事實、但其實沒驗證過？ | 複述對方的論點 |
| **漏掉的選項** | 除了 A 和 B，C／D 是什麼？為什麼沒被考慮？ | 硬湊三個爛選項充數 |
| **外行常識** | 不懂這行的人會問什麼？（「為什麼不直接…？」） | 假裝天真但用行話問 |
| **落地** | 明天早上第一件事幹什麼？做不到就攔下來 | 「先做個 POC」這種沒有動詞的話 |

軸可以少，不能假。某軸這題沒東西就寫「無」，不要為了填滿而生內容。

### 收斂——模式 B 的價值全在這裡

跑完軸**必須**收成這五格，缺一格等於沒做：

1. **值得做／要改／放棄** — 三選一，不准「看情況」
2. **最大風險** — 一條，不是清單
3. **最缺的證據** — 現在最不確定的那一件，**以及要花多少力氣才能變確定**
4. **今天的第一步** — 今天做得完的一個動作，有動詞、有結束條件
5. **可信度** — 高／中／低 ＋ 一句「什麼會讓它變高」

第 3 格最有用。風險清單人人會列；**把不確定變確定的成本**才是決策資訊。

### 速通 vs 深思

模式由 [`thinking-boundary`](../../rules/thinking-boundary.md) 決定，這裡只落地第 1 格：

| 思考模式 | 第 1 格怎麼寫 |
|---|---|
| **速通**（預設） | 給**推薦** ＋ 一句取捨 |
| **深思**（使用者喊才進） | **不給推薦**。攤開選項與取捨，第 1 格留白給他填 |

深思模式下第 3、4、5 格照樣要給——那是事實與成本，不是替他做決定。

### 什麼時候真的開 subagent

值得付這個成本的只有：**不可逆的技術選型、要對外承諾的方案、你自己已經有明顯偏好時**（定錨風險最高）。

派法見 `sunnydata-parallel-agents`；純架構題直接用 `architect` agent。**一軸一個 agent，各自看不到別人的結論**，你只做收斂。

反過來說：日常任務、雛型階段、改得回來的決定——inline 跑五軸就好。

---

## 不准做的

| 反模式 | 為什麼 |
|---|---|
| 為了顯得嚴謹去攻擊一個可逆的小決定 | 施壓有成本；雛型階段不值得（[`thinking-boundary`](../../rules/thinking-boundary.md)「分析深度配階段」） |
| 五軸全部有話說 | 硬填就是噪音。無話寫「無」 |
| 收斂成「兩邊都有道理」 | 那是把判斷丟回去，違反 `adhd-dev-mode` |
| 把批評本身當結論交出去 | 沒有第 4 格就不算跑完 |
| 同時套 `sunnydata-design` 或 `sunnydata-wayfind` | 專案 CLAUDE.md：不同時套多個流程型 skill。這個先跑，跑完交棒 |
| 模式 A 一次丟七個問題 | 上限 3 個；超過代表該撥霧了 |

## 交棒

| 跑完發現 | 交給 |
|---|---|
| 第 1 格缺口 > 3，問題本身還講不精準 | `sunnydata-wayfind` |
| 缺口的答案在別人身上 | `sunnydata-questionnaire` |
| 值得做，而且握得住 | `sunnydata-design` Phase 1 |
| 值得做，而且很小 | [PLAYBOOK](../../PLAYBOOK.md) A：直接做（先開分支） |
| 決定不可逆、且是真實取捨的結果 | 寫一則 [`04` ADR](../../../VibeCoding_Workflow_Templates/04_architecture_decision_record_template.md)——三條件都成立才寫 |

## Completion

- **模式 A**：每個缺口都分過級；問出去的只有第 1 格；第 2 格的假設都寫了「錯了會怎樣」。
- **模式 B**：五格收斂齊全；第 4 格今天做得完；可信度有給，且說了什麼會讓它變高。
- 沒有把未驗證的推論寫成事實（[`golden-rules`](../../rules/golden-rules.md) #1）。
