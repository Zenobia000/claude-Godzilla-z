---
id: FR-NNNN
title: "Functional Requirement — Rules + Page Contract"
status: active
tier: 2-contracts
owner: HYBRID
essence: bedrock
absorbs: [PC-0000-page-contract]
last-reviewed: null
last-synced-with: null
sync-source: doc
source-paths: []
synced-at: null
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
# FR-NNNN: <Functional Requirement Title — usually noun phrase, e.g. "Order creation rules">

> **Tier**: 2-contracts → Functional Requirement (FR)
> **Naming**: see `0-principles/PRIN-0001-flow-id-conventions.md`
>
> **Scope discipline**: this document answers **"how do we judge whether the system did it correctly?"** It does NOT answer "how does the user do it" (that's Flow) or "how does the system communicate it" (that's API).

---

## 1. Related Flow & Specs

| Type | ID | Relationship |
|---|---|---|
| Business Flow | `BF-NNNN` | Implements rules within this BF |
| User Flow | `UF-NNNN` | Triggered by this UF |
| Sub Flow | `SF-NNNN` | Validated within this SF |
| Parent FR | `FR-NNNN` | If this FR refines a broader rule |

## 2. Actor

Who must this rule apply to? (Customer / Admin / System / All)

## 3. Goal Statement

> Single sentence: what business outcome does following this rule guarantee?

Example: *"Customer can only create an order if every line item is in stock at the moment of submission."*

## 4. Pre-conditions

State that must hold before this rule applies:
- Authentication state required
- Data state (e.g. cart non-empty)
- Time/window constraints (e.g. business hours, promo period)
- Feature flag / cohort

## 5. Rules (the heart of an FR)

Numbered, atomic, testable rules. Each rule should be one sentence with **MUST / MUST NOT / SHALL / SHALL NOT** force.

1. The system **MUST** validate inventory availability for every line item before creating the order.
2. The system **MUST** calculate the total amount as `sum(item.unit_price × item.quantity) + shipping - discount`.
3. The system **MUST NOT** create the order if any line item's reserved inventory falls below the requested quantity at the moment of submission.
4. The system **MUST** persist the order with status `pending_payment` if all rules pass.
5. The system **MUST** reserve inventory atomically with order creation; partial reservation is forbidden.
6. The system **MUST** generate a unique idempotency key from `(customer_id, cart_hash)` to prevent duplicate orders within 60 seconds.

> **Rule writing hints**:
> - One rule = one verifiable assertion. If you wrote `AND` or `OR`, split it.
> - Avoid implementation detail (no "use Redis lock"). That's an ADR concern.
> - Avoid UI words (no "show error message"). That's UF concern.

## 6. Exception Rules

When the main rules can't be satisfied, what should happen?

| Case | Rule |
|---|---|
| Inventory insufficient | The system **MUST** reject the order with error code `ORDER_INVENTORY_INSUFFICIENT` and not reserve any inventory. |
| Invalid address | The system **MUST** reject the order with `ORDER_INVALID_ADDRESS` and return field-level errors. |
| Price changed since add-to-cart | The system **MUST** reject with `ORDER_PRICE_DRIFT`, and provide the current price for re-confirmation. |
| Idempotency key replay | The system **MUST** return the original order without creating a new one. |

## 7. Invariants (post-conditions)

State that must hold AFTER successful execution. These are what tests assert:

- Order state ∈ {`pending_payment`, `paid`} (never `cancelled` directly from creation)
- `inventory.reserved_qty` increased by exactly `sum(line.quantity)`
- `cart` cleared
- `OrderCreated` domain event emitted exactly once
- Order's `total_amount` equals the formula in rule §5.2

## 8. Acceptance Criteria (Gherkin-flavored)

Each criterion ties one rule (or rule combination) to an observable test. **One AC = one TC**.

| AC | Given | When | Then | Test |
|---|---|---|---|---|
| AC-1 | a customer with non-empty cart and full inventory | the customer submits the order | the order is created with status `pending_payment` and inventory is reserved | `TC-NNNN` |
| AC-2 | a customer with cart containing an out-of-stock item | the customer submits the order | the system rejects with `ORDER_INVENTORY_INSUFFICIENT` and reserves nothing | `TC-NNNN` |
| AC-3 | the same submission within 60 seconds | the customer submits twice | the second submission returns the original order | `TC-NNNN` |
| AC-4 | catalog price changed after add-to-cart | the customer submits the order | the system rejects with `ORDER_PRICE_DRIFT` and current price | `TC-NNNN` |

## 9. Related APIs

This FR is enforced at the boundary of these endpoints:

- `API-NNNN` — `POST /orders` (primary)
- `API-NNNN` — `POST /orders/preview` (rules also apply for dry-run)

## 10. Related Data Entities

Concepts this rule reads or writes:

- `Order` (writes)
- `OrderItem` (writes)
- `InventoryReservation` (writes)
- `Cart` (clears)
- `Catalog.Product` (reads price)

## 11. Related NFRs

Non-functional rules that interact with this FR:

- `NFR-NNNN` — Order create p95 < 200ms (this FR's complexity must fit budget)
- `NFR-NNNN` — Idempotency cache TTL ≥ 60s (rule §6 "duplicate prevention" depends on this)

## 12. Related Tests

| TC ID | What it asserts |
|---|---|
| `TC-NNNN` | AC-1 happy path |
| `TC-NNNN` | AC-2 inventory insufficient |
| `TC-NNNN` | AC-3 idempotent retry |
| `TC-NNNN` | AC-4 price drift |
| `TC-NNNN` | invariant §7: event emitted exactly once under retry |

## 13. Out of Scope (do NOT use this FR for)

- Order *cancellation* rules → see `FR-NNNN`
- Order *modification* rules → see `FR-NNNN`
- *Refund* calculation → see `FR-NNNN`
- UI behavior (error message wording, button states) → see `UF-NNNN`
- Performance budget enforcement → see `NFR-NNNN`

## 14. Open Questions

| Question | Owner | Status |
|---|---|---|
| Should pre-orders bypass inventory check? | Product | open |
| Idempotency window: 60s or 5min? | Architect | open |

## 15. Change History

| Date | CR | Change | Reviewer |
|---|---|---|---|
| YYYY-MM-DD | CR-NNNN | Initial | — |

---

## Where this FR fits in the bigger picture

```
BF (how it happens E2E)
  └─ UF (single-actor surface)
        └─ SF (reusable building block)
              └─ FR (this document — what's "correct")
                    ├─ enforced via API spec
                    ├─ verified via TC list
                    └─ measured against NFR
```

**Anti-pattern to refuse**: don't let an FR include flow steps ("first the customer clicks X, then ...") — that belongs in UF/SF. FR rules apply *whenever* the conditions in §4 hold, regardless of how the user got there.

---

## §page-contract (absorbs PC-0000)

> Use when this FR has a user-facing surface (web / mobile page). One §page-contract block per route this FR drives.

### Route

| Field | Value |
|---|---|
| Route ID | `PC-A12` (page IDs use `PC-` prefix even though no standalone file) |
| Path | `/orders/[order_id]` |
| Surface | web / mobile / SSR / CSR / RSC |
| Auth | required / anonymous / role-gated |
| Layout parent | `DashboardLayout` |

### Data dependencies

| Source | Endpoint | Cache strategy |
|---|---|---|
| Order | `GET /api/orders/{id}` | RSC fetch + revalidate 60s |
| Customer | `GET /api/customers/{id}` | TanStack Query, 5min stale |
| Permissions | `OPA evaluation` | Per-request (no cache) |

### Primary CTAs

| CTA | Action | Permission needed | Goes to |
|---|---|---|---|
| "Cancel order" | `POST /api/orders/{id}/cancel` | `orders.cancel` | Same page; toast |
| "Print invoice" | client-side render | `invoices.read` | `/invoices/[id].pdf` |

### State surfaces (one per case)

| State | UI |
|---|---|
| Loading | Skeleton (per `ARCH-NNNN §frontend §6.2`) |
| Empty | "No order found" CTA → `/orders` |
| Error | Error envelope per `API-NNNN §3` Problem; toast + retry button |
| Partial | Visible fields only; "loading remaining…" |
| Success | Full render |

### i18n keys this page emits

```
order_detail.title
order_detail.cancel_cta
order_detail.cancel_confirm
error.PERMISSION_DENIED
error.RESOURCE_NOT_FOUND
```

(Enforced by `CIG-0005` across locales.)

### SEO (if public)

| Field | Value |
|---|---|
| `<title>` | "Order #{order_id} — {brand}" |
| Meta description | Templated; max 160 chars |
| Open Graph | image generated server-side |
| `noindex`? | Yes if `order.state != "completed"` |

### A11y bar

Per `PRIN-NNNN §6.4`: WCAG 2.2 AA; keyboard navigable; focus trapping in cancel modal; ARIA announce on state change.

### Navigation context

- Entered from: `PC-A11 Inbox` (link click) / `PC-A10 Dashboard` (recent orders widget)
- Exits to: `PC-A11 Inbox` (after cancel) / `/invoices/[id]` (after print)
- Breadcrumb: `Home > Orders > #{order_id}`

### Forbidden patterns on this page

- Showing `customer.email` when viewer is anonymous (PII leak)
- Auto-redirect on 404 (back-button trap)
- Modal stacked > 2 deep (UX) 
