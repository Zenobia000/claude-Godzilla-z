---
id: BF-NNNN
title: "Business Flow Template"
status: draft        # draft | active | deprecated | superseded | archived
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
# BF-NNNN: <Business Flow Name>

> **Tier**: 2-contracts → Business Flow (L1, end-to-end across roles)
> **Naming**: see `0-principles/PRIN-0001-flow-id-conventions.md`

---

## 1. Purpose

> One paragraph. What business outcome does this flow exist to deliver, for whom?

## 2. Scope

### In scope
- Step / capability included in this BF

### Out of scope
- Adjacent capability that belongs to another BF (link to it)

## 3. Actors

| Actor | Responsibility | Internal/External |
|---|---|---|
| Customer | Initiates the flow | External |
| Sales | Reviews exceptional orders | Internal |
| Warehouse | Ships the order | Internal |
| Finance | Confirms payment & invoices | Internal |

## 4. Main Flow

Numbered, role-attributed, observable steps. **No implementation detail** — that's for FR / API / sub-flow.

1. **(Customer)** creates order
2. **(System)** validates inventory via `SF-NNNN`
3. **(System)** creates pending order, emits `OrderCreated` event
4. **(Customer)** completes payment
5. **(Payment Vendor)** sends callback handled by `SF-NNNN`
6. **(System)** confirms payment, transitions order state
7. **(Warehouse)** ships order via `UF-NNNN`
8. **(Finance)** issues invoice

## 5. Exception Flow

| Exception | Trigger | Expected Handling |
|---|---|---|
| Inventory insufficient | `SF-NNNN` returns false | Reject order, surface user message |
| Payment failed | Vendor callback `failed` | Order stays pending, payment-retry sub-flow |
| Duplicate callback | Same idempotency-key | Return success without re-applying |
| Shipment failed | Warehouse system error | Notify human operator, freeze order |

## 6. Pre/Post conditions

**Pre-conditions** (must hold before this flow can start):
- Customer authenticated
- Catalog has at least one purchasable item

**Post-conditions** (must hold after successful completion):
- Order state = `completed`
- Inventory decremented
- Invoice issued
- Customer notified

## 7. Related Sub Flows

- `SF-NNNN` — Inventory validation
- `SF-NNNN` — Payment callback handling
- `SF-NNNN` — Notification dispatch

## 8. Related User Flows

- `UF-NNNN` — Customer creates order
- `UF-NNNN` — Admin reviews flagged order
- `UF-NNNN` — Warehouse ships order

## 9. Related APIs

- `API-NNNN` — `POST /orders`
- `API-NNNN` — `POST /payments/callback`
- `API-NNNN` — `POST /shipments`

## 10. Related Functional Requirements

- `FR-NNNN` — Order creation rules
- `FR-NNNN` — Inventory reservation rules
- `FR-NNNN` — Payment confirmation rules

## 11. Related Tests

Specific test cases live in `TM-0000-traceability-matrix.template.md`. Quick links:

- `TC-NNNN` — Happy path: order to cash succeeds
- `TC-NNNN` — Inventory exhausted mid-flow
- `TC-NNNN` — Duplicate payment callback

## 12. State Machine

If this BF involves state transitions, link to the state machine document or embed inline:

```
[draft] → [pending_payment] → [paid] → [shipped] → [completed]
                            ↘ [cancelled] ← (any stage before shipped)
```

Detailed state transitions: `state-machine/<entity>.md`

## 13. Open Questions

| Question | Owner | Status | Decided in |
|---|---|---|---|
| Allow partial shipment? | Product | open | — |
| Refund timeline SLA? | Finance | open | — |

## 14. Change History

| Date | CR | Change | Reviewer |
|---|---|---|---|
| YYYY-MM-DD | CR-NNNN | Initial | — |
