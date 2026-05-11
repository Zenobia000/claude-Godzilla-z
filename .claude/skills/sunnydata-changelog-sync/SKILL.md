---
name: sunnydata-changelog-sync
description: Generate or update CHANGELOG.md from git history + ADR + CR docs in Keep-a-Changelog format. Scans conventional commit messages since the last release tag, plus newly accepted ADRs and implemented CRs, then prepends a new release section. Triggers on 'generate changelog', 'update CHANGELOG', '產生 changelog', 'release notes', 'sync changelog', 'changelog from commits'.
stability-tier: tooling
---

# Changelog Sync

## What this skill does

Produces a Keep-a-Changelog-formatted release section from three sources and prepends it to `CHANGELOG.md`:

1. **Conventional Commits** in `git log <last-tag>..HEAD`
2. **ADRs** at `docs/1-decisions/ADR-*.md` with `status: accepted` whose creation date falls in the release range
3. **CRs** at `docs/4-exploration/CR-*.md` with `status: implemented` in the range

## When to invoke

- Before creating a release tag (orchestrated by `/release` command)
- On demand to preview what changes are unreleased
- After a sprint to verify changelog is in sync

## Procedure

### Step 1: Determine release range

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  RANGE="HEAD"  # no prior tag — include all history
  echo "No previous tag found; treating all commits as Unreleased"
else
  RANGE="$LAST_TAG..HEAD"
  echo "Range: $RANGE"
fi
```

Ask user for the **new version number** if not provided. Default suggestion: bump minor (`v5.4` → `v5.5`) unless commits contain `BREAKING CHANGE:` (bump major) or only `fix:` (bump patch).

### Step 2: Parse commits

```bash
git log $RANGE --no-merges --format="%h|%s|%b" -z | tr '\0' '\n'
```

For each commit, parse conventional format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Type → category mapping:

| Conventional type | Changelog category |
|---|---|
| `feat:` | ### Added |
| `fix:` | ### Fixed |
| `perf:` | ### Changed (performance) |
| `refactor:` with `BREAKING CHANGE:` in body | ### Changed + flag as breaking |
| `refactor:` (non-breaking) | ### Changed |
| `security:` | ### Security |
| `deprecate:` or `chore:` mentioning deprecation | ### Deprecated |
| Body contains `BREAKING CHANGE:` | Add to ### Removed or note in relevant section with ⚠️ |
| `docs:`, `style:`, `test:`, `ci:`, `build:`, `chore:` | (skip unless user-facing) |
| `revert:` | ### Reverted |

### Step 3: Scan ADR and CR docs

```bash
# ADRs accepted in range — find by frontmatter date
find docs/1-decisions -name "ADR-*.md" 2>/dev/null | while read adr; do
  date=$(grep "^date:" "$adr" | awk '{print $2}')
  status=$(grep "^status:" "$adr" | awk '{print $2}')
  # Include if status: accepted AND date >= last-tag-date
  ...
done
```

Same for CRs (`docs/4-exploration/CR-*.md` with `status: implemented`).

These get their own subsection:

```markdown
### Architectural Decisions
- [ADR-0001](docs/1-decisions/ADR-0001-...md): <title>

### Change Requests Implemented
- [CR-0042](docs/4-exploration/CR-0042-...md): <title>
```

### Step 4: Format release section

```markdown
## [v5.5] - 2026-05-11

### Added
- feat(templates): add flow-index template (project-wide flow aggregation) ([fd932c5](../../commit/fd932c5))
- feat(skills): add sunnydata-auto-regen ([6c464d0](../../commit/6c464d0))

### Changed
- refactor(templates): segregate web-frontend templates into extras/ ([c583d52](../../commit/c583d52))

### Fixed
- fix(hooks): broaden post-write matcher to Edit/MultiEdit ([30092e0](../../commit/30092e0))

### Removed
- chore(commands): remove 6 pure-indirection commands superseded by skills ([4a3bae7](../../commit/4a3bae7))

### Architectural Decisions
- [ADR-0001](docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md): Frontend template tier realignment

### Change Requests Implemented
- [CR-0001](docs/4-exploration/CR-0001-frontend-template-tier-realignment.md): Frontend template tier realignment

[v5.5]: https://github.com/<org>/<repo>/compare/v5.4...v5.5
```

### Step 5: Prepend to CHANGELOG.md

Read existing `CHANGELOG.md`. Find the line after the header section (typically after "All notable changes..." paragraph). Insert the new release section there. Preserve the rest.

If `CHANGELOG.md` doesn't exist, create it with the standard Keep-a-Changelog header:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

(new release section here)
```

### Step 6: Report

Show diff of CHANGELOG.md and stop (do not auto-commit). User reviews, then commits and tags via `/release` command.

## Edge cases

- **No previous tag**: treat all commits as Unreleased; suggest `v0.1.0` or `v1.0.0` as first tag
- **No commits since last tag**: report "nothing to release"; offer to bump `[Unreleased]` placeholder
- **Commits without conventional format**: list under "### Other Changes" with a warning
- **BREAKING CHANGE without explicit type**: flag in summary and prompt user to confirm major bump

## Idempotency

Running twice without new commits should produce identical output (no duplicate sections). The skill detects existing `## [vX.Y]` headers and refuses to re-add.

## What this skill does NOT do

- Does **not** create git tags (that's `/release` command's job)
- Does **not** push to remote (orchestration layer)
- Does **not** publish to GitHub Releases (handled by CI workflow or `gh release create`)
- Does **not** modify ADRs / CRs / git history (read-only on those)

## Output style

Final summary table:

| Source | Count | Category breakdown |
|---|---|---|
| Commits | 27 | feat: 8, fix: 4, refactor: 9, chore: 6 |
| ADRs accepted | 1 | ADR-0001 |
| CRs implemented | 1 | CR-0001 |
| Lines added to CHANGELOG.md | 42 |

Then show the inserted section verbatim for user review.

## See also

- `.claude/commands/release.md` — orchestration command
- `.claude/rules/git-workflow.md` — Conventional Commits convention
- `VibeCoding_Workflow_Templates/INDEX.md` — template-level version history (different from release changelog)
