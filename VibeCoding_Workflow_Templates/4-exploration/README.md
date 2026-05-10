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
| `prd.template.md` | Product Requirement Document (problem, users, goals, scope, metrics) |
| `wbs.template.md` | Work Breakdown Structure for sprint/phase planning |
