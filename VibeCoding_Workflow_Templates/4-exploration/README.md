# Tier 4 — Exploration

> Per-task ephemeral. Documents here have a short useful life — they capture intent at a moment, then get archived.

## What lives here

- PRDs (Product Requirement Documents) for specific features or releases
- WBS (Work Breakdown Structures) for project planning
- Brainstorm notes, draft design proposals, RFC drafts
- Anything starting with "draft", "proposal", "idea"

## What does NOT live here

- Decisions that resulted from the exploration → tier 1 (decisions, ADR)
- Contracts that resulted from the exploration → tier 2 (contracts)
- Process improvements that resulted from the exploration → tier 3 (process)

## How AI should use this tier

These documents represent **intent at a point in time**, not current state. AI should:

1. Read for context on *why* something was built
2. **Never assume** an exploration doc still describes current behavior
3. When generating code, prefer tier 2 (contracts) and tier 5 (views) as ground truth, and use tier 4 only to understand motivation

When the user asks AI to "draft a PRD", "plan a sprint", or "brainstorm an approach" — the output belongs in this tier.

## How humans should maintain this tier

- Date-stamp filenames: `prd-2026-q2-onboarding-revamp.md`, not `prd-onboarding.md`
- Move stale exploration docs to `archive/` quarterly; don't delete (keeps the rationale trail)
- When a PRD ships, link the resulting ADRs and contracts in the PRD's footer

## Files

| File | Purpose |
|---|---|
| `CIA-0000-change-impact-analysis.template.md` | Change Impact Analysis template for tracking change scope across flows, contracts, data, tests |
| `PRD-0000-prd.template.md` | Product Requirement Document (problem, users, goals, scope, metrics) |
| `WBS-0000-wbs.template.md` | Work Breakdown Structure for sprint/phase planning |
| `EXP-0000-experiment-log.template.md` | ML experiment log — hypothesis, dataset, model config, results, reproducibility |
| `DISC-0000-discovery-research.template.md` | Discovery & user research — hypotheses, competitive analysis, opportunity sizing, go/no-go |

## Frontmatter Schema

All files in this tier MUST carry this frontmatter:

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | YES | string | `PRD-NNNN`, `WBS-NNNN`, `CIA-NNNN`, `EXP-NNNN`, or `DISC-NNNN` |
| `title` | YES | string | Human-readable title |
| `status` | YES | enum | `draft` / `active` / `deprecated` / `superseded` |
| `tier` | YES | const | `4-exploration` |
| `owner` | YES | enum | `HUMAN-ONLY` / `HYBRID` / `AI-AUTO` |
| `last-reviewed` | YES | date | `YYYY-MM-DD` |
| `created` | YES | date | Creation date |
| `target-release` | opt | string | Target version or quarter |
| `product-version` | opt | string | Product version this doc applies to |
| `supersedes` | opt | string | ID of predecessor |
| `superseded-by` | opt | string | ID of successor |
