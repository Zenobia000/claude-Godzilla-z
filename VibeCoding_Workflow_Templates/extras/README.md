# Extras — Domain-specific template add-ons

> The core templates in `0-principles/` ~ `5-views/` are **domain-neutral**: they work for any software project (web, CLI, library, ERP, ML, embedded, etc.). Templates in `extras/` are **domain-opinionated** — useful only when your project matches that domain.

## Why segregated

After v5.x development, an audit found that 6 frontend-specific templates were sitting in core tier directories alongside neutral ones. This created two problems:

1. Non-web projects (CLI tools, libraries, embedded firmware) saw irrelevant templates in their template catalog
2. Web projects had no clear signal that those 6 templates were "the web bundle" — they were just scattered across tiers

Moving them to `extras/web-frontend/` solves both: web projects can opt in by reading the `web-frontend/` directory; non-web projects can ignore it entirely.

## Available extras

| Subdirectory | When to use | Contents |
|---|---|---|
| `web-frontend/` | Web/SaaS frontend projects | 6 templates covering quality attributes, tech stack, design system, page contract, pre-merge checklist, route map |

## Future extras (not yet present)

If your project belongs to a domain not covered above, the core templates still apply — but you may need to write your own domain-specific template set. Candidate future extras:

- `mobile/` — iOS / Android specific (App Store contracts, native module governance)
- `ml/` — ML model lifecycle, experiment tracking, dataset governance
- `embedded/` — firmware (memory budgets, real-time constraints, safety)
- `data-pipeline/` — ETL, dataset versioning, lineage
- `cli/` — command-line tools (UX guidelines, distribution)
- `library-sdk/` — public API surface, semver, deprecation policy

These don't exist today. If you build one, contribute back.

## Adoption rule

Use the extras for **your** domain. Ignore the rest. Don't try to fit a CLI tool into web-frontend templates — that's slop.
