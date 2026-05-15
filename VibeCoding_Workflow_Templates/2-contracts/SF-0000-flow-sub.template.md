---
id: SF-NNNN
title: "Sub Flow Template"
status: draft
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: doc
source-paths: []
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
# SF-NNNN: <Sub-Flow Name — usually verb phrase>

> **Tier**: 2-contracts → Sub Flow (L3, reusable building block consumed by multiple BF/UF)
> **Naming**: see `0-principles/PRIN-0001-flow-id-conventions.md`
>
> **Reuse signal**: if this sub-flow is only used by one BF/UF, it probably belongs inside that flow rather than as a standalone SF. Promote to SF only when 2+ consumers exist or are imminent.

---

## 1. Used By

| Consumer ID | Consumer Type | How invoked |
|---|---|---|
| `BF-NNNN` | Business Flow | Step 5 of main flow |
| `UF-NNNN` | User Flow | Branch A2 |
| `UF-NNNN` | User Flow | Exception handling |

## 2. Trigger

What event/call invokes this sub-flow? (e.g. "called by parent flow with `<input>` payload"; "subscribed to `<event>` on event bus")

## 3. Inputs

| Field | Type | Required | Notes |
|---|---|---|---|
| order_id | string (UUID) | yes | Must exist in DB |
| amount | number | yes | Must equal order total |
| idempotency_key | string | yes | For duplicate-detection |

## 4. Outputs

| Field | Type | Notes |
|---|---|---|
| status | enum (success / failed / duplicate) | |
| reason | string (nullable) | Present when status=failed |

## 5. Pre-conditions

- Caller has authenticated to system
- Required entities exist (referenced by ID)

## 6. Main Flow

1. Validate inputs against schema (FR-NNNN)
2. Check idempotency: lookup `idempotency_key` in store
3. If duplicate → return cached result, do NOT re-apply
4. Execute the action (e.g. update payment status, dispatch notification)
5. Cache result against `idempotency_key`
6. Emit domain event (e.g. `PaymentConfirmed`)
7. Return success

## 7. Exception Flow

| Case | Detection | Expected Behavior |
|---|---|---|
| Invalid signature | Vendor signature verify fails | Reject, log, alert |
| Schema mismatch | Pydantic validation fails | Reject with 400, surface field errors |
| Duplicate `idempotency_key` | Store hit | Return cached result, log dedupe event |
| Amount mismatch | input.amount != order.total | Mark as `payment_exception`, freeze for human review |
| Downstream failure | Side-effect (DB / event bus) errors | Retry policy `<N>` attempts; on exhaustion, dead-letter |

## 8. Idempotency

- **Key source**: `<field-name>` from input
- **Storage**: `<store-name>` with TTL `<duration>`
- **Behavior on hit**: return cached result without re-applying side-effects

## 9. Side Effects

| Effect | Reversible? | Triggered When |
|---|---|---|
| Update DB row | yes (compensating tx) | After signature & idempotency pass |
| Emit domain event | no (event log) | After DB commit |
| Send notification | no (external) | After event consumed by notification service |

## 10. Domain Events Emitted

- `<EventName>` — payload schema, consumers (cross-reference relevant docs)

## 11. Related FRs

- `FR-NNNN` — Idempotency rule
- `FR-NNNN` — Signature verification rule

## 12. Related APIs

- `API-NNNN` — Endpoint that invokes this SF (if any)

## 13. Related Tests

- `TC-NNNN` — Happy path
- `TC-NNNN` — Duplicate request returns cached result
- `TC-NNNN` — Invalid signature rejected
- `TC-NNNN` — Amount mismatch freezes record

## 14. Open Questions

| Question | Owner | Status |
|---|---|---|
| TTL of idempotency cache? | Architect | open |

## 15. Change History

| Date | CR | Change | Reviewer |
|---|---|---|---|
| YYYY-MM-DD | CR-NNNN | Initial | — |
