---
id: MC-NNNN
title: "Module Contract — DbC + State Machine"
status: active
tier: 2-contracts
owner: HYBRID
essence: bedrock
absorbs: [SM-0000-state-machine]
last-reviewed: null
last-synced-with: null
sync-source: code
source-paths: ["src/<module>/"]
synced-at: null
product-version: null
supersedes: null
superseded-by: null
---

# MC-NNNN: Module Contract — `<ModuleName>`

> **Tier**: 2-contracts · **Essence**: bedrock — what a module promises (Design by Contract). State machine for stateful entities lives in §state-machine.
>
> **Sibling**: `MC-NNNN-<slug>.example.xstate.json` for the state machine if applicable.

---

## §1 — Module identity

| Field | Value |
|---|---|
| Module | `ShoppingCartService` |
| Owns | cart, line items, discount calc |
| Does NOT own | inventory (M-inventory), payment (M-billing) |
| Architecture link | `ARCH-NNNN §modules` row for this module |
| Linked BDD feature | `tests/features/cart.feature` |

---

## §2 — Public API (per function / method)

### `addItemToCart(cart_id, sku, qty) → Cart`

**Description**: Add a line item; merge if SKU already in cart.

**Design by Contract**:

| Type | Condition |
|---|---|
| **Pre** | `cart_id` exists; `qty > 0`; `sku` is valid format; cart is in `draft` or `active` state |
| **Post** | `Cart.line_items` contains `sku` with combined qty; `Cart.updated_at` advances; outbox event `cart.item-added.v1` emitted |
| **Invariant** | `Cart.total = sum(li.unit_price × li.qty)` always (before AND after) |
| **Forbidden** | Adding item to `cart.state ∈ {checked_out, expired}` |

**Test cases**:

| TC ID | Scenario | Arrange | Act | Assert |
|---|---|---|---|---|
| TC-001 | Happy path | New cart | `add(sku-A, 2)` | cart.items has (sku-A, 2); total updated |
| TC-002 | Merge existing SKU | Cart with (sku-A, 1) | `add(sku-A, 2)` | cart.items has (sku-A, 3) |
| TC-003 | Invalid qty | Cart | `add(sku-A, 0)` | throws `PreconditionError` |
| TC-004 | Wrong state | Cart in `checked_out` | `add(sku-A, 1)` | throws `InvariantError` |
| TC-005 | Concurrency | Two callers, same cart | parallel `add()` | both succeed; final qty = sum |

---

## §3 — State Machine (§state-machine, absorbs SM-0000)

> Use when the module manages an aggregate with ≥ 5 states or ≥ 10 transitions. For simpler entities, inline the state field in §2 invariants.

### §3.1 States

| State | Meaning | Final? |
|---|---|---|
| `draft` | Initial; mutable | No |
| `pending_approval` | Submitted; awaiting decision | No |
| `scheduled` | Approved; waiting to start | No |
| `in_progress` | Currently being executed | No |
| `paused` | Temporarily halted; resumable | No |
| `completed` | Successfully finished | **Yes** |
| `cancelled_with_fee` | Cancelled after approval; fee applied | **Yes** |
| `rejected` | Approval denied | **Yes** |
| `discarded` | Draft deleted before submit | **Yes** |
| `failed` | Terminal failure during execution | **Yes** |

### §3.2 Transition table

| From | Event | To | Guard | Side effects | Emits |
|---|---|---|---|---|---|
| `draft` | SUBMIT | `pending_approval` | `isComplete()` | — | `WorkOrderSubmitted.v1` |
| `draft` | DISCARD | `discarded` | — | soft-delete | — |
| `pending_approval` | APPROVE | `scheduled` | approver has permission | reserve resources | `WorkOrderApproved.v1` |
| `pending_approval` | REJECT | `rejected` | — | release reservations | `WorkOrderRejected.v1` |
| `scheduled` | DISPATCH | `in_progress` | dispatcher on duty | start clock | `WorkOrderStarted.v1` |
| `scheduled` | CANCEL | `cancelled_with_fee` | — | compute fee per FR-NNNN | `WorkOrderCancelled.v1` |
| `in_progress` | COMPLETE | `completed` | all checklist done | finalize | `WorkOrderCompleted.v1` |
| `in_progress` | PAUSE | `paused` | — | — | — |
| `in_progress` | FAIL | `failed` | — | record reason | `WorkOrderFailed.v1` |
| `paused` | RESUME | `in_progress` | — | — | — |
| `paused` | ABANDON | `failed` | — | — | `WorkOrderFailed.v1` |

### §3.3 Forbidden transitions (negative space)

- `draft → in_progress` (must pass through pending_approval + scheduled)
- `completed → *` (final)
- `rejected → scheduled` (restart requires DISCARD + new draft)
- Any final state → any state

### §3.4 Machine-readable form

The canonical xstate JSON is in the sibling file `MC-NNNN-<slug>.example.xstate.json`. The markdown table above is human-readable; the JSON is consumed by:

- Runtime: `import { createMachine } from 'xstate'`
- Visualization: Stately Studio (https://stately.ai/)
- CI: `sunnydata-auto-regen` cross-checks state count + transition count between markdown and JSON

If markdown § and JSON disagree → JSON is source of truth (it runs); fix markdown.

### §3.5 Acceptable substitutes

| Tool | When to pick |
|---|---|
| xstate JSON | TypeScript / JavaScript projects (recommended) |
| Stately Studio export | Same JSON; richer editor |
| GraphViz `.dot` | Visualization-only; no runtime |
| SCXML (W3C) | Industrial / regulated |

---

## §4 — Cross-cutting invariants

Hold across every method + state:
- `total = sum(line_items.amount × qty)` always
- Once `posted_to_gl_at` set, no field except audit columns may mutate
- Every state change writes audit row to `<entity>_audit_trail`
- Cancellation releases reservations idempotently

---

## §5 — Linkage

| To | How |
|---|---|
| API | `API-NNNN` (which endpoints expose §2 methods) |
| FR | `FR-NNNN` (which business rules §2 implements) |
| Flow | `BF/UF/SF-NNNN` (which flows trigger §3 transitions) |
| Data | `DATA-NNNN §master-data` (entity ownership) |
| Test | `TC-NNNN` in `tests/features/<module>.feature` |

---

## §6 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| DbC §2 with no invariants | Just method docs | Every method has ≥ 1 invariant |
| State machine in code, not docs | New engineer can't read the rules | This template + xstate JSON |
| State diagram only, no forbidden transitions | Negative space invisible | §3.3 mandatory |
| Markdown SM drifts from xstate JSON | Two sources of truth | CI cross-check; JSON wins |
| Test case "happy path" only | Edge cases break in prod | §2 must include at least one boundary + one violation |
| Side effects in §3 transitions not declared | Hidden writes | Every transition row declares side effects + emitted events |

---

## See also

- `PRIN-0003-engineering-contract-stack.md` §L2 (data layer) §L2.2 (state machine)
- `API-0000-api-spec.template.md` — wire surface exposing §2 methods
- `FR-0000-functional-requirement.template.md` — rules implemented in §2 invariants
- `DATA-0000-data-contract.template.md` §master-data — entity ownership
- `TEST-0000-testing-strategy.template.md` §contract — TC-NNNN methodology
- `MC-NNNN-<slug>.example.xstate.json` — machine-readable sibling
