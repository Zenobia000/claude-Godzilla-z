# Tier 2 — Contracts

> The boundary layer. Documents here describe **interfaces between systems, modules, or teams** — and they MUST stay synchronized with code.

## What lives here

- API specifications (OpenAPI, GraphQL schema)
- Module contracts (Design-by-Contract, public function signatures, invariants)
- Data schemas (DB tables, message envelopes, file formats)

## What does NOT live here

- Internal implementation → tier 5 (views, derivable from code)
- Why we chose this contract shape → tier 1 (decisions)
- Workflow for evolving a contract → tier 3 (process)

## How AI should use this tier

These documents are either **source-of-truth** (contract-first projects) or **mirror-of-truth** (code-first projects).

**Always check the `sync-source` frontmatter** of the instance file:
- `sync-source: doc` → the doc is authoritative, code follows
- `sync-source: code` → the code is authoritative, doc may be stale

When in doubt, run the `sunnydata-doc-freshness` skill before treating a contract doc as ground truth.

## How humans should maintain this tier

Every instance file in `docs/2-contracts/` MUST carry frontmatter:

```yaml
---
# Identity (REQUIRED — see 0-principles/PRIN-0001-flow-id-conventions.md)
id: BF-NNNN | UF-NNNN | SF-NNNN | API-NNNN | FR-NNNN

# Lifecycle (REQUIRED)
status: draft | active | deprecated | superseded | archived
owner: <team-or-person>
last-reviewed: <YYYY-MM-DD>

# Supersession chain (REQUIRED if status=superseded; null otherwise)
supersedes: <previous-doc-id-or-null>
superseded-by: <replacement-doc-id-or-null>

# Sync (REQUIRED for code-tracking contracts; omit for cross-cutting docs like traceability-matrix)
last-synced-with: <git-commit-sha>     # HEAD when last verified
sync-source: code | doc                 # which side is authoritative
source-paths:                            # code paths this contract describes
  - src/api/users.py
  - src/models/user.py
synced-at: <YYYY-MM-DD>
---
```

### Lifecycle states

| status | Meaning | AI behavior |
|---|---|---|
| `draft` | In progress, not yet authoritative | Read but warn user it's not active |
| `active` | Current source of truth (default) | Read normally |
| `deprecated` | Still works but discouraged; migrate when convenient | Warn; suggest replacement |
| `superseded` | Fully replaced; do not use | Skip; jump to `superseded-by` doc |
| `archived` | Historical record; not in use | Ignore unless user explicitly asks |

The `post-write` hook updates `last-synced-with` and `synced-at` automatically when you edit the file. The `sunnydata-doc-freshness` skill compares `last-synced-with` against the latest commit on each `source-path` AND inspects `status` to warn on stale content + lifecycle issues. The `change-governance` rule enforces that AI never treats a `status: deprecated` or `status: superseded` doc as authoritative.

## Files

| File | Purpose | Answers |
|---|---|---|
| `BF-0000-flow-business.template.md` | L1 Business Flow (BF) — end-to-end across roles | "How does it happen E2E?" |
| `DS-0000-frontend-design-system.template.md` | Frontend design system and communication contract (tokens, components, API layer) | "How do frontend components communicate and stay consistent?" |
| `UF-0000-flow-user.template.md` | L2 User Flow (UF) — single-actor surface-mapped flow | "How does *this actor* do it?" |
| `SF-0000-flow-sub.template.md` | L3 Sub Flow (SF) — reusable building block | "How does this shared step work?" |
| `FR-0000-functional-requirement.template.md` | Functional Requirement (FR) — business rules + acceptance criteria | "How do we judge correctness?" |
| `API-0000-api-spec.template.md` | REST/GraphQL API contract | "How do systems exchange data?" |
| `MC-0000-module-contract.template.md` | Module/class public contract (DbC) | "What does this module promise?" |
| `PC-0000-page-contract.template.md` | Per-page contract (route, data deps, SEO, auth) | "What does this page need and expose?" |
| `SM-0000-state-machine.template.md` | Per-entity state machine — states, transitions, guards, events | "How does this entity change over time?" *(extract when ≥5 states or ≥10 transitions)* |
| `MDS-0000-master-data.template.md` | Master entity governance contract — identification, lifecycle, DQ rules, replication, GDPR | "How do we govern this long-lived shared entity?" *(critical for ERP-class systems)* |
| `FI-0000-flow-index.template.md` | Project-wide Flow aggregation — BF/UF/SF/SM lists, coverage view, supersession ledger | "What Flows exist, and what shape are they in?" |
| `SLO-0000-slo-spec.template.md` | SLO specification — SLI definitions, error budget, burn-rate alerts, SLA mapping | "How do we measure reliability?" |
| `PIPE-0000-pipeline-contract.template.md` | Data pipeline contract — input/output schema, DQ gates, SLA, blast radius | "What does this pipeline promise?" |
| `MODEL-0000-model-card.template.md` | ML model card — intended use, metrics, bias analysis, deployment constraints, lineage | "What does this model do and where does it fail?" |
| `OBS-0000-observability-spec.template.md` | Observability specification — metrics, logs, traces, dashboards, alerting strategy | "How do we know the system is healthy?" |
| `CAP-0000-capacity-planning.template.md` | Capacity planning & cost management — resource model, growth forecast, cost allocation, scaling | "Can we handle the load, and at what cost?" |
| `TM-0000-traceability-matrix.template.md` | Cross-layer coverage map | "What links to what?" (BF→UF→SF→FR→API→Data→TC→CI) |

**flow-index vs traceability-matrix** — both are aggregation views but answer different questions:
- `flow-index` lists Flow **existence + status** (which BFs do we have, what's their state?)
- `traceability-matrix` lists **cross-layer coverage** (which BF → which API → which TC → which CI job?)
- Both should be present in a mature project; they're checked separately by `sunnydata-flow-audit` and `sunnydata-doc-freshness`.

**One doc, one question** — if you find yourself writing flow steps inside an FR, or rules inside a Flow, you're conflating layers. See `change-governance.md` for the AI-side enforcement.

## Frontmatter Schema

All files in this tier MUST carry this frontmatter:

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | YES | string | `BF-NNNN`, `UF-NNNN`, `SF-NNNN`, `API-NNNN`, `FR-NNNN`, `SLO-NNNN`, `PIPE-NNNN`, `MODEL-NNNN`, `OBS-NNNN`, `CAP-NNNN`, etc. |
| `title` | YES | string | Human-readable title |
| `status` | YES | enum | `draft` / `active` / `deprecated` / `superseded` |
| `tier` | YES | const | `2-contracts` |
| `owner` | YES | enum | `HUMAN-ONLY` / `HYBRID` / `AI-AUTO` |
| `last-reviewed` | YES | date | `YYYY-MM-DD` |
| `last-synced-with` | YES | string | Git commit SHA |
| `sync-source` | YES | enum | `code` / `doc` |
| `source-paths` | YES | list | Source file paths |
| `synced-at` | YES | date | Last sync date |
| `product-version` | opt | string | Product version this doc applies to |
| `supersedes` | opt | string | ID of predecessor |
| `superseded-by` | opt | string | ID of successor |
