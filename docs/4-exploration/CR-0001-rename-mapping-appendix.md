# CR-0001 Rename Mapping

## Prefix 體系

### 現有前綴（保留）
BF, UF, SF, FR, API, SM, TC, ADR, CR

### 新增前綴
| Prefix | Category | Tier |
|---|---|---|
| PRIN | Principles | 0 |
| GLOS | Glossary | 0 |
| ARCH | Architecture docs | 1 |
| DDD | Domain model | 1 |
| MC | Module Contract | 2 |
| MDS | Master Data Spec | 2 |
| FI | Flow Index | 2 |
| TM | Traceability Matrix | 2 |
| DS | Design System | 2 |
| PC | Page Contract | 2 |
| PROC | Process guide | 3 |
| QG | Quality Gates | 3 |
| TP | Test Plan | 3 |
| PRD | Product Requirements | 4 |
| WBS | Work Breakdown | 4 |
| CIA | Change Impact Analysis | 4 |
| VIEW | Code-derived view | 5 |

## 完整映射

### Tier 0 — 0-principles/
| Old | New |
|---|---|
| `product-principles.template.md` | `PRIN-0000-product-principles.template.md` |
| `flow-id-conventions.md` | `PRIN-0001-flow-id-conventions.md` |
| `glossary.template.md` | `GLOS-0000-glossary.template.md` |
| `frontend-quality-attributes.template.md` | `PRIN-0002-frontend-quality-attributes.template.md` |

### Tier 1 — 1-decisions/
| Old | New |
|---|---|
| `adr.template.md` | `ADR-0000-adr.template.md` |
| `architecture-overview.template.md` | `ARCH-0000-architecture-overview.template.md` |
| `module-boundary.template.md` | `ARCH-0001-module-boundary.template.md` |
| `domain-model.template.md` | `DDD-0000-domain-model.template.md` |
| `frontend-tech-stack.template.md` | `ARCH-0002-frontend-tech-stack.template.md` |

### Tier 2 — 2-contracts/
| Old | New |
|---|---|
| `flow-business.template.md` | `BF-0000-flow-business.template.md` |
| `flow-user.template.md` | `UF-0000-flow-user.template.md` |
| `flow-sub.template.md` | `SF-0000-flow-sub.template.md` |
| `flow-index.template.md` | `FI-0000-flow-index.template.md` |
| `functional-requirement.template.md` | `FR-0000-functional-requirement.template.md` |
| `api-spec.template.md` | `API-0000-api-spec.template.md` |
| `module-contract.template.md` | `MC-0000-module-contract.template.md` |
| `state-machine.template.md` | `SM-0000-state-machine.template.md` |
| `master-data-specification.template.md` | `MDS-0000-master-data.template.md` |
| `traceability-matrix.template.md` | `TM-0000-traceability-matrix.template.md` |
| `frontend-design-system.template.md` | `DS-0000-frontend-design-system.template.md` |
| `page-contract.template.md` | `PC-0000-page-contract.template.md` |

### Tier 3 — 3-process/
| Old | New |
|---|---|
| `workflow-manual.md` | `PROC-0001-workflow-manual.md` |
| `bdd-guide.md` | `PROC-0002-bdd-guide.md` |
| `code-review-checklist.md` | `PROC-0003-code-review-checklist.md` |
| `security-readiness-checklist.md` | `PROC-0004-security-readiness-checklist.md` |
| `deployment-runbook.template.md` | `PROC-0005-deployment-runbook.template.md` |
| `docs-maintenance-guide.md` | `PROC-0006-docs-maintenance-guide.md` |
| `quality-gates.md` | `QG-0000-quality-gates.md` |
| `test-plan.template.md` | `TP-0000-test-plan.template.md` |
| `vendor-api-test-requirement.template.md` | `PROC-0007-vendor-api-test.template.md` |
| `frontend-pre-merge-checklist.template.md` | `PROC-0008-frontend-pre-merge.template.md` |

### Tier 4 — 4-exploration/
| Old | New |
|---|---|
| `prd.template.md` | `PRD-0000-prd.template.md` |
| `wbs.template.md` | `WBS-0000-wbs.template.md` |
| `change-impact-analysis.template.md` | `CIA-0000-change-impact-analysis.template.md` |

### Tier 5 — 5-views/
| Old | New |
|---|---|
| `project-structure.template.md` | `VIEW-0001-project-structure.template.md` |
| `file-dependencies.template.md` | `VIEW-0002-file-dependencies.template.md` |
| `class-relationships.template.md` | `VIEW-0003-class-relationships.template.md` |
| `frontend-route-map.template.md` | `VIEW-0004-frontend-route-map.template.md` |

## 命名規則

- `.template.md` 檔案用 `0000` 序號 = 此為模板本身
- 非模板 guide/process 用 `0001` 起的序號 = 唯一識別碼
- 單一前綴的檔案（BF, UF, API 等）用 `0000`
- 共享前綴的檔案（PROC, VIEW, ARCH 等）用遞增序號
