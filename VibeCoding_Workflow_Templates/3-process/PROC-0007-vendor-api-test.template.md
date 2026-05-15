---
id: PROC-0007
title: "Vendor API Test Requirement"
status: draft
tier: 3-process
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
vendor: <vendor-name>
contract-status: pending | active | stale | broken
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
# Vendor API Test Requirement — `<Vendor Name>`

> **Tier**: 3-process → external dependency planning
>
> **Purpose**: capture **what we need from the vendor BEFORE we can test the integration**. Filled per vendor; live next to `TP-0000-test-plan.template.md`.
>
> **Why a dedicated template**: every late-stage integration disaster starts with "oh, the vendor doesn't have a sandbox" or "the test card doesn't trigger the failure callback". This template makes that conversation happen at design time, not at integration time.
>
> **Companion fields**: this vendor's row in `2-contracts/TM-0000-traceability-matrix.template.md` § External Dependency Coverage points back here.

---

## 1. Vendor Identification

| Field | Value |
|---|---|
| Vendor name | <e.g. Stripe> |
| Service category | payment / shipping / notification / KYC / ERP / ... |
| Used by Flow IDs | `BF-NNNN`, `SF-NNNN` |
| Primary contact | <person + email> |
| Account / contract owner | <internal team> |
| Vendor SLA | e.g. 99.95% uptime, 200ms p95 |

## 2. What We Need From the Vendor (THE checklist)

Tick each item before declaring integration "ready to develop". Open issues for missing items immediately.

### Documentation
- [ ] Public API reference (URL: ___)
- [ ] OpenAPI / GraphQL schema file
- [ ] Postman collection or equivalent
- [ ] Changelog / versioning policy
- [ ] Authentication & key-rotation guide
- [ ] Rate-limit policy (per-key, per-IP, per-endpoint)
- [ ] Idempotency mechanism (header name, scope, retention)

### Sandbox / Test Environment
- [ ] Sandbox endpoint URL: ___
- [ ] Separate credentials from prod
- [ ] Sandbox data reset policy / how to clean up
- [ ] Sandbox rate limits (often stricter than prod)
- [ ] Sandbox uptime / scheduled maintenance windows
- [ ] Differences between sandbox and prod (documented gaps)

### Test Data
- [ ] Test cards / test accounts / test IDs that trigger:
  - [ ] Success
  - [ ] Decline (each decline reason)
  - [ ] Timeout
  - [ ] Rate-limit hit
  - [ ] Auth failure
  - [ ] Schema rejection
- [ ] Bulk-data generation tool (for load testing)
- [ ] Anonymized real payload examples

### Callbacks / Webhooks (if applicable)
- [ ] Callback signature scheme + secret rotation
- [ ] Idempotency-key header format
- [ ] Replay window (how long do they retry?)
- [ ] Out-of-order delivery guarantees (or lack thereof)
- [ ] How to trigger a callback in sandbox (manual? auto on event?)
- [ ] How to inspect failed callback delivery (vendor dashboard?)

### Error Handling
- [ ] Complete error code table
- [ ] Per-error: retryable vs not
- [ ] Per-error: caller action required vs vendor-side issue
- [ ] HTTP status mapping consistency

### Operational
- [ ] Status page URL (for incident detection)
- [ ] Incident notification channel (email list / Slack / etc.)
- [ ] Support escalation procedure
- [ ] Maintenance window calendar

### Compliance / Legal
- [ ] DPA (Data Processing Agreement) signed
- [ ] PII handling clarified (what we send, what they store)
- [ ] Region of data processing
- [ ] Audit log access on our side

## 3. Test Scenarios We Must Cover

Each scenario maps to a `TC-NNNN` in the traceability matrix. Mark `vendor` if the test requires the sandbox; `mock` if a contract fixture is enough.

| # | Scenario | Mode | TC ID | Priority |
|---|---|---|---|---|
| 1 | Success — happy path | vendor + mock | `TC-NNNN` | Critical |
| 2 | Vendor returns timeout | mock | `TC-NNNN` | Critical |
| 3 | Vendor returns 5xx → our retry kicks in | mock | `TC-NNNN` | Critical |
| 4 | Vendor returns 4xx (decline) | vendor + mock | `TC-NNNN` | Critical |
| 5 | Callback signature invalid → reject | mock | `TC-NNNN` | Critical |
| 6 | Callback duplicate → idempotent return | vendor + mock | `TC-NNNN` | Critical |
| 7 | Callback delayed (after we expect) | mock | `TC-NNNN` | High |
| 8 | Callback amount mismatch with order | mock | `TC-NNNN` | High |
| 9 | Rate-limit hit → backoff and retry | mock | `TC-NNNN` | High |
| 10 | Auth token expired mid-flow | vendor + mock | `TC-NNNN` | Medium |
| 11 | Schema drift (vendor adds field) | mock | `TC-NNNN` | Medium |
| 12 | Vendor entire outage | mock | `TC-NNNN` | Medium |

## 4. Contract Test Strategy

| Concern | Approach |
|---|---|
| Where contract lives | `tests/contract/<vendor>.yaml` |
| Tool | dredd / pact / schemathesis / hand-rolled |
| Run when | Every PR (against fixture); nightly (against sandbox) |
| Sandbox failure handling | Don't block PR; alert ops + open ticket |
| Schema drift detection | Diff vendor's published spec vs our committed copy weekly |

## 5. Fallback / Degradation Plan

When the vendor is unavailable, what does our system do?

| Vendor State | Our Behavior |
|---|---|
| Slow (p95 > 2s) | Circuit breaker opens after 10 consecutive slow calls; error page or fallback path |
| 5xx responses | Exp-backoff retry up to N; on exhaust → dead-letter queue + manual review |
| Total outage | Display banner; queue write requests for replay; degrade reads to cached |
| Schema breaking change | Pin to last-known-good vendor SDK version; alert; open vendor ticket |

Forward-link to relevant `SF-NNNN` if the fallback is implemented as a sub-flow.

## 6. Cost & Quota Considerations

| Concern | Value |
|---|---|
| Pricing model | per-call / per-MB / monthly / etc. |
| Free tier limits | <quantity> per <window> |
| Our expected volume | <quantity> per <window> |
| Rate-limit headroom | x% buffer above expected peak |
| Test-volume cost | <amount> per nightly run; OK / needs vendor agreement |

## 7. Migration / Switching Cost

If we needed to switch this vendor for any reason:
- Equivalent vendors evaluated: <list>
- Code-side switching cost (estimated): <person-days>
- Adapter pattern in place? Yes / No
- Data migration concerns: <list>

## 8. Open Questions

| Question | Owner | Status | Decided in |
|---|---|---|---|
| Does sandbox support partial-cancel callback? | Backend | open | — |
| Can we get higher rate limit for nightly tests? | Vendor mgmt | open | — |
| What's vendor's plan for the v2 schema? | Vendor mgmt | open | — |

## 9. Sign-off

| Role | Name | Date | Approved? |
|---|---|---|---|
| Integration Lead | | | |
| Architect | | | |
| Security (if PII flows) | | | |
| Product (if customer-facing impact) | | | |

---

## See also

- `3-process/TP-0000-test-plan.template.md` — vendor row in §8 points here
- `2-contracts/TM-0000-traceability-matrix.template.md` — § External Dependency Coverage row points here
- `2-contracts/API-0000-api-spec.template.md` — our API surface that wraps this vendor
- `1-decisions/ADR-0000-adr.template.md` — vendor selection decision should have an ADR
- `.claude/rules/change-governance.md` — vendor change → CIA gate (it's "external integration")
