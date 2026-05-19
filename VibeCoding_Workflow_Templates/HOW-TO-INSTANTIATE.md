# How to Instantiate VibeCoding Templates in Your Project

> v6.0 — 20 templates total. Read [`BEDROCK.md`](./BEDROCK.md) first.

This repo provides empty forms (`*.template.md`) + read-only guides. Your project's filled-in instances live in YOUR repo, not here.

---

## Recommended `docs/` layout

Mirror the 4-tier structure inside your project (tier 5 is gone in v6.0):

```
your-project/
├── src/                                 # the code
├── tests/                               # the tests
└── docs/
    ├── BEDROCK.md                       # COPY from this repo; your entry point
    ├── 0-principles/
    │   ├── PRIN-0000-product-principles.md     # 1 file, filled from template
    │   ├── PRIN-0001-flow-id-conventions.md    # 1 file, near-immutable
    │   └── PRIN-0003-engineering-contract-stack.md
    │
    ├── 1-decisions/
    │   ├── ARCH-0000-architecture-overview.md  # 1 file, quarterly update
    │   └── ADR-0001-database-choice.md         # append-only, numbered
    │
    ├── 2-contracts/                     # MUST stay synced with code
    │   ├── api/
    │   │   ├── openapi.yaml             # canonical wire spec
    │   │   └── asyncapi.yaml            # if async channels exist
    │   ├── FLOW-0001-order-to-cash.md
    │   ├── MC-0001-cart-service.md (+ .example.xstate.json sibling if SM)
    │   ├── FR-0001-pricing-rules.md
    │   ├── DATA-0001-customer-master.md
    │   ├── AI-0001-support-triage.md    # only if AI features
    │   ├── SRE-0001-order-service.md
    │   └── EDGE-0001-billing.md
    │
    ├── 3-process/                       # usually copied verbatim
    │   ├── PROC-0001-developer-handbook.md
    │   ├── PROC-0002-ops-runbook.md     # if production traffic
    │   ├── TEST-0000-testing-strategy.md
    │   └── QG-0000-quality-gates.md
    │
    └── 4-exploration/                   # date-stamped; archive when done
        ├── PRD-2026-q3-triage.md
        ├── PLAN-2026-q3.md
        ├── CR-0042-cancellation-rule.md
        └── archive/
```

Tier-5 views (project structure, file deps, route map) — generated on demand via `sunnydata-auto-regen` skill; do not commit static copies.

---

## Mandatory frontmatter for tier 2 (contracts)

Every file in `docs/2-contracts/` carries:

```yaml
---
id: FLOW-0001
title: "Order to Cash"
status: active
tier: 2-contracts
owner: HYBRID
last-synced-with: <git-commit-sha>
sync-source: code | doc
source-paths:
  - src/orders/
synced-at: 2026-05-17
---
```

`post-write` hook auto-updates `last-synced-with` and `synced-at` on save. `sunnydata-doc-freshness` skill flags docs whose source moved on. `CIG-0007` blocks PR if source changed but doc didn't.

---

## Optional `essence` frontmatter (carries through from this template repo)

```yaml
essence: bedrock      # always-needed
essence: specialized  # opt-in based on situation
```

Bedrock files: AI must load on every non-trivial conversation. Specialized: load when relevant.

---

## Profiles (v6.0 — drastically simplified)

v5.x had a 5-column profile table. v6.0 collapses to: **start with all 10 bedrock; add specialized as you hit pain**. No more "do I need this for data-ml? for ai-native?" — your project's situation tells you.

| Project shape | Bedrock 10 | Likely additions |
|---|---|---|
| Solo dev, MVP | All 10 | None |
| Small team, pre-PMF | All 10 | + PRD (when PM joins) |
| Production-traffic SaaS | All 10 | + PROC-0002 + TEST + DATA + QG |
| AI-native (LLMs core) | All 10 | + AI + TEST + DATA |
| Multi-quarter roadmap | All 10 | + PLAN + PRD + CIA + ADR |
| Regulated / enterprise | All 10 | + ADR + CIA + everything |

Don't pick a profile up-front. Add a template the day you cannot answer its question without one.

---

## Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| One huge `docs/` folder, flat | Same problem these templates fixed | Use the 4-tier structure |
| Hand-maintaining `5-views/` (doesn't exist in v6.0) | Decays in a week | Run `sunnydata-auto-regen` skill |
| Editing accepted ADRs | Loses history | Write new ADR with `supersedes` |
| PRD without `target-release` date | Becomes timeless wishlist | Date-stamp; archive when shipped |
| Mixing tier-0 invariants with tier-4 PRDs | Stability semantic broken | Mirror 4-tier structure strictly |

---

## Skill / command quick reference

| Tool | When |
|---|---|
| `sunnydata-design` skill | Before non-trivial implementation |
| `sunnydata-change-impact-analysis` skill | Before any change touching flow/contract/data/architecture |
| `sunnydata-doc-freshness` skill | Weekly maintenance |
| `sunnydata-auto-regen` skill | After major refactor (regen tier-5 views) |
| `sunnydata-contract-stack-audit` skill | Pre-release (Gate 5) |
| `sunnydata-changelog-sync` skill | Before tagging release |
| `vibecoding-write-*` skills | When drafting a specific tier-2 contract |

---

## See also

- [`BEDROCK.md`](./BEDROCK.md) — entry point (read first)
- [`INDEX.md`](./INDEX.md) — full template catalog
- [`OWNERSHIP-MATRIX.md`](./OWNERSHIP-MATRIX.md) — who edits what
- `.claude/coordination/migration-v5-to-v6.md` — upgrading from v5.x
