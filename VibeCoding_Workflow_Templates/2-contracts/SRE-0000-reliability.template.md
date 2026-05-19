---
id: SRE-0000
title: "Reliability — SLO / Observability / Capacity"
status: active
tier: 2-contracts
owner: HYBRID
essence: bedrock
absorbs: [SLO-0000, OBS-0000, CAP-0000]
last-synced-with: null
sync-source: doc
source-paths: ["dashboards/", "alerts/", "infra/"]
synced-at: null
---

# SRE-0000: Reliability Contract

> **Tier**: 2-contracts · **Essence**: bedrock — without an SLO, "is it working?" has no answer; without observability, SLOs are aspirational; without capacity, the SLO is a wish.
>
> **One contract, three sections** — they're inseparable in practice. Targets (§slo) need metrics (§observability) need resources (§capacity).

---

## §0 — Identity

| Field | Value |
|---|---|
| Service | `order-service` (one SRE-NNNN per service or critical user-flow) |
| Owner | platform team + on-call rotation |
| Criticality tier | `T0` (revenue-critical) / `T1` (user-facing) / `T2` (internal) / `T3` (best-effort) |

---

## §1 — Service Level Objectives (§slo)

### §1.1 SLI catalog (what we measure)

| SLI | Definition | Good event |
|---|---|---|
| **Availability** | `successful_requests / total_requests` | HTTP 2xx / 3xx within 30s |
| **Latency-p95** | 95th percentile request duration | < 500ms |
| **Quality** | semantic correctness (per business rule) | passes downstream validation |
| **Freshness** | data lag | < 5min for CDC pipelines |

Pick 2-4 SLIs per service. More than 4 → noise.

### §1.2 SLOs (the actual targets)

| SLO | Target | Window | Error budget |
|---|---|---|---|
| Availability | 99.9% | 28 rolling days | 40min 19s/window |
| Latency-p95 | < 500ms 95% of requests | 7d | 5% slow requests/week |
| Order-create success | ≥ 99.5% (excluding 4xx) | 28d | 3h 21min |

T0 → 99.9%-99.95% (more is fantasy at startup scale).
T1 → 99.5%-99.9%.
T2 → 99% is fine.

### §1.3 Error budget policy

| Burn rate | Action |
|---|---|
| < 1× expected | Normal velocity |
| 1× — 2× | Reduce non-critical deploys this week |
| 2× — 14× | Freeze feature work; ops focus only |
| > 14× (fast burn) | Page on-call; incident response per `PROC-0002 §incident` |

Error-budget breach is **not** a punishment — it's a signal that "feature velocity" was costing reliability.

### §1.4 SLA mapping (external)

| External SLA | Internal SLO | Buffer |
|---|---|---|
| Customer-facing: 99.5% (contractual) | Internal: 99.9% | 0.4pp buffer absorbs minor incidents |

Never set internal SLO equal to external SLA — buffer is mandatory.

---

## §2 — Observability (§observability)

### §2.1 The three signals

| Signal | Storage | Retention | Cost |
|---|---|---|---|
| **Metrics** (time series) | Prometheus / CloudWatch | 30d hot / 1y agg | $$ |
| **Logs** (events) | Loki / DataDog | 7d hot / 30d cold | $$$ (logs are expensive) |
| **Traces** (request flow) | Tempo / Jaeger / Honeycomb | 7d | $$ |

Logs are the worst $-per-insight; metrics + traces should answer 80% of questions.

### §2.2 Metric catalog per service

| Metric | Type | Labels | Used for |
|---|---|---|---|
| `http_requests_total` | counter | (method, path, status) | availability SLI |
| `http_request_duration_seconds` | histogram | (method, path) | latency SLI |
| `db_query_duration_seconds` | histogram | (query_kind) | sub-latency attribution |
| `business_event_total` | counter | (event_type, outcome) | quality SLI |

**Cardinality rule**: total label values per metric < 10k. `user_id` as a label = always bad.

### §2.3 Log discipline

| Rule | Rationale |
|---|---|
| Structured JSON | Greppable; queryable |
| Always include `trace_id` | Stitch with traces |
| No PII in logs | GDPR + grep risk |
| No `print(f"got {request}")` debug logs in prod | Cost + noise |
| Log levels: ERROR / WARN / INFO; not DEBUG in prod | Cost |

### §2.4 Trace discipline

| Rule | Rationale |
|---|---|
| Trace every HTTP / queue / DB call | Latency attribution |
| Propagate `trace_id` across services | E2E view |
| Sample rate: 100% errors, 1% success | Cost vs coverage |
| Tag spans with business attributes (`order_id`, `tenant_id`) | Per-customer debugging |

### §2.5 Dashboards

| Dashboard | Audience | Refresh |
|---|---|---|
| Service health (SLI + SLO burn) | On-call | live |
| Per-customer health | Support | hourly |
| Cost burn (per `§3 §capacity`) | Eng leadership | daily |

Each dashboard JSON committed (`dashboards/<name>.json`), not click-built in UI.

### §2.6 Alerts

| Alert | Condition | Page? | Runbook |
|---|---|---|---|
| Burn rate fast | 2% budget in 1h | YES | `PROC-0002 §incident` |
| Burn rate slow | 10% budget in 6h | YES | same |
| Error rate spike | 10× baseline 5min | YES | same |
| Latency p95 > 2× target | sustained 10min | NO (slack) | investigate |

Forbidden: alerts that don't link to a runbook. An alert without a runbook is a notification; not actionable.

---

## §3 — Capacity / Cost (§capacity)

### §3.1 Resource model

| Component | Sizing today | At T+12mo (growth × N) |
|---|---|---|
| App servers | 2 × c6g.large | 6 × c6g.xlarge |
| DB | db.r6g.large | db.r6g.2xlarge + read replica |
| Cache (Redis) | 1 GB | 4 GB |
| Object storage | 50 GB | 500 GB |

Per-component sizing follows from §3.2 traffic estimate.

### §3.2 Traffic & growth

| Metric | Today | T+6mo | T+12mo |
|---|---|---|---|
| MAU | 10,000 | 25,000 | 50,000 |
| Peak QPS | 2 | 6 | 12 |
| Storage (yearly add) | 150 GB | 250 GB | 400 GB |
| AI inference (if applicable) | $1.5k/mo | $3k/mo | $5k/mo |

For design-phase estimation (pre-launch), use `ARCH-NNNN §capacity-estimation` (RESHADED E).

### §3.3 Cost breakdown

| Component | $ / month today | $ / month T+12mo |
|---|---|---|
| Compute | $80 | $200 |
| Database | $50 | $250 |
| Cache | $30 | $100 |
| Storage + egress | $20 | $80 |
| AI inference | $1,500 | $5,000 |
| Observability stack | $150 | $300 |
| **Total** | **$1,830** | **$5,930** |

**Cost / MAU**: $0.18 today → $0.12 at scale. Sanity check against `PRD-NNNN §unit-economics` (ARPU $58).

### §3.4 Cost burn alerts

| Threshold | Action |
|---|---|
| 80% monthly budget by day 25 | Notify owner |
| 100% by day 28 | Page on-call; degrade per §3.5 |
| 120% any time | Page leadership; freeze non-critical features |

### §3.5 Degradation when over budget

Same pattern as `AI-0000 §capacity §5.4` but for infra-wide cost:
1. Tier down (smaller instances at lower SLO temporarily)
2. Shed optional (disable nice-to-have features)
3. Queue / throttle (preserve service for critical paths)
4. Hard fail (rare; last resort)

### §3.6 Scaling triggers

| Trigger | Action |
|---|---|
| CPU > 70% sustained 30min | Horizontal scale +1 |
| DB connection pool > 80% | Pool size up OR read replica |
| AI tokens / month > 80% budget | `AI-0000 §capacity` degradation |
| p95 latency > 2× target sustained 1h | Add capacity OR investigate |

Forbidden: manual scaling on weekends (autoscale handles it OR you're under-engineered).

---

## §4 — CI gates

| Gate | What it checks |
|---|---|
| `CIG-0001` Spectral spec-lint | Endpoints declare SLIs in metadata |
| (custom) burn-rate alerts deployed | Alert config present per service in `alerts/` |
| Dashboard JSON committed | `dashboards/<service>.json` exists |
| Cost forecast updated | `last-synced-with` < 90d for SRE-NNNN |

---

## §5 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| SLO without error budget | "99.9%" is just a number; not a policy | §1.3 mandatory |
| Internal SLO = external SLA | First incident breaches SLA | Buffer per §1.4 |
| `user_id` as metric label | Cardinality explosion | Use trace spans for per-user |
| Alerts without runbook | Notification, not actionable | §2.6 link required |
| Cost line "infrastructure" lumps AI | Cannot manage what you can't see | Separate AI line per §3.3 |
| `99.99%` for everything | Cost balloons; team velocity dies | Pick tier per §0 |
| Same dashboard for on-call + leadership | Different audiences, different needs | §2.5 separate |
| "We'll add observability later" | First incident is blind | Day 1: metrics + structured logs |

---

## See also

- `PRIN-0003-engineering-contract-stack.md` §3 L4 — quality gates layer
- `API-0000-api-spec.template.md` — endpoints define `http_*` SLIs
- `ARCH-0000-architecture-overview.template.md` §infrastructure — physical topology this SRE doc measures
- `AI-0000-ai-system-contract.template.md` §capacity — AI-specific budget (subset)
- `PROC-0002-ops-runbook.template.md` §incident — when alerts fire
- `TEST-0000-testing-strategy.template.md` §performance — load testing feeds capacity model
