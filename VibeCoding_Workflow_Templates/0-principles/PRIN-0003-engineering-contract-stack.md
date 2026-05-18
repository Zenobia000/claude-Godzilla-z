---
id: PRIN-0003
title: "Engineering Contract Stack — The 10-Layer Map"
status: active
tier: 0-principles
owner: HUMAN-ONLY
essence: bedrock
last-reviewed: 2026-05-17
product-version: null
supersedes: null
superseded-by: null
---

# Engineering Contract Stack — The 10-Layer Map

> **Tier**: 0-principles — once adopted, every contract in this project lives on one of these 10 layers.
>
> **Why**: AI generates slop when it cannot tell which docs to trust, which contracts to honor, or which gate enforces what. A system without a layer map degrades into "23 markdowns, none authoritative." This document is the map.

---

## See also (don't duplicate scope)

| Doc | Answers |
|---|---|
| `PRIN-0001-flow-id-conventions.md` | **How to name** contracts (BF / API / ERR / ...) |
| `PRIN-0003` (this doc) | **What contract types exist** and how they layer |
| `HOW-TO-INSTANTIATE.md` | **Which contracts to instantiate** per profile (web-product / data-ml / platform-infra) |

If you came here looking for "should I write API-0042 or MC-0007?" → read this. For "what should I call the file?" → PRIN-0001. For "do I need this for an ML pipeline?" → HOW-TO-INSTANTIATE.

---

## §1 Why this stack (drift → AI slop)

Without an explicit stack, three failure modes dominate:

1. **Silent reconciliation**: AI reads `BF-0001 §4` saying "deduct inventory immediately" and `SF-0001 §3` saying "reserve inventory until paid" — it picks the "more reasonable" one and writes code that matches neither. The bug shipped six months later is uncatchable because nobody knows which doc was source of truth.
2. **Contract amnesia**: a contract exists (`API-0007.error.401`) but no CI gate enforces it. A refactor accidentally returns `403`. Tests pass because they were generated from code, not from the spec. The frontend silently misroutes.
3. **Phantom completion**: 23 markdown files exist, every section filled. Nobody noticed there is no contract for **idempotency** because no layer demands it. The Stripe webhook double-charges in production.

The fix is not "more docs." The fix is making the stack visible enough that gaps are obvious. **A stack with 5 layers and 5 CI gates beats a stack with 23 layers and 0 CI gates every single time.**

---

## §2 The 10 layers at a glance

```
┌─────────────────────────────────────────────────────────────────┐
│  L5 — Frontend contracts     Route / PC / Component / DS        │
├─────────────────────────────────────────────────────────────────┤
│  L4 — Quality gates          CT / BDD / i18n / TM               │
├─────────────────────────────────────────────────────────────────┤
│  L3 — Behavior contracts     POL / IDEM / Pagination / Filter   │
├─────────────────────────────────────────────────────────────────┤
│  L2 — Data contracts         MC(DbC) / SM / MIG / MDS           │
├─────────────────────────────────────────────────────────────────┤
│  L1 — Wire contracts         API / ASYNC / ERR                  │
└─────────────────────────────────────────────────────────────────┘
                          ↑
            Lower = closer to the wire (HTTP/AMQP/SQL).
            Higher = closer to the user (button / page).
            Every layer drifts the moment a CI gate stops watching it.
```

Read top-down when reviewing a feature ("does the page wire to a contract?").
Read bottom-up when designing a new module ("what wire & data contracts does this module export?").

---

## §3 Per-layer cells

Each cell answers five questions: **what** is the contract type, **what** is the machine-readable form, **which** CI gate enforces it, **which** skill helps author it, **which** rule mandates its use.

### L1 — Wire contracts

The bytes that cross process boundaries. If L1 drifts, every consumer (frontend, integration test, partner) sees a different system.

| Layer cell | Template ID | Machine-readable | CI gate | Skill | Rule |
|---|---|---|---|---|---|
| **L1.1 REST API** | `API-0000-api-spec.template.md` | `docs/2-contracts/api/openapi.yaml` | `CIG-0001` spec-lint (Spectral), `CIG-0002` types-sync, `CIG-0004` schemathesis | `vibecoding-write-api-contract`, `sunnydata-api-design` | `change-governance.md` (CIA on API change) |
| **L1.2 Async / Event** | `API-0000 §async` | `docs/2-contracts/api/asyncapi.yaml` + CloudEvents 1.0 | `CIG-0003` asyncapi-validate | `vibecoding-write-api-contract` (extend) | `change-governance.md` |
| **L1.3 Error envelope** | `API-0000 §errors` | RFC 7807 Problem Details + error-code registry YAML | `CIG-0001` (Spectral rules for RFC 7807) | `vibecoding-write-api-contract` (§errors) | `change-governance.md` |

### L2 — Data contracts

The shape, invariants, and lifecycle of long-lived data. L2 outlives any single endpoint.

| Layer cell | Template ID | Machine-readable | CI gate | Skill | Rule |
|---|---|---|---|---|---|
| **L2.1 Module / DbC** | `MC-0000-module-contract.template.md` | Code-level: `require()` / `ensure()` / Pydantic models | (none yet — manual review via `sunnydata-code-review`) | `vibecoding-write-ddd-aggregate`, `vibecoding-write-tdd` | `change-governance.md` |
| **L2.2 State machine** | `MC-0000 §state-machine` | `<entity>.example.xstate.json` | (regen check via `sunnydata-auto-regen`) | `vibecoding-write-ddd-aggregate` | `change-governance.md` |
| **L2.3 Schema migration** | `DATA-0000 §migration` | Alembic env + per-CR migration script | `CIG-0007` doc-freshness (cross-check migration head vs MIG-NNNN) | `vibecoding-write-db-schema`, `vibecoding-data-contract-evolution` | `change-governance.md` (data-touch triggers CIA) |
| **L2.4 Master data** | `DATA-0000 §master-data` | Catalog entry (DataHub / OpenMetadata) optional | (none — governance-only) | (manual) | `change-governance.md` |

### L3 — Behavior contracts

The rules of engagement between caller and service. L3 is mostly horizontal — it cuts across every API.

| Layer cell | Template ID | Machine-readable | CI gate | Skill | Rule |
|---|---|---|---|---|---|
| **L3.1 Auth / RBAC policy** | `ARCH-0000 §security` | OPA Rego / AWS Cedar | `CIG-0009` reverse-import-lint (no policy bypass) | `sunnydata-security`, `vibecoding-security-check` | `security.md`, `change-governance.md` |
| **L3.2 Idempotency** | `API-0000` §Idempotency (callout — no standalone template) | `Idempotency-Key` header + storage table schema | `CIG-0004` schemathesis (replay test) | `sunnydata-api-design` | `change-governance.md` |
| **L3.3 Pagination** | `API-0000` §Pagination | Cursor or RFC 5988 link | `CIG-0001` spec-lint Spectral rule | `sunnydata-api-design` | (style consistency only) |
| **L3.4 Filter / Query** | `API-0000` §Query | RQL / JSON:API subset / OData subset | `CIG-0001` spec-lint | `sunnydata-api-design` | — |

### L4 — Quality gates

The proofs that L1–L3 are honored. L4 is where AI generates the most slop if not enforced — "tests pass" is not "spec passes."

| Layer cell | Template ID | Machine-readable | CI gate | Skill | Rule |
|---|---|---|---|---|---|
| **L4.1 Contract test** | `TEST-0000 §contract` | Pact pacts / Schemathesis hypothesis | `CIG-0004` schemathesis-contract | `vibecoding-write-integration-tests`, `sunnydata-testing` | `testing.md` (80% coverage) |
| **L4.2 BDD acceptance** | `TEST-0000 §bdd` + `PROC-0001 §bdd` | `tests/features/*.feature` (Gherkin) | `CIG-0006` test-case-coverage | `vibecoding-write-bdd` | `testing.md` |
| **L4.3 i18n** | `FR-0000 §page-contract` + `ARCH-0000 §frontend` | `messages/{locale}.json` + key registry | `CIG-0005` i18n-keys-sync | (manual) | (style consistency only) |
| **L4.4 Traceability** | `(regen via sunnydata-auto-regen)` | AUTO-regen markdown table | `CIG-0008` orphan-check + `sunnydata-auto-regen` | `sunnydata-flow-audit`, `sunnydata-auto-regen` | `context-stability.md` (tier-2 sync) |

### L5 — Frontend contracts

The user-visible surface and the design system feeding it. L5 drifts fastest because designers and PMs touch it.

| Layer cell | Template ID | Machine-readable | CI gate | Skill | Rule |
|---|---|---|---|---|---|
| **L5.1 Route map** | `VIEW-0004-frontend-route-map.template.md` (AUTO) | Router config + route table | `CIG-0008` orphan-check (route ↔ PC) | `sunnydata-auto-regen` | `context-stability.md` |
| **L5.2 Page contract** | `FR-0000 §page-contract` | One PC-NNNN per route + frontmatter | `CIG-0007` doc-freshness | `vibecoding-write-frontend-bdd` | `context-stability.md` |
| **L5.3 Component prop** | (delegate to TS types generated from OpenAPI) | `web/types/api.generated.ts` | `CIG-0002` api-types-sync | `vibecoding-write-frontend-bdd` | `coding-style.md` (no `any`) |
| **L5.4 Design tokens** | `ARCH-0000 §frontend` | `<ds>.example.style-dictionary.json` → CSS vars | (regen check via `sunnydata-auto-regen`) | `community-ui-design-system`, `community-frontend-design` | (none) |

---

## §4 Decision tree — "I'm changing X, which layers do I touch?"

```
Q1: Does my change cross a process boundary (HTTP / queue / WebSocket / RPC)?
    YES → touch L1 (API/ASYNC) + ERR (any new error code) + L4.1 (contract test)
    NO  → continue

Q2: Does my change alter persistent data shape, an entity invariant, or master data?
    YES → touch L2 (MC / SM / MIG / MDS) + run CIA before code
    NO  → continue

Q3: Does my change affect who can do what, or how callers retry?
    YES → touch L3 (POL / IDEM) + L4.1 contract test (replay/auth scenarios)
    NO  → continue

Q4: Does my change have a UI surface?
    YES → touch L5 (PC / Route / DS) + L4.3 i18n
    NO  → continue

Q5: Did I add or change behavior anywhere?
    YES → touch L4.2 BDD (TC-NNNN) + L4.4 traceability row
    NO  → it's a no-op refactor; tier-5 views may regenerate
```

Anti-rule: **a PR that touches code but no contract layer should be a red flag in review**, not the default.

---

## §5 Profile mapping (which layers matter per product type)

See `HOW-TO-INSTANTIATE.md` for the full per-template table. Layer-level summary:

| Profile | L1 | L2 | L3 | L4 | L5 | AI track |
|---|---|---|---|---|---|---|
| **web-product** | All | All | All | All | All | Optional (when AI feature appears) |
| **data-ml** | API only (often gRPC) | MC + MIG + MDS heavy; SM rare | POL + IDEM | CT + BDD via notebooks | Skip (unless ML dashboard) | LLMEVAL + AICAP if LLM-based |
| **platform-infra** | API + ASYNC | MIG heavy | POL critical | CT + IaC tests | Skip | Skip |
| **ai-native** | All | All + RAG corpus | POL + AISAFE | CT + LLMEVAL | All | **All 5 cells required** |

Layers can be deferred but never **denied**: a `data-ml` project still needs error envelopes when its training API throws. An `ai-native` project that skips AISAFE is one prompt-injection away from front-page news.

---

## §6 Anti-patterns (the predictable failure modes)

| Anti-pattern | Smell | Fix |
|---|---|---|
| **L1 without lint** | OpenAPI exists but Spectral never runs | Add `CIG-0001` |
| **L2 markdown drifts from xstate** | `SM-0001-work-order.md` says 16 states; xstate JSON says 14 | Make `.example.xstate.json` a sibling and CI checks count match |
| **L3 idempotency missing** | API spec has no `Idempotency-Key` callout; webhooks double-fire in prod | Add `API-0000 §Idempotency` + replay test in `CIG-0004` |
| **L4 tests generated from code, not spec** | Refactor breaks contract, tests still pass | Switch to Schemathesis (spec-driven property-based) |
| **L4.3 i18n keys hand-added per locale** | `en.json` grows; `zh-TW.json` stale | Add `CIG-0005` key-sync lint |
| **L5 design tokens only in CSS** | iOS/Android can't reuse; designer changes vanish | Promote tokens to `.example.style-dictionary.json` |
| **All layers exist, none enforced** | 23 markdowns, 0 CI workflows | Run `sunnydata-contract-stack-audit` — every layer must point to ≥1 gate |
| **"It's just a small change"** | PR adds new field, skips CIA | `change-governance.md` makes CIA mandatory for any tier-2 touch |

---

## §7 How to use this map in practice

| When | Do this |
|---|---|
| Starting a new project | Read this doc → pick profile via HOW-TO → instantiate only the layers your profile demands |
| Onboarding a new engineer | Hand them this doc — it replaces "read all 52 templates" with "scan 10 cells" |
| Reviewing a PR | Walk the decision tree §4 — does the PR touch the right layers? |
| Auditing a project | Run `sunnydata-contract-stack-audit` skill — it reports layer-coverage / machine-readable presence / CI gate wiring |
| Adding a new contract type | Add a new row to §3, a new prefix to PRIN-0001, a CI gate to `3-process/ci-gates/`. Never just one of the three. |

---

## §8 AI-Native overlay (added v1.1)

For products where LLMs / agents are core (not a feature), the L1–L5 map gains a parallel **AI track** with 5 cells. They are not new layers — they are AI-specific implementations of existing layer semantics:

| AI cell | Sits on layer | Template | What it answers |
|---|---|---|---|
| **AI.1 Prompt contract** | L1 (wire — input to model) | `AI-0000 §prompt` | What text/schema does the model see, and against what eval did this version pass? |
| **AI.2 Agent + RAG** | L2 (data — runtime composition) | `AI-0000 §agent`, `AI-0000 §rag` | What is the agent's tool budget / loop / handoff? What is the retrieval pipeline? |
| **AI.3 Safety policy** | L3 (behavior — guardrails) | `AI-0000 §safety` | What 5-layer defense protects against injection / PII / misuse / toxicity? |
| **AI.4 Eval harness** | L4 (quality gate) | `TEST-0000 §llm-eval` | What datasets prove the AI feature works, and at what threshold? |
| **AI.5 Capacity / cost** | L5 (operational evaluation — feedback to business) | `AI-0000 §capacity` | What's the token budget per feature, and what's the degradation when exhausted? |

### Decision tree extension — "I'm changing an AI feature"

```
Q6: Am I editing a system prompt, tool list, or model pin?
    YES → bump PROMPT version + re-run LLMEVAL → AI.1 + AI.4
    NO  → continue

Q7: Am I adding / removing a tool, or changing the loop?
    YES → bump AGENT version + re-run agent dialog eval → AI.2 + AI.4
    NO  → continue

Q8: Am I changing corpus, chunking, embedding, or index?
    YES → re-embed + re-eval recall → RAG + AI.4
    NO  → continue

Q9: Did I add a new attack surface or content type?
    YES → AISAFE adversarial dataset row + re-run → AI.3 + AI.4
    NO  → continue

Q10: Will the change move token usage > 10% in either direction?
     YES → update AICAP budget; verify SLO burn-rate alerts → AI.5
     NO  → no AI-track changes required
```

### Anti-patterns specific to the AI track

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Prompt as string literal in code | No version, no eval, no rollback | `PROMPT-NNNN` for any production prompt |
| "We'll add evals later" | No baseline = no detection of regression on model upgrade | `LLMEVAL-NNNN` before launch, not after |
| Same model judges itself | Self-grading inflates scores | Different model in `LLMEVAL §4` |
| One token budget for staging + prod | Staging burn eats prod budget | Separate counters per `AICAP §3` |
| Trust system prompt to enforce safety | Models comply probabilistically | 5-layer defense per `AISAFE §2` |
| RAG without recall eval | Looks fine on demos, fails on production queries | `RAG-NNNN §9` mandatory |

---

## §9 Versioning this map

This document is **append-only-ish** in spirit: layers don't get removed, only added or split. If you split a layer (e.g. L3 grows a fifth cell for "rate limiting"), bump `last-reviewed` and note the addition in the version table below.

| Version | Date | Change |
|---|---|---|
| v1.1 | 2026-05-17 | Added §8 AI-Native overlay (5 cells: AI.1 Prompt, AI.2 Agent+RAG, AI.3 Safety, AI.4 Eval, AI.5 Capacity); decision tree extended Q6–Q10; 13 new prefixes (PROMPT, AGENT, RAG, AISAFE, AICAP, LLMEVAL, PERS, UE, EDGE, RM, ABT, GTM, EST) |
| v1.0 | 2026-05-16 | Initial 10-layer stack (L1×3, L2×4, L3×4, L4×4, L5×4) — 19 cells total; 6 new prefixes registered in PRIN-0001 (ERR / ASYNC / MIG / POL / CT / CIG) |

---

## See also

- `0-principles/PRIN-0001-flow-id-conventions.md` — ID prefix registry (now including ERR / ASYNC / MIG / POL / CT / CIG)
- `HOW-TO-INSTANTIATE.md` — profile picker
- `OWNERSHIP-MATRIX.md` — who edits which layer (Human / Hybrid / AI-AUTO)
- `3-process/QG-0000-quality-gates.md` — release gate that requires `contract-stack-audit` to pass
- `3-process/ci-gates/README.md` — the 10 CIG workflows
- `.claude/skills/sunnydata-contract-stack-audit/SKILL.md` — automated layer coverage audit
- `.claude/rules/change-governance.md` — CIA hard gate for L1–L2 changes
- `.claude/rules/context-stability.md` — 6-tier stability rules
