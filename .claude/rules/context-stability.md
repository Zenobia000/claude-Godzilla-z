# Context Stability Tiers

> **Why this rule exists**: AI generates slop when it cannot tell which docs to trust as ground truth. This rule encodes the project's stability hierarchy so AI loads, weighs, and updates each tier appropriately.

## The 6 tiers

| Tier | Path prefix | Update cadence | Treat as |
|---|---|---|---|
| **0 — principles** | `docs/0-principles/`, `VibeCoding_Workflow_Templates/0-principles/` | Yearly | **Hard constraint.** Overrides downstream. |
| **1 — decisions** | `docs/1-decisions/`, `.../1-decisions/` | Append-only | Honor or escalate; never silently contradict. |
| **2 — contracts** | `docs/2-contracts/`, `.../2-contracts/` | With code | Check `last-synced-with` frontmatter first. |
| **3 — process** | `docs/3-process/`, `.../3-process/` | Half-yearly | Follow the checklist verbatim. |
| **4 — exploration** | `docs/4-exploration/`, `.../4-exploration/` | Per-task | Read for motivation; **never assume current behavior**. |
| **5 — views** | `docs/5-views/`, `.../5-views/` | On-demand regen | **Treat as cache, not source of truth.** Code wins on disagreement. |

## Reading order for a new conversation

When starting any non-trivial task, load tiers in this order:

1. **Tier 0** — establishes worldview (mission, non-goals, technical invariants)
2. **Tier 1** — relevant ADRs for the touched area
3. **Tier 2** — contracts for any module/API the task touches *(after `sunnydata-doc-freshness` skill passes)*
4. **Tier 3** — relevant checklists for the kind of work
5. **Tier 4** — only if you need motivation context
6. **Tier 5** — explore the actual code first; use views only as a sanity check

## Writing rules per tier

| Tier | Who writes | When | How |
|---|---|---|---|
| 0 | Human only | Major version | Team review |
| 1 | Human or AI draft + human approve | New decision | New ADR file, never edit accepted ones |
| 2 | AI generates + human verifies | Contract change | Use `vibecoding-write-api-contract` / `vibecoding-write-tdd` skill; carry frontmatter |
| 3 | Human curates | Quarterly | Direct edit; bump version footer |
| 4 | AI drafts on demand | Task start | Use `vibecoding-write-prd` skill; date-stamp filename |
| 5 | AI auto-regenerates | After refactor | Use `sunnydata-auto-regen` skill; never hand-edit |

## When tiers conflict

| Conflict | Winner | Action |
|---|---|---|
| Tier 0 says X, Tier 2 says Y | Tier 0 | Update Tier 2 to comply or write ADR justifying override |
| Tier 1 ADR says X, code does Y | ADR | Either fix the code or write a new ADR superseding the old |
| Tier 2 contract says X, code does Y | Check `sync-source` frontmatter. `code` → update doc; `doc` → fix code |
| Tier 5 view says X, code does Y | Code | Regenerate the view |
| Tier 4 PRD says X, current behavior is Y | Current behavior | PRD captured intent at a moment; behavior moved on. Don't "restore" PRD's version |

## How AI signals tier awareness

When proposing a change, name the tier explicitly:
- ✅ "This is a tier-1 decision; I'll draft an ADR before changing the code."
- ✅ "The contract in tier 2 is stale (last-synced 30 commits behind); regenerating from code first."
- ❌ "I'll update the docs while I'm at it." *(which docs? what tier? what authority?)*

## Files

- Tier definitions: this file (`.claude/rules/context-stability.md`)
- Per-tier policy detail: `VibeCoding_Workflow_Templates/<tier>/README.md`
- Sync mechanism: `.claude/skills/sunnydata-doc-freshness/SKILL.md` + `.claude/hooks/post-write.sh`
- Recommended `docs/` layout: `VibeCoding_Workflow_Templates/HOW-TO-INSTANTIATE.md`
