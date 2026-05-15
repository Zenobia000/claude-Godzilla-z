# How to Instantiate VibeCoding Templates in Your Project

> This template repository provides **empty forms** (the `*.template.md` files) and **read-only guides**. When you use them in a real project, the **filled-in instances** belong in your project's own directory tree, not here.

## Recommended `docs/` layout for end-user projects

Mirror the same 6-tier structure inside your project:

```
your-project/
├── src/                                     # the code
├── tests/                                   # the tests
└── docs/
    ├── 0-principles/
    │   └── PRODUCT-PRINCIPLES.md            # one file, filled from template
    │
    ├── 1-decisions/
    │   ├── ADR-0001-database-choice.md      # append-only, numbered
    │   ├── ADR-0002-auth-strategy.md
    │   └── ARCHITECTURE-OVERVIEW.md         # one file, updated per-quarter
    │
    ├── 2-contracts/                         # MUST stay synced with code
    │   ├── api/
    │   │   └── v1.openapi.yaml
    │   └── modules/
    │       ├── user-service.md
    │       └── payment-service.md
    │
    ├── 3-process/                           # usually copied verbatim from templates
    │   ├── PROC-0003-code-review-checklist.md
    │   ├── PROC-0004-security-readiness-checklist.md
    │   └── PROC-0005-deployment-runbook.md
    │
    ├── 4-exploration/                       # date-stamped, archive when done
    │   ├── PRD-2026-Q2-onboarding.md
    │   ├── WBS-2026-Q2.md
    │   └── archive/                         # move stale stuff here, don't delete
    │
    └── 5-views/                             # auto-generated; never hand-edit
        ├── VIEW-0001-project-structure.md
        ├── VIEW-0002-file-dependencies.md
        └── VIEW-0003-class-relationships.md
```

## Why mirror the tier numbers?

Two reasons:
1. **Cognitive transfer**: anyone who knows VibeCoding tiers immediately understands your `docs/` layout
2. **AI context efficiency**: `0-principles` always loads first; `5-views` is read with skepticism. The path itself encodes that policy.

## Mandatory frontmatter for tier 2 (contracts)

Every file in `docs/2-contracts/` carries:

```yaml
---
last-synced-with: <git-commit-sha>
sync-source: code | doc                # which side is authoritative
source-paths:
  - src/api/users.py
  - src/models/user.py
synced-at: 2026-05-10
---
```

The `post-write` hook auto-updates `last-synced-with` and `synced-at` when you save the file. The `sunnydata-doc-freshness` skill flags docs whose source has moved on.

## Optional frontmatter for tier 4 (exploration)

```yaml
---
status: draft | accepted | shipped | archived
shipped-as: ADR-0007, src/payments/v2/
shipped-at: 2026-04-01
---
```

This lets old PRDs link forward to what they became, preserving the rationale trail.

## Anti-patterns to avoid

| Anti-pattern | Why it's bad | What to do instead |
|---|---|---|
| One huge `docs/` folder, flat | Same problem the templates had | Use the 6-tier structure |
| Hand-maintaining `5-views/` | Always becomes stale | Generate from code, regenerate often |
| Editing old ADRs in place | Loses rationale history | Write a new ADR that supersedes the old |
| PRDs without dates in filename | Can't tell which era they describe | Always date-stamp |
| Mixing tier 0 + tier 4 in one file ("vision doc") | Tier mismatch — different update cadences | Split: principles in tier 0, current bet in tier 4 |

## Skill / command quick reference

Once you've instantiated this layout, these are the commands you'll use most:

| Command / skill | When to use |
|---|---|
| `sunnydata-doc-freshness` skill | Weekly, or before any release; surfaces stale tier-2 docs |
| `sunnydata-auto-regen` skill | After any large refactor; rebuilds tier 5 |
| `vibecoding-write-prd` skill | Drafting a new feature PRD into tier 4 |
| `vibecoding-write-adr` skill | Recording a new architectural decision into tier 1 |
| `vibecoding-write-api-contract` skill | New endpoint or schema change into tier 2 |
