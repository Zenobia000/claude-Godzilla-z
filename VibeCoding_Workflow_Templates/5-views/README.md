# Tier 5 — Views

> Derived from code. **Never hand-maintained.** Stale by default.

## What lives here

Diagrams and structural snapshots that **describe code as it currently is**:
- Project structure trees
- File / module dependency graphs
- Class relationship diagrams (UML)
- Frontend component trees
- Information architecture maps

## What does NOT live here

- The *intended* architecture → tier 1 (decisions)
- The *contract* a module exposes → tier 2 (contracts)
- The *process* for restructuring → tier 3 (process)

## How AI should use this tier

**Treat these documents as caches, not sources of truth.**

When asked about current code structure:
1. **Don't** read these docs first
2. **Do** explore the actual code, then optionally compare against these docs to spot drift
3. If a view doc disagrees with the code, the **code wins** — propose regenerating the view

When asked to update a view doc:
1. Run the appropriate generator (tools like `pyan`, `madge`, `tree`, or AI-driven full reads)
2. Replace the doc wholesale; do not patch in place
3. The `sunnydata-auto-regen` skill (if available) handles this end-to-end

## How humans should maintain this tier

**You should not be hand-editing files in this tier.** If you find yourself doing so, that's a signal one of the following is true:

- The view doc is misclassified (it's actually a contract or decision; move it)
- The generator is missing (build one)
- You're using the doc to communicate intent instead of state (write that into tier 0/1 instead)

## Files

| File | Generator hint |
|---|---|
| `VIEW-0001-project-structure.template.md` | `tree` or `eza --tree` output, then annotate per directory |
| `VIEW-0002-file-dependencies.template.md` | Language-specific (Python: `pyan`, JS: `madge`, Go: `go list`) |
| `VIEW-0003-class-relationships.template.md` | UML extractor or AI-driven full read |
| `VIEW-0004-frontend-route-map.template.md` | Page tree + nav + route table + page-to-page data flow; AI-generated from router config (per [ADR-0001](../../docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md)) |

## Frontmatter Schema

All files in this tier MUST carry this frontmatter:

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | YES | string | `VIEW-NNNN` |
| `title` | YES | string | Human-readable title |
| `status` | YES | enum | `active` / `stale` / `regenerating` |
| `tier` | YES | const | `5-views` |
| `owner` | YES | const | `AI-AUTO` |
| `last-synced-with` | YES | string | Git commit SHA |
| `sync-source` | YES | const | `code` |
| `source-paths` | YES | list | Source file paths |
| `synced-at` | YES | date | Last sync date |
| `generated-by` | YES | string | Tool that generated this |
| `generated-from` | opt | string | Analysis source |
| `last-regenerated` | YES | date | Last regeneration date |
| `product-version` | opt | string | Product version |
| `supersedes` | opt | string | Predecessor VIEW ID |
| `superseded-by` | opt | string | Successor VIEW ID |
