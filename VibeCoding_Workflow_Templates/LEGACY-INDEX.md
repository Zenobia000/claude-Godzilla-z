# LEGACY INDEX (v3 phase-based view)

> **DEPRECATED:** This index is provided for downstream compatibility only.
> **Will be removed in v5** (target: 2026-Q4).
> **Use instead:** [INDEX.md](./INDEX.md)

---

If you previously used VibeCoding templates with the phase-based numbering (01-17), this file maps those phases to the new stability-tier paths.

## Phase 0: Overview & Workflow

| Phase | Old name | New path |
|---|---|---|
| 01 | workflow_manual | [`3-process/workflow-manual.md`](./3-process/workflow-manual.md) |

## Phase 1: Planning

| Phase | Old name | New path |
|---|---|---|
| 02 | project_brief_and_prd | [`4-exploration/prd.template.md`](./4-exploration/prd.template.md) |
| 03 | behavior_driven_development_guide | [`3-process/bdd-guide.md`](./3-process/bdd-guide.md) |

## Phase 2: Architecture & Design

| Phase | Old name | New path |
|---|---|---|
| 04 | architecture_decision_record | [`1-decisions/adr.template.md`](./1-decisions/adr.template.md) |
| 05 | architecture_and_design_document | [`1-decisions/architecture-overview.template.md`](./1-decisions/architecture-overview.template.md) |
| 06 | api_design_specification | [`2-contracts/api-spec.template.md`](./2-contracts/api-spec.template.md) |

## Phase 3: Detailed Design

| Phase | Old name | New path |
|---|---|---|
| 07 | module_specification_and_tests | [`2-contracts/module-contract.template.md`](./2-contracts/module-contract.template.md) |
| 08 | project_structure_guide | [`5-views/project-structure.template.md`](./5-views/project-structure.template.md) |
| 09 | file_dependencies | [`5-views/file-dependencies.template.md`](./5-views/file-dependencies.template.md) |
| 10 | class_relationships | [`5-views/class-relationships.template.md`](./5-views/class-relationships.template.md) |

## Phase 4: Development & Quality

| Phase | Old name | New path |
|---|---|---|
| 11 | code_review_and_refactoring | [`3-process/code-review-checklist.md`](./3-process/code-review-checklist.md) |
| 12 | frontend_architecture_specification | **split** per [ADR-0001](../docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md): `0-principles/frontend-quality-attributes` + `1-decisions/frontend-tech-stack` + `2-contracts/frontend-design-system` + `3-process/frontend-pre-merge-checklist` |
| 17 | frontend_information_architecture | **split** per [ADR-0001](../docs/1-decisions/ADR-0001-frontend-template-tier-realignment.md): `2-contracts/page-contract` + `5-views/frontend-route-map` + `4-exploration/prd.template.md §6` |

## Phase 5: Security & Deployment

| Phase | Old name | New path |
|---|---|---|
| 13 | security_and_readiness_checklists | [`3-process/security-readiness-checklist.md`](./3-process/security-readiness-checklist.md) |
| 14 | deployment_and_operations_guide | [`3-process/deployment-runbook.template.md`](./3-process/deployment-runbook.template.md) |

## Phase 6: Maintenance & Management

| Phase | Old name | New path |
|---|---|---|
| 15 | documentation_and_maintenance | [`3-process/docs-maintenance-guide.md`](./3-process/docs-maintenance-guide.md) |
| 16 | wbs_development_plan | [`4-exploration/wbs.template.md`](./4-exploration/wbs.template.md) |

---

## Why the change?

Phase-based numbering encoded *order of production* but hid *update frequency*. The new tiers encode update frequency in the path itself, which is the metadata that matters most when AI is deciding how much to trust each doc.

Read the rationale in the v4 [INDEX.md](./INDEX.md) header, or in the project root `README.md`.
