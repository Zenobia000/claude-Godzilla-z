# 提示詞消融紀錄（Prompt Ablation Log）

> 本檔**不常駐**。它是維護契約第 6 條的落地處：每一條常駐規則，都要能回答「你是因為什麼失敗才存在的？」

## 為什麼有這份檔

前緣模型的能力已經超過大部分 harness 的假設。為弱模型寫的鷹架留在 context 裡不是保險，是**負擔**——它壓縮解空間、製造規則之間的猶豫，讓模型花注意力解衝突而不是解問題。

Anthropic 在 Opus 5 發布時把 Claude Code 的系統提示詞砍掉 80%（約 2,686 字 → 514 字），模型變得更好。方法不是「憑感覺刪」，是 **ablation study**：全部刪光 → 跑 → 只在模型**反覆犯同一個錯**時，一行一行加回來。大多數行再也沒回來過。

## 兩種常駐內容，只有一種該被消融

| 類型 | 定義 | 消融策略 |
| :--- | :--- | :--- |
| **補丁（patch）** | 為了修正模型的錯誤行為而寫 | **每個模型大版本重驗**。沒有失敗證據就刪 |
| **意圖（intent）** | 承載使用者的方法論、決策邊界、成長設計 | **不消融**。刪掉模型不會變笨，但這套 harness 會失去存在理由 |

分類判準：把這行刪掉，壞掉的是**模型的行為**還是**這個 harness 的目的**？前者是補丁，後者是意圖。

## 消融流程

1. **選時機**：模型大版本更新後，或距上次消融滿六個月。
2. **建對照組**：暫時把 `rules/` 只留 `golden-rules.md`，跑三個最常做的任務。
3. **記錄失敗**：只記**反覆出現**的同一種失敗。一次性失誤不算證據。
4. **逐條加回**：一次加一行，加回後在下表登記「因為什麼失敗」。
5. **未加回的不留**：沒有失敗證據卻想保留的，改寫成 skill 按需載入，或進 `.out-of-scope/`。

驗證輔助：`CLAUDE_CODE_SIMPLE=1` 據報導會剝除所有系統提示詞（含工具描述內的）作為對照基準。**此旗標未經本專案實測**，把它當參考而非依據；可靠的對照仍是上面的第 2 步。

## 常駐內容分類現況

盤點日：2026-08-04。常駐面 = `.claude/CLAUDE.md` + `.claude/rules/*.md`。

| 檔案 | 類型 | 失敗證據 | 下次消融處置 |
| :--- | :--- | :--- | :--- |
| `CLAUDE.md` 元件責任與工作方式 | 意圖 | — | 保留 |
| `CLAUDE.md` 維護契約 | 意圖 | harness 改動造成 router 說謊、frontmatter 指向已刪檔 | 保留 |
| `golden-rules.md` | 意圖 | — | 保留（其他檔以「第 N 條」引用，編號須穩定） |
| `git-workflow.md` 先開分支 | 補丁 | **未登記** | 重驗：base 系統提示已含「若在預設分支先開分支」 |
| `git-workflow.md` 多 session 協調 | 補丁 | 跨 session duplicate cherry-pick、stale branch | 保留 |
| `git-workflow.md` backup tag | 補丁 | **未登記** | 重驗 |
| `git-workflow.md` commit→push→PR 連貫 | 補丁 | base 系統提示預設「只在使用者要求時 push」，需明確覆寫 | 保留（證據來自基準行為衝突） |
| `git-workflow.md` body 按需寫 | 補丁 | 與全域 `~/.claude/CLAUDE.md` 的 WHY/WHAT/IMPACT 強制衝突，需仲裁 | 保留至全域規範同步後刪除 |
| `language-register.md` | 意圖 | — | 保留 |
| `plain-language-answers.md` | 意圖 | — | 保留 |
| `thinking-boundary.md` | 意圖 | — | 保留（POC 路線的核心：明文擋掉過度前置治理） |

**未登記 = 下次消融的第一批刪除候選。** 新增任何常駐規則時，必須同時在本表新增一列並填「失敗證據」；填不出來的，不該常駐。

## 與 Pilot 路線的同步

本 repo 是 harness 的真相源；Pilot／企業級路線（`refactor/document-driven-ecosystem` 分支）是它的超集，額外承載 Excel 追蹤簿、簽核硬閘與追溯 ID 主鏈。

**必須雙線一致的檔案**（改一邊要同步另一邊）：

- `.claude/rules/golden-rules.md`
- `.claude/rules/git-workflow.md` 的鐵律段落
- `.claude/rules/thinking-boundary.md`
- `.claude/rules/plain-language-answers.md`
- `.claude/ABLATION.md` 的方法與分類表
- `.claude/skills/` 下所有非 Action Skill——**其中這幾個是兩線共用的工程紀律，最容易漂**：
  `sunnydata-codebase-design`（接縫詞彙）、`sunnydata-code-review/references/two-axis-review.md`、
  `sunnydata-testing` 的接縫與反模式段、`sunnydata-design` 的垂直切片段

**同名但刻意不同的**（不要盲目同步）：

| 檔案 | main（通用） | Pilot |
|---|---|---|
| `sunnydata-wayfind` / `wayfind` | 地圖在 `docs/maps/`，交棒 `sunnydata-design` | 地圖在 `docs/document-system/maps/`，交棒 `/intake`／`/specify` |
| `sunnydata-questionnaire` | 獨立 skill，答覆落 spec/plan | `/intake` 的 reference，答覆回填 ①需求決策 |
| 切片的落腳處 | `sunnydata-design` Phase 2，狀態靠原生 task | `/deliver` ＋ Excel ③ 切片看板 |

**刻意不一致**（各自服務不同階段，不要同步）：

- `CLAUDE.md`、`WORKFLOW.md`、`skills/INDEX.md` — 定位不同
- `rules/language-register.md` — POC 版不含追溯 ID 與簽核硬邊界
- `VibeCoding_Workflow_Templates/` — POC 保留 17 份經典模板；Pilot 走九層分類重組版

## 沿革

| 日期 | 動作 | 結果 |
| :--- | :--- | :--- |
| 2026-08-05 | 從 Pilot 路線移植**通用工程紀律**（接縫詞彙、垂直切片、兩軸 review、TDD 反模式、context 衛生、wayfind、問卷、ADR 三條件閘）。刻意不搬 Excel 看板、追溯 ID、簽核閘與證據閉環 | 常駐面 211 → 未新增規則，只加路由指標 |
| 2026-08-04 | 從 Pilot 路線移植消融後的 harness：刪 16 slash commands、18 output-styles、6 hooks、`context/`／`coordination/`／`taskmaster-data/` 與 7 份舊 rules；換上消融後的 `rules/`、skill 漸進揭露結構與本檔機制 | 常駐面 443 → 211 行（−52%）；`.claude/` 82,955 → 70,348 行、345 → 306 檔 |
