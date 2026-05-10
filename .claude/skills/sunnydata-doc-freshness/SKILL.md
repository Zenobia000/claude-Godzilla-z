---
name: sunnydata-doc-freshness
description: Detect stale documentation in docs/2-contracts/ by comparing each file's last-synced-with frontmatter against the latest commit on its source-paths. Triggers on 'check doc freshness', 'find stale docs', '檢查文件鮮度', 'doc drift audit', 'are docs in sync with code'.
stability-tier: tooling
---

# Doc Freshness Audit

## What this skill does

Walks `docs/2-contracts/**/*.md` and `docs/2-contracts/**/*.yaml`, parses each file's frontmatter, and reports which contract docs have fallen behind the code they describe.

## Required frontmatter shape

This skill assumes each contract doc carries:

```yaml
---
last-synced-with: <git-commit-sha>
sync-source: code | doc
source-paths:
  - src/api/users.py
  - src/models/user.py
synced-at: 2026-05-10
---
```

Files without this frontmatter are reported as "unmanaged" so the user can decide whether they belong in tier 2 at all.

## Procedure

1. **Verify location**: confirm `docs/2-contracts/` exists. If not, exit with note that the project hasn't adopted the v4 layered docs structure (point to `VibeCoding_Workflow_Templates/HOW-TO-INSTANTIATE.md`).

2. **Enumerate candidates**:
   ```bash
   find docs/2-contracts -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.yml" \)
   ```

3. **Per file, parse frontmatter**:
   - Extract `last-synced-with`, `source-paths` (list).
   - If frontmatter missing or fields absent → mark UNMANAGED.

4. **Per source-path, get latest commit**:
   ```bash
   git log -1 --format=%H -- <source-path>
   ```

5. **Compare**:
   - If `last-synced-with` == latest source commit → FRESH.
   - If `last-synced-with` is an ancestor of latest source commit → STALE; count commits between.
   - If `last-synced-with` is unknown to git → BROKEN (probably squashed).
   - If source path doesn't exist → ORPHAN.

6. **Output a single table** sorted by severity:

| Status | Doc | Source | Commits behind | Suggested action |
|---|---|---|---|---|
| BROKEN | docs/2-contracts/api/v1.md | src/api/v1.py | n/a | Re-baseline frontmatter |
| ORPHAN | docs/2-contracts/legacy.md | src/legacy/ | n/a | Move to archive or delete |
| STALE | docs/2-contracts/payment.md | src/payment/ | 12 | Regenerate via vibecoding-write-api-contract |
| UNMANAGED | docs/2-contracts/notes.md | — | — | Add frontmatter or move out of 2-contracts |
| FRESH | docs/2-contracts/auth.md | src/auth/ | 0 | None |

7. **Recommend remediation per row** — point to the relevant `vibecoding-*` skill for regeneration, or to the auto-frontmatter post-write hook for re-baselining.

## What this skill does NOT do

- It does **not** auto-update frontmatter — that's the post-write hook's job.
- It does **not** regenerate stale docs — that's the relevant `vibecoding-write-*` skill's job.
- It does **not** scan tier 0/1/3/4/5 docs — those tiers have different staleness semantics; tier 2 is the only one with a hard sync contract.

## Output style

Single markdown table, severity-sorted, no preamble. If everything is FRESH, say so in one line.

## When to invoke

- Weekly maintenance pass
- Before any release / deployment
- After a large refactor
- When the user asks "is X doc still accurate?"
- When `vibecoding-write-api-contract` or `vibecoding-write-db-schema` is about to write — to warn if the existing version is stale and needs ack first
