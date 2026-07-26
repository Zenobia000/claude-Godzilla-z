---
name: deliver
description: Implement one approved vertical slice from PRD, BDD, SAD, ADR, and traceability artifacts using native task tracking and relevant existing professional skills, with explicit human gates before code and external actions.
disable-model-invocation: true
argument-hint: "<FR-ID|NFR-ID|SCN-ID|slice> [--scope path] [--no-commit]"
---

# Deliver an Approved Vertical Slice

Treat `$ARGUMENTS` as the requested requirement, scenario, or bounded vertical
slice. Unless the user asks for plan/review only, invocation authorizes in-scope
local code, test, and documentation changes. It does not authorize commits,
pushes, PRs, destructive migrations, deployments, paid services, or production
access.

Read [references/delivery-contract.md](references/delivery-contract.md) before
planning the slice.

Write in the engineering register (L3) defined in
[../../rules/language-register.md](../../rules/language-register.md): be precise
about interfaces, fields, and commands. Trace business motivation to L1/L2 IDs
rather than restating it as implementation rationale.

## Readiness check

1. Read `docs/document-system/INDEX.md`, traceability, and only the in-scope
   approved PRD/BDD/SAD/ADR sections plus any affected contracts
   (openapi.yaml, db_design, ui_spec).
2. Confirm the target maps to an approved `FR/NFR`, `ACPT-ID`, observable
   `SCN-ID`, compatible architecture, and no unresolved blocking decision.
3. Inspect the working tree, project instructions, neighboring implementation,
   and real build/test/lint commands. Preserve unrelated user changes.
4. If specifications conflict or implementation would change external behavior,
   stop and route the issue back through `/specify`.

## Plan the slice

1. Choose the smallest end-to-end behavior that produces user-visible or
   externally observable value.
2. Map `FR/NFR → ACPT/SCN → files/interfaces → tests → verification commands`.
3. Use Claude Code native task tracking for the current session. Do not create or
   update TaskMaster state, hidden session snapshots, or another roadmap.
4. Select existing professional skills only when relevant:
   `sunnydata-api-design`, `sunnydata-shadcn-ui`, `sunnydata-testing`,
   `sunnydata-security`, `sunnydata-debugging`, or architecture/code review
   skills. Do not preload the entire library.
5. Identify schema migrations, compatibility risks, credentials, external
   effects, and rollback needs.

## Implementation authorization

State the slice, file/test map, assumptions, and material risks before editing,
then proceed with the authorized local work. Stop for clarification only when
the approved artifacts conflict, a missing decision materially changes behavior,
or the required action expands beyond the requested scope.

## Implement

1. Add or update tests in proportion to risk, covering the approved scenario and
   applicable failure behavior.
2. Implement the minimal compatible change. Do not silently change requirements,
   architecture, public contracts, or data policy.
3. Run the approved project checks incrementally. A failing check triggers
   diagnosis; it does not authorize broader refactoring.
4. Keep native task state aligned with completed work. Record newly discovered
   specification issues separately.
5. Update project documentation only when the approved implementation changes a
   documented interface or operational fact.

## Human Gate: external actions

Require separate explicit approval before commit, push, PR creation, destructive
migration, deployment, paid service use, or production access. A successful
implementation is not implicit authorization for these actions.

## Handoff

Report completed `FR/NFR`, `ACPT` and `SCN` IDs, changed files, commands actually run,
results, unverified items, residual risks, and the recommended `/verify`
invocation. Never report success from expectation or a subagent claim alone.
