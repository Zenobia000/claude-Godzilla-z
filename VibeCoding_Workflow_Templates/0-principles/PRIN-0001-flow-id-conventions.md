---
id: PRIN-0001
title: "Flow ID Naming Conventions"
status: active
tier: 0-principles
owner: HUMAN-ONLY
essence: bedrock
last-reviewed: 2026-05-17
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

### Extended prefixes (v6.0 — 17 canonical)

These prefixes name the **20 canonical templates** in v6.0 (+ CIG workflow files). Sub-concepts that used to have their own prefix now live as §sections inside a canonical template.

| Prefix | Meaning | Tier | Canonical file |
|---|---|---|---|
| **PRIN** | Principles (mission + quality bars + glossary + unit-economics) | 0 | `PRIN-0000-product-principles.template.md` |
| **ARCH** | Architecture (C4 + modules + stack + infra + DDD + capacity-est + security + frontend) | 1 | `ARCH-0000-architecture-overview.template.md` |
| **ADR** | Architecture Decision Record (append-only) | 1 | `ADR-0000-adr.template.md` |
| **FLOW** | Flow (BF + UF + SF — 3 scopes in one) | 2 | `FLOW-0000-flow.template.md` |
| **API** | API spec (REST + Async + Errors + Idempotency) | 2 | `API-0000-api-spec.template.md` |
| **MC** | Module Contract (DbC + State machine) | 2 | `MC-0000-module-contract.template.md` |
| **FR** | Functional Requirement (rules + Page contract) | 2 | `FR-0000-functional-requirement.template.md` |
| **DATA** | Data Contract (master data + migration + pipeline + model card) | 2 | `DATA-0000-data-contract.template.md` |
| **AI** | AI System (prompt + agent + RAG + safety + capacity) | 2 | `AI-0000-ai-system-contract.template.md` |
| **SRE** | Reliability (SLO + observability + capacity) | 2 | `SRE-0000-reliability.template.md` |
| **EDGE** | Edge case catalog | 2 | `EDGE-0000-edge-case-catalog.template.md` |
| **PROC** | Process guide (handbook OR ops runbook; instance-numbered) | 3 | `PROC-0001-developer-handbook.template.md`, `PROC-0002-ops-runbook.template.md` |
| **QG** | Quality Gates | 3 | `QG-0000-quality-gates.md` |
| **TEST** | Testing strategy (unit + contract + BDD + LLM-eval + experiment) | 3 | `TEST-0000-testing-strategy.template.md` |
| **CIG** | CI Gate workflow (enforcement; not a fillable template) | 3 | `3-process/ci-gates/CIG-0001..0010.workflow.yml` |
| **PRD** | Product Requirements (discovery + personas + spec + experiments + launch) | 4 | `PRD-0000-prd.template.md` |
| **PLAN** | Planning (roadmap + WBS) | 4 | `PLAN-0000-planning.template.md` |
| **CIA** | Change Impact Analysis | 4 | `CIA-0000-change-impact-analysis.template.md` |

### Sub-prefixes (used inside §sections; no standalone files)

These names still appear in flow ID references but live as §sections of canonical templates:

| Sub-prefix | Lives in | Identifies |
|---|---|---|
| **BF / UF / SF** | `FLOW-NNNN` §1 / §2 / §3 — instance-numbered per scope | Business / User / Sub flow at three scopes |
| **TC** | `tests/features/*.feature` + `tests/llmeval/*.jsonl` (registry) | Test case |
| **CR** | `4-exploration/CR-NNNN-*.md` | Change request |
| **PC** | `FR-NNNN §page-contract` | Page contract |
| **SM** | `MC-NNNN §state-machine` + `MC-NNNN-<slug>.example.xstate.json` | State machine |

**v5.x prefixes retired** (content merged): GLOS, DDD, ARCH-0001/0002/0003, MDS, MIG, PIPE, MODEL, ERR, ASYNC, SLO, OBS, CAP, POL, DS, FI, TM, PROMPT, AGENT, RAG, AISAFE, AICAP, PERS, UE, EST, CT, LLMEVAL, ONBOARD, TP, DISC, EXP, ABT, GTM, RM, WBS, VIEW. See `migration-v5-to-v6.md` for which §section each became.

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

- `0-principles/PRIN-0003-engineering-contract-stack.md` — the 10-layer map; consumer of every prefix above
- `2-contracts/BF-0000-flow-business.template.md` — BF template
- `2-contracts/UF-0000-flow-user.template.md` — UF template
- `2-contracts/SF-0000-flow-sub.template.md` — SF template
- `2-contracts/TM-0000-traceability-matrix.template.md` — the Flow ID consumer
- `1-decisions/ADR-0000-adr.template.md` — ADR template
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — CR-driven analysis using these IDs
