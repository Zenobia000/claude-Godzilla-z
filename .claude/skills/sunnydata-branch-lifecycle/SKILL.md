---
name: sunnydata-branch-lifecycle
description: Git branch lifecycle management — create isolated worktrees for feature work, then finish with structured merge/PR/cleanup options. Use when starting feature work that needs isolation or when implementation is complete and ready to integrate.
---

> **繁體中文說明**：本技能整合了 `sp-using-git-worktrees` 與 `sp-finishing-a-development-branch` 兩個技能，涵蓋分支從建立、隔離工作到完成整合的完整生命週期。

# Branch Lifecycle

## Overview

One skill for the full branch lifecycle: **Create → Work → Close**

- **Phase 1** sets up an isolated git worktree so you can work without disturbing the current workspace.
- **Phase 2** verifies completion, presents structured integration options, and cleans up.

**Core principle:** Systematic isolation at the start + verified closure at the end = no lost work, no polluted branches.

**Announce at start of Phase 1:** "I'm using the branch-lifecycle skill to set up an isolated workspace."
**Announce at start of Phase 2:** "I'm using the branch-lifecycle skill to complete this work."

---

## Phase 1: Create Worktree

### Directory Selection

Follow this priority order strictly:

**Step 1 — Check existing directories:**

```bash
ls -d .worktrees 2>/dev/null   # preferred (hidden)
ls -d worktrees 2>/dev/null    # alternative
```

If found, use that directory. If both exist, `.worktrees` wins.

**Step 2 — Check CLAUDE.md:**

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

If a preference is specified, use it without asking.

**Step 3 — Ask user (only if no directory and no CLAUDE.md preference):**

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

### Safety Verification

**For project-local directories (`.worktrees` or `worktrees`) — MUST verify ignored:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If NOT ignored:
1. Add the appropriate line to `.gitignore`
2. Commit the change
3. Then proceed

This prevents worktree contents from being accidentally committed to the repository.

**For global directory (`~/.config/superpowers/worktrees`):** No `.gitignore` check needed — it is outside the project entirely.

### Creation Steps

**1. Detect project name:**

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

**2. Create worktree with new branch:**

```bash
# Project-local
git worktree add .worktrees/<branch-name> -b <branch-name>

# Global
git worktree add ~/.config/superpowers/worktrees/$project/<branch-name> -b <branch-name>

cd <worktree-path>
```

**3. Auto-detect and install dependencies:**

```bash
if [ -f package.json ];      then npm install; fi
if [ -f Cargo.toml ];        then cargo build; fi
if [ -f requirements.txt ];  then pip install -r requirements.txt; fi
if [ -f pyproject.toml ];    then poetry install; fi
if [ -f go.mod ];            then go mod download; fi
```

**4. Verify clean baseline** — run project tests:

```bash
npm test / cargo test / pytest / go test ./...
```

- Tests pass: report ready.
- Tests fail: report failures, ask whether to proceed or investigate. Do not proceed silently.

**5. Report location:**

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

### Phase 1 Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → ask user |
| Directory not ignored | Add to `.gitignore` + commit |
| Tests fail at baseline | Report failures + ask |
| No manifest file found | Skip dependency install |

---

## Phase 2: Finish Branch

### Step 1: Verify Tests (mandatory pre-condition)

```bash
npm test / cargo test / pytest / go test ./...
```

If tests fail: stop. Do not present options until tests pass.

### Step 2: Audit Commit History (mandatory pre-condition)

Before presenting options, review the commit log for quality:

```bash
git log --oneline <base-branch>..HEAD
```

**Use this advisory commit-quality review (project-specific conventions take precedence):**

| Check | Fail action |
|-------|-------------|
| Subject > 72 chars or vague ("fix", "update", "misc") | Flag to user, suggest reword |
| Missing body (WHY/WHAT/IMPACT) | Flag to user, suggest amend or squash |
| Single commit touches 10+ unrelated files | Suggest splitting into logical commits |
| Multiple commits do the same thing | Suggest squash |

**Present audit summary to user:**

```
Commit history review (N commits):
✓ <sha> <subject>  — OK
✗ <sha> <subject>  — Missing WHY in body
✗ <sha> <subject>  — Subject too vague

Recommend: squash/reword before merge?
```

User may choose to proceed as-is or fix. Do not block — this is advisory, not a gate. But always surface the audit.

### Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or confirm with user: "This branch split from main — is that correct?"

### Step 4: Present Exactly 4 Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Do not add explanation — keep options concise.

### Step 5: Execute Choice

#### Option 1 — Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>          # verify merged result
git branch -d <feature-branch>
```

Then: proceed to Step 5 (cleanup worktree).

#### Option 2 — Push and Create PR

**Pre-flight checklist (mandatory — present to user before proceeding):**

```
PR Pre-flight Check:
✓/✗ All tests passing
✓/✗ Commit history audited (Step 2)
✓/✗ Self-review of full diff completed
✓/✗ No debug code residue (console.log, TODO hacks)
✓/✗ PR size reasonable (< 400 lines diff, < 10 files)
```

If PR exceeds size limits, suggest splitting:
```
This PR touches <N> files with <M> lines changed.
Consider splitting into smaller, focused PRs:
1. <suggested split 1>
2. <suggested split 2>

Proceed as single PR anyway?
```

**Execute:**

```bash
git push -u origin <feature-branch>
```

Review full diff before writing PR body:

```bash
git diff <base-branch>...HEAD
```

Analyze ALL commits (not just the latest) to write an accurate summary:

```bash
git log --oneline <base-branch>..HEAD
```

Create a PR using the repository template when present; otherwise use this
project-neutral baseline:

```bash
gh pr create --title "<type>(<scope>): <subject>" --body "$(cat <<'EOF'
## Background
<Why this PR exists — the problem, what triggered it, the motivation>
<Link to issue: #NNN>

## Changes
<Key decisions and tradeoffs — not a file list>
<Why approach A over B>

## Impact
<Breaking changes, migration steps, affected modules>
<If none: "No breaking changes.">

## Test Plan
- [ ] <specific verification step>
- [ ] <specific verification step>
EOF
)"
```

After PR is created, invoke `sunnydata-code-review` skill for structured self-review.

Then: proceed to Step 5 (cleanup worktree).

#### Option 3 — Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

Do NOT cleanup worktree.

#### Option 4 — Discard

Confirm first with explicit details:

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word `discard`. No other input proceeds.

If confirmed:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: proceed to Step 5 (cleanup worktree).

### Step 6: Cleanup Worktree

**For Options 1, 2, 4** — check if a worktree is registered, then remove it:

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>
```

**For Option 3** — keep worktree, do nothing.

### Phase 2 Quick Reference

| Option | Merge | Push | Keep Worktree | Delete Branch |
|--------|-------|------|---------------|---------------|
| 1. Merge locally | yes | no | no | yes (soft) |
| 2. Create PR | no | yes | yes | no |
| 3. Keep as-is | no | no | yes | no |
| 4. Discard | no | no | no | yes (force) |

---

## Quick Reference: When to Use Each Phase

```
Need to start isolated feature work?
  └─ Yes → Phase 1: Create Worktree
       └─ Work until implementation complete
            └─ All tests passing? → Phase 2: Finish Branch

Already on a regular branch (no worktree)?
  └─ Go directly to Phase 2 (skip Phase 1)
       └─ Step 5 worktree cleanup will no-op if no worktree is registered

Interrupted mid-work on a worktree?
  └─ Phase 2, Option 3 (Keep as-is) — return later
```

---

## Red Flags

**Never:**
- Create a project-local worktree without verifying it is ignored
- Skip baseline test verification in Phase 1
- Proceed to Phase 2 options while tests are failing
- Delete work (Option 4) without typed `discard` confirmation
- Force-push without explicit user request
- Proceed with failing tests after merge (Option 1)

**Always:**
- Directory priority: existing > CLAUDE.md > ask
- Auto-detect dependencies from manifest files
- Present exactly 4 options in Phase 2
- Clean up worktree for Options 1, 2, and 4 only

---

## Integration

**Called by:**
- `sunnydata-design` (Phase 1) — REQUIRED when design approved and implementation follows
- `sunnydata-design` (Phase 3) — REQUIRED before and after executing task batches
- `sp-subagent-driven-development` — REQUIRED bookends for task execution

**Pairs with:**
- `sunnydata-code-review` skill — run Phase 1 of sunnydata-code-review before finalizing Phase 2 here
- Project `CLAUDE.md`, contribution guide, and PR template — repository-specific
  commit and PR conventions
