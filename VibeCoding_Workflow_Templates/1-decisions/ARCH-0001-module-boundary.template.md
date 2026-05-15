---
id: ARCH-0001
title: "Module Boundary"
status: draft
tier: 1-decisions
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
date: <YYYY-MM-DD>
decider: <person-or-team>
bounded-context: <DDD bounded context name>
product-version: null
supersedes: null
superseded-by: null
---

# MOD-NNNN: `<Module Name>` — Module Boundary

> **Tier**: 1-decisions — architectural module charter
>
> **Why a dedicated doc per module**: in ERP-class systems, the most expensive long-term failure is a module that quietly took on a neighbor's responsibility (Sales doing inventory math, Inventory doing pricing). This document is the **charter**: what this module owns, what it explicitly refuses, and how it touches its neighbors.
>
> **Promotion criterion**: a module deserves this doc when it has ≥ 1 distinct entity, ≥ 1 public API, and ≥ 1 dedicated owning team. Sub-modules can be enumerated in §3 without separate docs.

---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (Customer, Order, Inventory, PurchaseOrder, Stripe, etc.) come
> from a worked e-commerce/ERP example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.
## 1. Identity


| Field            | Value                               |
| ---------------- | ----------------------------------- |
| Module name      | `Inventory`                         |
| Bounded context  | Inventory Management                |
| Owning team      | `@inventory-team`                   |
| Repo / package   | `src/inventory/`                    |
| External-facing? | No (internal) / Yes (vendor-facing) |
| Multi-tenant?    | per-org isolated                    |


## 2. Mission Statement

> One sentence: what business outcome does this module own?

Example: *"Inventory module owns the source of truth for physical-and-virtual stock quantities and reservations, across all locations, for all SKUs."*

## 3. What This Module OWNS

### Entities (write authority)


| Entity               | Identifier                           | Aggregate root?     |
| -------------------- | ------------------------------------ | ------------------- |
| Item (SKU)           | `item_id`                            | Yes                 |
| InventoryLocation    | `location_id`                        | Yes                 |
| StockLevel           | composite (`item_id`, `location_id`) | No (within Item)    |
| InventoryReservation | `reservation_id`                     | Yes                 |
| StockMovement        | `movement_id`                        | Yes (event-sourced) |


### Capabilities (operations exposed)


| Capability          | Public API                                     | Notes                        |
| ------------------- | ---------------------------------------------- | ---------------------------- |
| Reserve inventory   | `API-NNNN POST /inventory/reservations`        | idempotent                   |
| Release reservation | `API-NNNN DELETE /inventory/reservations/{id}` | idempotent                   |
| Move stock          | `API-NNNN POST /inventory/movements`           | event-sourced, audit-trailed |
| Query stock level   | `API-NNNN GET /inventory/levels?…`             | eventual-consistent OK       |


### Events (we publish)


| Event                   | Payload                             | Triggered by           |
| ----------------------- | ----------------------------------- | ---------------------- |
| `InventoryReserved`     | reservation_id, item_id, quantity   | Successful reservation |
| `InventoryReleased`     | reservation_id, reason              | Cancellation / expiry  |
| `StockLevelChanged`     | item_id, location_id, delta         | Any movement           |
| `StockReorderTriggered` | item_id, location_id, suggested_qty | Below safety stock     |


## 4. What This Module Does NOT OWN

> **This is the most load-bearing section.** Adjacent modules are listed by what's commonly confused.


| NOT owned                                                 | Owner module                      | Why this matters                                                          |
| --------------------------------------------------------- | --------------------------------- | ------------------------------------------------------------------------- |
| Item **price**                                            | Catalog / Pricing                 | Inventory holds quantity, not money. A $0 item is still inventory.        |
| Item **description / images**                             | Catalog                           | Inventory holds physical existence, not marketing.                        |
| Customer-facing **availability messaging** ("In stock")   | Sales / Storefront                | We provide raw quantity; UI decides messaging.                            |
| **Ordering** decisions / replenishment quantity           | Procurement (Reorder Engine)      | We trigger the signal; Procurement decides quantity & vendor.             |
| **Cost** of inventory (financial valuation)               | Cost Accounting (GL)              | We hold quantity; Cost Accounting computes $$ via methods (FIFO/Avg/Std). |
| **Forecasting** future demand                             | Demand Planning                   | We hold history; Planning runs models.                                    |
| **Physical movement** logistics (truck, warehouse layout) | Warehouse Management System (WMS) | We record the move happened; WMS optimizes how.                           |


If you find yourself adding any of the above to this module, **stop and write an ADR justifying the boundary change** — this is exactly the pattern that turns ERP modules into god-modules over 5 years.

## 5. Dependencies

### Upstream (we consume from)


| Dependency   | What we use it for                                 | Coupling                       |
| ------------ | -------------------------------------------------- | ------------------------------ |
| Catalog      | Item master metadata (existence, units of measure) | Read-only API + cached locally |
| Organization | Location hierarchy, multi-org rules                | Read-only API                  |
| Auth         | Role/permission for inventory operations           | Token validation               |


### Downstream (we publish to / they consume us)


| Consumer             | What they use                                    | Coupling style             |
| -------------------- | ------------------------------------------------ | -------------------------- |
| Sales (Order module) | Reservation API + InventoryReserved event        | API call + event subscribe |
| Procurement          | StockLevelChanged + StockReorderTriggered events | Event subscribe            |
| Warehouse (WMS)      | StockMovement event                              | Event subscribe            |
| Cost Accounting (GL) | StockMovement event for cost ledger              | Event subscribe            |
| Reporting            | StockLevel snapshot via API                      | Polling API                |


## 6. Anti-Corruption Layers (ACL)

When integrating with modules whose model differs significantly:


| Neighbor                | ACL purpose                                         | Where it lives                     |
| ----------------------- | --------------------------------------------------- | ---------------------------------- |
| Legacy WMS              | Map our `movement_type` enum to their numeric codes | `src/inventory/acl/wms_adapter.py` |
| Catalog v1 (deprecated) | Map old `sku` (string) to new `item_id` (UUID)      | `src/inventory/acl/catalog_v1.py`  |
| External 3PL vendor     | Translate vendor's stock format to our model        | `src/inventory/acl/vendor_3pl.py`  |


## 7. Public Contract Surface

Aggregate listing — for full specs see referenced docs:

- APIs (tier 2): `2-contracts/api-spec/inventory-*.yaml`
- Domain Model (tier 1): `1-decisions/domain-model.<inventory>.md`
- State Machines (tier 2): `2-contracts/state-machine.<entity>.md` for each aggregate root
- Master Data Specs (tier 2): `2-contracts/master-data.<item>.md`, `…location.md`, `…reservation.md`

## 8. Internal Surface (NOT public)

These exist but are **NOT** part of the module's contract. Consumers MUST NOT rely on them:

- Internal queue topic naming
- Database table names / schemas
- Cache layout
- Feature flag names

If a consumer depends on internals, that's a bug — open a ticket to expose a proper API or event.

## 9. Quality Attributes


| Attribute                         | Target                          | Linked NFR |
| --------------------------------- | ------------------------------- | ---------- |
| Reservation latency p95           | < 50ms                          | NFR-NNNN   |
| Stock-level query consistency     | Eventually consistent within 1s | NFR-NNNN   |
| Movement audit trail retention    | 7 years                         | NFR-NNNN   |
| Concurrent reservation throughput | ≥ 200 rps                       | NFR-NNNN   |


## 10. Governance


| Concern                                | Policy                                                           |
| -------------------------------------- | ---------------------------------------------------------------- |
| Adding a new public endpoint           | Requires module owner review + traceability matrix update        |
| Changing an existing endpoint contract | Requires CIA + 3-month deprecation if breaking                   |
| Adding a new event                     | Requires consumer impact analysis (broadcast to subscriber list) |
| Schema migration on owned entities     | Requires zero-downtime migration plan                            |


## 11. Open Boundary Questions


| Question                                                           | Owner     | Status                                       |
| ------------------------------------------------------------------ | --------- | -------------------------------------------- |
| Should we own "in-transit" stock or does that belong to Logistics? | Architect | open                                         |
| Reservation TTL: per-item or per-Order?                            | Product   | decided 2026-04-01 (per-Order); see ADR-NNNN |


## 12. Change History


| Date       | CR / ADR | Change          | Reviewer |
| ---------- | -------- | --------------- | -------- |
| YYYY-MM-DD | ADR-NNNN | Initial charter | —        |


---

## See also

- `1-decisions/ARCH-0000-architecture-overview.template.md` — system-wide context
- `1-decisions/DDD-0000-domain-model.template.md` — entities listed in §3 mapped here
- `1-decisions/ADR-0000-adr.template.md` — every boundary change should produce an ADR
- `2-contracts/SM-0000-state-machine.template.md` — per-entity state machines
- `2-contracts/MDS-0000-master-data.template.md` — for master entities owned here
- `.claude/rules/change-governance.md` — boundary changes are "architecture boundary" → CIA gate

