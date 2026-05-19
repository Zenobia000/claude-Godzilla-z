---
id: PRIN-0000
title: "Product Principles — Mission / Glossary / Quality Bars / Unit Economics"
status: active
tier: 0-principles
owner: HUMAN-ONLY
essence: bedrock
absorbs: [GLOS-0000-glossary, UE-0000-unit-economics, PRIN-0002-frontend-quality-attributes]
last-reviewed: null
product-version: null
supersedes: null
superseded-by: null
---

# PRIN-0000: Product Principles — `<PROJECT_NAME>`

> **Tier**: 0-principles · **Essence**: bedrock — strategic invariants. Change at most once per major version.
>
> **One foundation, five sections** — read first by every new engineer, AI, and stakeholder. Without these answers, every other doc is built on sand.

---

## §1 — Mission

> One sentence. What this product exists to do, for whom, and why it matters now.

Example: *"Help solo founders ship a working MVP in two weekends by replacing template hunting with one opinionated workflow."*

The mission lives on the landing page hero copy. If they diverge, one of the two is lying.

---

## §2 — Target Users (and Anti-Users)

### §2.1 Primary personas

| Persona | Role / context | Pain we address | Success state |
|---|---|---|---|
| Alex the Solo Founder | indie product builder; 1-3 person team | sleep-loss from overnight ticket pile-up | sleeps; AI triages |
| Sara the Support Lead | small-team support manager | 30 unread tickets every morning | tickets categorized & prioritized at open of day |

Primary count ≤ 2. A product with 5 "primary" personas has no priority.

### §2.2 Anti-personas (NOT designing for)

| Anti-persona | Why excluded |
|---|---|
| Fortune-500 enterprise IT admin | requires SOC-2 type 2 + on-prem; burns 6mo eng on features blocking primary persona |
| Anonymous casual reader | no commercial intent; not in monetization path |

### §2.3 Validation evidence

| Claim | Evidence | Source |
|---|---|---|
| Sleep-loss is top pain | 8 interviews, 7 mentioned | `4-exploration/DISC-NNNN` (folded into PRD §discovery) |
| 75% desktop usage | Posthog Q1 sessions | analytics dashboard |

Claims without evidence marked `[GUESS]`; re-validate annually.

---

## §3 — Non-Goals (what we explicitly will NOT do)

The most load-bearing section. Without it, AI generalizes the product into a competitor of every adjacent tool.

- We will NOT build native mobile apps (web responsive = 92% of mobile usage)
- We will NOT build a marketplace / 3rd-party plugin system (< 50 enterprise customers)
- We will NOT do on-prem deployment (eng cost > revenue ceiling at this stage)
- We will NOT support paid plans below $29/mo (unit economics §5 fail below)

These are not "not now" — they are "not us." Promote to "not now" only with a CR + this doc update.

---

## §4 — Glossary (§terminology, absorbs GLOS-0000)

The vocabulary contract. If two engineers use "customer" to mean different things, every doc downstream is broken.

| Term | Definition | NOT to be confused with |
|---|---|---|
| **Customer** | Paying tenant; owns a workspace | "user" (Customer can have many users) |
| **User** | Person who logs in; belongs to a Customer | "Customer", "account" |
| **Account** | DEPRECATED — use "Workspace" | Customer, User |
| **Workspace** | Tenant-scoped data container | Project (Workspace contains Projects) |
| **Order** | Single fulfillment unit | Subscription (recurring), Invoice (billing artifact) |
| **Subscription** | Recurring billing relationship | Plan (template), Order (one-time) |

Add ≥5 entries on Day 1; grow as terms become ambiguous in PR review. AI MUST defer to this glossary when terms collide.

---

## §5 — Unit Economics (§unit-economics, absorbs UE-0000)

| Metric | Value | Healthy band |
|---|---|---|
| **CAC** (Customer Acquisition Cost) | $150 (paid + content + tools / new paying) | declining or stable |
| **ARPU** (paying-only avg) | $58 | growing |
| **COGS / customer / mo** | $17.40 (infra $4.20 + AI inference $6.80 + support $3.50 + payment $1.80 + vendor $1.10) | < 30% ARPU at scale |
| **Gross margin** | 70% | 60–85% (AI-native SaaS) |
| **Monthly logo churn** | 4.2% | < 5% self-serve healthy |
| **Avg lifetime** | 24 months | longer = healthier |
| **LTV** | $974 | — |
| **LTV / CAC** | 6.5× | > 3× good; > 5× very good |
| **CAC payback** | 3.7 months | < 12 mo self-serve |

**AI inference is a first-class COGS line** — in 2026, often 30–50% of total COGS for AI-native products. If hidden in "infra," you can't manage it.

Sensitivities (top 3 levers):
1. AI inference cost ↓ → LTV ↑↑
2. Monthly churn ↓ → LTV ↑↑↑ (compounds)
3. ARPU ↑ → revenue ↑ but churn-risk ↑

Re-validate quarterly OR on pricing change OR on AI cost shift > 30%.

---

## §6 — Quality Bars (§quality-bars, absorbs PRIN-0002 frontend QA)

Concrete, measurable. Not aspirational.

### §6.1 Performance

| Dimension | Bar | How measured |
|---|---|---|
| API p95 latency (hot path) | < 200ms | k6 nightly + `SRE-NNNN §slo` |
| Frontend FCP | < 1.5s on 3G | Lighthouse CI |
| Frontend LCP | < 2.5s | Web Vitals (RUM) |
| Frontend CLS | < 0.1 | Web Vitals |
| Frontend INP | < 200ms | Web Vitals |
| Time-to-interactive | < 3s on 4G | Lighthouse |
| Bundle size (initial) | < 200 KB gzipped | webpack-bundle-analyzer in CI |

### §6.2 Reliability

| Tier | Target | Window |
|---|---|---|
| T0 services | 99.9% | 28d |
| T1 services | 99.5% | 28d |
| T2 (internal) | 99% | 28d |

Detail in `SRE-NNNN §slo`.

### §6.3 Security

| Bar | Frequency |
|---|---|
| OWASP top 10 reviewed | per release |
| Dependency scan (`npm/pip/cargo audit`) | per PR (`CIG-*`) |
| Pen-test (external) | annually |
| `AI-NNNN §safety` 100% on adversarial set | per AI feature deploy |

### §6.4 Accessibility (frontend)

| Bar | Test |
|---|---|
| WCAG 2.2 Level AA | `community-a11y-audit` skill |
| Keyboard navigation | manual + axe-core |
| Color contrast ≥ 4.5:1 (text) | design tokens enforce; Chromatic |
| Screen-reader smoke | manual per major release |

### §6.5 Responsive breakpoints

| Name | Width | Target devices |
|---|---|---|
| `sm` | ≥ 640px | small tablet |
| `md` | ≥ 768px | tablet |
| `lg` | ≥ 1024px | laptop |
| `xl` | ≥ 1280px | desktop |

Mobile-first; > 75% of CSS in `lg:` prefix → re-evaluate.

### §6.6 Test coverage

| Layer | Bar |
|---|---|
| Unit (line) | 80% |
| Unit (branch) | 70% (drop in pure-DTO modules) |
| Integration | every API endpoint + critical flow |
| E2E | 5 golden paths per release |
| LLM-eval | per `AI-NNNN §safety §6` if AI feature |

---

## §7 — Technical Invariants (cannot violate without ADR)

- **Data sovereignty**: User data stays in EU region for EU users (`DATA-NNNN §master-data §residency`)
- **Backwards compatibility**: Public API breaking change requires 6mo deprecation (per `PROC-0002 §deprecation`)
- **Tech-stack constraints**: Backend on PostgreSQL only; no second OLTP DB
- **Operational constraints**: All long-running jobs idempotent (per `FLOW-NNNN §sub-flow §idempotency`)
- **AI safety**: 5-layer defense per `AI-NNNN §safety §2`; no single-layer trust
- **Cost**: AI inference per customer ≤ $10/mo (else unit economics §5 breaks)

Violation requires `1-decisions/ADR-NNNN` with `supersedes` pointing at the invariant being relaxed.

---

## §8 — Decision-Making Defaults

When the team (or AI) faces a tradeoff with no explicit guidance:

- **Simplicity over flexibility** until flexibility is proven necessary
- **Read paths over write paths** when optimizing
- **Explicit over implicit** in API design
- **Server-side over client state** unless interaction demands otherwise
- **Append-only over mutation** in audit / event paths
- **Standard library over dependency** for problems < 100 LOC
- **Boring tech over shiny tech** in core path; new tech in periphery only

Customize per project. Encode team instincts so AI doesn't guess.

---

## §9 — Out-of-Date Indicators

This document is stale when ANY of the following is true. Re-review immediately:

- [ ] §1 mission no longer matches public landing page headline
- [ ] §2 persona added / removed without §2 update
- [ ] An ADR overrode a §7 invariant without §7 update
- [ ] Competitor launched feature we now differentiate against, not in §3
- [ ] §5 unit economics last refreshed > 6 months ago
- [ ] §5 AI inference cost moved > 30% since last review
- [ ] §6 quality bars haven't been hit by 2 consecutive releases (bar too high OR slipping)

---

## See also

- `PRIN-0001-flow-id-conventions.md` — ID naming
- `PRIN-0003-engineering-contract-stack.md` — 10-layer map
- `1-decisions/ADR-0000-adr.template.md` — how to record §7 violations
- `1-decisions/ARCH-0000-architecture-overview.template.md` — system shape that serves §1 mission
- `4-exploration/PRD-0000-prd.template.md` — features must serve §2 primary personas + §5 economics
- `2-contracts/SRE-0000-reliability.template.md` — §6.2 SLO operationalization
- `2-contracts/AI-0000-ai-system-contract.template.md` — §7 AI safety implementation
