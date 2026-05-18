---
id: FLOW-0000
title: "Flow — Business / User / Sub-flow Template"
status: active
tier: 2-contracts
owner: HYBRID
essence: bedrock
absorbs: [BF-0000, UF-0000, SF-0000]
last-synced-with: null
sync-source: doc
source-paths: []
synced-at: null
---

# FLOW-0000: Flow Template (BF / UF / SF)

> **Tier**: 2-contracts · **Essence**: bedrock — every non-trivial system has flows.
>
> **One template, three scopes**: Business Flow (E2E across roles) → User Flow (single actor surface) → Sub-Flow (reusable building block). The shape is the same; the scope shrinks as you go deeper.

---

## Picking the scope

Choose the scope by answering: **"who is on stage in this flow?"**

| Scope | On stage | Answers | Example |
|---|---|---|---|
| **BF — Business Flow** | Multi-role E2E across modules | "How does the business deliver value end-to-end?" | `BF-0001` Order to Cash |
| **UF — User Flow** | Single actor / single surface | "How does *this actor* do *this task*?" | `UF-0007` Customer cancels order |
| **SF — Sub-Flow** | Reusable across BFs/UFs | "How does this shared step work?" | `SF-0014` Partial cancellation rule |

**Naming**: `BF-NNNN-<slug>.md`, `UF-NNNN-<slug>.md`, `SF-NNNN-<slug>.md` (same prefix system, separate sequence per type per `PRIN-0001`).

Delete the sections below that don't apply to your scope.

---

## §1 — Identity (all scopes)

| Field | Value |
|---|---|
| ID | `BF-NNNN` / `UF-NNNN` / `SF-NNNN` |
| Title | Human-readable (3-7 words) |
| Scope | business / user / sub |
| Status | `draft` / `active` / `deprecated` / `superseded` |
| Owner | Team + on-call escalation |
| Linked FRs | `FR-NNNN, FR-NNNN+1` (what rules this flow enforces) |
| Linked APIs | `API-NNNN` (endpoints this flow touches) |
| Linked SMs | (only if MC has state machine) `MC-NNNN §state-machine` |

---

## §2 — Business Flow (only if scope = BF)

### §2.1 Actors

| Actor | Role | What they want |
|---|---|---|
| Customer | external | place an order, get product |
| Operator | internal | fulfill efficiently |
| Finance | internal | recognize revenue |
| External: Stripe | vendor | process payment |

### §2.2 Trigger

Event that starts the flow: customer clicks "Pay" / cron at 02:00 UTC / webhook arrives.

### §2.3 End-to-end happy path

```
1. Customer submits cart (UF-0001 reference)
2. System reserves inventory (SF-0014 reference)
3. Payment authorized (external: Stripe)
4. Order created (DB write; outbox event emitted)
5. Fulfillment picks up event (cross-module → BF-0003 Fulfillment)
6. Shipment dispatched
7. Customer notified
8. Revenue recognized (next billing close)
```

### §2.4 Exception flows

| Exception | Detected at | Handled by |
|---|---|---|
| Payment declined | Step 3 | UF-0002 retry; fall to manual review after 2 attempts |
| Inventory unavailable | Step 2 | Reject with `OUT_OF_STOCK`; offer backorder UF |
| Fulfillment delay | Step 5 | SLO breach → alert (`SRE-NNNN`) |

### §2.5 Cross-context boundaries

If the BF crosses bounded contexts (e.g. Ordering ↔ Fulfillment ↔ Billing), each boundary is a **contract surface** — `API-NNNN` for sync, `ASYNC` channel (see `API-NNNN §async`) for async, with explicit ownership.

---

## §3 — User Flow (only if scope = UF)

### §3.1 Actor & surface

- Actor: `<role>` (matches a persona in `PRD-NNNN §personas`)
- Surface: web `/orders/new` / mobile / CLI / API / chat
- Entry point: how the user arrives here (link, deep-link, push notification, voice trigger)

### §3.2 Happy-path step list

```
1. User lands on /orders/new (PC reference if web)
2. User fills form (validates against FR-NNNN business rules)
3. User submits → POST /orders (API-NNNN)
4. System returns 200 + redirect to /orders/{id}
5. User sees confirmation
```

### §3.3 Decisions a user makes

| Decision | Options | Default | Affects |
|---|---|---|---|
| Pickup vs delivery | Pickup / Delivery | Delivery | shipping fee, ETA |
| Payment method | Card / wallet / invoice (enterprise only) | last-used | flow branches to SF-NNNN |

### §3.4 Exception UFs (per actor)

| Exception | UI surface | Recovery |
|---|---|---|
| Validation fail | Inline field errors | Stay on form; preserve input |
| Network timeout | Toast | Auto-retry once; offer "save draft" |
| Session expired | Modal → /login | Resume after re-auth |

### §3.5 Acceptance criteria (link to FR or inline)

Each AC is a testable statement. Prefer `FR-NNNN` reference (single source of truth). Inline only if AC is purely UI behavior with no business rule.

---

## §4 — Sub-Flow (only if scope = SF)

### §4.1 Reuse evidence

A sub-flow exists because **≥ 2 parent flows** share it. List them:

- Used by `BF-0001 §step 2`
- Used by `UF-0007 §step 3`
- Used by `BF-0003 §step 1`

If only one parent uses it, it's a §step in that parent, not an SF.

### §4.2 Inputs / Outputs

| Input | Type | Source |
|---|---|---|
| `order_id` | uuid | parent flow |
| `tenant_id` | string | request context |

| Output | Type | Semantics |
|---|---|---|
| `reservation_id` | uuid | created reservation row |
| `expires_at` | datetime | 15min TTL |

### §4.3 Idempotency

Required for sub-flows. Use `Idempotency-Key` (see `API-NNNN §idempotency`); same input + same key → same output without side effect duplication.

### §4.4 Side effects

| Side effect | Scope | Reversible? |
|---|---|---|
| DB write to `inventory_reservations` | Local | Yes (within TTL) |
| Outbox event `inventory.reserved` | Async | No (idempotent consumer required) |

### §4.5 Failure modes

| Failure | Behavior |
|---|---|
| Insufficient stock | Return `INSUFFICIENT_STOCK`; no partial reservation |
| DB timeout | Retry-able (deterministic) |
| Outbox emit fail | Local row committed; outbox table picks up retry |

---

## §5 — Linkage table (all scopes)

| Layer | This flow links to |
|---|---|
| FR (rules) | `FR-NNNN, FR-NNNN+1` |
| API (wire) | `API-NNNN` |
| MC (modules) | `MC-NNNN` (which module owns this) |
| SM (state) | `MC-NNNN §state-machine` (if stateful entity involved) |
| TC (tests) | `TC-NNNN .. TC-NNNN+X` |
| CR (changes) | `CR-NNNN` (if introduced via change request) |

---

## §6 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| BF that includes UI button colors | Scope creep into UF | Move to UF or PC |
| UF that names DB columns | Scope creep into MC | Move to MC |
| SF without ≥ 2 parents | Not actually reusable | Inline back into parent |
| Flow with no exception branch | Hides real failure modes | Document at least 3 exceptions |
| Flow as a wall of prose | Unreadable | Numbered steps + tables |
| Flow that contradicts the SM | Drift between flow and entity state | Cross-reference `MC §state-machine`; reconcile |

---

## See also

- `PRIN-0001-flow-id-conventions.md` — naming
- `PRIN-0003-engineering-contract-stack.md` §3 — where flows sit in the 10-layer map
- `FR-0000-functional-requirement.template.md` — rules this flow enforces
- `API-0000-api-spec.template.md` — wire surface (§async for events)
- `MC-0000-module-contract.template.md` §state-machine — state transitions
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — flow change governance
