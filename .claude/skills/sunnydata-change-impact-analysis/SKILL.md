---
name: sunnydata-change-impact-analysis
description: Produce a Change Impact Analysis (CIA) before AI mutates code that touches user flow, API contract, domain model, DB schema, external integration, test plan, or architecture boundary. Triggers on 'change request', 'modify API', 'update flow', 'add field to', 'remove endpoint', '需求變更', '修改流程', 'CR-', 'before changing X', 'I want to add/remove/modify <feature>'. This skill is enforced by .claude/rules/change-governance.md.
stability-tier: tooling
---

# Change Impact Analysis (CIA)

## What this skill does

Produces a written analysis that maps a proposed change to every artifact it touches — Flow IDs, Spec IDs, API IDs, Data entities, Test IDs, plus the human decisions the change requires. Output is a Markdown table that the user reviews and approves *before* AI starts modifying code.

This skill is the **hard gate** mandated by `.claude/rules/change-governance.md`.

## When this skill MUST be invoked

Before AI implements code changes that touch any of these surfaces:

1. **User flow / Business flow** (BF / UF / SF)
2. **API contract** (new endpoint, deleted endpoint, schema change, error-code change)
3. **Domain model** (new entity, new relation, changed invariant)
4. **DB schema** (new table, column, index, migration)
5. **External integration** (new vendor, callback rule change, retry policy change)
6. **Test plan** (structural change to coverage targets, new test category)
7. **Architecture boundary** (new module, new service, new bounded context)

**Exempted** from CIA: pure typo fixes, comment changes, log message wording, formatting that carries no semantic shift.

## When this skill is NOT needed

- Pure refactor with no observable behavior change AND no contract change
- Adding tests without changing source under test
- Documentation-only edits to tier-3 process guides
- Bug fix where the bug is clearly inside one function with no contract impact

For these, prefer `sunnydata-design` skill or just write the code.

## Procedure

### Step 1: Re-state the change

Write one sentence in the form:
> "**As-is**: <current behavior>. **To-be**: <new behavior>. **Driver**: <what prompted this — incident, customer request, compliance, etc.>"

If you can't write this in one sentence, the change isn't well-defined yet — stop and clarify with the user.

### Step 2: Allocate a CR ID

1. Scan `docs/4-exploration/` for the highest existing `CR-NNNN-*.md` filename
2. Allocate next sequential 4-digit number
3. Reserve filename: `CR-NNNN-<short-kebab>.md`

### Step 3: Identify affected artifacts

For each surface in scope, search and list. Use the project's Flow IDs (see `VibeCoding_Workflow_Templates/0-principles/PRIN-0001-flow-id-conventions.md`):

```bash
# Find existing flows the change might touch
grep -l "<keyword>" docs/2-contracts/flow-*.md
grep -l "<keyword>" docs/2-contracts/api/openapi.yaml
grep -l "<keyword>" docs/2-contracts/module-contract.*.md

# Find SLO / pipeline / model contracts that may be affected
grep -l "<keyword>" docs/2-contracts/slo-*.md docs/2-contracts/pipeline-*.md docs/2-contracts/model-*.md 2>/dev/null

# Find tests already targeting affected behavior
grep -rln "<keyword>" tests/
```

### Step 4: Fill the CIA template

Open `VibeCoding_Workflow_Templates/4-exploration/CIA-0000-change-impact-analysis.template.md` as the structure. Write the result to `docs/4-exploration/CR-NNNN-<short-kebab>.md`.

Required sections (in order):
1. **Change statement** (the one-sentence as-is/to-be/driver from Step 1)
2. **Affected Flow** (BF / UF / SF list with Modified/New/Deleted)
3. **Affected Spec** (FR / NFR list)
4. **Affected API** (per-endpoint with breaking-change flag)
5. **Affected Data** (entity / column / migration impact)
6. **Affected Test** (TC list, existing-update vs new)
7. **Affected Architecture** (module boundary or ADR implications)
8. **Human Decisions Required** (table of open business or technical questions, each with Owner)
9. **Suggested Implementation Order** (dependency-respecting sequence)

### Step 5: Stop and report

Output the CIA, then **stop**. Do NOT begin code changes until:
- Human reviews the CIA
- All "Human Decisions Required" items have a recorded answer
- Human gives explicit go-ahead

## What this skill does NOT do

- It does **not** modify code.
- It does **not** write the actual flow / spec / contract changes — those happen *after* approval, by the relevant `vibecoding-write-*` skills.
- It does **not** auto-update the traceability matrix — that happens after implementation, by the implementer.

## Output style

Single Markdown document, written to `docs/4-exploration/CR-NNNN-<short-kebab>.md`. Render the same content inline in the chat for the user to review. End the chat response with:

> **🛑 Awaiting your decisions on the items in §8 before any code changes.**

## Edge cases

- **No `docs/2-contracts/` folder yet**: project hasn't adopted the v4 layout; ask user whether to bootstrap the layout (`HOW-TO-INSTANTIATE.md`) before continuing, or accept that the CIA will be lightweight (no IDs to reference).
- **Change is tiny** (1 line, 1 file, no contract): say so explicitly in the CIA, mark §2-7 as N/A, and §8 as "None — proceeding directly". CIA is not skipped, just minimal.
- **Change is huge** (touches >5 BFs or >10 APIs): the CIA itself becomes a planning doc. Recommend splitting into multiple CRs first.

## When to chain to other skills

- **After approval, before implementation**: dispatch to `vibecoding-write-architecture` (if architecture changes), `vibecoding-write-api-contract` (if API changes), `vibecoding-write-tdd` (if new tests needed) — in the order from §9 of the CIA.
- **After implementation**: re-run `sunnydata-doc-freshness` to confirm tier-2 contracts that referenced the old behavior have been updated.
