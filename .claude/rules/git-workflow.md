# Git 工作流

## Commit Message 格式

```
<type>(<optional scope>): <subject>

<WHY — 背景與動機>

<WHAT — 關鍵變更摘要>

<IMPACT — 影響範圍與破壞性變更>
```

Types: feat, fix, refactor, docs, test, chore, perf, ci

## AI 協作時代的 Commit 分層策略

Commit message 的讀者不只是人 — **AI 是最頻繁讀 git log 的消費者**。好的 commit history 讓 AI 進入新 session 時能快速重建專案脈絡，站在前人的肩膀上。

### 核心原則：type prefix 是 AI 的索引

AI 用 `git log --oneline` 掃描歷史時，type prefix 告訴它該不該展開讀 body：

| Type | AI 讀取深度 | Body 長度 | 說明 |
|---|---|---|---|
| `feat` | 讀 subject + body | WHY/WHAT/IMPACT 完整 | 有架構決策，值得深讀 |
| `fix` | 讀 subject + root cause | WHY + 一句 root cause | 知道修了什麼、根因是什麼 |
| `refactor` | 讀 subject + 動機 | WHY 就好 | 為什麼重構比怎麼重構重要 |
| `perf` | 讀 subject + 數據 | before/after benchmark | 數據說話 |
| `docs`, `test` | 只讀 subject | 一行夠了 | AI 掃描跳過 |
| `chore`, `ci` | 只讀 subject | 一行夠了 | AI 掃描跳過 |

### 學徒模式連動（選用）

使用 Apprentice output style 時，`feat` commit 的 body 可附規模燈號，讓未來 AI session 直接從 git history 重建決策脈絡：

```
feat(billing): add Strategy Pattern for multi-plan billing

🟢 MVP-appropriate: Strategy over if-else even with 2 plans —
cost of one interface + two impls is lower than future if-else
untangling (OCP, Rule of Three).

Upgrade path: 🟡 Plugin Architecture when plans exceed 5 and
require dynamic loading.
```

未來 AI 讀到這段，不需要問任何人就知道：
1. 當初的決策是什麼
2. 為什麼在 MVP 階段就這樣做
3. 什麼條件下該升級

## Commit Message 品質標準

### Subject（第一行）
- 說明做了什麼，限 72 字元
- 用祈使句：「add」而非「added」或「adds」

### Body（依 type 分層）

**`feat` / 架構決策 — 完整 WHY/WHAT/IMPACT：**

**WHY（為什麼）**— 第一段永遠回答動機：
- 解決什麼問題？現狀有什麼痛點？
- 什麼事件觸發了這次變更？
- 若不做會怎樣？

**WHAT（做了什麼）**— 第二段說明關鍵決策：
- 選了方案 A 而非 B 的原因
- 重要取捨（tradeoff）
- 不是 diff 的重複，是 diff 無法表達的上下文

**IMPACT（影響）**— 第三段列出波及範圍：
- 哪些模組/功能受影響
- 破壞性變更（breaking changes）須明確標記
- 後續需要的動作（如 migration）

**`fix` — WHY + root cause：**

```
fix(auth): prevent token reuse after rotation

Root cause: refresh token was not invalidated in Redis after
issuing a new one, allowing replay within the old TTL window.
```

**`refactor` — WHY 就好：**

```
refactor(billing): extract pricing rules into dedicated module

Pricing logic was scattered across 3 services, making it
impossible to unit test billing rules in isolation.
```

**`docs`, `test`, `chore`, `ci` — subject 一行即可：**

```
docs(api): update authentication endpoint examples
test(billing): add edge case for zero-amount invoices
chore(deps): bump fastapi to 0.115.0
```

### 鐵律
- 想像一個**從沒看過這個 repo 的 AI agent** 讀你的 commit message — 它能從 subject 判斷要不要深入嗎？
- 一個 commit 做一件事 — 大型變更拆成多個邏輯 commit
- 每個 commit 可獨立 review、獨立 revert
- 禁止「fix」「update」「misc」等無意義 subject

## 分支策略

### 保護分支
- `main`/`master` 禁止直接 commit — 所有變更透過 PR 合入
- 發現在保護分支上時，**立即停止**並詢問使用者

### 命名慣例

格式：`<type>/<short-description>`

範例：
- `feat/user-auth`
- `fix/market-data-cache`
- `refactor/api-response-format`
- `chore/update-dependencies`

### 分支生命週期

```
main ──┬── feat/xxx ──── PR ──→ main
       ├── fix/yyy  ──── PR ──→ main
       └── refactor/zzz ─ PR ──→ main
```

- 一個分支做一件事 — 與 commit 原則一致
- 分支壽命越短越好 — 長壽命分支 = merge conflict
- 完成後載入 sunnydata-branch-lifecycle skill 收尾

### 禁止

- 禁止 `git stash` 作為工作流替代品（stash 只用於臨時中斷）
- 禁止在功能分支混做不相關任務
- 禁止 force push 到共享分支（除非明確請求且確認影響）

## Pull Request 流程

### 前置條件（建立 PR 前必須全部滿足）

- [ ] 所有測試通過（unit + integration + E2E）
- [ ] commit 歷史已審計（WHY/WHAT/IMPACT body 完整）
- [ ] 已自我 review 完整 diff：`git diff <base>...HEAD`
- [ ] 無殘留 debug code（console.log、TODO hack、commented-out code）
- [ ] PR 大小合理 — 超過 400 行 diff 或 10+ 檔案時，考慮拆分

### 品質標準

標題：`<type>(<scope>): <subject>`（< 70 字元）

Body 結構（每個區段必填）：

| 區段 | 內容 |
| :--- | :--- |
| **Background** | 為什麼做這個 PR — 問題、動機、關聯 issue |
| **Changes** | 核心決策和取捨（不是 file list） |
| **Impact** | 破壞性變更、migration、受影響模組 |
| **Test Plan** | 具體驗證步驟 checklist |

### 提交步驟

1. 確認前置條件全部滿足
2. `git push -u origin <branch>`
3. `gh pr create`（使用上述 Body 結構）
4. 載入 sunnydata-code-review skill 進行 self-review
5. 指定 reviewer（如適用）

### Merge 策略

| 場景 | 策略 | 理由 |
| :--- | :--- | :--- |
| 功能分支（1-3 commits，邏輯清晰） | Merge commit | 保留完整歷史 |
| 功能分支（多個零散 commit） | Squash merge | 合併為一個乾淨 commit |
| 長期分支同步 | Rebase | 保持線性歷史 |
| Hotfix | Merge commit | 可追溯修復點 |

Merge 後刪除遠端分支：`git push origin --delete <branch>`

## 版本管理

- 使用語義化版本（MAJOR.MINOR.PATCH）
- 重要版本建立 git tag
- 維護 CHANGELOG.md（依 Keep a Changelog 格式）

## Release 自動化

不要手動跑 `git tag` + 手動寫 CHANGELOG。使用 `/release <version>` command：

1. Pre-flight 檢查（branch、clean tree、tests）
2. 呼叫 `sunnydata-changelog-sync` skill 從 Conventional Commits + ADR + CR 自動產生 release notes
3. 🛑 人類審核 CHANGELOG diff
4. Commit CHANGELOG（`chore(release): vX.Y.Z`）
5. 建立 annotated tag
6. Push branch + tag
7. `.github/workflows/release.yml` 偵測 tag 推送 → 自動建立 GitHub Release

Conventional Commits 規範強制（見上方 §commit type）— 違反規範的 commit 會出現在 changelog 的「Other Changes」段，提醒下次規範化。
