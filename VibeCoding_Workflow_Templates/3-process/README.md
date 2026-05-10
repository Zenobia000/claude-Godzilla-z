# Tier 3 — Process

> Half-yearly stable. How we work, not what we build.

## What lives here

- Workflow guides (how features move from idea to production)
- Checklists (code review, security, deployment readiness)
- Methodology references (BDD, TDD, code review style)
- Operational runbooks (deployment, rollback, incident response)

## What does NOT live here

- The product we're building → tier 0 (principles) or tier 4 (exploration)
- The contracts the product exposes → tier 2 (contracts)
- Decision *records* about process → tier 1 (decisions)

## How AI should use this tier

**Read the relevant process file before starting a category of work**:
- About to write a new feature? → load `bdd-guide.md` and `code-review-checklist.md`
- About to deploy? → load `deployment-runbook.template.md` and `security-readiness-checklist.md`
- About to write tests? → load `bdd-guide.md`

These documents constrain *how* AI executes — they don't dictate the architecture (that's tier 0/1).

## How humans should maintain this tier

- Review every 6 months
- When a checklist item produces zero hits across 3 reviews, consider deleting it (it's not catching anything)
- When the same incident type recurs twice, add a check that would have caught it

## Files

| File | Purpose | Type |
|---|---|---|
| `workflow-manual.md` | How to choose between full-process and MVP-mode workflows | Guide |
| `bdd-guide.md` | Gherkin scenarios, step definition patterns | Guide |
| `code-review-checklist.md` | Reviewer-side and author-side checklists | Checklist |
| `security-readiness-checklist.md` | Pre-launch security gates | Checklist |
| `deployment-runbook.template.md` | Per-service deployment + rollback steps | Template |
| `docs-maintenance-guide.md` | When to write/update/delete documentation | Guide |
| `quality-gates.md` | Gate 0-4 stage prerequisites (requirements / FE buildable / BE parallelizable / DB / tests) | Guide |
| `test-plan.template.md` | **Strategic** test document (quality targets, test pyramid, stages, data strategy, CI gate spec, risk register) | Template |
| `vendor-api-test-requirement.template.md` | Per-vendor test prerequisites (sandbox / contract / scenarios / fallback) | Template |
