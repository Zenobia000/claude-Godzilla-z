---
id: EDGE-0000
title: "Edge Case Catalog (RESHADED D) — Template"
status: active
tier: 2-contracts
owner: HYBRID
essence: specialized
layer: cross-cutting
last-synced-with: null
sync-source: doc
source-paths: ["src/", "tests/"]
synced-at: null
---

# EDGE-NNNN: Edge Case Catalog

> **Tier**: 2-contracts · **Layer**: cross-cutting (touches L2 data, L3 behavior, L4 quality)
>
> **Why**: RESHADED's final D — "Distinctive Features / Edge Cases" — is where prototype-grade code dies in production. Without a catalog, every engineer re-discovers the same edge cases independently. With one, the catalog is the institutional memory: every production bug becomes a row.

---

## §1 Scope

One `EDGE-NNNN` per **bounded context** or major feature. Examples:
- `EDGE-0001-billing` — payment, refunds, currency, retries
- `EDGE-0002-auth` — sessions, expiry, multi-device, password reset
- `EDGE-0003-ai-triage` — language, length, injection, model timeouts

Edge cases for a single endpoint may live inline in the `API-NNNN`; broad / cross-cutting cases live here.

---

## §2 The catalog format

```
EDGE-NNNN.<short-id>
  Title:        <one line>
  Class:        boundary | concurrency | failure | input | locale | scale | security | timing | data | external
  Likelihood:   common | rare | exotic
  Severity:     CRITICAL | HIGH | MEDIUM | LOW
  First seen:   <date or "design phase">
  Reproducer:   <test ID, or "see test_edge_0042">
  Behavior:     <one sentence>
  Forbidden:    <what we MUST NOT do>
  Mitigation:   <link to code + spec sections>
```

Each row is small. The catalog earns its keep at 20+ rows.

---

## §3 Classes of edge case (use as a checklist)

When designing a feature, walk these 10 classes and decide which apply:

| Class | Probe question |
|---|---|
| **Boundary** | What at min, max, empty, one, all? |
| **Concurrency** | Two users / two tabs / two retries doing this at once? |
| **Failure** | Each external dep down, slow, half-broken? |
| **Input** | Unicode, RTL, very long, very short, base64 in a string field? |
| **Locale** | Different language, timezone, currency, calendar, plural rule? |
| **Scale** | 1× volume vs 100× vs 10,000×? |
| **Security** | What if the actor is malicious / has stolen creds / is the wrong tenant? |
| **Timing** | Daylight savings, leap second, leap day, year rollover, T-1 sec? |
| **Data** | NULL, corrupted, schema drift, soft-deleted, archived? |
| **External** | Vendor returns malformed, deprecated, billing-overdue? |

This is the checklist for RESHADED's last D.

---

## §4 Worked examples (illustrative — replace per feature)

### EDGE-0001.B1 — Billing: refund > original charge
- **Class**: data, boundary
- **Likelihood**: rare
- **Severity**: HIGH
- **Behavior**: API rejects with `INVALID_REFUND_AMOUNT`; logs incident
- **Forbidden**: silently truncate to charge amount
- **Mitigation**: schema validation `amount <= charge.amount` in `MC-billing §invariant.3`; test `test_refund_overcharge_rejected`

### EDGE-0001.C2 — Billing: double-click on Pay button (concurrency)
- **Class**: concurrency
- **Likelihood**: common
- **Severity**: CRITICAL
- **Behavior**: Idempotency-Key dedupes; only one charge processed
- **Forbidden**: rely on frontend disabling button
- **Mitigation**: `API-0007 §Idempotency`; integration test `test_payment_idempotent_double_click`

### EDGE-0001.L1 — Billing: amount in JPY (no decimals)
- **Class**: locale
- **Likelihood**: common (Asian markets)
- **Severity**: HIGH
- **Behavior**: store as integer minor unit; format per locale rules
- **Forbidden**: divide JPY by 100 like USD
- **Mitigation**: Money type wraps `(amount: int, currency: ISO-4217)`; covered in `EDGE-0001` §local.currency

### EDGE-0001.T1 — Billing: month rollover during recurring charge
- **Class**: timing
- **Likelihood**: common (last day of month)
- **Severity**: MEDIUM
- **Behavior**: charge dated to last actual day of shorter month; "Jan 31 anchor" billed Feb 28
- **Forbidden**: skip the cycle; charge double next month
- **Mitigation**: anchored on `bill_anchor_day`; clamp to `last_day_of_month`

### EDGE-0003.X1 — AI triage: prompt injection via ticket body
- **Class**: security
- **Likelihood**: common
- **Severity**: CRITICAL
- **Behavior**: Layer 1 sanitization strips known patterns; Layer 4 output scrubbing catches leakage
- **Forbidden**: trust ticket body content
- **Mitigation**: `AISAFE-0000 §3 §4`; adversarial eval `LLMEVAL-NNNN-adversarial`

### EDGE-0003.S1 — AI triage: 100K-token ticket body
- **Class**: scale, boundary
- **Likelihood**: rare
- **Severity**: MEDIUM
- **Behavior**: truncate to 8K tokens; flag as "truncated" in output
- **Forbidden**: silently send (cost runaway); reject without explanation
- **Mitigation**: `AICAP-NNNN §2` per-call token cap; user-facing warning

---

## §5 Sourcing edge cases

The catalog grows from five sources:

1. **Design walk-through** — walk §3 classes during design review; record rows for any "yes, that's a real case"
2. **Production incident** — every post-mortem (`PROC-0009`) produces ≥ 1 EDGE row
3. **Adversarial eval** — every failing `LLMEVAL-NNNN-adversarial` row → EDGE row (for AI features)
4. **Customer-reported bug** — non-incident bugs that pass §2 severity bar
5. **Code review observation** — "what about X?" comments where X turns out to be real

A "this won't happen" comment in code review is a candidate EDGE row — capture it before forgetting.

---

## §6 Severity / handling matrix

| Severity | Coverage required |
|---|---|
| **CRITICAL** | Test (`TC-NNNN`) + monitored metric + runbook in `PROC-NNNN` |
| **HIGH** | Test + alert (no runbook required if recoverable) |
| **MEDIUM** | Test |
| **LOW** | Documented behavior; no enforcement |

A CRITICAL EDGE row without a test → blocker for merge.

---

## §7 Integration with CI

| Check | How | When |
|---|---|---|
| Every CRITICAL EDGE row has a TC | Grep `EDGE-*` for `Severity: CRITICAL`, verify referenced TC exists in `test-cases/registry.yaml` | `CIG-0006` per PR |
| Every HIGH EDGE row has a TC | Same as CRITICAL | `CIG-0006` per PR |
| Reproducer test actually runs and is not skipped | pytest collection + skip detection | `CIG-0006` per PR |
| No row added in PR with `Reproducer: TBD` for ≥ 30 days | Cron scan against creation date in row | Nightly |
| EDGE row TC IDs match implemented tests | Cross-reference against `pytest --collect-only -q` output | `CIG-0006` per PR |

Implementation note for `CIG-0006` extension:

```python
# In CIG-0006 workflow, append:
edge_rows = parse_edge_catalog("docs/2-contracts/EDGE-*.md")
for row in edge_rows:
    if row.severity in ("CRITICAL", "HIGH"):
        tc_id = row.reproducer_tc
        if not tc_id or tc_id not in registry["test_cases"]:
            fail(f"EDGE {row.id} severity={row.severity} has no TC; add one or downgrade severity")
```

A row without a passing reproducer is a known bug, not a documented behavior — re-classify or remove.

---

## §8 What this catalog is NOT

- Not a bug tracker (use issues for unresolved; this is for resolved + accepted-behavior)
- Not a security audit (a CRITICAL security row triggers `AISAFE-NNNN` / `POL-NNNN` follow-up)
- Not generic best-practices ("validate input" — that's a §3 class, not a row)

---

## §9 Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Edge cases scattered in comments | Lost during refactor; AI cannot index | Single catalog file per bounded context |
| Only documenting cases that have happened | Reactive; preventable bugs ship | Walk §3 checklist during design |
| Generic entries ("handle errors") | No actionable behavior | One concrete sentence per §2 fields |
| Edge case found by customer → "we'll fix it later" | Becomes folklore | Open a row immediately; assign severity |
| Catalog reviewed once and abandoned | Decays in 6 months | Open one row per incident makes it self-fueling |

---

## §10 Catalog table (real entries — append, never reorder)

| ID | Title | Class | Severity | First seen | TC |
|---|---|---|---|---|---|
| EDGE-NNNN.B1 | <example> | boundary | HIGH | 2026-05-12 | TC-0142 |
| EDGE-NNNN.C2 | <example> | concurrency | CRITICAL | 2026-04-30 | TC-0156 |
| ... | | | | | |

Rows added with `git add`. Removed only with deprecation reason in row body (`DEPRECATED: behavior changed in CR-NNNN`).

---

## See also

- `0-principles/PRIN-0003-engineering-contract-stack.md` — cross-cutting layer cell
- `2-contracts/FR-0000-functional-requirement.template.md` — FRs reference EDGE rows for acceptance
- `2-contracts/MC-0000-module-contract.template.md` — invariants come from EDGE rows
- `2-contracts/AISAFE-0000-ai-safety-policy.template.md` — security edge cases overlap
- `3-process/PROC-0009-incident-response.template.md` — incidents seed §5 row 2
- `3-process/LLMEVAL-0000-eval-harness.template.md` — adversarial dataset seeds §5 row 3
- `3-process/ci-gates/CIG-0006-test-case-coverage.workflow.yml` — coverage check (§7)
