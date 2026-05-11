---
description: 完整自動化發佈流程 — 同步 CHANGELOG、建立 tag、推送、產生 GitHub Release。觸碰 git 與 GitHub 系統狀態，是正當的 command 工作流。
---

# `/release <version>` — Full Release Pipeline

> Touches multiple system states (git tag, remote push, GitHub Release). Per `rules/primitive-selection.md`, this is the right kind of work for a command.

## Usage

```
/release v5.5
```

If no version provided, AI suggests one based on Conventional Commits since last tag:
- Only `fix:` / `chore:` → patch bump
- Any `feat:` → minor bump
- Any `BREAKING CHANGE:` → major bump

## Pipeline (7 steps)

### Step 1: Pre-flight checks

- [ ] Branch is `main` or `dev` (configurable)
- [ ] Working tree clean (`git status --short` empty)
- [ ] Up to date with origin (`git fetch && git status` reports no behind/ahead)
- [ ] All tests pass (if test command configured)
- [ ] Linter passes

Abort with clear message if any fails.

### Step 2: Generate CHANGELOG via skill

Invoke `sunnydata-changelog-sync` skill with the target version. It:
- Scans `git log <last-tag>..HEAD`
- Scans accepted ADRs / implemented CRs in range
- Prepends release section to `CHANGELOG.md`
- Reports diff for review

### Step 3: Human review checkpoint 🛑

Show the diff. **Wait for user confirmation** before proceeding. User may:
- Approve as-is → continue
- Request edits → AI edits `CHANGELOG.md`, re-show diff
- Abort → no changes committed

### Step 4: Commit CHANGELOG.md

```bash
git add CHANGELOG.md
git commit -m "chore(release): v5.5"
```

Use commit type `chore(release): <version>` — short, conventional, doesn't pollute the changelog for next release.

### Step 5: Create annotated tag

```bash
git tag -a v5.5 -m "Release v5.5

<extract first ## section from CHANGELOG.md as tag message>
"
```

Annotated tags carry release notes accessible via `git show v5.5`.

### Step 6: Push branch + tag

```bash
git push origin <branch>
git push origin v5.5
```

If `.github/workflows/release.yml` exists, the tag push triggers automatic GitHub Release creation. Otherwise:

### Step 7: Create GitHub Release manually (fallback)

```bash
gh release create v5.5 \
  --title "v5.5" \
  --notes-from-tag
```

Or extract the release notes section from CHANGELOG.md:

```bash
# Extract the v5.5 section between this and the previous version header
gh release create v5.5 \
  --title "v5.5" \
  --notes "$(awk '/^## \[v5\.5\]/{f=1;print;next} f&&/^## \[/{exit} f{print}' CHANGELOG.md)"
```

## Output format

After each step, report:

```
✓ Step 1: Pre-flight passed (branch=dev, clean, synced)
✓ Step 2: CHANGELOG generated (27 commits → 4 categories, +1 ADR, +1 CR)
🛑 Step 3: Awaiting human review of CHANGELOG.md diff
   (run /release continue after approval)
```

After full success:

```
✓ Released v5.5
  Tag: refs/tags/v5.5 → 9f18fa7
  GitHub Release: https://github.com/Zenobia000/claude-Godzilla-z/releases/tag/v5.5
  CHANGELOG.md: updated (42 lines added)
```

## Edge cases

- **No previous tag**: skill defaults to all commits as "Unreleased"; suggest `v0.1.0` for first release
- **No commits since last tag**: abort with "nothing to release"
- **Dirty working tree**: abort; tell user to commit or stash
- **`gh` CLI not installed**: skip Step 7 (post-tag GitHub release); print manual command for user

## Forbidden in this command

- Do NOT skip Step 3 (human review). The CHANGELOG goes public; humans must approve.
- Do NOT force-push tags. If the tag already exists, abort and ask user to choose new version or delete old tag.
- Do NOT release from main without explicit confirmation if branch policy says dev → main flow.

## See also

- `.claude/skills/sunnydata-changelog-sync/SKILL.md` — does the changelog generation
- `.claude/rules/git-workflow.md` — Conventional Commits + branch policy
- `.github/workflows/release.yml` — automated GitHub Release on tag push (if present)
- `CHANGELOG.md` — Keep-a-Changelog formatted release history
