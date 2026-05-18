# BEDROCK — The Linus Minimum

> v6.0 entry point. **Read this before anything else.** 5 minutes total.
>
> 20 canonical templates. 10 bedrock (always needed). 10 specialized (opt-in). No "set of 76 to memorize."

---

## The 10 BEDROCK templates (every non-trivial project)

If you don't have these, your engineers and AI will hallucinate the answers. Order matters — read them in this order.

| # | File | Without it you cannot answer |
|---|---|---|
| 1 | [`0-principles/PRIN-0000-product-principles.template.md`](./0-principles/PRIN-0000-product-principles.template.md) | What is this product? Who is it for? What are we NOT building? |
| 2 | [`0-principles/PRIN-0001-flow-id-conventions.md`](./0-principles/PRIN-0001-flow-id-conventions.md) | How do we name flows, contracts, decisions? |
| 3 | [`0-principles/PRIN-0003-engineering-contract-stack.md`](./0-principles/PRIN-0003-engineering-contract-stack.md) | Where does this contract live? (the 10-layer map) |
| 4 | [`1-decisions/ARCH-0000-architecture-overview.template.md`](./1-decisions/ARCH-0000-architecture-overview.template.md) | What's the system shape? (C4 + modules + stack + infra + security + frontend) |
| 5 | [`2-contracts/FLOW-0000-flow.template.md`](./2-contracts/FLOW-0000-flow.template.md) | How does the business / user / sub-task happen? |
| 6 | [`2-contracts/API-0000-api-spec.template.md`](./2-contracts/API-0000-api-spec.template.md) | What crosses the wire? (REST + async + errors + idempotency) |
| 7 | [`2-contracts/MC-0000-module-contract.template.md`](./2-contracts/MC-0000-module-contract.template.md) | What does this module promise? (DbC + state machine) |
| 8 | [`2-contracts/FR-0000-functional-requirement.template.md`](./2-contracts/FR-0000-functional-requirement.template.md) | How do we judge correctness? (rules + page contract) |
| 9 | [`2-contracts/SRE-0000-reliability.template.md`](./2-contracts/SRE-0000-reliability.template.md) | Is it working? (SLO + observability + capacity) |
| 10 | [`3-process/PROC-0001-developer-handbook.template.md`](./3-process/PROC-0001-developer-handbook.template.md) | How do we ship? (onboarding + workflow + review + security + BDD) |

**That's it.** A solo dev shipping an MVP can do it with these 10. Stop here if you're under 5 engineers / pre-PMF.

---

## The 10 SPECIALIZED templates (opt-in by need)

Add a specialized template the day you hit the pain it solves. Not before.

| # | File | Add when |
|---|---|---|
| 11 | [`2-contracts/EDGE-0000-edge-case-catalog.template.md`](./2-contracts/EDGE-0000-edge-case-catalog.template.md) | After your first production incident |
| 12 | [`2-contracts/DATA-0000-data-contract.template.md`](./2-contracts/DATA-0000-data-contract.template.md) | When master data / migrations / pipelines have ≥ 3 sources of truth |
| 13 | [`2-contracts/AI-0000-ai-system-contract.template.md`](./2-contracts/AI-0000-ai-system-contract.template.md) | When LLMs are core (not a feature). Includes prompt + agent + RAG + safety + capacity |
| 14 | [`3-process/PROC-0002-ops-runbook.template.md`](./3-process/PROC-0002-ops-runbook.template.md) | When you have a real on-call rotation |
| 15 | [`3-process/TEST-0000-testing-strategy.template.md`](./3-process/TEST-0000-testing-strategy.template.md) | When tests > a few notebooks; needed before LLM features |
| 16 | [`3-process/QG-0000-quality-gates.md`](./3-process/QG-0000-quality-gates.md) | When team > 5 OR multi-track parallel work |
| 17 | [`1-decisions/ADR-0000-adr.template.md`](./1-decisions/ADR-0000-adr.template.md) | When "why did we choose X?" surfaces from past decisions |
| 18 | [`4-exploration/PRD-0000-prd.template.md`](./4-exploration/PRD-0000-prd.template.md) | When PM + eng + design need a shared spec (incl. discovery + personas + experiments + launch) |
| 19 | [`4-exploration/PLAN-0000-planning.template.md`](./4-exploration/PLAN-0000-planning.template.md) | When you have a multi-quarter roadmap; before that, just a list |
| 20 | [`4-exploration/CIA-0000-change-impact-analysis.template.md`](./4-exploration/CIA-0000-change-impact-analysis.template.md) | When a single change touches ≥ 2 services / ≥ 1 contract |

---

## What v6.0 removed and why

We deleted 51 templates from v5.8. Each was good for the niche it served, but **collectively** they made onboarding take 2 days and AI overwhelmed by cross-references.

The deletion principle: a template earns its place only if **AI cannot derive its content from code + the 10 bedrock docs**. If you can grep for the answer, the template was scaffolding, not contract.

What previously had its own file, now a §section:

| v5.x file | v6.0 location |
|---|---|
| BF / UF / SF | `FLOW-0000` §1 / §2 / §3 |
| GLOS-0000 | `PRIN-0000 §terminology` |
| ARCH-0001 / 0002 / 0003 | `ARCH-0000 §modules / §stack / §infrastructure` |
| DDD-0000 | `ARCH-0000 §domain-model` |
| EST-0000 | `ARCH-0000 §capacity-estimation` |
| POL-0000 | `ARCH-0000 §security` |
| DS-0000 | `ARCH-0000 §frontend` |
| ERR-0000 / ASYNC-0000 | `API-0000` (§errors / §async) |
| SM-0000 | `MC-0000 §state-machine` + `.example.xstate.json` sibling |
| PC-0000 | `FR-0000 §page-contract` |
| MDS-0000 / MIG-0000 / PIPE-0000 / MODEL-0000 | `DATA-0000` (§master-data / §migration / §pipeline / §model-card) |
| PROMPT / AGENT / RAG / AISAFE / AICAP / LLMEVAL | `AI-0000` (§prompt / §agent / §rag / §safety / §capacity) + `TEST-0000 §llm-eval` |
| SLO / OBS / CAP | `SRE-0000` (§slo / §observability / §capacity) |
| CT-0000 / TP-0000 / EXP-0000 | `TEST-0000` (§contract / §unit / §experiment) |
| FI-0000 / TM-0000 / VIEW-* | regenerated on demand via `sunnydata-auto-regen` skill |
| PROC-0002..0008 + ONBOARD | `PROC-0001 §workflow / §bdd / §code-review / §security-review / §onboarding` |
| PROC-0005/0006/0009/0010/0011/0012 | `PROC-0002 §deploy / §gitops / §incident / §chaos / §deprecation / §docs-maintenance` |
| UE-0000 / PERS-0000 | `PRIN-0000 §unit-economics` + `PRD-0000 §personas` |
| DISC-0000 / ABT-0000 / GTM-0000 | `PRD-0000 §discovery / §experiments / §launch` |
| RM-0000 / WBS-0000 | `PLAN-0000 §roadmap / §wbs` |
| PRIN-0002 (frontend QA) | `PRIN-0000 §quality-bars §6.1-§6.5` |

Full mapping in `.claude/coordination/migration-v5-to-v6.md` (if you're upgrading from v5.x).

---

## The CI gates — separate concern, not templates

`3-process/ci-gates/CIG-0001..0010` are **enforcement workflows**, not docs. They live in the template repo so you can copy them but they're executable YAML. They survive v6.0 unchanged.

---

## Decision tree — "do I need template X?"

```
Q1: Is your task in a green-field codebase (< 5 files)?
    YES → read just PRIN-0000 and write code. Templates can wait.
    NO  → continue

Q2: Does the task touch the wire (API / queue) / data shape / module boundary?
    YES → load the relevant bedrock template (API / MC / DATA / FLOW)
    NO  → continue

Q3: Does the task involve LLMs as a core capability (not a feature)?
    YES → load AI-0000
    NO  → continue

Q4: Is there a real incident / outage / spike concern?
    YES → load SRE-0000 + PROC-0002
    NO  → continue

Q5: Is the change > 400 lines OR crosses 2 services?
    YES → load CIA-0000
    NO  → ship it.
```

If you find yourself loading > 5 templates for one task, **you are over-thinking it OR the task should be split**.

---

## Aesthetic principles (GitHub top-1% repo discipline)

- **README is THE doc**, not 60 markdowns. BEDROCK.md is the README.
- **Code is the source of truth**, docs explain WHY not WHAT.
- **Negative space matters** — what we explicitly don't build (PRIN-0000 §3) is as important as what we do.
- **Every doc earns its place** or it's deleted (this is what v5→v6 did).
- **AI is the reader as much as humans** — terse + concrete + cross-referenced beats verbose + abstract.

> "If you need more than 3 levels of indentation, you're screwed and should fix your program." — Linus

The same applies to docs.

---

## See also

- [`INDEX.md`](./INDEX.md) — full template catalog (sorted; for browsing)
- [`HOW-TO-INSTANTIATE.md`](./HOW-TO-INSTANTIATE.md) — how to copy these into YOUR project's `docs/`
- [`OWNERSHIP-MATRIX.md`](./OWNERSHIP-MATRIX.md) — who edits what (Human / Hybrid / AI-AUTO)
- `0-principles/PRIN-0003-engineering-contract-stack.md` — the 10-layer map (where every contract sits)
