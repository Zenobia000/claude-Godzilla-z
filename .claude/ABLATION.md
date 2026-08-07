# 常駐面消融紀錄

> **這份檔的用途只有一個**：想加一條常駐規則時，先回答 ——
>
> ## 「這條是因為模型反覆犯什麼錯才存在？」
>
> **答不出來就不准加。** 改寫成 skill 按需載入，或進 `.out-of-scope/`。

本檔不常駐。維護契約第 6 條的落地處。

## 加東西之前

1. 判斷類型：

   | 類型 | 是什麼 | 處置 |
   |---|---|---|
   | **補丁** | 修正模型的錯誤行為 | 每個模型大版本**重驗**，沒證據就刪 |
   | **意圖** | 你的方法論、決策邊界、成長設計 | **不消融** |

   判準：刪掉它，壞的是**模型的行為**還是**這個 harness 的目的**？

2. 在下方分類表新增一列，填「失敗證據」。

## 消融流程（每個模型大版本或滿六個月）

1. `rules/` 暫時只留 `golden-rules.md`
2. 跑三個最常做的任務
3. 只記**反覆出現**的同一種失敗（一次性失誤不算）
4. 一次加回一行，登記證據
5. 沒加回的不留

> 背景：Anthropic 在 Opus 5 把 Claude Code 系統提示詞砍掉 80%（2,686 → 514 字），模型變更好。方法不是憑感覺刪，是全部刪光再逐行加回——大多數行再也沒回來。
>
> `CLAUDE_CODE_SIMPLE=1` 據報導會剝除所有提示詞作對照。**本專案未實測**，當參考不當依據。

## 分類現況

盤點日 2026-08-05（根目錄 `CLAUDE.md` 於 2026-08-07 新增，未重跑全面消融）。常駐面 = 根目錄 `CLAUDE.md` + `.claude/CLAUDE.md` + `rules/*.md`，共 237 行。

| 檔案 | 類型 | 失敗證據 | 下次處置 |
|---|---|---|---|
| 根目錄 `CLAUDE.md` 入口與節奏 | 意圖 | — | 保留（只放入口；長出細節就是該下放到連結目標的訊號）|
| `.claude/CLAUDE.md` 元件責任 | 意圖 | — | 保留 |
| `.claude/CLAUDE.md` 維護契約 | 意圖 | router 說謊、frontmatter 指向已刪檔 | 保留 |
| `golden-rules.md` | 意圖 | — | 保留（他檔以「第 N 條」引用，編號須穩定）|
| `git-workflow.md` 先開分支 | 補丁 | **未登記** | ⚠ 重驗：base 提示已含「預設分支先開分支」 |
| `git-workflow.md` 多 session 協調 | 補丁 | 跨 session duplicate cherry-pick、stale branch | 保留 |
| `git-workflow.md` backup tag | 補丁 | **未登記** | ⚠ 重驗 |
| `git-workflow.md` commit→push→PR 連貫 | 補丁 | base 提示預設「只在使用者要求時 push」，需覆寫 | 保留 |
| `git-workflow.md` body 按需寫 | 補丁 | 與全域 `~/.claude/CLAUDE.md` 的 WHY/WHAT/IMPACT 衝突 | 全域同步後刪除 |
| `language-register.md` | 意圖 | — | 保留 |
| `plain-language-answers.md` | 意圖 | — | 保留 |
| `thinking-boundary.md` | 意圖 | — | 保留（擋過度前置治理）|

**⚠ 未登記 = 下次消融的第一批刪除候選。**

## 雙線同步

main（通用）是 harness 真相源；Pilot（`refactor/document-driven-ecosystem`）是超集，多帶 Excel 追蹤簿、簽核閘、追溯主鏈。

**改一邊要同步另一邊**：

- `rules/golden-rules.md`、`git-workflow.md` 鐵律段、`thinking-boundary.md`、`plain-language-answers.md`
- 本檔的方法與分類表
- `skills/` 下所有非 Action Skill —— **最容易漂的四個**：`sunnydata-codebase-design`、`sunnydata-code-review/references/two-axis-review.md`、`sunnydata-testing` 接縫與反模式段、`sunnydata-design` 垂直切片段

**同名但刻意不同，別盲目同步**：

| | main | Pilot |
|---|---|---|
| wayfind | 地圖 `docs/maps/`，交棒 `sunnydata-design` | 地圖 `docs/document-system/maps/`，交棒 `/intake`／`/specify` |
| questionnaire | 獨立 skill，答覆落 spec/plan | `/intake` 的 reference，回填 ①需求決策 |
| 切片落腳處 | `sunnydata-design` Phase 2，原生 task | `/deliver` ＋ Excel ③ 切片看板 |

**完全不同步**：根目錄 `CLAUDE.md`、`.claude/CLAUDE.md`、`WORKFLOW.md`、`PLAYBOOK.md`、`skills/INDEX.md`（定位不同）、`rules/language-register.md`（POC 版無追溯 ID 與簽核邊界）、`VibeCoding_Workflow_Templates/`（含 `_meta/new_project_bootstrap.md`）。

## 沿革

| 日期 | 動作 | 結果 |
|---|---|---|
| 2026-08-05 | 從 Pilot 移植**通用工程紀律**（接縫詞彙、垂直切片、兩軸 review、TDD 反模式、context 衛生、wayfind、問卷、ADR 三條件閘）。不搬 Excel 看板、追溯 ID、簽核閘、證據閉環 | 未新增常駐規則，只加路由指標；211 行不變 |
| 2026-08-04 | 從 Pilot 移植消融後的 harness：刪 16 commands、18 output-styles、6 hooks、`context/`／`coordination/`／`taskmaster-data/`、7 份舊 rules | 常駐面 443 → 211（−52%）；`.claude/` 82,955 → 70,348 行、345 → 306 檔 |
