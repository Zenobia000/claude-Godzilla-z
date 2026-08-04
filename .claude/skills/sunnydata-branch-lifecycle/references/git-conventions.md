# Commit / PR 慣例與歷史恢復

按需載入。常駐的最小約束在 [`../../../rules/git-workflow.md`](../../../rules/git-workflow.md)；本檔是它指向的細則，**不重述**那邊已有的鐵律。

## Commit Message 細則

**第一步永遠是看專案怎麼寫。** `git log --oneline -10` 觀察平均 subject 長度、是否常用 body、是否走 Conventional Commits。「對的 commit message」相對於專案文化，不是絕對標準。

### Subject

- 祈使句、< 72 字元
- 禁止「fix」「update」「misc」等空泛詞
- 走 Conventional Commits 的專案：`type(scope): subject`
- 讓人不看 diff 也能猜中 80% 在做什麼

### Body 是按需寫，不是必填

Diff 已經是 WHAT 的單一真相源，重述 diff 是噪音。

| 該寫 body（任一即寫） | 不寫 body（任一即停手） |
| :--- | :--- |
| 動機非顯而易見（為什麼這樣修？為什麼選 A 不選 B？） | Subject 已完整說明 |
| 反直覺決策 | Diff 小且 self-evident |
| Breaking change／棄用 — **一定要寫**，標 `BREAKING:` 前綴 | 純格式化、純 rename、純依賴升級 |
| 微妙行為改變、跨檔案隱含影響、diff 看不出來的事 | OSS／squash-merge 專案（長解釋寫在 PR description） |
| 引用 issue／PR：`fixes #4415`、`refs #4461` | |

寫 body 時每一句都要帶新資訊，不重述 diff、不重述 subject；引用具體檔案行號比泛泛而談有用十倍。一個 commit 做一件事，可獨立 review、獨立 revert。

## Commit 歷史稽核（Phase 2 Step 2 使用）

| 檢查 | 失敗時的動作 |
| :--- | :--- |
| Subject > 72 字元或空泛（fix／update／misc） | 標示並建議 reword |
| 該寫 body 卻沒寫（見上表左欄） | 標示並建議 amend 或 squash |
| 單一 commit 動 10+ 個不相關檔案 | 建議拆成邏輯 commit |
| 多個 commit 做同一件事 | 建議 squash |

**這是 advisory，不是 gate。** 一律呈報稽核結果，但使用者可選擇照原樣進行。

## Pull Request

**前置條件**：測試通過、commit 稽核完成、self-review 過完整 diff、無 debug 殘留、diff < 400 行且 < 10 檔（超過先建議拆分，使用者仍可選擇單一 PR）。

**Body 四段**（專案有 PR 模板時以模板優先）：

```
## Background
<為什麼有這個 PR — 問題、觸發原因、動機。連結 issue：#NNN>

## Changes
<關鍵決策與取捨 — 不是檔案清單。為什麼選 A 不選 B>

## Impact
<Breaking change、migration 步驟、受影響模組。若無：「No breaking changes.」>

## Test Plan
- [ ] <具體驗證步驟>
```

寫 body 前先 `git diff <base>...HEAD` 與 `git log --oneline <base>..HEAD`，涵蓋**所有** commit 而非只看最新一筆。

**Merge 策略**：清晰 commit → merge；零散 commit → squash；純同步 → rebase。Merge 後刪除遠端分支。

## Tangled History 恢復策略

當 local main 已大幅領先 origin 且包含散落的工作：

| 場景 | 推薦策略 |
| :--- | :--- |
| 單人專案、無 review 需求 | 把 local main 整批包成「wrapper PR」推上 origin/main（含 `.gitattributes` 標準化等收尾改動） |
| 多人協作或需 review | Tag backup → reset main → cherry-pick 工作到 feature branch → stacked PR |
| 行尾飄移造成假 diff | 先 `git diff --ignore-all-space --stat` 驗證；若全是 EOL，加 `.gitattributes` 一次解決 |
