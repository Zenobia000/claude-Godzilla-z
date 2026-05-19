---
id: TEST-0000
title: "Testing Strategy — Unit / Contract / BDD / LLM-Eval / Experiment"
status: active
tier: 3-process
owner: HYBRID
essence: specialized
absorbs: [CT-0000, LLMEVAL-0000, TP-0000, EXP-0000]
last-reviewed: null
---

# TEST-0000: Testing Strategy

> **Tier**: 3-process · **Essence**: bedrock — without a test strategy, "tests pass" means nothing because nobody agreed what "passing" means.
>
> **One template, five sections** — pick what applies. Every project has §unit + §contract; AI-native adds §llm-eval; data-ml adds §experiment.

---

## §0 — Identity

| Field | Value |
|---|---|
| Subject | Project / service / feature name |
| Owner | QA / eng lead |
| Coverage target | 80% (or stated otherwise per project) |
| Sections used | `[unit, contract, bdd]` (declare; rest auto-N/A) |

---

## §1 — Pyramid & test mix

```
                      △
                     ╱E╲          E2E (~5%): Playwright / Cypress for golden paths
                    ╱2E ╲         Slow, expensive, brittle. Few but critical.
                   ╱─────╲
                  ╱  IT   ╲       Integration (~15%): DB + service layer
                 ╱  + CT   ╲      Contract tests live here (§3)
                ╱───────────╲
               ╱   UT (80%)  ╲    Unit (~80%): pure functions, modules
              ╱───────────────╲   Fast, deterministic, abundant.
```

This split is the default. Adjust by domain:
- Pure UI library: invert to E2E-heavy
- Data pipeline: heavier contract + DQ tests
- AI-native: §llm-eval is its own pyramid (golden / regression / adversarial)

---

## §2 — Unit tests (§unit)

| Property | Rule |
|---|---|
| Coverage minimum | 80% line, 70% branch (drop branch in pure-DTO modules) |
| Determinism | No network, no time, no random — inject all three |
| Speed | < 10ms per test (slower = move to integration) |
| Mocking | Mock external services; **do not mock the DB** (use ephemeral SQLite/Postgres in CI) |
| Fixture scope | Test-local; no shared mutable global state |

CI command: `pytest tests/unit/ --cov=src --cov-fail-under=80`.

---

## §3 — Contract tests (§contract)

> Validate spec ↔ code. Two complementary techniques.

### §3.1 Schemathesis (spec-driven, single service)

```bash
schemathesis run \
  --base-url=http://localhost:8000 \
  --hypothesis-deadline=5000 \
  --checks=all --workers=4 \
  docs/2-contracts/api/openapi.yaml
```

Catches: undeclared 4xx/5xx, schema-mismatch responses, server crash on edge input, stateful inconsistency.

CI gate: `CIG-0004` runs this on every PR.

### §3.2 Pact (consumer-driven, multi-service)

Use when: ≥2 services consume a producer's API and you want consumer expectations enforced.

```ts
const provider = new PactV3({ consumer: "WebApp", provider: "OrderService" });
await provider.given("order o_42 exists")
  .uponReceiving("GET /orders/o_42")
  .withRequest({ method: "GET", path: "/orders/o_42" })
  .willRespondWith({ status: 200, body: { id: "o_42", state: "confirmed" } });
```

Provider verification: `pact-verifier --provider-base-url=http://localhost:8000 --pact-urls=https://broker.example/...`.

### §3.3 When to use which

| Situation | Tool |
|---|---|
| Single service, spec-first, want max coverage | Schemathesis |
| Multi-service, want consumer expectations enforced | Pact |
| Both | Schemathesis in unit CI + Pact in integration CI |
| Webhook / async | Pact Message + `asyncapi-cli validate` |

---

## §4 — BDD acceptance (§bdd)

> The shared language between PM / engineering / QA.

### §4.1 Gherkin format

```gherkin
Feature: Order cancellation
  Background:
    Given a confirmed order o_42 with total $100

  Scenario: Customer cancels within 1h — full refund
    When the customer requests cancellation at t+30min
    Then a refund of $100 is issued
    And the order state becomes "cancelled"

  Scenario: Customer cancels after 24h — partial refund per FR-0089
    When the customer requests cancellation at t+25h
    Then a refund of $70 is issued
    And the order state becomes "cancelled_with_fee"
```

### §4.2 BDD discipline

| Rule | Why |
|---|---|
| One feature file per FR | 1:1 mapping; easy to audit |
| Scenarios must be testable (Given/When/Then, no narrative) | Forces falsifiability |
| `Background` for shared setup | DRY |
| `Examples` for parametric variants | Don't multiply scenarios |
| Reference FR ID in feature file header | Traceability |

CI: `pytest-bdd tests/features/` (Python) / `cucumber` (JS) / `godog` (Go).

### §4.3 Coverage

Every FR-NNNN with `Severity ≥ HIGH` must have ≥ 1 scenario. `CIG-0006` test-case-coverage enforces.

---

## §5 — LLM Eval (§llm-eval)

> Required for any AI feature. Use this section together with `AI-0000`.

### §5.1 Dataset taxonomy

| Type | Purpose | Size | Refresh |
|---|---|---|---|
| **Golden** | Hand-curated canonical | 100–500 rows | When spec changes |
| **Regression** | Production samples + historical labels | 50–200 rows | Monthly |
| **Adversarial** | Injection / jailbreak / edge | 20–100 rows | When new attack surface |
| **Bias / fairness** | Demographic-balanced | 100+ rows | Quarterly |

Files: `tests/llmeval/<feature>.golden.jsonl`, `.regression.jsonl`, `.adversarial.jsonl`.

### §5.2 Row format (JSONL)

```json
{
  "id": "triage-golden-0042",
  "input": { "ticket_body": "Cannot reset password", "customer_tier": "pro" },
  "expected": { "severity": "P2", "category": "bug", "needs_followup": true },
  "judge": "exact_match",
  "tags": ["account-recovery", "common-case"]
}
```

### §5.3 Judges

| Judge | When | Cost |
|---|---|---|
| `exact_match` | Closed enum / structured | Free |
| `subset_match` | Required fields present | Free |
| `regex_match` | Pattern | Free |
| `unit_test` | `def check(output) -> bool` | Free |
| `llm_judge` | Open-ended quality / faithfulness | $$ |
| `human` | Subjective fallback | $$$ |

**LLM-as-judge rules**: judge model ≠ model under test; judge prompt is itself a versioned prompt in `AI-NNNN`; calibrate against ≥ 30 human labels (Cohen's κ ≥ 0.7).

### §5.4 Pass thresholds

| Severity | Threshold | If breached |
|---|---|---|
| Golden | ≥ 92% | Block deploy |
| Adversarial (injection/jailbreak) | 100% blocked | Block deploy |
| Regression | within 3pp of last release | Manual review |
| Bias | no subgroup gap > 5pp | File incident |

### §5.5 Dataset curation discipline

1. Every production incident → row in regression set within a week
2. Adversarial datasets grow on disclosure; never delete failing rows
3. Golden datasets signed (checksum committed); PR edit requires 2 reviewers
4. Tag every row — without tags, you can't slice failures

### §5.6 CI wiring

| Trigger | Workflow | Datasets | Fail action |
|---|---|---|---|
| PR touches `prompts/` | `CIG-LLM-001.workflow.yml` | Golden | Block PR |
| Nightly | scheduled | All, deeper fuzz | Open issue |
| Pre-release | `release.yml` step | All, full sweep | Block tag |

---

## §6 — Experiments (§experiment)

> Use for ML training runs OR product A/B tests. Two flavors, same shape.

### §6.1 Pre-registration

| Field | Value (example) |
|---|---|
| Experiment ID | `EXP-NNNN-churn-v3.2` |
| Hypothesis | "Adding session-recency feature lifts AUC > 0.02" |
| Falsifiable | Yes — if AUC delta < 0.02 OR p > 0.05, hypothesis rejected |
| Owner | ml-team |
| Pre-registered | `2026-05-10` (locked before run) |

### §6.2 Setup (ML)

| Field | Value |
|---|---|
| Dataset | `s3://example-data/churn-training/2026-04/` (300k rows, 90d horizon) |
| Train / val / test split | 70 / 15 / 15 (deterministic seed) |
| Baseline model | `churn_predictor v3.1` |
| Treatment | v3.1 + recency feature |
| Compute | 4× A10G, 6h budget |

### §6.3 Setup (A/B product)

| Field | Value |
|---|---|
| Variants | control / treatment (50/50 by user_id hash, sticky) |
| Primary metric | One only (e.g. `trial_signup_rate`) |
| Guardrail metrics | 3 — retention, support tickets, revenue/visitor |
| MDE | 3% relative |
| Sample size | per power calc (e.g. 14,000 per arm) |

### §6.4 Decision rule (both flavors)

| Result | Action |
|---|---|
| Treatment wins, no guardrail breach, CI lower > MDE | Ship treatment |
| Inconclusive | Ship control; don't retest same idea for 6mo |
| Guardrail breach | Ship safer variant; investigate |

The decision is **mechanical**. Opinion lives in the hypothesis, not the conclusion.

### §6.5 Results (filled after concluded)

| Field | Value |
|---|---|
| Sample sizes | C 14,021 / T 13,998 |
| Primary metric | C 11.8% / T 13.4% |
| Relative lift | +13.5%; 95% CI [+6.1%, +20.9%] |
| p-value | 0.0008 |
| Guardrails | All pass |
| Decision | Ship treatment |
| Post-mortem at T+30d | (filled later) |

---

## §7 — Test failure response

1. Load `sunnydata-debugging` skill
2. Reproduce locally with same fixtures
3. Fix root cause (NOT the test — unless test is wrong)
4. Add regression row if production incident
5. Re-run full suite (no partial fixes)

---

## §8 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Tests as docs ("explains the code") | Tests must catch regressions, not narrate | Re-write as assertions |
| Mocking the DB in integration tests | False sense of safety; migrations break in prod | Real DB (containerized) |
| Tests generated from code | Refactor breaks contract; tests still pass | Generate from spec (Schemathesis) |
| `pytest -k` skip-tag growing | Hides flaky reality | Investigate or delete |
| Same LLM judges itself | Inflated scores | Different model |
| "Eval passes locally, not CI" | Temperature non-zero | Pin temp=0 in eval |
| Editing failing rows to pass | Teaching to the test | Move to regression OR delete with reason |
| One eval = 5 examples in notebook | Tells you nothing | 100-row minimum for golden |
| Peeking + early-stop for A/B significance | Inflates type-I to ~30% | Fixed sample OR sequential analysis |
| Post-hoc segments | Cherry-picking | Pre-register §8 of `ABT` |

---

## See also

- `PRIN-0003-engineering-contract-stack.md` §3 L4.1 — quality gates layer
- `API-0000-api-spec.template.md` — spec consumed by Schemathesis
- `AI-0000-ai-system-contract.template.md` — what §llm-eval validates
- `DATA-0000-data-contract.template.md` §model-card — what §experiment produces
- `QG-0000-quality-gates.md` Gate 4 — coverage requirements
- `PROC-0001-developer-handbook.template.md` §code-review — what reviewers check
