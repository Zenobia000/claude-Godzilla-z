---
id: PRIN-0000
title: "Product Principles"
status: draft
tier: 0-principles
owner: HUMAN-ONLY
last-reviewed: <YYYY-MM-DD>
product-version: null
supersedes: null
superseded-by: null
---
# Product Principles — `<PROJECT_NAME>`

> **Tier**: 0-principles — strategic invariants; change at most once per major version

---

## 1. Mission

> One sentence. What this product exists to do, for whom, and why it matters now.

Example: *"Help solo founders ship a working MVP in two weekends by replacing template hunting with one opinionated workflow."*

---

## 2. Target Users

List 1-3 user personas. Each persona has:
- **Role / context**: what they do, what tools they live in
- **Pain we address**: the problem they have *before* this product
- **Success state**: what their world looks like after we succeed

---

## 3. Non-Goals (what we explicitly will NOT do)

This is the most load-bearing section. Without it AI will happily generalize the product into a competitor of every adjacent tool.

- We will NOT …
- We will NOT …
- We will NOT …

---

## 4. Quality Bars (what "good enough to ship" means here)

Concrete, measurable. Not aspirational.

| Dimension | Bar | How we measure |
|---|---|---|
| Performance | e.g. p95 < 200ms on the hot path | k6 nightly run |
| Reliability | 99.9% monthly | uptime monitor |
| Security | OWASP top 10 reviewed each release | security checklist |
| Accessibility | WCAG 2.2 AA on all user-facing pages | community-a11y-audit |
| Test coverage | 80% on domain logic | pytest --cov |

---

## 5. Technical Invariants

Things that must remain true regardless of feature work. Violating any of these requires an ADR.

- **Data sovereignty**: e.g. *"User data never leaves EU region"*
- **Backwards compatibility**: e.g. *"Public API breaking changes require a 12-month deprecation"*
- **Tech-stack constraints**: e.g. *"Backend stays on PostgreSQL — no second OLTP database"*
- **Operational constraints**: e.g. *"All long-running jobs must be idempotent"*

---

## 6. Decision-Making Defaults

When the team (or the AI) faces a tradeoff with no explicit guidance, default to:

- **Simplicity over flexibility** until flexibility is proven necessary
- **Read paths over write paths** when optimizing
- **Explicit over implicit** in API design
- **Server-side rendering over client state** unless interaction demands otherwise

(Customize for your project. The point is to encode the team's instincts so the AI doesn't have to guess.)

---

## 7. Out-of-Date Indicators

This document is stale when ANY of the following is true. Re-review immediately:

- [ ] The mission statement no longer matches the headline on the public landing page
- [ ] A persona was added/removed in the past quarter without updating §2
- [ ] An ADR overrode a "Technical Invariant" without updating §5
- [ ] A competitor launched a feature that we now actively differentiate against, but it isn't in §3 Non-Goals

---

**Maintained by**: `<owner>`
**Last reviewed**: `<YYYY-MM-DD>`
**Next review due**: `<YYYY-MM-DD + 6 months>`