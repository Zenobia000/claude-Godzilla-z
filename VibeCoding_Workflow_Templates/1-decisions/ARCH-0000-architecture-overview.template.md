---
id: ARCH-0000
title: "Architecture Overview — C4 / Modules / Stack / Infra / DDD / Capacity / Security / Frontend"
status: active
tier: 1-decisions
owner: HUMAN-ONLY
essence: bedrock
absorbs: [ARCH-0001-module-boundary, ARCH-0002-frontend-tech-stack, ARCH-0003-infra-architecture, DDD-0000-domain-model, EST-0000-capacity-estimation, POL-0000-policy-as-code, DS-0000-frontend-design-system]
last-reviewed: null
product-version: null
supersedes: null
superseded-by: null
---

# ARCH-0000: Architecture Overview

> **Tier**: 1-decisions · **Essence**: bedrock — single source of truth for the system's shape.
>
> **One document, seven sections** — every architectural concern that previously had its own template now lives as a §section here. Read top to bottom on Day 1; come back when adding a module or changing infra.

---

## §1 — System (C4)

### §1.1 Context (L1)

Diagram: who uses the system (actors), what external systems it talks to.

```
[Customer] ──HTTPS──► [our system] ──┬──► [Stripe]
                                     ├──► [SendGrid]
                                     └──► [Anthropic API]
[Admin]    ──HTTPS──►
```

### §1.2 Containers (L2)

Deployable units + tech per container.

| Container | Tech | Purpose |
|---|---|---|
| Web (SSR) | Next.js 14 | Customer + admin UI |
| API | FastAPI / Python 3.12 | REST endpoints |
| Worker | Celery / Redis broker | Async jobs (email, report) |
| Database | Postgres 16 | All persistent data |
| Cache | Redis 7 | Session + hot query cache |
| Search | Postgres FTS (start) → ElasticSearch (when > 1M docs) | Full-text search |
| Object store | S3 | User uploads + generated PDFs |

### §1.3 Components (L3, selective)

Drill into containers that warrant it. Don't draw every internal class — that's `5-views` auto-regen territory.

---

## §2 — Modules (§modules, absorbs ARCH-0001 boundary)

Per-module charter. Each row is the equivalent of an old ARCH-0001 file.

| Module | Owns | Does NOT own | Depends on | Owner team |
|---|---|---|---|---|
| `M01-iam` | user, session, token, MFA | billing tier (M11) | — | platform |
| `M11-billing` | invoice, subscription, payment | refund policy (M12) | M01 | billing |
| `M12-orders` | order, cart, fulfillment | payment processing (M11) | M01, M11 | commerce |
| `M21-analytics` | metrics, dashboards | source data ownership | (CDC from all) | data-eng |

**Boundary rules**:
- Module imports a sibling only via its public API (`API-NNNN` or `MC-NNNN`)
- Cross-module data access via CDC / outbox events, not direct DB joins
- Forbidden: reverse-import (lower-level imports auth/policy) — enforced by `CIG-0009`

---

## §3 — Domain Model (§domain-model, absorbs DDD)

### §3.1 Bounded contexts

| Context | Module | Aggregates | Lang ubiquitous |
|---|---|---|---|
| Identity | M01-iam | `User`, `Session` | "user", "principal" |
| Billing | M11-billing | `Subscription`, `Invoice`, `Payment` | "subscription" (≠ "plan") |
| Commerce | M12-orders | `Order`, `Cart`, `Fulfillment` | "order" |

### §3.2 Aggregates (one block per critical aggregate)

#### `Order` (Commerce context)

**Identity**: `order_id: UUID`

**Invariants** (always true):
- `total = sum(line_items.amount × line_items.qty)`
- `status ∈ {draft, confirmed, paid, shipped, cancelled}` (state machine in `MC-orders §state-machine`)
- `cancelled` → refund recorded within 24h

**Domain events emitted**:
- `OrderCreated.v1` — after first commit
- `OrderConfirmed.v1` — after inventory reserve + payment auth
- `OrderCancelled.v1` — after status → cancelled

**Forbidden mutations**: cannot change `customer_id` after creation; cannot decrement `total` outside refund flow.

### §3.3 Context map (relationships)

```
Identity ──(upstream)──► Billing
                          ├──(downstream)──► Commerce
                          └──(partner)──► Analytics (CDC)
```

Relationship types: upstream/downstream, customer/supplier, conformist, anti-corruption layer (ACL), shared-kernel.

---

## §4 — Tech Stack (§stack, absorbs ARCH-0002 frontend stack)

### §4.1 Backend

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 | team strength + AI lib ecosystem |
| Web framework | FastAPI | async + Pydantic schemas |
| ORM | SQLAlchemy 2 + Alembic | mature; migration tool (`DATA-NNNN §migration`) |
| DB | Postgres 16 | JSON + FTS + extensions |
| Queue | Redis + Celery | low-friction at start; revisit at 10× scale |

### §4.2 Frontend

| Layer | Choice | Rationale |
|---|---|---|
| Framework | Next.js 14 (App Router) | SSR + RSC + file-based routing |
| UI library | React 19 | concurrent features |
| Styling | Tailwind + shadcn/ui | utility-first; design tokens via §6 |
| State | TanStack Query + Zustand | server cache + minimal client state |
| Type generation | `openapi-typescript` from `openapi.yaml` | spec → types automation |

### §4.3 AI / ML (only if applicable)

| Layer | Choice |
|---|---|
| LLM | Anthropic Claude (primary), OpenAI (fallback per `AI-NNNN §capacity`) |
| Embeddings | `text-embedding-3-large` (pinned) |
| Vector store | pgvector (start) → Pinecone (when > 1M chunks) |
| Eval harness | `TEST-NNNN §llm-eval` |

### §4.4 Tooling

| Concern | Choice |
|---|---|
| Package mgr | uv (Python), pnpm (Node) |
| Linter | Ruff (Py), ESLint (JS), Spectral (OpenAPI) |
| Test | pytest, Vitest, Playwright (E2E) |
| Migration | Alembic |

---

## §5 — Infrastructure (§infrastructure, absorbs ARCH-0003)

### §5.1 Topology

```
Internet ──► CloudFront (CDN) ──► ALB ──► ECS Fargate (app + worker)
                                          │
                                          ├──► RDS Postgres (primary + RR)
                                          ├──► ElastiCache Redis
                                          ├──► S3 (uploads + backups)
                                          └──► Secrets Manager
```

### §5.2 Regions & DR

| Property | Value |
|---|---|
| Primary region | `us-east-1` |
| DR region | `us-west-2` (warm standby; daily snapshot replica) |
| RPO (recovery point) | 1 hour |
| RTO (recovery time) | 4 hours |
| Multi-AZ | Yes (RDS, ECS) |

### §5.3 IaC

| Tool | Scope |
|---|---|
| Terraform | All AWS resources |
| Helm | Kubernetes (if applicable) |
| ArgoCD | GitOps for K8s (see `PROC-0002 §gitops`) |

State file in S3 backend, locked via DynamoDB. Never `terraform apply` from a laptop.

### §5.4 Networking

| Concern | Value |
|---|---|
| VPC | 10.0.0.0/16 |
| Subnets | 3 AZs × (public + private + DB) |
| Egress | NAT GW per AZ (HA) |
| Private endpoints | S3, Secrets Manager via VPC endpoints |

### §5.5 Security baseline

| Control | Implementation |
|---|---|
| At-rest encryption | RDS + S3 KMS-encrypted (per-env keys) |
| In-transit | TLS 1.2+ everywhere; mTLS service-to-service |
| Secrets | AWS Secrets Manager + Vault SDK; never in env files committed |
| Access logs | CloudTrail to S3 + GuardDuty enabled |

---

## §6 — Frontend Design System (§frontend, absorbs DS-0000)

### §6.1 Design tokens

Machine-readable source: `frontend/tokens/design-tokens.json` (Style Dictionary format).
Build output: CSS variables (web), Swift extensions (iOS), Android XML — `npm run build:tokens`.

Token categories: color (brand / neutral / semantic), spacing, radius, font (family / size / weight / line-height), shadow, breakpoint, motion.

**Rule**: components consume `color.semantic.text-primary`, NOT `color.neutral.900` — semantic layer is the API.

### §6.2 Atomic levels

```
Atoms      → Button, Input, Icon, Badge
Molecules  → SearchBar, FormField, Card
Organisms  → Header, Sidebar, DataTable
Templates  → DashboardLayout, AuthLayout
Pages      → /dashboard, /orders/[id]   (one PC-NNNN per route → see FR-NNNN §page-contract)
```

### §6.3 Component contract

Every shared component declares:
- TypeScript prop types (generated from OpenAPI where applicable)
- Storybook story (one happy + one edge)
- Visual regression baseline (Chromatic / Percy)
- A11y AAA per `PRIN-0000 §quality-bars`

### §6.4 API client + auth

Client: generated TS types from `openapi.yaml` + thin fetch wrapper.

Auth: cookie-based session (httpOnly + SameSite=Strict + Secure) for SSR pages; bearer token for SPA endpoints.

### §6.5 Frontend security checklist

See `PROC-0001 §security-review §4.1`.

---

## §7 — Capacity Estimation (§capacity-estimation, absorbs EST-0000)

> Design-phase napkin math. Production capacity = `SRE-NNNN §capacity`.

### §7.1 Assumptions (state before estimating)

| Assumption | Value | Source |
|---|---|---|
| MAU at launch | 10,000 | PRD `PRD-NNNN §3` |
| DAU / MAU ratio | 30% | Industry baseline |
| Peak / avg traffic | 5× | Last 30d analytics |
| Actions per DAU per day | 12 | Posthog event volume |
| Growth 12mo | 5× | Roadmap target |

### §7.2 Traffic (RESHADED E)

| Metric | Value |
|---|---|
| DAU | 3,000 |
| Avg actions/day | 36,000 |
| Average QPS | 0.42 |
| Peak QPS | 2.1 |
| Peak QPS at T+12mo | ~10 |

Round generously. Order of magnitude, not 3 sig figs.

### §7.3 Storage (RESHADED S)

| Object | Bytes/record | Records/yr | Total/yr |
|---|---|---|---|
| User profile | 2 KB | 11k | 22 MB |
| Audit event | 500 B | 13M | 6.5 GB |
| Artifact w/ content | 50 KB | 2.9M | 145 GB |
| **Total/yr** | — | — | **~152 GB** |

Retention scenarios: hot 90d / hot+warm 1y / +cold 3y. Pick before schema.

### §7.4 Cost forecast (design-phase)

| Component | At launch | T+12mo |
|---|---|---|
| Compute | $80 | $200 |
| Database | $50 | $250 |
| Storage + egress | $5 + $10 | $20 + $40 |
| AI inference | $1,500 | $5,000 |
| Observability | $150 | $300 |
| **Total** | **$1,800** | **~$5,800** |

Cost / MAU sanity vs ARPU (`PRD-NNNN §unit-economics`): $0.18 today → $0.12 at scale.

### §7.5 Bottlenecks (forward-looking)

| Bottleneck | Trigger | Mitigation |
|---|---|---|
| Single-writer DB | Writes > 500/sec | Read replicas; eventually shard by `tenant_id` |
| AI inference cost | $5k/mo line | `AI-NNNN §capacity` degradation |
| Cross-region latency | > 30% APAC users | Multi-region — file new ADR |

### §7.6 Sharding decision (forward-looking)

If you can't rule out future sharding → make `tenant_id` the partition key from day 1. Adding it later is the most painful migration.

---

## §8 — Security Policy (§security, absorbs POL-0000)

### §8.1 Authz model

| Subject | Identity | Roles | ABAC attributes |
|---|---|---|---|
| End user | OIDC `sub` | admin / operator / viewer | `mfa_verified`, `tenant_id` |
| Service | mTLS cert CN | (no roles) | service name |
| API key | DB-issued | rate-limited subset | — |

### §8.2 Policy as Code

Engine: OPA (Rego) sidecar OR AWS Cedar in-process. Pick one per project.

Default DENY. Every `allow` rule opts in explicitly.

```rego
package authz
import rego.v1

default allow := false

allow if {
    "admin" in input.subject.roles
    input.subject.attributes.tenant_id == input.resource.attributes.tenant_id
}

allow if {
    input.action in {"read", "cancel"}
    input.resource.type == "order"
    input.resource.attributes.owner_id == input.subject.id
    input.resource.attributes.state in {"created", "confirmed"}
}
```

### §8.3 Evaluation contract

- Auth middleware builds `{subject, action, resource}` from request.
- OPA call latency budget: p99 < 10ms (sidecar) or < 5ms (in-process Cedar).
- Cache: 60s TTL per (subject, action, resource).
- **Engine down → DENY (fail-closed)**.
- Every decision logged with policy version.

### §8.4 Frontend mirror

Frontends receive `permissions: ["cancel", "reassign"]` per resource. Disable/hide based on this — but **always re-check on submit**; backend is source of truth.

### §8.5 Tools / forbidden patterns

See `PROC-0001 §security-review §4`.

---

## §9 — ADR catalog (decisions over time)

| ADR | Topic | Status |
|---|---|---|
| ADR-0001 | (project-specific) | accepted |
| ADR-0002 | ... | accepted |

ADRs live in `1-decisions/ADR-NNNN-*.md` and are append-only. This catalog is the index; each ADR has its own file.

---

## §10 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Architecture diagram only, no tradeoffs | Diagrams hide constraints | Document tradeoffs in this doc OR ADR |
| C4 L4 (every class) hand-drawn | Drifts in a week | Auto-regen (`sunnydata-auto-regen class-graph`) |
| Module boundaries documented, not enforced | Drift to ball of mud | `CIG-0009` reverse-import-lint |
| DDD aggregates without invariants | Just data structures with names | §3.2 invariants block mandatory |
| Stack chosen by hype | Wrong tool, painful migration | §4 rationale column |
| Multi-region claimed but never tested | Discovers it doesn't work during outage | `PROC-NNNN §chaos` annual DR exercise |
| Design tokens in CSS only | iOS/Android can't reuse | §6.1 Style Dictionary JSON |
| Capacity estimate skipped | Architecture chosen blindly | §7 mandatory for design-phase |
| Policy in code | No single source of truth; impossible to audit | §8.2 OPA / Cedar |

---

## See also

- `0-principles/PRIN-0000-product-principles.template.md` — mission this architecture serves
- `0-principles/PRIN-0001-flow-id-conventions.md` — ID naming
- `0-principles/PRIN-0003-engineering-contract-stack.md` — the 10-layer map
- `2-contracts/API-0000-api-spec.template.md` — wire surface this architecture exposes
- `2-contracts/MC-0000-module-contract.template.md` — per-module DbC contracts referenced in §2
- `2-contracts/DATA-0000-data-contract.template.md` — schema / migration / pipeline
- `2-contracts/SRE-0000-reliability.template.md` — production capacity (§7 evolves into this)
- `2-contracts/AI-0000-ai-system-contract.template.md` — AI-specific architecture
- `3-process/PROC-0002-ops-runbook.template.md` — deploy, incident, chaos
- `1-decisions/ADR-0000-adr.template.md` — how to record §9 entries
