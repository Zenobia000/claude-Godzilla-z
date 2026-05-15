# VibeCoding Workflow Templates

> **Version:** v5.6 — Profile-based template selection + multi-role coverage
> **Updated:** 2026-05-15
> **🚪 New here?** Start at [OWNERSHIP-MATRIX.md](./OWNERSHIP-MATRIX.md) — tells you which files demand human decisions vs which AI auto-manages.

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

## Domain Scope & Profiles

These templates are **not universal** — they're opinionated toward specific product types. The table below shows current coverage:

| Profile | Coverage | Key templates |
|---|---|---|
| 🟢 **web-product** (Full Stack) | 95% | API spec, DB schema, flows, frontend contracts, CI/CD, security |
| 🟡 **platform-infra** (DevOps / SRE) | 60% | Deployment runbook, SLO spec, incident response, chaos engineering, GitOps, infra architecture |
| 🟡 **data-ml** (Data Scientist) | 40% | Pipeline contract, model card, experiment log |
| 🟢 **full** | — | All templates |

When initializing a project with `/task-init`, choose the profile that matches your product type. Templates outside your profile can still be used — the profile just controls which ones are instantiated by default.

See the **Profile Selection Table** in [HOW-TO-INSTANTIATE.md](./HOW-TO-INSTANTIATE.md) for the full per-template breakdown.

---

## The 6 tiers

### 0-principles — *near-immutable invariants*
Mission, non-goals, quality bars, technical hard limits, naming conventions, terminology. Reviewed every 6 months, changed only on major version. AI loads this first.
- [`PRIN-0000-product-principles.template.md`](./0-principles/PRIN-0000-product-principles.template.md)
- [`PRIN-0001-flow-id-conventions.md`](./0-principles/PRIN-0001-flow-id-conventions.md) — Flow ID prefix system (9 core + 22 extended)
- [`GLOS-0000-glossary.template.md`](./0-principles/GLOS-0000-glossary.template.md) — **NEW v5.2**: business terminology source of truth (critical for ERP-class systems)
- [`PRIN-0002-frontend-quality-attributes.template.md`](./0-principles/PRIN-0002-frontend-quality-attributes.template.md) — **NEW v5.4**: frontend SLO / Core Web Vitals / A11y / responsive breakpoints (per ADR-0001)

### 1-decisions — *append-only judgments*
ADRs, architecture overviews, module charters, domain models. Once Accepted, never edited; superseded by writing a new decision.
- [`ADR-0000-adr.template.md`](./1-decisions/ADR-0000-adr.template.md)
- [`ADR-0001-frontend-template-tier-realignment.md`](./1-decisions/ADR-0001-frontend-template-tier-realignment.md) — v5.4 decision: split monolithic frontend-architecture into 6 tier-aligned files
- [`ARCH-0000-architecture-overview.template.md`](./1-decisions/ARCH-0000-architecture-overview.template.md)
- [`ARCH-0001-module-boundary.template.md`](./1-decisions/ARCH-0001-module-boundary.template.md) — **NEW v5.2**: per-module charter (owns / does NOT own / dependencies / ACL)
- [`DDD-0000-domain-model.template.md`](./1-decisions/DDD-0000-domain-model.template.md) — **NEW v5.2**: per-bounded-context DDD model (aggregates, invariants, ERD, events)
- [`ARCH-0002-frontend-tech-stack.template.md`](./1-decisions/ARCH-0002-frontend-tech-stack.template.md) — **NEW v5.4**: frontend layered tech selection + project structure (per ADR-0001)
- [`ARCH-0003-infra-architecture.template.md`](./1-decisions/ARCH-0003-infra-architecture.template.md) — **NEW v5.6**: infrastructure architecture (VPC, compute, IaC, DR) — profile: `platform-infra`

### 2-contracts — *interfaces that MUST track code*
API specs, module contracts, layered Flows, FRs, traceability. Carry frontmatter `id`, `status`, `last-synced-with`; the `sunnydata-doc-freshness` skill flags drift + lifecycle issues.
- [`API-0000-api-spec.template.md`](./2-contracts/API-0000-api-spec.template.md) — "how do systems exchange data?"
- [`MC-0000-module-contract.template.md`](./2-contracts/MC-0000-module-contract.template.md) — "what does this module promise?"
- [`BF-0000-flow-business.template.md`](./2-contracts/BF-0000-flow-business.template.md) — L1 BF; "how does it happen E2E?"
- [`UF-0000-flow-user.template.md`](./2-contracts/UF-0000-flow-user.template.md) — L2 UF; "how does this actor do it?"
- [`SF-0000-flow-sub.template.md`](./2-contracts/SF-0000-flow-sub.template.md) — L3 SF; "how does this shared step work?"
- [`FR-0000-functional-requirement.template.md`](./2-contracts/FR-0000-functional-requirement.template.md) — FR; "how do we judge correctness?"
- [`SM-0000-state-machine.template.md`](./2-contracts/SM-0000-state-machine.template.md) — per-entity state transitions (extract when ≥5 states)
- [`MDS-0000-master-data.template.md`](./2-contracts/MDS-0000-master-data.template.md) — master entity governance (critical for ERP)
- [`FI-0000-flow-index.template.md`](./2-contracts/FI-0000-flow-index.template.md) — **NEW v5.3**: project-wide Flow aggregation view (paired with `sunnydata-flow-audit` skill)
- [`TM-0000-traceability-matrix.template.md`](./2-contracts/TM-0000-traceability-matrix.template.md) — cross-layer coverage map
- [`DS-0000-frontend-design-system.template.md`](./2-contracts/DS-0000-frontend-design-system.template.md) — **NEW v5.4**: design tokens + atomic design + API client + auth + frontend security checklist (per ADR-0001)
- [`PC-0000-page-contract.template.md`](./2-contracts/PC-0000-page-contract.template.md) — **NEW v5.4**: per-page contract (route / responsibility / data / CTA / nav) (per ADR-0001)
- [`SLO-0000-slo-spec.template.md`](./2-contracts/SLO-0000-slo-spec.template.md) — **NEW v5.6**: SLO specification (SLI / error budget / burn-rate alerts / SLA mapping) — profile: `platform-infra`
- [`PIPE-0000-pipeline-contract.template.md`](./2-contracts/PIPE-0000-pipeline-contract.template.md) — **NEW v5.6**: data pipeline contract (input/output schema / DQ gates / SLA) — profile: `data-ml`
- [`MODEL-0000-model-card.template.md`](./2-contracts/MODEL-0000-model-card.template.md) — **NEW v5.6**: ML model card (intended use / metrics / bias / lineage) — profile: `data-ml`
- [`OBS-0000-observability-spec.template.md`](./2-contracts/OBS-0000-observability-spec.template.md) — **NEW v5.6**: observability specification (metrics / logs / traces / dashboards / alerting) — profile: `platform-infra`
- [`CAP-0000-capacity-planning.template.md`](./2-contracts/CAP-0000-capacity-planning.template.md) — **NEW v5.6**: capacity planning & cost management (resource model / cost allocation / scaling) — profile: `platform-infra`

### 3-process — *how we work*
Workflow guides, checklists, methodology references, runbooks, gates.
- [`PROC-0001-workflow-manual.md`](./3-process/PROC-0001-workflow-manual.md)
- [`PROC-0002-bdd-guide.md`](./3-process/PROC-0002-bdd-guide.md)
- [`PROC-0003-code-review-checklist.md`](./3-process/PROC-0003-code-review-checklist.md)
- [`PROC-0004-security-readiness-checklist.md`](./3-process/PROC-0004-security-readiness-checklist.md)
- [`PROC-0005-deployment-runbook.template.md`](./3-process/PROC-0005-deployment-runbook.template.md)
- [`PROC-0006-docs-maintenance-guide.md`](./3-process/PROC-0006-docs-maintenance-guide.md)
- [`QG-0000-quality-gates.md`](./3-process/QG-0000-quality-gates.md) — **NEW v5**: Gate 0-4 stage prerequisites
- [`TP-0000-test-plan.template.md`](./3-process/TP-0000-test-plan.template.md) — **NEW v5.1**: strategic test document
- [`PROC-0007-vendor-api-test.template.md`](./3-process/PROC-0007-vendor-api-test.template.md) — **NEW v5.1**: per-vendor test prerequisites
- [`PROC-0008-frontend-pre-merge.template.md`](./3-process/PROC-0008-frontend-pre-merge.template.md) — **NEW v5.4**: frontend test strategy + code/quality/IA checklists (per ADR-0001)
- [`PROC-0009-incident-response.template.md`](./3-process/PROC-0009-incident-response.template.md) — **NEW v5.6**: incident response (SEV1-4 / on-call / post-mortem / comms) — profile: `platform-infra`
- [`PROC-0010-chaos-engineering.template.md`](./3-process/PROC-0010-chaos-engineering.template.md) — **NEW v5.6**: chaos engineering (game day / fault injection / blast radius) — profile: `platform-infra`
- [`PROC-0011-gitops-runbook.template.md`](./3-process/PROC-0011-gitops-runbook.template.md) — **NEW v5.6**: GitOps runbook (ArgoCD/Flux / environment promotion / drift detection) — profile: `platform-infra`
- [`PROC-0012-deprecation-playbook.template.md`](./3-process/PROC-0012-deprecation-playbook.template.md) — **NEW v5.6**: deprecation & sunset playbook (compatibility windows / migration paths / data retention) — profile: `full`
- [`ONBOARD-0000-team-onboarding.template.md`](./3-process/ONBOARD-0000-team-onboarding.template.md) — **NEW v5.6**: team onboarding & knowledge transfer (Day 1-30 / offboarding / handoff) — profile: `full`

### 4-exploration — *per-task ephemeral intent*
PRDs, WBS, brainstorms, change-impact analyses. Date-stamp filenames, archive when shipped.
- [`PRD-0000-prd.template.md`](./4-exploration/PRD-0000-prd.template.md)
- [`WBS-0000-wbs.template.md`](./4-exploration/WBS-0000-wbs.template.md)
- [`CIA-0000-change-impact-analysis.template.md`](./4-exploration/CIA-0000-change-impact-analysis.template.md) — **NEW v5**: CIA (CR-NNNN) — produced by `sunnydata-change-impact-analysis` skill, mandated by `change-governance` rule
- [`EXP-0000-experiment-log.template.md`](./4-exploration/EXP-0000-experiment-log.template.md) — **NEW v5.6**: ML experiment log (hypothesis / dataset / results / reproducibility) — profile: `data-ml`
- [`DISC-0000-discovery-research.template.md`](./4-exploration/DISC-0000-discovery-research.template.md) — **NEW v5.6**: discovery & user research (hypotheses / competitive analysis / opportunity sizing) — profile: `full`

### 5-views — *derived from code; do not hand-edit*
Project structure, dependency graphs, class diagrams, frontend trees. Regenerate via `sunnydata-auto-regen` skill or language-specific tooling.
- [`VIEW-0001-project-structure.template.md`](./5-views/VIEW-0001-project-structure.template.md)
- [`VIEW-0002-file-dependencies.template.md`](./5-views/VIEW-0002-file-dependencies.template.md)
- [`VIEW-0003-class-relationships.template.md`](./5-views/VIEW-0003-class-relationships.template.md)
- [`VIEW-0004-frontend-route-map.template.md`](./5-views/VIEW-0004-frontend-route-map.template.md) — **NEW v5.4**: page tree + nav + route table + page-to-page data passing (derived from router config; per ADR-0001)

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
| Starting a project | `0-principles/PRIN-0000-product-principles.template.md` |
| Recording an architectural choice | `1-decisions/ADR-0000-adr.template.md` |
| Documenting a service boundary | `2-contracts/API-0000-api-spec.template.md` |
| Documenting a module's public surface | `2-contracts/MC-0000-module-contract.template.md` |
| Drafting a feature spec | `4-exploration/PRD-0000-prd.template.md` |
| Planning a sprint | `4-exploration/WBS-0000-wbs.template.md` |
| Adopting BDD on a new feature | `3-process/PROC-0002-bdd-guide.md` (read, don't fill) |
| Pre-launch checks | `3-process/PROC-0004-security-readiness-checklist.md` (read, don't fill) |
| Onboarding diagrams | `5-views/*` — but **regenerate**, don't write by hand |

---

## Old-numbering → new-path migration table

| v3 path | v4 path |
|---|---|
| `01_workflow_manual.md` | `3-process/PROC-0001-workflow-manual.md` |
| `02_project_brief_and_prd.md` | `4-exploration/PRD-0000-prd.template.md` |
| `03_behavior_driven_development_guide.md` | `3-process/PROC-0002-bdd-guide.md` |
| `04_architecture_decision_record_template.md` | `1-decisions/ADR-0000-adr.template.md` |
| `05_architecture_and_design_document.md` | `1-decisions/ARCH-0000-architecture-overview.template.md` |
| `06_api_design_specification.md` | `2-contracts/API-0000-api-spec.template.md` |
| `07_module_specification_and_tests.md` | `2-contracts/MC-0000-module-contract.template.md` |
| `08_project_structure_guide.md` | `5-views/VIEW-0001-project-structure.template.md` |
| `09_file_dependencies_template.md` | `5-views/VIEW-0002-file-dependencies.template.md` |
| `10_class_relationships_template.md` | `5-views/VIEW-0003-class-relationships.template.md` |
| `11_code_review_and_refactoring_guide.md` | `3-process/PROC-0003-code-review-checklist.md` |
| `12_frontend_architecture_specification.md` | **split across 0/1/2/3** (per [ADR-0001](../docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md)): `0-principles/PRIN-0002-frontend-quality-attributes`, `1-decisions/ARCH-0002-frontend-tech-stack`, `2-contracts/DS-0000-frontend-design-system`, `3-process/PROC-0008-frontend-pre-merge` |
| `13_security_and_readiness_checklists.md` | `3-process/PROC-0004-security-readiness-checklist.md` |
| `14_deployment_and_operations_guide.md` | `3-process/PROC-0005-deployment-runbook.template.md` |
| `15_documentation_and_maintenance_guide.md` | `3-process/PROC-0006-docs-maintenance-guide.md` |
| `16_wbs_development_plan_template.md` | `4-exploration/WBS-0000-wbs.template.md` |
| `17_frontend_information_architecture_template.md` | **split** (per [ADR-0001](../docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md)): `2-contracts/PC-0000-page-contract` (per-page contract), `5-views/VIEW-0004-frontend-route-map` (route/nav derive), `4-exploration/PRD-0000-prd.template.md §6` (IA principles) |
| *(new in v4)* | `0-principles/PRIN-0000-product-principles.template.md` |
| *(new in v5)* | `0-principles/PRIN-0001-flow-id-conventions.md` |
| *(new in v5)* | `2-contracts/BF-0000-flow-business.template.md` |
| *(new in v5)* | `2-contracts/UF-0000-flow-user.template.md` |
| *(new in v5)* | `2-contracts/SF-0000-flow-sub.template.md` |
| *(new in v5)* | `2-contracts/TM-0000-traceability-matrix.template.md` |
| *(new in v5)* | `3-process/QG-0000-quality-gates.md` |
| *(new in v5)* | `4-exploration/CIA-0000-change-impact-analysis.template.md` |
| *(new in v5.1)* | `2-contracts/FR-0000-functional-requirement.template.md` |
| *(new in v5.1)* | `3-process/TP-0000-test-plan.template.md` |
| *(new in v5.1)* | `3-process/PROC-0007-vendor-api-test.template.md` |
| *(new in v5.2)* | `0-principles/GLOS-0000-glossary.template.md` |
| *(new in v5.2)* | `1-decisions/ARCH-0001-module-boundary.template.md` |
| *(new in v5.2)* | `1-decisions/DDD-0000-domain-model.template.md` |
| *(new in v5.2)* | `2-contracts/SM-0000-state-machine.template.md` |
| *(new in v5.2)* | `2-contracts/MDS-0000-master-data.template.md` |
| *(new in v5.3)* | `2-contracts/FI-0000-flow-index.template.md` |
| *(new in v5.6)* | `1-decisions/ARCH-0003-infra-architecture.template.md` |
| *(new in v5.6)* | `2-contracts/SLO-0000-slo-spec.template.md` |
| *(new in v5.6)* | `2-contracts/PIPE-0000-pipeline-contract.template.md` |
| *(new in v5.6)* | `2-contracts/MODEL-0000-model-card.template.md` |
| *(new in v5.6)* | `3-process/PROC-0009-incident-response.template.md` |
| *(new in v5.6)* | `3-process/PROC-0010-chaos-engineering.template.md` |
| *(new in v5.6)* | `3-process/PROC-0011-gitops-runbook.template.md` |
| *(new in v5.6)* | `4-exploration/EXP-0000-experiment-log.template.md` |
| *(new in v5.6)* | `2-contracts/OBS-0000-observability-spec.template.md` |
| *(new in v5.6)* | `2-contracts/CAP-0000-capacity-planning.template.md` |
| *(new in v5.6)* | `3-process/PROC-0012-deprecation-playbook.template.md` |
| *(new in v5.6)* | `3-process/ONBOARD-0000-team-onboarding.template.md` |
| *(new in v5.6)* | `4-exploration/DISC-0000-discovery-research.template.md` |

A migration script for downstream forks is at `scripts/migrate-templates-v3-to-v4.sh`.

---

## Version history

| Version | Date | Change |
|---|---|---|
| v5.6 | 2026-05-15 | Profile-based template selection + lifecycle completion: Domain Scope declaration, 4 profiles (web-product / data-ml / platform-infra / full); 13 new templates — SRE (SLO, incident response, chaos engineering, observability), DevOps (infra architecture, GitOps runbook, capacity planning), Data Scientist (pipeline contract, model card, experiment log), Lifecycle (deprecation playbook, team onboarding, discovery research) |
| v5.4 | 2026-05-10 | Frontend template tier realignment (ADR-0001 / CR-0001): split `5-views/frontend-architecture` and `5-views/frontend-information-architecture` into 6 properly-tiered templates (0/1/2/3/5) + integrated IA principles into `PRD-0000-prd.template.md §6` |
| v5.3 | 2026-05-10 | Flow self-monitoring: project-wide flow-index aggregation template; sunnydata-flow-audit skill detecting broken refs / orphans / layering violations / stale flows / index drift |
| v5.2 | 2026-05-10 | ERP-class foundation: Glossary (terminology source of truth); Module Boundary charter (per-module owns/NOT-owns); Domain Model (DDD aggregates + ERD + invariants); State Machine (extracted when complex); Master Data Specification (governance for long-lived shared entities) |
| v5.1 | 2026-05-10 | "One doc, one question" enforcement: standalone Functional Requirement template (decouple FR from Flow); Test Plan strategic template; Vendor API Test Requirement template |
| v5.0 | 2026-05-10 | Change Governance: Flow ID system (BF/UF/SF/FR/NFR/API/TC/ADR/CR), layered Flow templates, Traceability Matrix, Quality Gates, CIA template & skill, change-governance hard-gate rule, lifecycle frontmatter (status/supersedes) |
| v4.0 | 2026-05-10 | Stability-tier layout; added 0-principles; .template.md naming; sync metadata for tier 2 |
| v3.0 | 2026-03-16 | Phase-based numbering, removed cookbook, unified zh-TW |
| v2.1 | 2025-10-03 | Added 17 (frontend IA) |
| v2.0 | 2025-10-03 | Reorganized numbering, added INDEX |
| v1.0 | 2025-10-01 | Initial release |
