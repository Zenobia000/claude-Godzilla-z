# VibeCoding Workflow Templates

> **Version:** v6.0 — Linus-minimum convergence (20 templates; 71 → 20 = -72%)
> **Updated:** 2026-05-17
> **🚪 NEW HERE? Read [`BEDROCK.md`](./BEDROCK.md) first** — 5 minutes, lists the 10 essentials.

---

## Why this layout

Templates are organized by **stability tier**. Path prefix (`0-`, `1-`, ..., `4-`) tells you and AI **how often this kind of doc changes** — which is the metadata that matters most for trust.

```
0-principles  ←  trust most; changes < 1×/year
1-decisions
2-contracts
3-process
4-exploration ←  trust as motivation; changes per task
```

Tier 5 (auto-regen views) was deleted in v6.0 — generated on demand via `sunnydata-auto-regen` skill instead.

---

## The 20 canonical templates

### Tier 0 — Principles (3, all bedrock)
- [`PRIN-0000-product-principles.template.md`](./0-principles/PRIN-0000-product-principles.template.md) — mission · personas · non-goals · glossary · unit-economics · quality bars · invariants
- [`PRIN-0001-flow-id-conventions.md`](./0-principles/PRIN-0001-flow-id-conventions.md) — naming invariant
- [`PRIN-0003-engineering-contract-stack.md`](./0-principles/PRIN-0003-engineering-contract-stack.md) — 10-layer map (where every contract lives)

### Tier 1 — Decisions (2)
- [`ARCH-0000-architecture-overview.template.md`](./1-decisions/ARCH-0000-architecture-overview.template.md) **bedrock** — C4 + modules + stack + infra + DDD + capacity-est + security + frontend
- [`ADR-0000-adr.template.md`](./1-decisions/ADR-0000-adr.template.md) specialized — append-only decision record

### Tier 2 — Contracts (8)
- [`FLOW-0000-flow.template.md`](./2-contracts/FLOW-0000-flow.template.md) **bedrock** — BF / UF / SF (3 scopes, one template)
- [`API-0000-api-spec.template.md`](./2-contracts/API-0000-api-spec.template.md) **bedrock** — REST + async + errors + idempotency
- [`MC-0000-module-contract.template.md`](./2-contracts/MC-0000-module-contract.template.md) **bedrock** — DbC + state machine (+ xstate JSON sibling)
- [`FR-0000-functional-requirement.template.md`](./2-contracts/FR-0000-functional-requirement.template.md) **bedrock** — rules + page contract
- [`SRE-0000-reliability.template.md`](./2-contracts/SRE-0000-reliability.template.md) **bedrock** — SLO + observability + capacity
- [`DATA-0000-data-contract.template.md`](./2-contracts/DATA-0000-data-contract.template.md) specialized — master data / migration / pipeline / model card
- [`AI-0000-ai-system-contract.template.md`](./2-contracts/AI-0000-ai-system-contract.template.md) specialized — prompt / agent / RAG / safety / capacity
- [`EDGE-0000-edge-case-catalog.template.md`](./2-contracts/EDGE-0000-edge-case-catalog.template.md) **bedrock** — production memory (10 classes)

### Tier 3 — Process (4)
- [`PROC-0001-developer-handbook.template.md`](./3-process/PROC-0001-developer-handbook.template.md) **bedrock** — onboarding + workflow + code review + security review + BDD
- [`PROC-0002-ops-runbook.template.md`](./3-process/PROC-0002-ops-runbook.template.md) specialized — deploy + gitops + incident + chaos + deprecation
- [`TEST-0000-testing-strategy.template.md`](./3-process/TEST-0000-testing-strategy.template.md) specialized — unit + contract + BDD + LLM-eval + experiment
- [`QG-0000-quality-gates.md`](./3-process/QG-0000-quality-gates.md) specialized — Gate 0–5 stage prerequisites

### Tier 4 — Exploration (3, all specialized)
- [`PRD-0000-prd.template.md`](./4-exploration/PRD-0000-prd.template.md) — discovery + personas + spec + experiments + launch
- [`PLAN-0000-planning.template.md`](./4-exploration/PLAN-0000-planning.template.md) — roadmap + WBS
- [`CIA-0000-change-impact-analysis.template.md`](./4-exploration/CIA-0000-change-impact-analysis.template.md) — CR-driven impact

### Tier 3 — CI Gates (10 enforcement workflows, not templates)

`3-process/ci-gates/CIG-0001..0010.workflow.yml` — see [`ci-gates/README.md`](./3-process/ci-gates/README.md).

---

## How AI should consume these

| Tier | When to load | How to treat |
|---|---|---|
| 0-principles | Every new conversation | Hard constraint — overrides downstream |
| 1-decisions | Before proposing architecture | Honor or escalate; never silently contradict |
| 2-contracts | When touching public interfaces | Check `last-synced-with` first |
| 3-process | Before category of work (review / deploy / test) | Follow checklist |
| 4-exploration | For motivation context | Don't assume current behavior |
| (5-views removed) | — | Use `sunnydata-auto-regen` skill for on-demand views |

---

## Version history

| Version | Date | Change |
|---|---|---|
| **v6.0** | **2026-05-17** | **Linus-minimum convergence**. 71 templates → 20. Deleted 5-views/, GLOS, DDD, ARCH-0001/2/3, MDS, MIG, PIPE, MODEL, ERR, ASYNC, SLO, OBS, CAP, POL, DS, FI, TM, BF/UF/SF, SM, PC, CT, TP, EXP, PROMPT, AGENT, RAG, AISAFE, AICAP, LLMEVAL, PERS, UE, EST, ABT, GTM, RM, WBS, DISC, ONBOARD, PRIN-0002, ADR-0001, PROC-0002..0012. Content merged into 8 new consolidated templates: `FLOW`, `DATA`, `AI`, `SRE`, `TEST`, `PLAN`, `PROC-0001` (handbook), `PROC-0002` (ops runbook). New entry point: `BEDROCK.md`. Profile system simplified. CI gates unchanged. |
| v5.8 | 2026-05-17 | AI-native + startup completion (13 new templates: 6 AI, 5 product, 2 system-design) |
| v5.7 | 2026-05-16 | Engineering contract stack distillation (PRIN-0003 10-layer map + 6 contracts + 10 CI gates) |
| v5.6 | 2026-05-15 | Profile-based template selection + lifecycle completion (13 new templates) |
| v5.4 | 2026-05-10 | Frontend template tier realignment |
| v5.3 | 2026-05-10 | Flow self-monitoring |
| v5.2 | 2026-05-10 | ERP foundation (Glossary, Module Boundary, DDD, SM, MDS) |
| v5.1 | 2026-05-10 | "One doc, one question" enforcement |
| v5.0 | 2026-05-10 | Change governance: Flow ID system, layered Flow templates, CIA |
| v4.0 | 2026-05-10 | Stability-tier layout |
