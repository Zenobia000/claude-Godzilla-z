---
id: PRIN-0001
title: "Flow ID Naming Conventions"
status: active
tier: 0-principles
owner: HUMAN-ONLY
last-reviewed: 2026-05-15
product-version: null
supersedes: null
superseded-by: null
---
# Flow ID Naming Conventions

> **Tier**: 0-principles — project-wide naming invariant; once adopted, every artifact uses these IDs forever.
>
> **Why**: large systems can't use names like "the order flow" — front-stage? back-stage? payment? cancellation? Without IDs, traceability is impossible and AI cannot reliably reference what it changed.

---

## The prefix system

### Core prefixes (original 9)

| Prefix | Meaning | Lives in (typical) | Lifetime |
|---|---|---|---|
| **BF** | Business Flow | `docs/2-contracts/BF-NNNN-*.md` | Long-lived; major rewrite is rare |
| **UF** | User / Role Flow | `docs/2-contracts/UF-NNNN-*.md` | Medium; changes with feature evolution |
| **SF** | Sub Flow (reusable) | `docs/2-contracts/SF-NNNN-*.md` | Medium; shared across BF/UF |
| **FR** | Functional Requirement | `docs/2-contracts/FR-NNNN-*.md` or grouped | Per-release |
| **NFR** | Non-Functional Requirement | `docs/0-principles/` (or grouped) | Long-lived |
| **API** | API Endpoint | `docs/2-contracts/api/openapi.yaml#operationId` | Tracks contract changes |
| **TC** | Test Case | tests/ source files; tracked in traceability matrix | Per-feature |
| **ADR** | Architecture Decision Record | `docs/1-decisions/ADR-NNNN-*.md` | Append-only |
| **CR** | Change Request | `docs/4-exploration/CR-NNNN-*.md` | Per-change ephemeral |

### Extended prefixes (added CR-0001)

These prefixes extend the ID system to non-flow artifacts — templates, process guides, and governance files — so that every file in `VibeCoding_Workflow_Templates/` has a scannable, sortable ID prefix.

| Prefix | Meaning | Tier | Template filename example |
|---|---|---|---|
| **PRIN** | Principles | 0 | `PRIN-0000-product-principles.template.md` |
| **GLOS** | Glossary | 0 | `GLOS-0000-glossary.template.md` |
| **ARCH** | Architecture docs | 1 | `ARCH-0000-architecture-overview.template.md` |
| **DDD** | Domain model | 1 | `DDD-0000-domain-model.template.md` |
| **MC** | Module Contract | 2 | `MC-0000-module-contract.template.md` |
| **MDS** | Master Data Spec | 2 | `MDS-0000-master-data.template.md` |
| **FI** | Flow Index | 2 | `FI-0000-flow-index.template.md` |
| **TM** | Traceability Matrix | 2 | `TM-0000-traceability-matrix.template.md` |
| **DS** | Design System | 2 | `DS-0000-frontend-design-system.template.md` |
| **PC** | Page Contract | 2 | `PC-0000-page-contract.template.md` |
| **SM** | State Machine | 2 | `SM-0000-state-machine.template.md` |
| **SLO** | SLO Specification | 2 | `SLO-0000-slo-spec.template.md` |
| **PIPE** | Pipeline Contract | 2 | `PIPE-0000-pipeline-contract.template.md` |
| **MODEL** | Model Card | 2 | `MODEL-0000-model-card.template.md` |
| **OBS** | Observability Spec | 2 | `OBS-0000-observability-spec.template.md` |
| **CAP** | Capacity Planning | 2 | `CAP-0000-capacity-planning.template.md` |
| **PROC** | Process guide | 3 | `PROC-0001-workflow-manual.md` |
| **QG** | Quality Gates | 3 | `QG-0000-quality-gates.md` |
| **TP** | Test Plan | 3 | `TP-0000-test-plan.template.md` |
| **ONBOARD** | Team Onboarding | 3 | `ONBOARD-0000-team-onboarding.template.md` |
| **PRD** | Product Requirements | 4 | `PRD-0000-prd.template.md` |
| **WBS** | Work Breakdown | 4 | `WBS-0000-wbs.template.md` |
| **CIA** | Change Impact Analysis | 4 | `CIA-0000-change-impact-analysis.template.md` |
| **EXP** | Experiment Log | 4 | `EXP-0000-experiment-log.template.md` |
| **DISC** | Discovery Research | 4 | `DISC-0000-discovery-research.template.md` |
| **VIEW** | Code-derived view | 5 | `VIEW-0001-project-structure.template.md` |

### Template vs instance numbering

- **`0000`** = the template itself (e.g. `BF-0000-flow-business.template.md`)
- **`0001`+** = instantiated artifacts (e.g. `BF-0001-order-to-cash.md`)
- Single-prefix files (BF, UF, API, etc.) use `0000` for their template
- Shared-prefix files (PROC, VIEW, ARCH, etc.) use incrementing numbers for distinct guides/views

---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (Customer, Order, Inventory, PurchaseOrder, Stripe, etc.) come
> from a worked e-commerce/ERP example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.
## Numbering rules

- **4-digit zero-padded sequential**: `BF-0001`, `UF-0042`, `ADR-0007`
- **Sequential per prefix**, never reused, never renumbered
- **Numbers are immutable**; if you delete an artifact, the number is retired (don't reuse)
- **First-class IDs**: BF, UF, SF, ADR, CR. **Derived IDs**: FR, API, TC may use sub-numbering (e.g. `FR-0001.1`) when grouped

## Title format

Each artifact's title in the file uses both ID and human-readable name:

```markdown
# BF-0001: Order to Cash
```

Filenames mirror this: `BF-0001-order-to-cash.md`

## Cross-reference syntax

When one artifact references another, always use the ID:

- ✅ "Triggered by `BF-0001`"
- ✅ "Implements `FR-0023`, validated by `TC-0145`, exposed as `API-0008`"
- ❌ "Used in the order flow" *(which one?)*

In code comments and commit messages, the same convention:
```python
# Implements UF-0012 (admin review order)
```
```
fix(payment): handle duplicate callback per SF-0003 idempotency rule
```

---

## When a new ID is required

Allocate a new ID **before** writing the artifact. The allocation step is:

1. Open the relevant `<prefix>-INDEX.md` file (one per prefix, lives in same dir as the artifacts)
2. Take the next sequential number
3. Reserve it by adding the row (status: `draft`)
4. Write the artifact file using the reserved ID

This prevents the "two PRs allocated the same number" race.

---

## When IDs are NOT required

Tier 5 derived views (project-structure, dependency graph, class diagram) **do not** need Flow IDs — they're snapshots of code, not contracts. Their generators reference the source code directly.

Tier 0 product principles **do not** need IDs — they're a single document per project, not enumerated artifacts.

Tier 4 exploration drafts (PRD, brainstorm) **do not** need IDs *while exploring*; only when promoted to a tier-1/2 artifact does it get an ID.

---

## Example chain

A real change cuts across many IDs:

```
CR-0042 "Support partial order cancellation"
  ↓ touches
BF-0001 (Order to Cash) — adds partial-cancel branch
  ↓ adds
UF-0007 (Customer cancel order) — modifies main flow
  ↓ extracts
SF-0014 (Partial cancellation rule) — NEW reusable sub-flow
  ↓ requires
FR-0089 (Partial cancel calculation) — NEW functional rule
  ↓ exposed via
API-0034 (POST /orders/{id}/cancel) — schema change
  ↓ recorded as
ADR-0019 (Partial-cancel state machine choice)
  ↓ validated by
TC-0211 ~ TC-0218 (8 new test cases)
```

This chain becomes one row in `TM-0000-traceability-matrix.template.md`.

---

## See also

- `2-contracts/BF-0000-flow-business.template.md` — BF template
- `2-contracts/UF-0000-flow-user.template.md` — UF template
- `2-contracts/SF-0000-flow-sub.template.md` — SF template
- `2-contracts/TM-0000-traceability-matrix.template.md` — the Flow ID consumer
- `1-decisions/ADR-0000-adr.template.md` — ADR template
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — CR-driven analysis using these IDs
