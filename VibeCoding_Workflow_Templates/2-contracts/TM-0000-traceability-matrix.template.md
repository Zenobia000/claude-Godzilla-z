---
id: TM-0000
title: "Traceability Matrix"
status: active
tier: 2-contracts
owner: AI-AUTO
last-reviewed: <YYYY-MM-DD>
last-synced-with: <git-commit-sha>
sync-source: doc                # this matrix IS authoritative for cross-cutting links
source-paths: []
synced-at: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---

# Traceability Matrix

> **Tier**: 2-contracts → cross-layer coverage map
> **Purpose**: single source of truth for "what's connected to what" — Flow → Spec → API → Data → Test → CI Job
> **Updated by**: implementer at end of every CR (after `sunnydata-change-impact-analysis`)
> **Verified by**: `sunnydata-doc-freshness` skill on weekly maintenance

---


> **⚠️ WORKED EXAMPLE — DELETE BEFORE USE**
> Concrete names below (Customer, Order, Inventory, PurchaseOrder, Stripe, etc.) come
> from a worked e-commerce/ERP example to give AI strong few-shot context. **Replace
> them with your domain's terms** when filling for your project. The structure (sections,
> tables, frontmatter) is what to keep; the example content is what to swap or delete.
> If your domain doesn't fit (CLI / library / ML / embedded), the example is still
> useful as a structural reference — copy the shape, change the words.
## How to read this table

Each row is a slice of system behavior wide enough to verify end-to-end. Reading left-to-right answers "if BF-X breaks, what to check; if TC-Y fails, what regressed."

- A blank cell means "no instance yet" (gap to plan or accept)
- `—` means "deliberately not applicable" (e.g. UF that has no API surface)
- ID columns use the prefixes from `0-principles/PRIN-0001-flow-id-conventions.md`

## Coverage Matrix


| BF                        | UF                                   | SF                             | FR                                   | API                                                               | Data Entity                    | TC              | CI Job              |
| ------------------------- | ------------------------------------ | ------------------------------ | ------------------------------------ | ----------------------------------------------------------------- | ------------------------------ | --------------- | ------------------- |
| `BF-0001` Order to Cash   | `UF-0001` Customer create order      | `SF-0001` Inventory validation | `FR-0001` Order creation rules       | `API-0001` `POST /orders`                                         | `orders`, `order_items`        | `TC-0001..0008` | `test-order-create` |
| `BF-0001`                 | `UF-0002` Admin review flagged order | `SF-0001` Inventory validation | `FR-0002` Risk-flag rules            | `API-0002` `POST /orders/{id}/review`                             | `orders`, `risk_flags`         | `TC-0009..0012` | `test-order-review` |
| `BF-0001`                 | `UF-0003` Customer pay order         | `SF-0002` Payment callback     | `FR-0003` Payment confirmation rules | `API-0003` `POST /payments`, `API-0004` `POST /payments/callback` | `payments`, `idempotency_keys` | `TC-0020..0028` | `test-payment`      |
| `BF-0001`                 | `UF-0004` Warehouse ship order       | `SF-0003` Shipment dispatch    | `FR-0004` Shipment trigger rules     | `API-0005` `POST /shipments`                                      | `shipments`                    | `TC-0030..0035` | `test-shipment`     |
| `BF-0001`                 | `UF-0005` Finance issue invoice      | —                              | `FR-0005` Invoice issuance rules     | `API-0006` `POST /invoices`                                       | `invoices`                     | `TC-0040..0042` | `test-invoice`      |
| `BF-0002` Return & Refund | `UF-0010` Customer return order      | `SF-0010` Refund calculation   | `FR-0020` Refund rules               | `API-0010` `POST /returns`                                        | `returns`, `refunds`           | `TC-0100..0108` | `test-return`       |


## NFR Coverage

Non-functional requirements get their own row tracking:


| NFR        | Description                                | Verified by                 | Last measured         |
| ---------- | ------------------------------------------ | --------------------------- | --------------------- |
| `NFR-0001` | Order create p95 < 200ms                   | `perf-order-create` job     | YYYY-MM-DD: 142ms ✅   |
| `NFR-0002` | Payment callback handler accepts ≥ 100 rps | `load-payment-callback` job | YYYY-MM-DD: 134 rps ✅ |
| `NFR-0003` | Cross-region failover RTO < 5min           | `dr-drill` quarterly        | YYYY-MM-QQ: 4m12s ✅   |
| `NFR-0004` | Audit log retention ≥ 7 years              | manual quarterly review     | YYYY-MM-QQ ✅          |


## Domain Event Coverage

Events that cross module boundaries — each must have at least one consumer test:


| Event              | Producer  | Consumers                    | Producer Test | Consumer Test(s)                |
| ------------------ | --------- | ---------------------------- | ------------- | ------------------------------- |
| `OrderCreated`     | `BF-0001` | Notification, Analytics      | `TC-0001`     | `TC-0050`, `TC-0070`            |
| `PaymentConfirmed` | `SF-0002` | Order, Notification, Finance | `TC-0020`     | `TC-0027`, `TC-0051`, `TC-0080` |
| `ShipmentCreated`  | `SF-0003` | Notification, ERP            | `TC-0030`     | `TC-0052`, `TC-0090`            |


## External Dependency Coverage

APIs / services we don't own — each must have a contract test + a fallback plan:


| Dependency       | Used in               | Contract Test                               | Fallback                                    | Vendor SLA |
| ---------------- | --------------------- | ------------------------------------------- | ------------------------------------------- | ---------- |
| Stripe (payment) | `SF-0002`             | `contract/stripe-callback.yaml` → `TC-0021` | Retry with exp backoff; manual review queue | 99.95%     |
| ERP cancel API   | `BF-0002`             | `contract/erp-cancel.yaml` → `TC-0102`      | Compensating-tx adapter (`SF-0011`)         | 99.5%      |
| SendGrid (email) | Notification consumer | `contract/sendgrid-send.yaml` → `TC-0053`   | Queue + retry; degrade silently             | 99.9%      |


## Gaps & Coverage Debt

Track known holes here — review at every retro:


| Gap                                                                      | Severity | Owner     | Target date |
| ------------------------------------------------------------------------ | -------- | --------- | ----------- |
| `UF-0006` (Customer cancel) has no chaos-test for concurrent ship+cancel | Medium   | QA        | 2026-Q3     |
| `NFR-0005` (encryption-at-rest verified) — no automated check yet        | High     | Security  | 2026-Q2     |
| `BF-0002` Domain Event consumers in Analytics not tested                 | Low      | Analytics | backlog     |


## Update Procedure

After every CR:

1. Open the resulting `CR-NNNN` document
2. For each "New" item in §2-§7, append a row here
3. For each "Modified" item, update the existing row
4. For each "Deleted" item, mark the row `~~strikethrough~~` and move to "Deleted IDs" appendix
5. Bump `last-reviewed` and let the post-write hook refresh `last-synced-with`

## Deleted IDs (do not reuse)


| ID         | Deleted in | Reason                                                         |
| ---------- | ---------- | -------------------------------------------------------------- |
| `BF-0003`  | CR-0007    | Merged into BF-0001 (was duplicated work)                      |
| `API-0007` | CR-0012    | Replaced by `API-0034`; kept here so the number isn't recycled |


---

## See also

- `0-principles/PRIN-0001-flow-id-conventions.md` — ID semantics and allocation
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — what to update in this matrix per CR
- `3-process/QG-0000-quality-gates.md` — when this matrix must be filled out
- `.claude/skills/sunnydata-doc-freshness/SKILL.md` — freshness verification

