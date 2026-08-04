---
name: sunnydata-branch-lifecycle
description: Git branch lifecycle management — create isolated worktrees for feature work, then finish with structured merge/PR/cleanup options. Use when starting feature work that needs isolation or when implementation is complete and ready to integrate.
---

> **繁體中文說明**：本技能整合了 `sp-using-git-worktrees` 與 `sp-finishing-a-development-branch`，涵蓋分支從建立、隔離工作到完成整合的完整生命週期。

# Branch Lifecycle

## Overview

One skill for the full branch lifecycle: **Create → Work → Close**。Systematic isolation at the start + verified closure at the end = no lost work, no polluted branches.

已經在一般分支上（沒有 worktree）就直接跳到 Phase 2；Step 6 的 worktree 清理在沒有註冊 worktree 時自動 no-op。工作中途被打斷，走 Phase 2 的 Option 3 保留現場。

**Announce at start of Phase 1:** "I'm using the branch-lifecycle skill to set up an isolated workspace."
**Announce at start of Phase 2:** "I'm using the branch-lifecycle skill to complete this work."

## 與常駐規則的關係

本 skill **不定義** commit message 格式、PR body 結構或 push 時機——那些的權威在：

- 常駐鐵律（先開分支、多 session ref 驗證、destructive 先 backup tag、commit→push→PR 連貫）：[`../../rules/git-workflow.md`](../../rules/git-workflow.md)
- Commit / PR 慣例細則與歷史恢復：[`references/git-conventions.md`](references/git-conventions.md)

本 skill 只負責**流程編排**：什麼時候做哪一步、每步的前置條件、以及 worktree 的建立與清理。

---

## Phase 1: Create Worktree

完整步驟（目錄選擇、ignore 驗證、依賴安裝、baseline 測試）見 [`references/worktree-setup.md`](references/worktree-setup.md)。

**這一階段不可跳過的兩條紅線：**

1. 建立 project-local worktree（`.worktrees/` 或 `worktrees/`）前，**必須**先確認該目錄已被 `.gitignore` 忽略；未忽略就先補上並 commit。
2. **必須**跑一次 baseline 測試。測試失敗時回報並詢問，不得靜默繼續。

---

## Phase 2: Finish Branch

### Step 1: Verify Tests（強制前置）

```bash
npm test / cargo test / pytest / go test ./...
```

測試失敗就停止，在測試通過前不呈現任何整合選項。

### Step 2: Audit Commit History（強制前置）

```bash
git log --oneline <base-branch>..HEAD
```

依 [`references/git-conventions.md`](references/git-conventions.md) 的稽核表逐筆檢查，並呈報結果：

```
Commit history review (N commits):
✓ <sha> <subject>  — OK
✗ <sha> <subject>  — Subject too vague
✗ <sha> <subject>  — Breaking change 未在 body 說明

Recommend: squash/reword before merge?
```

**Advisory，不是 gate。** 一律呈報，但使用者可選擇照原樣進行。

### Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

或向使用者確認：「This branch split from main — is that correct?」

### Step 4: Decide Integration Path

**先看使用者是否已經表態。**

| 使用者已說 | 動作 |
| :--- | :--- |
| 「commit」「推上去」「PR 這個」「這段做完了」 | **直接走 Option 2，不呈現選單**——`rules/git-workflow.md` 的「commit→push→PR 為單一連貫操作」在此生效 |
| 「merge 回 main」 | 走 Option 1（merge 是共享分支寫入，執行前確認時機） |
| 「先放著」 | 走 Option 3 |
| **沒有表態** | 呈現下方四選項 |

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

呈現選單時不加說明，保持簡潔。

### Step 5: Execute Choice

#### Option 1 — Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>          # verify merged result
git branch -d <feature-branch>
```

Merge 後測試失敗時不得繼續。然後進入 Step 6。

#### Option 2 — Push and Create PR

**Pre-flight（呈現給使用者）：**

```
PR Pre-flight Check:
✓/✗ All tests passing
✓/✗ Commit history audited (Step 2)
✓/✗ Self-review of full diff completed
✓/✗ No debug code residue (console.log, TODO hacks)
✓/✗ PR size reasonable (< 400 lines diff, < 10 files)
```

超出大小上限時建議拆分，但使用者仍可選擇單一 PR。

**Execute:**

```bash
git push -u origin <feature-branch>
git diff <base-branch>...HEAD      # 寫 body 前先看完整 diff
git log --oneline <base-branch>..HEAD
gh pr create --title "..." --body "..."
```

PR body 結構（Background / Changes / Impact / Test Plan）與撰寫要求見 [`references/git-conventions.md`](references/git-conventions.md)；專案有 PR 模板時以模板優先。

建立後呼叫 `sunnydata-code-review` skill 做結構化 self-review。然後進入 Step 6。

#### Option 3 — Keep As-Is

回報：「Keeping branch `<name>`. Worktree preserved at `<path>`.」**不**清理 worktree。

#### Option 4 — Discard

先明確確認：

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

等待**確切**的 `discard` 字樣，其他輸入一律不執行。確認後：

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然後進入 Step 6。

### Step 6: Cleanup Worktree

**Options 1、2、4** — 檢查是否有註冊的 worktree，有就移除：

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>
```

**Option 3** — 保留 worktree，不動作。

## Red Flags

**Never:**
- Create a project-local worktree without verifying it is ignored
- Skip baseline test verification in Phase 1
- Present Phase 2 options while tests are failing
- Delete work (Option 4) without typed `discard` confirmation
- Force-push without explicit user request
- 使用者已表態要 PR 時還去問「要不要 push？」（違反 `rules/git-workflow.md`）

**Always:**
- Directory priority: existing > CLAUDE.md > ask
- Surface the commit audit even when advisory
- Clean up worktree for Options 1, 2, and 4 only

## Integration

**Called by:**
- `sunnydata-design`（Phase 1）— design 核准、要進入實作時 REQUIRED
- `sunnydata-design`（Phase 3）— 執行任務批次前後 REQUIRED

**Pairs with:**
- `sunnydata-code-review` — 在本 skill Phase 2 定案前先跑它的 Phase 1
- 專案 `CLAUDE.md`、貢獻指南、PR 模板 — repository-specific 慣例優先
