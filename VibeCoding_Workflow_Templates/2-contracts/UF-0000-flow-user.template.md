---
id: UF-NNNN
title: "User Flow Template"
status: draft
tier: 2-contracts
owner: HYBRID (AI-drafts, human-approves)
last-reviewed: <YYYY-MM-DD>
parent-business-flow: BF-NNNN
last-synced-with: <git-commit-sha>
sync-source: doc
source-paths: []
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---

# UF-NNNN: <User Flow Name — verb + noun, e.g. "Customer Create Order">

> **Tier**: 2-contracts → User Flow (L2, single-actor operating one slice of a business flow)
> **Naming**: see `0-principles/PRIN-0001-flow-id-conventions.md`

---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (Customer, Order, Inventory, PurchaseOrder, Stripe, etc.) come
> from a worked e-commerce/ERP example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.
## 1. Actor


| Field       | Value                                      |
| ----------- | ------------------------------------------ |
| Role        | Customer / Admin / Operator / …            |
| Permission  | What this role can/can't do in this flow   |
| Entry point | Page / API / channel where the flow begins |


## 2. Trigger

How does this flow start? (User action, event, schedule, etc.)

## 3. Pre-conditions

- Auth state required
- Data state required (e.g. cart non-empty)
- Feature flags / experiment cohorts

## 4. Main Flow (Happy Path)

Step-by-step from the actor's perspective. Annotate UI surface where relevant.


| #   | Actor Action                 | System Response                   | Surface               |
| --- | ---------------------------- | --------------------------------- | --------------------- |
| 1   | Click "Add to cart"          | Add item, update cart counter     | `/products/[id]`      |
| 2   | Click "Checkout"             | Navigate to checkout page         | `/cart`               |
| 3   | Fill shipping address        | Validate format                   | `/checkout`           |
| 4   | Select payment method        | Show payment widget               | `/checkout`           |
| 5   | Click "Confirm"              | Create order, redirect to payment | `POST /orders`        |
| 6   | Complete payment with vendor | Vendor sends callback (`SF-NNNN`) | external              |
| 7   | Returns to confirmation page | Display order detail              | `/orders/[id]/thanks` |


## 5. Alternative / Branch Flows

- **A1**: Guest checkout (no auth) → falls back to `UF-NNNN`
- **A2**: Coupon applied → triggers `SF-NNNN`
- **A3**: Out-of-stock during checkout → `UF-NNNN`

## 6. Exception Flow


| Exception                | UI Behavior                          | System Behavior                 |
| ------------------------ | ------------------------------------ | ------------------------------- |
| Card declined            | Inline error on payment widget       | Order kept as `pending_payment` |
| Network drop on submit   | Retry button + idempotency-key reuse | Backend dedupes via `SF-NNNN`   |
| Session expired mid-flow | Re-auth modal, restore cart          | Cart persisted in session store |


## 7. Post-conditions (per outcome)


| Outcome        | State                                                         |
| -------------- | ------------------------------------------------------------- |
| Success        | Order = `paid`; cart = empty; user redirected to confirmation |
| Payment failed | Order = `pending_payment`; cart preserved; retry CTA shown    |
| User abandoned | Cart preserved 24h; abandonment email triggered (`SF-NNNN`)   |


## 8. Related Sub Flows

- `SF-NNNN` — Auth & session refresh
- `SF-NNNN` — Coupon validation
- `SF-NNNN` — Payment vendor callback

## 9. Related Screens / Components

- `/products/[id]` — Product detail page
- `/cart` — Cart summary
- `/checkout` — Checkout form
- `/orders/[id]/thanks` — Confirmation

## 10. Related APIs

- `API-NNNN` — `POST /cart/items`
- `API-NNNN` — `POST /orders`
- `API-NNNN` — `POST /payments/init`

## 11. Acceptance Criteria (Gherkin-flavored)

- **Given** authenticated customer with non-empty cart, **when** customer completes checkout with valid payment, **then** order moves to `paid` and confirmation page displays.
- **Given** authenticated customer with non-empty cart, **when** payment is declined, **then** order stays `pending_payment` and customer sees retry option.
- **Given** authenticated customer, **when** session expires mid-checkout, **then** cart is restored after re-authentication.

## 12. Related Tests

- `TC-NNNN` — Happy path checkout
- `TC-NNNN` — Card declined
- `TC-NNNN` — Session restoration
- `TC-NNNN` — Coupon application

## 13. Open Questions


| Question                                           | Owner   | Status |
| -------------------------------------------------- | ------- | ------ |
| Should we show estimated delivery on confirmation? | Product | open   |


## 14. Change History


| Date       | CR      | Change  | Reviewer |
| ---------- | ------- | ------- | -------- |
| YYYY-MM-DD | CR-NNNN | Initial | —        |


