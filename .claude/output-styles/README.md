# Output Styles

> **See `.claude/rules/primitive-selection.md` for the full command vs skill vs output-style decision rule.**
>
> **As of v4 (2026-05-10):** 14 of the original 15 output-styles were converted into Skills. Only true behavioral modes remain here.

## Why the change

Output styles in Claude Code's harness **replace the system prompt** for the entire session — they're meant for switching the AI's persona/voice (e.g., "explain visually" mode, "Socratic tutor" mode), not for one-off task templates.

The original `01-prd-product-spec` through `14-ci-quality-gates` were really **task templates** that should activate when the user requests them, not stay active for the whole session. Forcing them through `output-style` meant constantly switching modes mid-conversation.

In v4 they live as Skills under `.claude/skills/vibecoding-*/` — the Skill tool loads the right one on demand without changing your session mode.

## What remains

| File | Purpose |
|---|---|
| `Vision-output.md` | Genuine output mode: forces visualization-first responses (diagrams, comparisons, tables) instead of code |
| `Apprentice-output.md` | Cognitive Apprenticeship mode: every code change includes decision chains, tradeoff reasoning, and decision previews so engineers learn alongside AI |

Activate with `/output-style Vision-output` or `/output-style Apprentice-output`.

## Migration map (old output-style → new skill)

| Old `/output-style` | New Skill | Triggers on |
|---|---|---|
| `01-prd-product-spec` | `vibecoding-write-prd` | "write PRD", "draft product spec" |
| `02-bdd-scenario-spec` | `vibecoding-write-bdd` | "write BDD", "Gherkin scenarios" |
| `03-architecture-design-doc` | `vibecoding-write-architecture` | "design architecture", "C4 diagram" |
| `04-ddd-aggregate-spec` | `vibecoding-write-ddd-aggregate` | "DDD aggregate", "bounded context" |
| `05-api-contract-spec` | `vibecoding-write-api-contract` | "API contract", "OpenAPI spec" |
| `06-tdd-unit-spec` | `vibecoding-write-tdd` | "TDD spec", "unit test design" |
| `07-code-review-checklist` | `vibecoding-code-review` | "review code", "PR review" |
| `08-security-checklist` | `vibecoding-security-check` | "security check", "OWASP review" |
| `09-database-schema-spec` | `vibecoding-write-db-schema` | "database schema", "DB design" |
| `10-backend-python-impl` | `vibecoding-impl-backend-py` | "implement backend Python" |
| `11-frontend-component-bdd` | `vibecoding-write-frontend-bdd` | "frontend BDD" |
| `12-integration-contract-suite` | `vibecoding-write-integration-tests` | "integration tests" |
| `13-data-contract-evolution` | `vibecoding-data-contract-evolution` | "schema migration plan" |
| `14-ci-quality-gates` | `vibecoding-ci-quality-gates` | "CI quality gates", "pipeline design" |

Each new Skill carries `template-ref:` frontmatter pointing to the canonical template under `VibeCoding_Workflow_Templates/<tier>/`.

## Adding a new output style

Only add a new file here if the user wants a **persistent voice/format change** for the whole session. If you find yourself writing one that says "produce X structured doc", it should be a Skill, not an output style.

Reference: `Vision-output.md` is the model for how an output style is shaped.
