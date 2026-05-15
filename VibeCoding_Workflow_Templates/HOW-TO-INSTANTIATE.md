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

## Profile Selection Table

Not every project needs all 47 templates. Choose a **profile** that matches your product type, then instantiate only the templates marked for that profile. Templates outside your profile can still be added later.

Legend: **R** = required, **O** = optional, **—** = skip

| Template | `web-product` | `data-ml` | `platform-infra` | `full` |
|---|---|---|---|---|
| **Tier 0 — Principles** | | | | |
| PRIN-0000 Product Principles | R | R | R | R |
| PRIN-0001 Flow ID Conventions | R | O | O | R |
| GLOS-0000 Glossary | R | R | O | R |
| PRIN-0002 Frontend Quality Attributes | R | — | — | R |
| **Tier 1 — Decisions** | | | | |
| ADR-0000 ADR template | R | R | R | R |
| ARCH-0000 Architecture Overview | R | R | R | R |
| ARCH-0001 Module Boundary | R | O | O | R |
| DDD-0000 Domain Model | R | O | — | R |
| ARCH-0002 Frontend Tech Stack | R | — | — | R |
| ARCH-0003 Infra Architecture | O | O | R | R |
| **Tier 2 — Contracts** | | | | |
| API-0000 API Spec | R | O | O | R |
| MC-0000 Module Contract | R | O | O | R |
| BF-0000 Business Flow | R | O | O | R |
| UF-0000 User Flow | R | O | — | R |
| SF-0000 Sub Flow | R | O | — | R |
| FR-0000 Functional Requirement | R | O | O | R |
| SM-0000 State Machine | O | O | O | R |
| MDS-0000 Master Data | R | O | — | R |
| FI-0000 Flow Index | R | — | — | R |
| TM-0000 Traceability Matrix | R | O | O | R |
| DS-0000 Design System | R | — | — | R |
| PC-0000 Page Contract | R | — | — | R |
| SLO-0000 SLO Spec | O | O | R | R |
| PIPE-0000 Pipeline Contract | — | R | O | R |
| MODEL-0000 Model Card | — | R | — | R |
| OBS-0000 Observability Spec | O | O | R | R |
| CAP-0000 Capacity Planning | O | O | R | R |
| **Tier 3 — Process** | | | | |
| PROC-0001 Workflow Manual | R | R | O | R |
| PROC-0002 BDD Guide | R | O | — | R |
| PROC-0003 Code Review Checklist | R | R | R | R |
| PROC-0004 Security Readiness | R | O | R | R |
| PROC-0005 Deployment Runbook | R | O | R | R |
| PROC-0006 Docs Maintenance | R | O | O | R |
| QG-0000 Quality Gates | R | O | O | R |
| TP-0000 Test Plan | R | R | O | R |
| PROC-0007 Vendor API Test | O | O | O | R |
| PROC-0008 Frontend Pre-merge | R | — | — | R |
| PROC-0009 Incident Response | O | O | R | R |
| PROC-0010 Chaos Engineering | — | — | R | R |
| PROC-0011 GitOps Runbook | — | — | R | R |
| PROC-0012 Deprecation Playbook | O | O | O | R |
| ONBOARD-0000 Team Onboarding | R | R | R | R |
| **Tier 4 — Exploration** | | | | |
| PRD-0000 PRD | R | R | O | R |
| WBS-0000 WBS | R | R | O | R |
| CIA-0000 Change Impact Analysis | R | O | O | R |
| EXP-0000 Experiment Log | — | R | — | R |
| DISC-0000 Discovery Research | O | R | O | R |
| **Tier 5 — Views** | | | | |
| VIEW-0001 Project Structure | R | R | R | R |
| VIEW-0002 File Dependencies | R | O | O | R |
| VIEW-0003 Class Relationships | R | O | — | R |
| VIEW-0004 Frontend Route Map | R | — | — | R |

**Quick counts:**
- `web-product`: 33 R + 8 O = 41 relevant (skip 11)
- `data-ml`: 14 R + 23 O = 37 relevant (skip 15)
- `platform-infra`: 15 R + 19 O = 34 relevant (skip 18)
- `full`: 52 R (all templates)

---

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
