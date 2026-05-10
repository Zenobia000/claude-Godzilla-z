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

When in doubt, run the `/check-doc-freshness` skill before treating a contract doc as ground truth.

## How humans should maintain this tier

Every instance file in `docs/2-contracts/` MUST carry frontmatter:

```yaml
---
# Identity (REQUIRED — see 0-principles/flow-id-conventions.md)
id: BF-NNNN | UF-NNNN | SF-NNNN | API-NNNN | FR-NNNN

# Lifecycle (REQUIRED)
status: draft | active | deprecated | superseded | archived
owner: <team-or-person>
last_reviewed: <YYYY-MM-DD>

# Supersession chain (REQUIRED if status=superseded; null otherwise)
supersedes: <previous-doc-id-or-null>
superseded_by: <replacement-doc-id-or-null>

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
| `superseded` | Fully replaced; do not use | Skip; jump to `superseded_by` doc |
| `archived` | Historical record; not in use | Ignore unless user explicitly asks |

The `post-write` hook updates `last-synced-with` and `synced-at` automatically when you edit the file. The `sunnydata-doc-freshness` skill compares `last-synced-with` against the latest commit on each `source-path` AND inspects `status` to warn on stale content + lifecycle issues. The `change-governance` rule enforces that AI never treats a `status: deprecated` or `status: superseded` doc as authoritative.

## Files

| File | Purpose | Answers |
|---|---|---|
| `flow-business.template.md` | L1 Business Flow (BF) — end-to-end across roles | "How does it happen E2E?" |
| `flow-user.template.md` | L2 User Flow (UF) — single-actor surface-mapped flow | "How does *this actor* do it?" |
| `flow-sub.template.md` | L3 Sub Flow (SF) — reusable building block | "How does this shared step work?" |
| `functional-requirement.template.md` | Functional Requirement (FR) — business rules + acceptance criteria | "How do we judge correctness?" |
| `api-spec.template.md` | REST/GraphQL API contract | "How do systems exchange data?" |
| `module-contract.template.md` | Module/class public contract (DbC) | "What does this module promise?" |
| `state-machine.template.md` | Per-entity state machine — states, transitions, guards, events | "How does this entity change over time?" *(extract when ≥5 states or ≥10 transitions)* |
| `master-data-specification.template.md` | Master entity governance contract — identification, lifecycle, DQ rules, replication, GDPR | "How do we govern this long-lived shared entity?" *(critical for ERP-class systems)* |
| `traceability-matrix.template.md` | Cross-layer coverage map | "What links to what?" (BF→UF→SF→FR→API→Data→TC→CI) |

**One doc, one question** — if you find yourself writing flow steps inside an FR, or rules inside a Flow, you're conflating layers. See `change-governance.md` for the AI-side enforcement.
