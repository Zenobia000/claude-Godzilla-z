---
id: MDS-NNNN
title: "Master Data Specification Template"
status: draft        # draft | active | deprecated | superseded | archived
tier: 2-contracts
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
entity: <master-entity-name>
authoritative-system: <system-of-record-for-this-entity>
last-synced-with: <git-commit-sha>
sync-source: doc                # MDS is authoritative; code follows
source-paths:
  - src/<module>/master/<entity>.py
  - src/<module>/api/<entity>.py
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (Customer, Order, Inventory, PurchaseOrder, Stripe, etc.) come
> from a worked e-commerce/ERP example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.
# MDS-NNNN: `<Entity>` Master Data Specification

> **Tier**: 2-contracts → master data governance contract
>
> **Why a dedicated doc**: in ERP-class systems, **master data ≠ transactional data**. Master data (Customer, Vendor, Item, GL Account, COA, BOM, Routing) lives for years/decades, is shared across modules, has its own approval workflow, and demands data-quality rules that transactional schemas don't. Cramming master data spec into a regular `module-contract` or `domain-model` understates the governance burden.
>
> **Promotion criterion**: any entity that is (a) referenced by ≥ 2 modules, (b) has a manual create/approve/deactivate workflow, (c) is mastered in a system distinct from its consumers — needs a Master Data Spec.

---

## 1. Identity & Classification

| Field | Value |
|---|---|
| Master entity | `Customer` |
| Domain | Sales / CRM |
| Mastered in (system of record) | CRM |
| Replicated to | ERP-AR, Marketing, Support |
| Glossary entry | `0-principles/GLOS-0000-glossary.template.md#Customer` |
| Domain model entry | `1-decisions/DDD-0000-domain-model.template.md` (Sales context) |
| Owning module | `MOD-NNNN` (`Sales` / `CRM`) |
| Data steward | `@customer-master-data-team` |

## 2. Identification Strategy

| Concern | Choice | Rationale |
|---|---|---|
| Surrogate key | `customer_id` (UUID v7) | Sortable, generated, opaque to business |
| Natural key | `(tax_id, country_code)` | Legal identity; uniquely identifies a tax entity |
| Display key | `customer_code` (human-readable, e.g. `ACME-001`) | For UI; can be regenerated; not used in joins |
| Partition key (multi-tenant) | `tenant_id` | Tenant isolation |
| Cross-system correlation | `external_ids[]` (per replica system) | Handles legacy / vendor IDs without coupling |

## 3. Lifecycle States

Reference the dedicated state machine if complex. Inline otherwise.

| State | Meaning | Allowed Operations | Visible to |
|---|---|---|---|
| `prospect` | Identified but not yet onboarded | edit, qualify | Sales only |
| `onboarding` | KYC + credit check in progress | edit, complete_onboarding | Sales + Compliance |
| `active` | Approved; can transact | edit (limited), suspend, deactivate | All consumers |
| `suspended` | Temporary halt (credit / dispute) | reactivate, deactivate | All consumers (read-only) |
| `deactivated` | No longer transactable | reactivate (with approval) | All consumers (historical only) |
| `archived` | Retention period expired data | (none) | Compliance only |

Detailed state machine: `2-contracts/state-machine.<customer>.md`

## 4. Required Attributes (Schema Contract)

Tier into: **Mandatory** (system rejects without), **Strongly Recommended** (warning), **Optional**.

### Mandatory
| Field | Type | Validation | Source |
|---|---|---|---|
| `customer_id` | UUID v7 | system-generated | system |
| `legal_name` | string(255) | non-empty, normalized | user |
| `tax_id` | string | per-country format check | user; verified via tax-authority API |
| `country_code` | ISO 3166-1 alpha-2 | enum | user |
| `default_currency` | ISO 4217 | enum | derived from country |
| `lifecycle_state` | enum | from §3 | system |
| `created_at`, `created_by` | timestamp, user_id | system-set | system |
| `tenant_id` | UUID | tenant context | system |

### Strongly Recommended
| Field | Type | Why |
|---|---|---|
| `industry_code` | ISIC enum | Reporting & risk segmentation |
| `parent_customer_id` | UUID FK | For corporate hierarchies |
| `payment_terms_default` | enum (NET15/NET30/...) | Pre-fills order terms |

### Optional
| Field | Type | Notes |
|---|---|---|
| `notes` | text | Free-form; not searchable |
| `tags[]` | string[] | Marketing segmentation |

## 5. Data Quality Rules

Rules that the master data MUST satisfy. Run as DQ checks (continuous), not just at create.

| Rule ID | Rule | Severity | Detection |
|---|---|---|---|
| DQ-001 | `tax_id` valid format per country | Critical | At create + nightly batch |
| DQ-002 | `tax_id` verified against tax authority | High | Async on create; re-verify yearly |
| DQ-003 | No duplicate `(tax_id, country_code)` within tenant | Critical | DB unique constraint + nightly fuzzy dedup |
| DQ-004 | `parent_customer_id` does not create cycle | Critical | At create + on update |
| DQ-005 | Inactive customer has zero open orders | High | Pre-condition for `deactivate` transition |
| DQ-006 | `default_currency` matches country's default | Warning | At create; UI suggestion |
| DQ-007 | Address geocoding successful | Warning | Async; bulk reprocess weekly |

## 6. Hierarchy & Relationships

Many master entities have hierarchies (corporate parent, GL account roll-up, BOM tree). Document them here:

| Hierarchy | Cardinality | Cycle Detection | Example |
|---|---|---|---|
| Corporate parent (`parent_customer_id`) | optional one-to-one | DQ-004 | ACME US → ACME Holdings |
| Group membership | many-to-many via `customer_groups` | N/A | "VIP Tier", "Wholesale Partners" |

Visualization (mermaid or PNG export from authoritative system).

## 7. Authoritative System & Replication

| Concern | Detail |
|---|---|
| System of record | CRM (writes go here first) |
| Replicas | ERP-AR (read), Marketing (read), Support (read) |
| Replication mechanism | Event-driven via `CustomerCreated` / `CustomerUpdated` events |
| Replication lag SLO | < 30s p95; < 5min p99 |
| Conflict resolution | SoR always wins; replicas reject local writes with `ERR_REPLICA_READONLY` |
| Reconciliation | Nightly sync job catches dropped events |

If you find code modifying customer in ERP-AR, that's a violation — open a ticket, route the write to CRM.

## 8. Authoring Workflow

How does a new master record come to exist?

1. **Initiate**: Sales rep creates `prospect` in CRM
2. **Enrich**: Marketing fills `industry_code`, `tags`
3. **KYC**: Compliance triggers KYC check via vendor (`PROC-0007-vendor-api-test.template.md` for vendor)
4. **Credit Check**: Finance pulls credit report
5. **Approval**: Customer Master Data team transitions `onboarding` → `active`
6. **Replication**: System emits `CustomerActivated` event; replicas pick up
7. **Notify**: Welcome email triggered (`SF-NNNN`)

Every step is auditable; SLA tracked.

## 9. Modification Governance

| Field type | Who can change | Approval needed | Audit |
|---|---|---|---|
| Mandatory legal fields (`legal_name`, `tax_id`) | Compliance only | Yes (4-eyes) | Full audit + reason |
| Financial fields (`payment_terms_default`, `credit_limit`) | Finance | Yes (4-eyes) | Full audit + reason |
| Marketing fields (`tags`, `industry_code`) | Marketing + Sales | Self-approve | Audit |
| Operational (`primary_contact`) | Sales | Self-approve | Audit |
| State transitions | Per state machine §3 | Per state machine | Full audit + reason |

## 10. Deletion / Archival Policy

| Concern | Policy |
|---|---|
| Hard delete | **NEVER** for master data with transaction history |
| Soft delete | Set `lifecycle_state = deactivated`; data retained |
| Archival | After retention period (`7 years` regulatory minimum); move to cold storage |
| GDPR right-to-be-forgotten | Anonymize PII fields; retain transactional skeleton; document in `audit-trail-requirements.md` |

## 11. Initial Data Load (Migration)

For ERP go-live, the first-time data load is a major project of its own.

| Concern | Plan |
|---|---|
| Source | Legacy CRM export (CSV / DB dump) |
| Validation | Run all DQ rules in §5 against the load file BEFORE import |
| Mapping | Source-field → target-field mapping document (separate spreadsheet) |
| De-duplication | Fuzzy match on `(legal_name + tax_id)` to detect legacy duplicates |
| Cutover | Big-bang on cutover weekend; parallel-run for 30 days |
| Rollback | Snapshot before load; restore script tested in staging |
| Sign-off | Data steward sign-off required before go-live |

## 12. Reporting & Analytics

| Concern | Detail |
|---|---|
| Slowly-Changing Dimension (SCD) type | Type 2 (preserve history with effective dates) |
| Effective-date fields | `valid_from`, `valid_to` (exclusive) |
| Snapshot frequency | Daily snapshot to data warehouse |
| Reporting consumers | Customer 360, Cohort analysis, Revenue ops |

## 13. Compliance & Regulatory

| Concern | Requirement |
|---|---|
| PII fields | `legal_name`, `tax_id`, `addresses[]`, `phone_numbers[]`, `emails[]` |
| Encryption at rest | Yes (column-level for PII) |
| Encryption in transit | TLS 1.3 |
| Audit retention | 7 years (financial regs) |
| Geographic restrictions | EU customers' PII processed only in EU regions |
| Right to access (GDPR) | API endpoint to export all customer data within 30 days |
| Right to erasure (GDPR) | Anonymization workflow (preserves transactional skeleton) |

## 14. Test Coverage Required

| Concern | TC ID |
|---|---|
| Each DQ rule (12 rules → 12 TCs minimum) | `TC-NNNN..` |
| Each state transition with role check | `TC-NNNN..` |
| Replication lag within SLO | `TC-NNNN` (perf) |
| Conflict resolution (replica write rejected) | `TC-NNNN` |
| Hierarchy cycle detection | `TC-NNNN` |
| GDPR anonymization preserves transactional integrity | `TC-NNNN` |

## 15. Open Questions

| Question | Owner | Status |
|---|---|---|
| Should we adopt MDM (Master Data Management) tool? | Architect | open |
| How long should anonymized records be kept? | Legal | open |

## 16. Change History

| Date | CR / ADR | Change | Reviewer |
|---|---|---|---|
| YYYY-MM-DD | ADR-NNNN | Initial spec | — |

---

## See also

- `0-principles/GLOS-0000-glossary.template.md` — entity term must trace here
- `1-decisions/DDD-0000-domain-model.template.md` — how this entity fits in the broader DDD model
- `1-decisions/ARCH-0001-module-boundary.template.md` — module that masters this entity
- `2-contracts/SM-0000-state-machine.template.md` — lifecycle state transitions
- `2-contracts/API-0000-api-spec.template.md` — APIs exposing this master data
- `3-process/PROC-0007-vendor-api-test.template.md` — for vendor enrichment APIs
- `.claude/rules/change-governance.md` — master data schema changes are "domain model" + "DB schema" → CIA gate
