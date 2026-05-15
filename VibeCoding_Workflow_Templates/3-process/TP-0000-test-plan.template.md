---
id: TP-0000
title: "Test Plan"
status: draft
tier: 3-process
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
target-release: <version-or-quarter>
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
# Test Plan — `<Project / Module / Release>`

> **Tier**: 3-process → strategic test document
>
> **Purpose**: this is the **strategy** layer. It answers "**why** are we testing this, and **how** are we organizing the effort?". The execution layer (which test asserts which rule) lives in `2-contracts/TM-0000-traceability-matrix.template.md`.
>
> **Difference from traceability matrix**: matrix says "BF-0001 → TC-0001..0008 → test-order-create job". This plan says "we test order creation because order is the highest-revenue surface, target 90% line coverage on OrderService, accept 70% on Notification".

---

## 1. Scope

### In scope
- Modules / surfaces this plan covers
- Release window or feature set

### Out of scope
- Modules deliberately not tested in this plan (link to their own plan)
- Manual exploratory testing (covered separately)

## 2. Quality Targets

| Dimension | Target | Floor (must-not-fall-below) | Measurement |
|---|---|---|---|
| Domain logic line coverage | 90% | 80% | `pytest --cov=src/domain` |
| Service layer line coverage | 80% | 70% | `pytest --cov=src/services` |
| Infrastructure (adapters) | 60% | 50% | `pytest --cov=src/infra` |
| API contract coverage | 100% endpoints have ≥1 test | 100% | `dredd openapi.yaml` |
| BF coverage | 100% BFs have ≥1 happy + ≥1 exception E2E | 100% | manual matrix review |
| External dependency contracts | 100% vendors have contract test | 100% | `pact verify` |
| Critical path NFR | All `priority: critical` NFRs auto-verified | 100% | nightly perf job |

## 3. Test Pyramid (proportions, not absolutes)

| Layer | Target % of total | What lives here |
|---|---|---|
| Unit | 70% | Pure functions, business rules, value objects |
| Component / Module | 15% | Single module + its direct deps (in-process) |
| Contract | 8% | API contract tests + vendor contract tests |
| Integration | 5% | Cross-module flows with real DB / queue |
| E2E | 2% | Full BF happy + critical exception only |

> **Rationale**: cost grows roughly 10× per layer up. Heavy E2E reliance correlates with flaky tests, slow feedback, ignored failures.

## 4. Test Stage Catalog

| Stage | When run | Speed budget | Owner | Tools |
|---|---|---|---|---|
| Unit | Every save (watch mode) | < 30s full suite | Dev | pytest / vitest |
| Component | Every commit (pre-push) | < 2 min | Dev | pytest / RTL |
| Contract | Every PR | < 1 min | Dev | dredd / pact |
| Integration | Every PR | < 5 min | Dev | pytest + testcontainers |
| E2E | Every PR (critical) + nightly (full) | < 15 min critical / < 60 min full | QA | Playwright |
| Performance | Nightly | (async, alert on regression) | SRE | k6 |
| Security (SAST) | Every PR | < 3 min | Sec | semgrep |
| Security (DAST) | Weekly | (async) | Sec | OWASP ZAP |
| UAT | Per-release | (manual) | Product | manual checklist |
| Regression | Pre-release | (subset of above) | QA | tag-filtered run |

## 5. Test Data Strategy

| Data Source | Used by | Lifecycle | Provenance |
|---|---|---|---|
| Fixtures (committed JSON) | Unit, Component | Versioned in repo | Hand-curated minimal cases |
| Factories (factory-boy / faker) | Component, Integration | Generated per test | Schema-derived |
| Seed (SQL bootstrap) | Integration, E2E | Reset per suite | Idempotent migration scripts |
| Sandbox (vendor) | Contract, vendor E2E | Vendor-managed | See `PROC-0007-vendor-api-test.template.md` |
| Anonymized prod snapshot | Performance, edge-case discovery | Quarterly refresh | Pipeline strips PII before commit |
| Synthetic at scale | Performance | Generated | Mimas / locust dataset gen |

**Anti-patterns to refuse**:
- ❌ Using prod data in unit tests
- ❌ Tests that depend on a specific seed timestamp ("works on Tuesdays")
- ❌ Shared mutable fixture across tests (creates order-of-execution coupling)

## 6. Coverage by Risk Area

> Higher risk → higher coverage target. Override the §2 default per area.

| Area | Risk | Coverage target | Why |
|---|---|---|---|
| Payment processing | CRITICAL | ≥ 95% domain + property-based + chaos | Money loss, regulatory fines |
| Authentication / authorization | CRITICAL | ≥ 95% + security-focused tests | Account takeover, data breach |
| Order state machine | HIGH | ≥ 90% + state-transition exhaustive | Inventory mismatch, customer complaints |
| Notification dispatch | MEDIUM | ≥ 70% | User annoyance only |
| Reporting export | LOW | ≥ 50% | Eventually-consistent OK; manual fallback |

## 7. CI Quality Gate Specification

### What CI MUST output (beyond pass/fail)

```
PR #1234 affects:
  Flows:    UF-0007, UF-0012
  FRs:      FR-0023, FR-0089
  APIs:     API-0034 (BREAKING)
  Tests:    TC-0211..TC-0218 (executed: 8/8 passed)
  Coverage: src/orders/ 87% (-2% from main)
  NFRs:     NFR-0001 perf p95 = 154ms (target < 200ms ✅)
  Vendors:  Stripe contract OK; ERP contract STALE (last verified 14 days ago)

  Coverage debt this PR introduces:
    - new code in src/orders/cancel.py:42 not covered

  Required reviewers (per CODEOWNERS): @order-team @architect
```

### Blocking conditions (fail the build)

- Any test in modified path failed
- Coverage below floor (§2)
- Any contract test failed
- Any new public API endpoint without contract test
- Any FR with `status: active` whose linked TCs all failing

### Warning conditions (annotate but don't block)

- Coverage dropped 1-3%
- New code paths uncovered
- Vendor contract test stale (> 7 days)
- Flaky test detected (rerun reverted result)

## 8. Vendor / External Test Strategy

For each external dependency, fill `PROC-0007-vendor-api-test.template.md` separately. Summary index here:

| Vendor | Plan link | Sandbox available? | Contract test status |
|---|---|---|---|
| Stripe | `vendor/stripe.md` | Yes (test mode) | active |
| ERP | `vendor/erp-acme.md` | Yes (separate creds) | stale (#issue-123) |
| SendGrid | `vendor/sendgrid.md` | Limited (no callbacks) | mock-only |

## 9. Risk Register (testing-specific)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Flaky E2E in payment flow | High | Medium | Quarantine + root-cause within 1 sprint; never just retry |
| Vendor sandbox unstable | Medium | High | Maintain contract-test fallback that runs without sandbox |
| Coverage games (test the easy paths) | Medium | High | Mutation testing quarterly; review uncovered branches in code review |
| Test suite > 60 min | Medium | Medium | Parallelize; split critical vs full E2E |

## 10. Schedule & Ownership

| Phase | Owner | Deliverable | Due |
|---|---|---|---|
| Author Test Plan | QA Lead | This document | Sprint 1 |
| Fill vendor templates | Backend Lead | `vendor/*.md` | Sprint 1 |
| Set up coverage tools | DevOps | CI gate + dashboards | Sprint 2 |
| Backfill traceability matrix | All devs | Matrix entries for legacy code | Sprint 2-4 |
| Mutation testing baseline | QA | Stryker / mutmut report | Sprint 5 |
| Quarterly Test Plan review | QA Lead | Updated doc + retro | Every Q |

## 11. Sign-off

| Role | Name | Date | Approved? |
|---|---|---|---|
| QA Lead | | | |
| Engineering Lead | | | |
| Product (UAT scope) | | | |
| Security Lead | | | |
| SRE Lead (NFR) | | | |

---

## See also

- `2-contracts/TM-0000-traceability-matrix.template.md` — execution-layer "what tests what"
- `3-process/PROC-0007-vendor-api-test.template.md` — per-vendor detail
- `3-process/QG-0000-quality-gates.md` — Gate 4 prerequisites depend on this plan
- `3-process/PROC-0004-security-readiness-checklist.md` — security-test-specific checklist
- `.claude/rules/change-governance.md` — Test Plan changes are tier-3, but big restructures should go through CIA
