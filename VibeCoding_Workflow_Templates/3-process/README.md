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
- About to write a new feature? → load `PROC-0002-bdd-guide.md` and `PROC-0003-code-review-checklist.md`
- About to deploy? → load `PROC-0005-deployment-runbook.template.md` and `PROC-0004-security-readiness-checklist.md`
- About to write tests? → load `PROC-0002-bdd-guide.md`

These documents constrain *how* AI executes — they don't dictate the architecture (that's tier 0/1).

## How humans should maintain this tier

- Review every 6 months
- When a checklist item produces zero hits across 3 reviews, consider deleting it (it's not catching anything)
- When the same incident type recurs twice, add a check that would have caught it

## Files

| File | Purpose | Type |
|---|---|---|
| `PROC-0001-workflow-manual.md` | How to choose between full-process and MVP-mode workflows | Guide |
| `PROC-0002-bdd-guide.md` | Gherkin scenarios, step definition patterns | Guide |
| `PROC-0003-code-review-checklist.md` | Reviewer-side and author-side checklists | Checklist |
| `PROC-0004-security-readiness-checklist.md` | Pre-launch security gates | Checklist |
| `PROC-0005-deployment-runbook.template.md` | Per-service deployment + rollback steps | Template |
| `PROC-0006-docs-maintenance-guide.md` | When to write/update/delete documentation | Guide |
| `QG-0000-quality-gates.md` | Gate 0-4 stage prerequisites (requirements / FE buildable / BE parallelizable / DB / tests) | Guide |
| `TP-0000-test-plan.template.md` | **Strategic** test document (quality targets, test pyramid, stages, data strategy, CI gate spec, risk register) | Template |
| `PROC-0007-vendor-api-test.template.md` | Per-vendor test prerequisites (sandbox / contract / scenarios / fallback) | Template |
| `PROC-0008-frontend-pre-merge.template.md` | Frontend pre-merge quality gate checklist | Checklist |
| `PROC-0009-incident-response.template.md` | Incident response — SEV1-4 definitions, on-call, post-mortem, comms | Runbook |
| `PROC-0010-chaos-engineering.template.md` | Chaos engineering — game day plan, fault injection, blast radius | Guide |
| `PROC-0011-gitops-runbook.template.md` | GitOps — ArgoCD/Flux, environment promotion, drift detection | Runbook |
| `PROC-0012-deprecation-playbook.template.md` | Deprecation & sunset — compatibility windows, migration paths, data retention | Playbook |
| `ONBOARD-0000-team-onboarding.template.md` | Team onboarding & offboarding — Day 1-30, mentorship, knowledge transfer | Runbook |

## Frontmatter Schema

All files in this tier MUST carry this frontmatter:

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | YES | string | `PROC-NNNN`, `QG-NNNN`, `TP-NNNN`, or `ONBOARD-NNNN` |
| `title` | YES | string | Human-readable title |
| `status` | YES | enum | `draft` / `active` / `deprecated` / `superseded` |
| `tier` | YES | const | `3-process` |
| `owner` | YES | enum | `HUMAN-ONLY` / `HYBRID` / `AI-AUTO` |
| `last-reviewed` | YES | date | `YYYY-MM-DD` |
| `product-version` | opt | string | Product version this doc applies to |
| `supersedes` | opt | string | ID of predecessor |
| `superseded-by` | opt | string | ID of successor |
