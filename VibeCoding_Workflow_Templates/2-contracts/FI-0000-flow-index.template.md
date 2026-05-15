---
id: FI-0000
title: "Flow Index"
status: active
tier: 2-contracts
owner: AI-AUTO
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: doc                # this index aggregates other tier-2 docs; doc is authoritative
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
# Flow Index — `<Project Name>`

> **Tier**: 2-contracts → project-wide Flow aggregation view
>
> **Why**: once a project has 30+ Flows, no one can keep the map in their head. This index is the **map**. AI uses it to answer "what BFs exist?" without scanning every file.
>
> **Difference from `TM-0000-traceability-matrix.template.md`**: this index lists **Flow existence + status**; the traceability matrix lists **cross-layer coverage** (Flow → Spec → API → Data → Test → CI). Both needed; different purposes.
>
> **Maintenance**: append a row whenever a new Flow is created. Update status when a Flow transitions. The `sunnydata-flow-audit` skill verifies this index matches the actual files weekly.

---

## How to read

- **ID** — Flow ID per `0-principles/PRIN-0001-flow-id-conventions.md`
- **Status** — frontmatter status of the linked file (`draft / active / deprecated / superseded / archived`)
- **Owner** — accountable team or person
- **Related Modules** — which `MOD-NNNN` modules this Flow touches (forward link to `module-boundary.md`)
- **Related** — for UF: parent BF; for SF: BF/UF that consume it

A blank cell means "not yet specified" (gap to fill or accept).

---

## Business Flows (L1 — BF)

> End-to-end across roles. Each BF should map to a major business capability.

| ID | Name | Status | Owner | Related Modules | Notes |
|---|---|---|---|---|---|
| `BF-0001` | Order to Cash | active | @sales-team | sales, payment, shipment, invoice | Primary revenue path |
| `BF-0002` | Procure to Pay | active | @procurement-team | procurement, ap, gl | Vendor payment cycle |
| `BF-0003` | Record to Report | draft | @finance-team | gl, reporting | Period close |
| `BF-0004` | Return & Refund | active | @sales-team | sales, payment, inventory | Inverse of BF-0001 |

## User Flows (L2 — UF)

> Single-actor surface flows. Each UF belongs to a parent BF.

| ID | Name | Parent BF | Actor | Status | Owner |
|---|---|---|---|---|---|
| `UF-0001` | Customer create order | BF-0001 | Customer | active | @sales-team |
| `UF-0002` | Admin review flagged order | BF-0001 | Admin | active | @sales-team |
| `UF-0003` | Customer pay order | BF-0001 | Customer | active | @payment-team |
| `UF-0004` | Warehouse ship order | BF-0001 | Operator | active | @warehouse-team |
| `UF-0005` | Finance issue invoice | BF-0001 | Finance | active | @finance-team |
| `UF-0010` | Customer return order | BF-0004 | Customer | active | @sales-team |
| `UF-0011` | Buyer create PO | BF-0002 | Buyer | active | @procurement-team |
| `UF-0012` | Approver approve PO | BF-0002 | Approver | active | @procurement-team |
| `UF-0013` | Warehouse receive goods | BF-0002 | Operator | active | @warehouse-team |

## Sub Flows (L3 — SF)

> Reusable building blocks. Each SF lists its consumers.

| ID | Name | Used By | Status | Owner |
|---|---|---|---|---|
| `SF-0001` | Inventory validation | UF-0001, UF-0011 | active | @inventory-team |
| `SF-0002` | Payment callback | UF-0003 | active | @payment-team |
| `SF-0003` | Shipment dispatch | UF-0004 | active | @warehouse-team |
| `SF-0010` | Refund calculation | UF-0010 | active | @sales-team |
| `SF-0014` | Partial cancellation rule | UF-0006 (planned) | draft | @sales-team |
| `SF-0020` | Notification dispatch | BF-0001, BF-0004, BF-0002 | active | @platform-team |

## State Machines (SM)

> Per-entity state machines (extracted when ≥5 states).

| ID | Entity | Module | Status | File |
|---|---|---|---|---|
| `SM-0001` | Order | sales | active | `state-machine.order.md` |
| `SM-0002` | Payment | payment | active | `state-machine.payment.md` |
| `SM-0003` | Shipment | shipment | active | `state-machine.shipment.md` |
| `SM-0004` | PurchaseOrder | procurement | active | `state-machine.purchase-order.md` |
| `SM-0005` | Invoice | invoice | draft | `state-machine.invoice.md` |

---

## Coverage View (cross-cutting summary)

Quick health snapshot — full detail in `TM-0000-traceability-matrix.template.md`:

| BF | UFs | SFs | APIs | TCs | CI Jobs | Status |
|---|---|---|---|---|---|---|
| BF-0001 | 5 | 4 | 6 | ~30 | 5 | 🟢 covered |
| BF-0002 | 3 | 2 | 4 | ~15 | 3 | 🟡 needs E2E |
| BF-0003 | 0 | 0 | 0 | 0 | 0 | 🔴 not started |
| BF-0004 | 1 | 1 | 1 | 9 | 1 | 🟢 covered |

---

## Deprecation / Supersession Ledger

When a Flow is deprecated or superseded, log it here so the ID is **never reused**:

| ID | Status | Reason | Superseded By | Date |
|---|---|---|---|---|
| `BF-0099` | superseded | Merged into BF-0001 | — | 2026-Q1 |
| `UF-0099` | deprecated | Replaced by mobile-first UF-0050 | UF-0050 | 2026-03-15 |
| `SF-0099` | archived | Vendor integration retired | — | 2025-Q4 |

---

## Open Questions Aggregation

> Pulled from each Flow doc's §Open Questions section. Review at retro.

| Source Flow | Question | Owner | Status |
|---|---|---|---|
| BF-0001 §13 | Allow partial shipment? | @product | open |
| UF-0001 §13 | Show estimated delivery on confirmation? | @product | open |
| SF-0014 §16 | Allow partial cancel re-cancellation? | @product | open |

---

## How AI uses this index

1. **First read** in any task touching Flows — gives map without scanning every file
2. **Reference resolution** — when a CR mentions "BF-0001", look up here for status + related modules
3. **Coverage gap detection** — empty cells in Coverage View signal where work is needed
4. **Audit input** — `sunnydata-flow-audit` skill cross-references this index against actual files

---

## Maintenance procedure

After every CR that creates / modifies / deprecates a Flow:

1. Append/update the row in the relevant section
2. Bump `last-reviewed` (post-write hook updates `last-synced-with` automatically)
3. If deprecating, move to "Deprecation / Supersession Ledger"
4. If aggregating an Open Question from a flow doc, add to "Open Questions Aggregation" section
5. Run `sunnydata-flow-audit` skill to verify index matches reality

---

## See also

- `0-principles/PRIN-0001-flow-id-conventions.md` — ID semantics
- `2-contracts/BF-0000-flow-business.template.md`, `UF-0000-flow-user.template.md`, `SF-0000-flow-sub.template.md` — the underlying Flow files
- `2-contracts/SM-0000-state-machine.template.md` — state machines listed here
- `2-contracts/TM-0000-traceability-matrix.template.md` — execution-layer cross-coverage (different purpose)
- `1-decisions/ARCH-0001-module-boundary.template.md` — modules referenced in "Related Modules" column
- `.claude/skills/sunnydata-flow-audit/SKILL.md` — verifies this index against reality
- `.claude/rules/change-governance.md` — CR workflow that updates this index
