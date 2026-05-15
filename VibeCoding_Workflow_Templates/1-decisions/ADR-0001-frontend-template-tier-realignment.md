---
id: ADR-0001
title: "Frontend Template Tier Realignment"
status: accepted
tier: 1-decisions
owner: HUMAN-ONLY
last-reviewed: 2026-05-15
date: 2026-05-10
decider: project-maintainer
product-version: "v5.4"
supersedes: null
superseded-by: null
---
# ADR-0001: Frontend Template Tier Realignment

> **Tier**: 1-decisions -- append-only architectural decision record

---

## 1. Context and Problem

- **Context**: `5-views/frontend-architecture.template.md` was a monolithic ~800-line file that mixed tier-0 principles (performance budgets, accessibility bars), tier-1 decisions (framework choice, state management), tier-2 contracts (design system tokens, page-level data dependencies), and tier-5 views (route maps) in a single document.
- **Problem**: The monolithic structure caused three concrete issues:
  1. AI had to load the entire 800-line file even when only one tier was relevant, wasting context window.
  2. Ownership was ambiguous -- tier-0 principles require human-only review, while tier-5 views are auto-generated. A single file cannot carry both ownership models.
  3. Update cadence conflicts -- principles change yearly, contracts change with code, views regenerate on demand. One file cannot have three different update schedules.
- **Driving factors**:
  - Context stability tier system (see `rules/context-stability.md`) assigns different trust levels, update cadences, and ownership rules per tier
  - AI context window is a finite resource; loading irrelevant tiers degrades response quality
  - Clear ownership per file enables automated freshness checking via `sunnydata-doc-freshness`

## 2. Options Considered

### Option A: Keep monolithic file, add internal section markers

- **Description**: Add tier annotations as comments within the existing file
- **Pros**: No file reorganization needed; single place to read everything
- **Cons**: AI still loads the full file; ownership and update cadence remain ambiguous; freshness checking cannot target individual tiers
- **Cost/Complexity**: Low

### Option B: Split into 6 tier-aligned files

- **Description**: Extract each logical section into the tier where it belongs, following the naming conventions of that tier
- **Pros**: Each file has clear ownership, update cadence, and tier semantics; AI loads only what it needs; freshness checking works per-file
- **Cons**: More files to navigate; cross-references needed between the split files
- **Cost/Complexity**: Medium

## 3. Decision

**Choice**: Option B -- Split into 6 tier-aligned files.

The resulting files:

| # | File | Tier |
|---|---|---|
| 1 | `0-principles/PRIN-0002-frontend-quality-attributes.template.md` | 0-principles |
| 2 | `1-decisions/ARCH-0002-frontend-tech-stack.template.md` | 1-decisions |
| 3 | `2-contracts/DS-0000-frontend-design-system.template.md` | 2-contracts |
| 4 | `2-contracts/PC-0000-page-contract.template.md` | 2-contracts |
| 5 | `3-process/PROC-0008-frontend-pre-merge.template.md` | 3-process |
| 6 | `5-views/VIEW-0004-frontend-route-map.template.md` | 5-views |

**Rationale**: Each tier has different update cadence, ownership, and AI trust level per `rules/context-stability.md`. A monolithic file that spans tiers violates the core invariant of the tier system. The medium cost of splitting is a one-time effort; the ongoing benefit of correct tier alignment compounds over every AI conversation.

## 4. Consequences

- **Positive**:
  - Tier-aligned loading: AI reads only the tier it needs for the current task
  - Clear ownership: each file carries a single `owner` value (HUMAN-ONLY for tier-0, HYBRID for tier-1/2, AI-AUTO for tier-5)
  - Smaller files: each file stays well under the 400-line guideline
  - Freshness checking: `sunnydata-doc-freshness` can validate each file independently
- **Negative**:
  - More files to navigate (6 instead of 1)
  - Cross-references needed between split files (e.g., PRIN-0002 references ARCH-0002 for tech stack context)
  - Existing references to the monolithic file need updating
- **Impact scope**: All tier README files need updated Files tables; any skills or docs referencing the old monolithic path need path updates
- **Re-evaluation trigger**: If the tier system itself is restructured, revisit whether the split boundaries still align

---

| Date | Reviewer | Notes |
| :--- | :--- | :--- |
| 2026-05-10 | project-maintainer | Accepted and implemented in v5.4 |
| 2026-05-15 | project-maintainer | Tier README Files tables updated |
