---
id: DATA-0000
title: "Data Contract — Master Data / Migration / Pipeline / Model"
status: active
tier: 2-contracts
owner: HYBRID
essence: specialized
absorbs: [MDS-0000, MIG-0000, PIPE-0000, MODEL-0000]
last-synced-with: null
sync-source: doc
source-paths: ["db/migrations/", "data/", "models/"]
synced-at: null
---

# DATA-0000: Data Contract

> **Tier**: 2-contracts · **Essence**: bedrock — every system has data; without a contract, schema drifts faster than docs can chase.
>
> **One template, four sections**: pick the §sections that apply to your data asset. `§master-data` for governed entities; `§migration` for any schema change; `§pipeline` for data-eng workflows; `§model-card` for ML artifacts.

---

## §0 — Identity

| Field | Value |
|---|---|
| ID | `DATA-NNNN` (or sub-IDs: `DATA-NNNN.MDS`, `DATA-NNNN.MIG-rev`, `DATA-NNNN.PIPE`, `DATA-NNNN.MODEL`) |
| Asset | Table / dataset / model name |
| Owner | Team responsible |
| Domain | Bounded context this data lives in |
| Classification | `public` / `internal` / `confidential` / `regulated` (PII / PHI / PCI) |

---

## §1 — Master Data (§master-data)

> Use when the asset is a long-lived governed entity (`customer`, `product`, `account`, `agreement`).

### §1.1 Identity & lifecycle

| Property | Value |
|---|---|
| Natural key | `email_lowercased + tenant_id` |
| Surrogate key | `uuid` |
| States | active → suspended → archived → deleted (after retention) |
| Retention | 7y after delete-request (regulated); 30d soft-delete window |
| Owner-of-record | CRM (Stripe customer record is mirror, not master) |

### §1.2 Data quality rules

| Rule | Severity | Detection |
|---|---|---|
| Email format valid | Block | Schema validation |
| One active customer per tenant | Block | Unique constraint |
| `last_login_at` ≥ `created_at` | Warn | Nightly batch |
| Country in ISO 3166-1 | Block | CHECK constraint |

### §1.3 GDPR / consent

| Right | Mechanism | SLA |
|---|---|---|
| Access (Art. 15) | `/me/export` endpoint; JSON+ZIP | 30d |
| Erasure (Art. 17) | Hard-delete after 30d cool-off | 30d (60d max if disputes) |
| Portability (Art. 20) | Same as access | 30d |
| Consent receipts | Per-tenant `consent_log` table | Immutable |

### §1.4 Replication

| Target | Direction | Lag SLO | Conflict resolution |
|---|---|---|---|
| Read replica | Master → replica | < 5s | Eventually consistent |
| Search index (Elastic) | Master → index | < 30s | Master wins |
| Stripe (vendor) | Master → vendor (push) | Manual reconcile nightly | Vendor record advisory only |

---

## §2 — Schema Migration (§migration)

> Use for every schema-altering change. One §section per migration revision.

### §2.1 Migration metadata

| Field | Value |
|---|---|
| Revision | `0042_cancel_fee` |
| Parent | `0041_partial_cancel` (forms DAG) |
| References | `CR-NNNN`, `MC-NNNN §invariant.4`, `FR-NNNN` |
| Tool | Alembic / Flyway / sqitch / golang-migrate (state once per project in `ARCH-NNNN`) |
| Reversible? | Yes / "see PROC-0002 §incident.recovery" |

### §2.2 Forward (`upgrade()`)

```python
def upgrade() -> None:
    op.add_column("work_orders",
        sa.Column("cancel_fee_amount", sa.Numeric(12, 2),
                  nullable=False, server_default="0"))
    op.create_check_constraint("ck_wo_cancel_fee_nonneg",
                               "work_orders", "cancel_fee_amount >= 0")
```

### §2.3 Reverse (`downgrade()`)

```python
def downgrade() -> None:
    op.drop_constraint("ck_wo_cancel_fee_nonneg", "work_orders", type_="check")
    op.drop_column("work_orders", "cancel_fee_amount")
```

### §2.4 Migration policy (per project, written once)

| Topic | Rule |
|---|---|
| Branching | One head only; multi-head requires `CR-NNNN` justification |
| Backfill in migration | OK for < 100k rows; larger → async job + reference in docstring |
| Long-locking DDL | Forbidden; use `CREATE INDEX CONCURRENTLY` / pt-osc / gh-ost |
| Online schema change | Required for tables > 1M rows |
| Production downtime allowed? | No, except major version with announced window |

### §2.5 Migration sibling example

See `MIG-0000-schema-migration.example.alembic-env.py` in v5.8 (now archived); typical `env.py` reads `DATABASE_URL` from env, configures `compare_type=True` + `transaction_per_migration=True`.

---

## §3 — Data Pipeline (§pipeline)

> Use for ETL / ELT / streaming pipelines. One §section per pipeline.

### §3.1 Pipeline identity

| Field | Value |
|---|---|
| Name | `daily_revenue_rollup` |
| Type | Batch (Airflow) / Stream (Kafka + Flink) / Reverse-ETL |
| Cadence | Daily 02:00 UTC / continuous |
| Owner | data-eng team |

### §3.2 Input contract

| Source | Format | Schema | Freshness SLA |
|---|---|---|---|
| `orders` table | Postgres CDC | matches `MC-orders §schema` | < 5min |
| `refunds` table | Postgres CDC | matches `MC-refunds §schema` | < 5min |

### §3.3 Output contract

| Sink | Format | Schema | Consumer |
|---|---|---|---|
| `analytics.daily_revenue` table | Postgres | (date, tenant_id, gross_cents, refund_cents, net_cents) | BI dashboards, finance close |

### §3.4 Data quality gates

| Gate | Threshold | Action on breach |
|---|---|---|
| Row count vs 7d baseline | ±20% | Page on-call; freeze downstream |
| Null rate on `tenant_id` | 0% | Fail run; do not partial-publish |
| Schema match | exact | Fail; alert schema team |
| Freshness | source < 30min old | Wait + retry 3× |

### §3.5 Lineage

```
orders (Postgres) ─┐
                   ├──► daily_revenue_rollup ──► analytics.daily_revenue ──► Looker / Metabase
refunds (Postgres) ┘
```

Lineage is **machine-readable** in OpenLineage / DataHub if available; this diagram is the human-readable mirror.

---

## §4 — ML Model Card (§model-card)

> Use for each deployed ML / LLM-fine-tuned model. For prompt-engineering only (no training), see `AI-0000 §prompt` instead.

### §4.1 Model identity

| Field | Value |
|---|---|
| Name + version | `churn_predictor v3.2` |
| Type | Classification (binary) / Regression / Generation / Embedding |
| Training framework | scikit-learn 1.4 / PyTorch 2.3 / fine-tuned LLM |
| Artifact location | `s3://example-models/churn/v3.2/` |
| Owner | ml-team |

### §4.2 Intended use (and NON-use)

| Intended | Forbidden |
|---|---|
| Predict churn in next 30d for paying customers | Block accounts based on predicted churn |
| Inform retention email targeting | Used as evidence in disputes |
| | Inputs from < 30d-tenured users (training data was 90d+) |

### §4.3 Metrics (validation set)

| Metric | Value | Baseline |
|---|---|---|
| AUC-ROC | 0.83 | random = 0.5 |
| Precision @ top-10% | 0.42 | base rate = 0.08 |
| Recall @ top-10% | 0.51 | — |
| Demographic parity gap (by region) | 0.04 | < 0.10 target |

### §4.4 Bias / fairness analysis

| Subgroup | Performance | Note |
|---|---|---|
| US users | AUC 0.85 | Baseline |
| EU users | AUC 0.78 | -7pp; investigate; usable but flag in retention copy |
| APAC users | AUC 0.71 | Below threshold; do NOT deploy in APAC |

### §4.5 Lineage

| Property | Value |
|---|---|
| Training data | `s3://example-data/churn-training/2026-04/` (300k rows, 90d horizon) |
| Training pipeline | `PIPE-NNNN-churn-training` |
| Trained from | `churn_predictor v3.1` (transfer learning) |
| Code | `git@example:ml-models@a7b3c2d` |
| Reproducibility | `EXP-NNNN-churn-v3.2` (see `TEST-0000 §experiment`) |

### §4.6 Deployment constraints

| Constraint | Rationale |
|---|---|
| Don't serve under-30d tenured users | Training distribution mismatch |
| Don't serve APAC region | §4.4 bias |
| Inference SLO p95 < 100ms | Synchronous prediction path |
| Retraining cadence | Quarterly OR when feature drift > 0.15 |

---

## §5 — CI gates (which apply per §section)

| §section | CI gate |
|---|---|
| §master-data | None automated (governance; quarterly review) |
| §migration | `CIG-0007` doc-freshness; manual `alembic upgrade head` smoke |
| §pipeline | DQ assertion runs (great_expectations / dbt tests) per run |
| §model-card | Eval set re-run on every deploy (see `TEST-0000 §llm-eval` for LLM; classic ML uses own harness) |

---

## §6 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Master-data spec without retention policy | GDPR audit fails | §1.3 mandatory for regulated data |
| Migration without `downgrade()` body | Non-prod environments stuck | Write it, or raise `NotImplementedError` with link |
| Pipeline without DQ gates | Bad data ships silently | §3.4 mandatory |
| Model card without "non-use" section | Misuse in prod | §4.2 anti-pattern table |
| "We'll write migrations later" | Race conditions on shared tables | Migration tool from day 1 |
| Bias analysis only on overall set | Subgroup harms hidden | §4.4 mandatory subgroup breakdown |

---

## See also

- `PRIN-0003-engineering-contract-stack.md` §L2 — data layer
- `MC-0000-module-contract.template.md` — entity invariants (DbC) consumed by §master-data
- `API-0000-api-spec.template.md` — wire surface for data writes
- `AI-0000-ai-system-contract.template.md` — LLM-specific; this template covers classic ML
- `TEST-0000-testing-strategy.template.md` §experiment — reproducibility for §model-card
- `SRE-0000-reliability.template.md` — pipeline SLO + DQ alerting
