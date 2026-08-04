# Worktree 建立細則（Phase 1）

按需載入。何時進入 Phase 1、以及「必須驗證 worktree 目錄已被 ignore」這條紅線在 [`../SKILL.md`](../SKILL.md)。

## Directory Selection

Follow this priority order strictly.

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

**Step 3 — Ask user** (only if no directory and no CLAUDE.md preference):

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

## Safety Verification

**For project-local directories (`.worktrees` or `worktrees`) — MUST verify ignored:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

If NOT ignored: add the line to `.gitignore`, commit it, then proceed. This prevents worktree contents from being accidentally committed.

**For the global directory:** no `.gitignore` check needed — it is outside the project entirely.

## Creation Steps

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

**4. Verify clean baseline** — run project tests (`npm test` / `cargo test` / `pytest` / `go test ./...`):

- Tests pass: report ready.
- Tests fail: report failures, ask whether to proceed or investigate. Do not proceed silently.

**5. Report location:**

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check CLAUDE.md → ask user |
| Directory not ignored | Add to `.gitignore` + commit |
| Tests fail at baseline | Report failures + ask |
| No manifest file found | Skip dependency install |
