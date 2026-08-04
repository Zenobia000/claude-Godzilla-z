# Git 工作流

本檔只留**每次 git 操作都成立、而且與模型預設行為不同**的約束。commit message 細則、PR 前置與 body 結構、tangled history 恢復策略屬按需內容，見 [`../skills/sunnydata-branch-lifecycle/references/git-conventions.md`](../skills/sunnydata-branch-lifecycle/references/git-conventions.md)——要 commit／開 PR 時才載入。

## 鐵律：先開分支，再動程式碼

- 收到開發任務的第一步：`git branch --show-current` + `git status`。
- 在 main/master 上、有未提交變更、或使用者沒指定分支就要改 code → **停止並詢問**，不自行決定。
- 不用 `git stash` 當工作流替代品。分支命名 `<type>/<short-description>`。

## 多 Session 並行協調

使用者可能同時跑多個 Claude Code session 在同一個 repo。**任何 git 寫操作前先驗證 ref 沒被別處推進**：`git branch --show-current`、`git log --oneline -3`、`git status`。

任一警訊出現就 STOP 並詢問：工作樹有不認得的變更、同 subject 不同 SHA 的 commit（跨 session cherry-pick 殘留）、分支 tip 與上次所見不同、出現未追蹤的 backup tag 或 sibling branch、HEAD 指向不認得的 commit。

## Destructive 操作先打 backup tag

`reset --hard`、`push --force`、`branch -D`、`rebase` 之前：

```bash
git tag -a backup/<branch>-<YYYY-MM-DD> -m '安全快照, tip <oid>'
```

恢復路徑：`git reset --hard backup/<branch>-<YYYY-MM-DD>`。

## Commit → Push → PR 為單一連貫操作

使用者說「commit」「提交」「PR 這個」「推上去」或表達「這段工作做完」時，預設**一氣呵成**執行 `git commit` → `git push -u origin <branch>` → `gh pr create`。**禁止在中間插入「要不要 push？」「要不要開 PR？」。**

例外（明確中斷）：使用者明說只要 commit 或只要 push；merge 到共享分支；destructive 操作。

## Commit Message 的兩條常駐約束

1. 寫之前先 `git log --oneline -10` 對齊該專案的既有風格。
2. **Body 按需寫，不是必填**——diff 已經是 WHAT 的單一真相源。此條**取代**全域 `~/.claude/CLAUDE.md` 的 `WHY / WHAT / IMPACT` 三段式強制規定。

## 程式碼 ↔ 文件同步

實作 code 與更新 docs 屬**同一個任務、同一個 PR**，不接受「以後再補文件」。哪一類變更要動哪些文件，見 [`../skills/deliver/references/doc-sync-triggers.md`](../skills/deliver/references/doc-sync-triggers.md)。
