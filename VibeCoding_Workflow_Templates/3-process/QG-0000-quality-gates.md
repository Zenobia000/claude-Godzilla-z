---
id: QG-0000
title: "Quality Gates"
status: active
tier: 3-process
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---
# Quality Gates

> **Tier**: 3-process → process guide
>
> **Purpose**: enforce sequence on the early-stage decisions that, if rushed, cause the most expensive rework. Five gates, each with explicit prerequisites. **Don't pass a gate until prerequisites are met. Don't rework downstream artifacts to fix an upstream gate violation.**
>
> **Why this matters**: AI is a fast worker. If you let it lay foundations before the floorplan is set, it lays the foundations very quickly — and you pay the rework very expensively.

---

## Gate 0 — Requirements Ready

> *Pass before any documentation, design, or code work begins.*

### Prerequisites

- [ ] **Product principles** filled (`0-principles/PRIN-0000-product-principles.template.md`): mission, non-goals, quality bars, technical invariants
- [ ] **Core actors** identified with roles and responsibilities
- [ ] **Core User Flow** drafted at L1 (`BF-NNNN`) — even rough, the shape exists
- [ ] **Non-goals** explicit ("we will NOT do X")
- [ ] **Success metrics** named — at least one north star + 2-3 health metrics

### Failure modes if you skip

- AI generates features no one asked for ("looked useful")
- Scope creep in week 2; abandonment in week 6
- Stakeholders disagree on what was promised after delivery

### Forbidden until passed

- Building tables / DB schema
- Writing API contracts
- Designing UI mockups beyond rough sketch

---

## Gate 1 — Frontend-Buildable

> *Pass before frontend can start meaningful work beyond static prototypes.*

### Prerequisites

- [ ] All Gate 0 items still hold
- [ ] **User Flow (L2, `UF-NNNN`)** for each primary persona, including main happy path AND main exception
- [ ] **Screen map** — list of screens with purpose; rough wireframes acceptable
- [ ] **Main feature list** with priority (Must / Should / Could)
- [ ] **State definitions** — what does the UI need to display? (e.g. `loading / empty / error / partial / complete`)
- [ ] **Error states** — at least one mockup or written description per primary error class

### Failure modes if you skip

- Frontend builds 3 versions of the same screen because flow changed
- "Just add another modal" syndrome → UI architecture rots
- Empty / error states discovered in production

### Forbidden until passed

- Writing real API integration code (mocks are fine)
- Building components that depend on contract shape

---

## Gate 2 — Backend Parallelizable

> *Pass before frontend and backend can develop in parallel without constant re-sync.*

### Prerequisites

- [ ] All Gate 1 items still hold
- [ ] **OpenAPI spec** (`2-contracts/API-0000-api-spec.template.md` instances) covers every endpoint frontend will call
- [ ] **Mock server** stood up serving the OpenAPI spec
- [ ] **Error envelope shape** decided and documented (one consistent format across all endpoints)
- [ ] **Error code catalog** (at minimum: auth, validation, not-found, conflict, rate-limit, server-error)
- [ ] **Auth/authz model** documented — token flow, refresh, scope/role mapping
- [ ] **Main data schemas** in OpenAPI components (request/response/event payloads)
- [ ] **`PRIN-0001-flow-id-conventions.md`** adopted; APIs have `API-NNNN` IDs

### Failure modes if you skip

- Frontend ships against assumed shape; backend ships actual shape; integration day = chaos
- 5 versions of "what does the error look like?" across endpoints
- Auth flow gets bolted on instead of designed in

### Forbidden until passed

- Frontend wiring to real backend (use mock)
- Backend committing to schema in DB (still subject to API change)

---

## Gate 3 — DB-Schema-Buildable

> *Pass before any DDL migration is committed.*

### Prerequisites

- [ ] All Gate 2 items still hold
- [ ] **Domain model** documented (`1-decisions/ARCH-0000-architecture-overview.template.md` or per-aggregate `2-contracts/MC-0000-module-contract.template.md`)
- [ ] **State machines** for stateful entities (Order, Payment, etc.) — every transition labeled
- [ ] **Data lifecycle** — for each entity: how is it created, updated, soft-deleted, hard-deleted, archived?
- [ ] **Query patterns** enumerated — read paths, write paths, hot reads, batch jobs
- [ ] **Transactional boundaries** decided — which operations must be atomic
- [ ] **Audit/compliance requirements** captured (retention, encryption-at-rest, PII handling)

### Failure modes if you skip

- Schema invented by writing code, not by modeling business → schema reflects implementer's mental model, not domain
- Missing indexes discovered in prod load test
- "Soft delete vs hard delete" decided per-table inconsistently → bug breeding ground
- Compliance retrofit costs 10× more than designing in

### Forbidden until passed

- `CREATE TABLE` migrations for the affected entities
- Production-bound seed data

### Hard rule

> 🛑 **Flow not stable → don't build tables.** This is the one rule that pays for itself most often. DB schema is "where business process becomes physical state". If the process isn't stable, the schema bakes in ambiguity that's painful to migrate later.

---

## Gate 4 — Comprehensive Tests Writable

> *Pass before declaring "we have a test plan" — i.e. before relying on CI for confidence.*

### Prerequisites

- [ ] All Gate 3 items still hold
- [ ] **Test Matrix** filled (`2-contracts/TM-0000-traceability-matrix.template.md`) — every BF/UF/SF has at least one TC
- [ ] **Test categories defined** — unit, component, contract, integration, E2E, performance, security; each with what they own
- [ ] **External dependency matrix** — every external API has a contract test + a fallback story
- [ ] **Coverage policy** — minimum % per layer (e.g. domain ≥ 80%, infra ≥ 60%); written down
- [ ] **CI quality gate definition** — what CI must enforce on every PR (lint / unit / integration / contract; what's blocking vs warning)
- [ ] **Vendor API testing strategy** — sandbox vs mock vs production; who provides credentials

### Failure modes if you skip

- "CI passes" stops meaning "code is correct"
- Heavy E2E reliance → flaky tests, slow feedback loop, ignored failures
- Vendor API quirks discovered the day you go live

### Forbidden until passed

- Calling CI green coverage as "tested"
- Releasing to production with only unit tests

---

## Gate Decision Cheat Sheet

When unsure whether a gate has been met, ask:

| Question | If "no" → |
|---|---|
| Can a new contributor read these docs and start building correctly? | Gate 0 / 1 not met |
| Can frontend mock-up a complete user journey without asking the backend a question? | Gate 2 not met |
| If we shipped this schema today, what would we regret in 6 months? | Gate 3 not met |
| If CI goes green, can the on-call sleep tonight? | Gate 4 not met |

---

## How this connects to the other rules

- **Gate 0/1** answers go into tier-0 (`product-principles`) and tier-2 (`flow-business`, `flow-user`)
- **Gate 2** outputs are tier-2 contracts (API spec) — sync mechanism applies
- **Gate 3** outputs are tier-1 decisions (schema choice → ADR) and tier-5 views (ERD)
- **Gate 4** output is the tier-2 traceability matrix
- **Change Governance**: when a CR touches a gate's prerequisite, re-pass that gate before implementation

## See also

- `.claude/rules/change-governance.md` — change must re-validate the gate it touches
- `.claude/rules/context-stability.md` — gate outputs map cleanly onto stability tiers
- `0-principles/PRIN-0000-product-principles.template.md` — Gate 0 deliverable
- `2-contracts/BF-0000-flow-business.template.md`, `UF-0000-flow-user.template.md` — Gate 0/1 deliverables
- `2-contracts/API-0000-api-spec.template.md` — Gate 2 deliverable
- `2-contracts/MC-0000-module-contract.template.md` — Gate 3 deliverable (per aggregate)
- `2-contracts/TM-0000-traceability-matrix.template.md` — Gate 4 deliverable
