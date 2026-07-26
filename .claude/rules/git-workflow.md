# Git 工作流

本檔是全域 `~/.claude/CLAUDE.md` Git 規範在本專案的落地版本，內容與全域一致。它**取代**舊版強制 `WHY / WHAT / IMPACT` 三段式 commit body 的規定；body 依專案文化按需寫。

## 鐵律：先開分支，再動程式碼

- 收到開發任務時，第一步是 `git branch --show-current` + `git status`。
- 在 main/master 上 → **停止，詢問使用者分支策略**。
- 有未提交變更 → **停止，詢問使用者先 commit 還是放棄**。
- 使用者沒指定分支就要改 code → **停止，詢問使用者**。
- 禁止 `git stash` 作為工作流替代品。
- 分支命名：`<type>/<short-description>`（如 `feat/user-auth`、`fix/market-data-cache`）。

## 多 Session 並行協調

使用者可能同時跑多個 Claude Code session 在同一個 repo。**任何 git 寫操作前必須驗證 ref 沒被別處推進**，否則會產生 duplicate cherry-pick、stale branch、ahead-of-origin main 等問題。

執行 commit／branch／merge／rebase／cherry-pick／push 前：

- `git branch --show-current` — 確認分支沒換
- `git log --oneline -3` — 確認 tip 沒移動
- `git status` — 確認工作樹預期狀態
- `ps aux | grep [g]it` — 是否有別的 git process 在跑

警示訊號（任一就 STOP 並詢問使用者）：

- 工作樹有不認得的 modified／untracked 檔
- duplicate commit subject 但不同 SHA（cherry-pick 跨 session 殘留）
- 分支 tip 跟你上次看到的不同
- 出現未追蹤的 backup tag 或 sibling branch
- HEAD 指向不認得的 commit

## Destructive 操作必先 backup tag

執行 `reset --hard`、`push --force`、`branch -D`、`rebase` 前必須先：

```bash
git tag -a backup/<branch>-<YYYY-MM-DD> -m '安全快照, tip <oid>'
```

恢復路徑：`git reset --hard backup/<branch>-<YYYY-MM-DD>`。

## Tangled History 恢復策略

當 local main 已大幅領先 origin 且包含散落的工作：

| 場景 | 推薦策略 |
| :--- | :--- |
| 單人專案、無 review 需求 | 把 local main 整批包成「wrapper PR」推上 origin/main（含 .gitattributes 標準化等收尾改動）|
| 多人協作或需 review | Tag backup → reset main → cherry-pick 工作到 feature branch → stacked PR |
| 行尾飄移造成假 diff | 先 `git diff --ignore-all-space --stat` 驗證；若全是 EOL，加 `.gitattributes` 一次解決 |

## Commit Message（隨專案文化調整）

**第一步：先看專案怎麼寫。** Commit 前必跑 `git log --oneline -10` 觀察該專案的 commit 風格；平均 subject 長度、是否常用 body、是否走 Conventional Commits，都要符合既有慣例。「對的 commit message」是相對於專案文化，不是絕對標準。

**Subject 永遠的鐵律**

- 祈使句、< 72 字元
- 禁止「fix」「update」「misc」等空泛詞
- 走 Conventional Commits 慣例的專案：`type(scope): subject`（看 git log 確認）
- Subject 必須讓人不看 diff 也能猜中 80% 在做什麼

**Body 是按需寫，不是必填。** Diff 已經是 WHAT 的單一真實來源，重述 diff 是噪音。

該寫 body 的情境（任一即寫）：

- 動機非顯而易見（為什麼這樣修？為什麼選 A 不選 B？）
- 反直覺決策
- Breaking change／棄用 — **一定要寫**，並標 `BREAKING:` 前綴
- 微妙的行為改變、跨檔案的隱含影響、diff 看不出來的事
- 引用 issue／PR：`fixes #4415`、`refs #4461`

不寫 body 的情境（任一即停手）：

- Subject 已經完整說明
- Diff 小且 self-evident
- 純格式化、純 rename、純依賴升級
- OSS／squash-merge 專案 — 長解釋寫在 PR description，不是 commit body

寫 body 時每一句都要帶新資訊，不重述 diff、不重述 subject；引用具體檔案行號比泛泛而談有用十倍。一個 commit 做一件事，可獨立 review、獨立 revert。

## Pull Request

- 前置條件：測試通過、commit 審計、self-review diff、無 debug 殘留、< 400 行
- Body 結構：Background / Changes / Impact / Test Plan
- Merge 策略：清晰 commit → merge、零散 commit → squash、同步 → rebase
- Merge 後刪除遠端分支

## Commit → Push → PR 為單一連貫操作

當使用者要求「commit」「提交」「PR 這個」「推上去」或表達「這段工作做完」時，預設一氣呵成執行：

1. `git commit`
2. `git push -u origin <branch>`
3. `gh pr create`

**禁止在中間插入「要不要 push？」「要不要開 PR？」這類詢問。**

例外（明確中斷）：

- 使用者明說「先 commit 不要 push」或「push 但暫不開 PR」
- merge 動作（共享分支寫入，必須讓使用者確認時機）
- destructive 操作（force-push、push 到保護分支等）

## 程式碼 ↔ 文件同步（強制）

**實作 code 與更新 docs 屬同一個任務、同一個 PR。** 寫完 code 立刻盤點受影響的 docs 並一併修改，禁止「以後再補文件」——之後再補幾乎都會忘，最後產生 doc drift。

每次 commit 前 + 每次 PR 前自問：

```
[ ] 這個 commit 動了哪幾類 code？
[ ] 對應觸發表，需要動哪些 docs？
[ ] 已動 / 已確認不需動 / 還沒動？
[ ] single-source-of-truth（docs/document-system/、追溯矩陣、狀態）已更新？
[ ] ADR-worthy 決策已寫或已 cross-ref？
```

本專案觸發對映（doc 名稱依 `docs/document-system/` 與 `VibeCoding_Workflow_Templates/` 結構）：

| Code 變更類型 | 必查 docs |
| :--- | :--- |
| 新模組 / 重大目錄重組 | lld（專案結構與依賴段）、`docs/document-system/architecture.md` 權威矩陣 |
| ADR-worthy 決策（換引擎、升版、改通道等）| adr、`docs/document-system/INDEX.md` |
| Schema / DDL / 資料契約變更 | sad 資料段、db_design、api_spec／openapi.yaml、追溯矩陣 |
| 依賴升級（pyproject / package.json）| prd 依賴清單、相關 adr |
| 環境變數新增 / 改名 | `.env.example`、deployment_and_operations 的環境變數表 |
| 新 API endpoint / CLI 子命令 | api_spec／openapi.yaml、README、CLI manual |
| 新測試類別（performance / e2e）| sds 測試段、test_plan |
| 部署 / Docker / 拓撲變更 | deployment_and_operations、runbook |
| 需求 / 驗收 / 追溯變化 | intake 需求登錄、`docs/document-system/` 追溯矩陣（永遠要動）|
| 跨多檔重構 / 結構大改 | 受影響文件的版本 banner、lld 專案結構段 |

例外（允許延後同步）：

- 純內部重構，無對外介面、無架構文件描述（但仍要更新追溯／狀態）
- WIP commit（branch 內 squash 前）— PR 提出前必須補齊
- dependency lock 自動更新（uv.lock、package-lock.json 等）

## 與 Golden Rules 的關係

本檔是操作規範；不覆蓋 [golden-rules.md](golden-rules.md)。破壞性或影響外部系統的動作，仍受 golden-rules 第 3 條「先確認精確範圍與授權」約束。
