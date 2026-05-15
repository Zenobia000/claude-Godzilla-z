---
id: GLOS-0000
title: "Glossary"
status: draft
tier: 0-principles
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
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
# Glossary — `<Project / Domain>`

> **Tier**: 0-principles — terminology source of truth
>
> **Why**: in ERP-class systems, "Customer" / "Buyer" / "Account" / "Member" are **NOT** synonyms — and treating them as such causes data-model errors, contract bugs, and audit findings. Every term that has a specific business meaning belongs here.
>
> **Reading order for AI**: load this **before** any code/contract work in a domain you haven't seen this session.

---

## How to use

- **Add a term when**: two stakeholders use it differently, OR it appears in any FR / BF / API / Data entity, OR it's a regulatory/legal term.
- **Don't add**: generic English words (unless they have domain meaning), brand names of vendors, technology jargon (those go in tech glossary).
- **One term, one definition**. If a term means two things in two domains, add two entries with `domain` qualifier.

---

## Term Index by Domain

| Domain | Term Count | Last Updated |
|---|---|---|
| Accounting | 0 | YYYY-MM-DD |
| Inventory | 0 | YYYY-MM-DD |
| Sales | 0 | YYYY-MM-DD |
| Procurement | 0 | YYYY-MM-DD |
| Manufacturing | 0 | YYYY-MM-DD |
| HR | 0 | YYYY-MM-DD |
| Cross-cutting | 0 | YYYY-MM-DD |

---

## Entries

### Customer

| Field | Value |
|---|---|
| **Domain** | Sales |
| **Definition** | A legal entity (individual or organization) that has been onboarded and KYC-approved and is eligible to place orders. |
| **NOT** | Not a Lead (pre-onboarding); not a Prospect (in pipeline); not a Buyer (one-time anonymous purchase via guest checkout). |
| **Identifier** | `customer_id` (UUID); natural key: tax_id + country |
| **Owned by** | Sales / Customer Master Data |
| **Authoritative system** | CRM (write); ERP-AR (read replica) |
| **Lifecycle states** | prospect → onboarding → active → suspended → archived |
| **Examples** | "ACME Corp Ltd. (cust_id: 7f3...)" |
| **Related** | Buyer, Account, Lead, Prospect, Tax Entity |
| **First defined** | YYYY-MM-DD |
| **Status** | active |

### Buyer

| Field | Value |
|---|---|
| **Domain** | Sales |
| **Definition** | The natural person who completes a purchase transaction, regardless of whether they are an onboarded Customer. |
| **NOT** | Not necessarily a Customer; a single Customer can have many Buyers (e.g. corporate accounts). |
| **Identifier** | `buyer_id`; for guest purchases this is session-bound and ephemeral. |
| **Owned by** | Sales |
| **Examples** | "John Doe purchasing on behalf of ACME Corp"; "anonymous guest checkout" |
| **Related** | Customer, Order, Cart |
| **Status** | active |

### Account (Sales context)

| Field | Value |
|---|---|
| **Domain** | Sales |
| **Definition** | A commercial relationship aggregating one or more Customers under a single negotiated price tier or credit line. |
| **NOT** | NOT the same as **Account (Accounting context)** below; NOT the same as a User Account (auth). |
| **Identifier** | `sales_account_id` |
| **Status** | active |

### Account (Accounting context)

| Field | Value |
|---|---|
| **Domain** | Accounting |
| **Definition** | A line in the Chart of Accounts (COA) used to classify financial transactions. |
| **NOT** | NOT a Sales Account; NOT a User Account; NOT a Customer. Despite the same English word, these are distinct entities with distinct IDs and lifecycles. |
| **Identifier** | `gl_account_code` (natural key, e.g. "1100"); `gl_account_id` (surrogate) |
| **Status** | active |

### Order

| Field | Value |
|---|---|
| **Domain** | Sales |
| **Definition** | An immutable record of a Buyer's intent to purchase, including line items and agreed terms at the moment of placement. |
| **NOT** | Not a Cart (pre-submission, mutable); not a Quote (offered but not accepted); not a Subscription (recurring). |
| **Lifecycle states** | draft → pending_payment → paid → fulfilled → completed; (cancelled / partially_cancelled / refunded as exception paths) |
| **Identifier** | `order_id` |
| **Related** | Cart, Quote, Invoice, Shipment, Payment |

### (template — copy this row for each new term)

| Field | Value |
|---|---|
| **Domain** | … |
| **Definition** | … |
| **NOT** | … |
| **Identifier** | … |
| **Owned by** | … |
| **Authoritative system** | … |
| **Lifecycle states** | … |
| **Examples** | … |
| **Related** | … |
| **First defined** | YYYY-MM-DD |
| **Status** | draft |

---

## Cross-domain ambiguity ledger

Track terms where the same English word means different things in different domains. AI must check `domain` qualifier whenever a term appears in this list.

| English word | Meanings | Resolution |
|---|---|---|
| Account | Sales Account / GL Account / User Account | Always qualify with domain when discussing |
| Balance | AR Balance / Inventory On-hand / Cash Balance | Always qualify |
| Order | Sales Order / Purchase Order / Manufacturing Order / Work Order | Always use full term, never bare "Order" |
| Invoice | Customer Invoice (AR) / Vendor Invoice (AP) | Always qualify direction |
| Posting | GL Posting (accounting) / Job Posting (HR) | Distinct domains; usually unambiguous in context |

---

## Anti-patterns to refuse

- ❌ Coining a new term in code without registering it here
- ❌ Using a term in a CR / ADR / Flow that doesn't exist in this glossary (block the doc; require glossary entry first)
- ❌ Defining a term inside a Flow document instead of here
- ❌ Letting two domains share one definition row when they actually differ

---

## Maintenance

- Quarterly review with domain leads
- When superseding: mark old entry `status: superseded` + add `superseded-by` pointing at the new term name
- Never reuse a term name; if "Customer" gets redefined, the old definition lives on as `Customer (legacy)` archived

## See also

- `1-decisions/DDD-0000-domain-model.template.md` — entities here trace to terms here
- `2-contracts/MDS-0000-master-data.template.md` — master entities have richer specs
- `.claude/rules/change-governance.md` — terms with no glossary entry should fail the gate
