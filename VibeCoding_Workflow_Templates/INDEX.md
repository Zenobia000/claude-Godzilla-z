# VibeCoding Workflow Templates

> **Version:** v4.0 — Stability-tier layout
> **Updated:** 2026-05-10
> **Migration from v3:** see [LEGACY-INDEX.md](./LEGACY-INDEX.md)

---

## Why this layout

Templates are organized by **stability tier**, not by workflow phase. The path prefix (`0-`, `1-`, ..., `5-`) tells you and your AI **how often this kind of doc changes** — which is the metadata that matters most when deciding whether to trust a doc as ground truth.

Lower number = more stable. Higher number = changes more often.

```
0-principles  ←  read first, trust most
1-decisions
2-contracts
3-process
4-exploration
5-views        ←  read last, trust least (regenerate from code)
```

See [HOW-TO-INSTANTIATE.md](./HOW-TO-INSTANTIATE.md) for how to use these templates inside your own project.

---

## The 6 tiers

### 0-principles — *near-immutable invariants*
Mission, non-goals, quality bars, technical hard limits, naming conventions, terminology. Reviewed every 6 months, changed only on major version. AI loads this first.
- [`product-principles.template.md`](./0-principles/product-principles.template.md)
- [`flow-id-conventions.md`](./0-principles/flow-id-conventions.md) — Flow ID 9-prefix system
- [`glossary.template.md`](./0-principles/glossary.template.md) — **NEW v5.2**: business terminology source of truth (critical for ERP-class systems)

### 1-decisions — *append-only judgments*
ADRs, architecture overviews, module charters, domain models. Once Accepted, never edited; superseded by writing a new decision.
- [`adr.template.md`](./1-decisions/adr.template.md)
- [`architecture-overview.template.md`](./1-decisions/architecture-overview.template.md)
- [`module-boundary.template.md`](./1-decisions/module-boundary.template.md) — **NEW v5.2**: per-module charter (owns / does NOT own / dependencies / ACL)
- [`domain-model.template.md`](./1-decisions/domain-model.template.md) — **NEW v5.2**: per-bounded-context DDD model (aggregates, invariants, ERD, events)

### 2-contracts — *interfaces that MUST track code*
API specs, module contracts, layered Flows, FRs, traceability. Carry frontmatter `id`, `status`, `last-synced-with`; the `sunnydata-doc-freshness` skill flags drift + lifecycle issues.
- [`api-spec.template.md`](./2-contracts/api-spec.template.md) — "how do systems exchange data?"
- [`module-contract.template.md`](./2-contracts/module-contract.template.md) — "what does this module promise?"
- [`flow-business.template.md`](./2-contracts/flow-business.template.md) — L1 BF; "how does it happen E2E?"
- [`flow-user.template.md`](./2-contracts/flow-user.template.md) — L2 UF; "how does this actor do it?"
- [`flow-sub.template.md`](./2-contracts/flow-sub.template.md) — L3 SF; "how does this shared step work?"
- [`functional-requirement.template.md`](./2-contracts/functional-requirement.template.md) — FR; "how do we judge correctness?"
- [`state-machine.template.md`](./2-contracts/state-machine.template.md) — per-entity state transitions (extract when ≥5 states)
- [`master-data-specification.template.md`](./2-contracts/master-data-specification.template.md) — master entity governance (critical for ERP)
- [`flow-index.template.md`](./2-contracts/flow-index.template.md) — **NEW v5.3**: project-wide Flow aggregation view (paired with `sunnydata-flow-audit` skill)
- [`traceability-matrix.template.md`](./2-contracts/traceability-matrix.template.md) — cross-layer coverage map

### 3-process — *how we work*
Workflow guides, checklists, methodology references, runbooks, gates.
- [`workflow-manual.md`](./3-process/workflow-manual.md)
- [`bdd-guide.md`](./3-process/bdd-guide.md)
- [`code-review-checklist.md`](./3-process/code-review-checklist.md)
- [`security-readiness-checklist.md`](./3-process/security-readiness-checklist.md)
- [`deployment-runbook.template.md`](./3-process/deployment-runbook.template.md)
- [`docs-maintenance-guide.md`](./3-process/docs-maintenance-guide.md)
- [`quality-gates.md`](./3-process/quality-gates.md) — **NEW v5**: Gate 0-4 stage prerequisites
- [`test-plan.template.md`](./3-process/test-plan.template.md) — **NEW v5.1**: strategic test document
- [`vendor-api-test-requirement.template.md`](./3-process/vendor-api-test-requirement.template.md) — **NEW v5.1**: per-vendor test prerequisites

### 4-exploration — *per-task ephemeral intent*
PRDs, WBS, brainstorms, change-impact analyses. Date-stamp filenames, archive when shipped.
- [`prd.template.md`](./4-exploration/prd.template.md)
- [`wbs.template.md`](./4-exploration/wbs.template.md)
- [`change-impact-analysis.template.md`](./4-exploration/change-impact-analysis.template.md) — **NEW v5**: CIA (CR-NNNN) — produced by `sunnydata-change-impact-analysis` skill, mandated by `change-governance` rule

### 5-views — *derived from code; do not hand-edit*
Project structure, dependency graphs, class diagrams, frontend trees. Regenerate via `/regenerate-views` skill or language-specific tooling.
- [`project-structure.template.md`](./5-views/project-structure.template.md)
- [`file-dependencies.template.md`](./5-views/file-dependencies.template.md)
- [`class-relationships.template.md`](./5-views/class-relationships.template.md)
- [`frontend-architecture.template.md`](./5-views/frontend-architecture.template.md)
- [`frontend-information-architecture.template.md`](./5-views/frontend-information-architecture.template.md)

---

## How AI should consume these templates

| Tier | When to load | How to treat the content |
|---|---|---|
| 0-principles | Every new conversation | Hard constraint — overrides downstream |
| 1-decisions | Before proposing architecture | Honor or escalate; never silently contradict |
| 2-contracts | When touching public interfaces | Check `last-synced-with` first |
| 3-process | Before category of work (review, deploy, test) | Follow the checklist |
| 4-exploration | For motivation context | Don't assume current behavior |
| 5-views | Almost never directly | Read the code, then optionally compare |

---

## How humans should pick a template to fill

| You're doing… | Reach for… |
|---|---|
| Starting a project | `0-principles/product-principles.template.md` |
| Recording an architectural choice | `1-decisions/adr.template.md` |
| Documenting a service boundary | `2-contracts/api-spec.template.md` |
| Documenting a module's public surface | `2-contracts/module-contract.template.md` |
| Drafting a feature spec | `4-exploration/prd.template.md` |
| Planning a sprint | `4-exploration/wbs.template.md` |
| Adopting BDD on a new feature | `3-process/bdd-guide.md` (read, don't fill) |
| Pre-launch checks | `3-process/security-readiness-checklist.md` (read, don't fill) |
| Onboarding diagrams | `5-views/*` — but **regenerate**, don't write by hand |

---

## Old-numbering → new-path migration table

| v3 path | v4 path |
|---|---|
| `01_workflow_manual.md` | `3-process/workflow-manual.md` |
| `02_project_brief_and_prd.md` | `4-exploration/prd.template.md` |
| `03_behavior_driven_development_guide.md` | `3-process/bdd-guide.md` |
| `04_architecture_decision_record_template.md` | `1-decisions/adr.template.md` |
| `05_architecture_and_design_document.md` | `1-decisions/architecture-overview.template.md` |
| `06_api_design_specification.md` | `2-contracts/api-spec.template.md` |
| `07_module_specification_and_tests.md` | `2-contracts/module-contract.template.md` |
| `08_project_structure_guide.md` | `5-views/project-structure.template.md` |
| `09_file_dependencies_template.md` | `5-views/file-dependencies.template.md` |
| `10_class_relationships_template.md` | `5-views/class-relationships.template.md` |
| `11_code_review_and_refactoring_guide.md` | `3-process/code-review-checklist.md` |
| `12_frontend_architecture_specification.md` | `5-views/frontend-architecture.template.md` |
| `13_security_and_readiness_checklists.md` | `3-process/security-readiness-checklist.md` |
| `14_deployment_and_operations_guide.md` | `3-process/deployment-runbook.template.md` |
| `15_documentation_and_maintenance_guide.md` | `3-process/docs-maintenance-guide.md` |
| `16_wbs_development_plan_template.md` | `4-exploration/wbs.template.md` |
| `17_frontend_information_architecture_template.md` | `5-views/frontend-information-architecture.template.md` |
| *(new in v4)* | `0-principles/product-principles.template.md` |
| *(new in v5)* | `0-principles/flow-id-conventions.md` |
| *(new in v5)* | `2-contracts/flow-business.template.md` |
| *(new in v5)* | `2-contracts/flow-user.template.md` |
| *(new in v5)* | `2-contracts/flow-sub.template.md` |
| *(new in v5)* | `2-contracts/traceability-matrix.template.md` |
| *(new in v5)* | `3-process/quality-gates.md` |
| *(new in v5)* | `4-exploration/change-impact-analysis.template.md` |
| *(new in v5.1)* | `2-contracts/functional-requirement.template.md` |
| *(new in v5.1)* | `3-process/test-plan.template.md` |
| *(new in v5.1)* | `3-process/vendor-api-test-requirement.template.md` |
| *(new in v5.2)* | `0-principles/glossary.template.md` |
| *(new in v5.2)* | `1-decisions/module-boundary.template.md` |
| *(new in v5.2)* | `1-decisions/domain-model.template.md` |
| *(new in v5.2)* | `2-contracts/state-machine.template.md` |
| *(new in v5.2)* | `2-contracts/master-data-specification.template.md` |
| *(new in v5.3)* | `2-contracts/flow-index.template.md` |

A migration script for downstream forks is at `scripts/migrate-templates-v3-to-v4.sh`.

---

## Version history

| Version | Date | Change |
|---|---|---|
| v5.2 | 2026-05-10 | ERP-class foundation: Glossary (terminology source of truth); Module Boundary charter (per-module owns/NOT-owns); Domain Model (DDD aggregates + ERD + invariants); State Machine (extracted when complex); Master Data Specification (governance for long-lived shared entities) |
| v5.1 | 2026-05-10 | "One doc, one question" enforcement: standalone Functional Requirement template (decouple FR from Flow); Test Plan strategic template; Vendor API Test Requirement template |
| v5.0 | 2026-05-10 | Change Governance: Flow ID system (BF/UF/SF/FR/NFR/API/TC/ADR/CR), layered Flow templates, Traceability Matrix, Quality Gates, CIA template & skill, change-governance hard-gate rule, lifecycle frontmatter (status/supersedes) |
| v4.0 | 2026-05-10 | Stability-tier layout; added 0-principles; .template.md naming; sync metadata for tier 2 |
| v3.0 | 2026-03-16 | Phase-based numbering, removed cookbook, unified zh-TW |
| v2.1 | 2025-10-03 | Added 17 (frontend IA) |
| v2.0 | 2025-10-03 | Reorganized numbering, added INDEX |
| v1.0 | 2025-10-01 | Initial release |
