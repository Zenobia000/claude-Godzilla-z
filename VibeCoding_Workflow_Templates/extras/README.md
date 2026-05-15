# Extras — Domain-specific template add-ons (placeholder)

> The core templates in `0-principles/` ~ `5-views/` are **domain-neutral**: they work for any software project (web, CLI, library, ERP, ML, embedded, etc.). This directory is reserved for future **domain-opinionated** add-ons.

## History

The 6 frontend-specific templates that were originally placed in `extras/web-frontend/` have been **moved to their proper tier directories** per ADR-0001 (v5.4):

| File | Moved to |
|---|---|
| `PRIN-0002-frontend-quality-attributes.template.md` | `0-principles/` |
| `ARCH-0002-frontend-tech-stack.template.md` | `1-decisions/` |
| `DS-0000-frontend-design-system.template.md` | `2-contracts/` |
| `PC-0000-page-contract.template.md` | `2-contracts/` |
| `PROC-0008-frontend-pre-merge.template.md` | `3-process/` |
| `VIEW-0004-frontend-route-map.template.md` | `5-views/` |

## Future extras (not yet present)

If your project belongs to a domain not covered by core templates, you may need domain-specific add-ons. Candidate future extras:

- `mobile/` — iOS / Android specific (App Store contracts, native module governance)
- `ml/` — ML model lifecycle, experiment tracking, dataset governance
- `embedded/` — firmware (memory budgets, real-time constraints, safety)
- `data-pipeline/` — ETL, dataset versioning, lineage
- `cli/` — command-line tools (UX guidelines, distribution)
- `library-sdk/` — public API surface, semver, deprecation policy

These don't exist today. If you build one, contribute back.
