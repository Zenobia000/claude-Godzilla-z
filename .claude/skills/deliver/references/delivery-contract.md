# Vertical-slice delivery contract

Load this reference before implementing or proposing implementation.

## Ready criteria

A slice is ready only when:

- its `FR/NFR`, `ACPT-ID`, and acceptance behavior are Approved;
- relevant BDD scenarios are observable and unambiguous;
- the SAD supplies required boundaries and interfaces;
- required ADRs are Accepted, or a reversible choice is explicitly delegated;
- project build and test commands are discoverable;
- external credentials or irreversible actions are not required merely to begin.

If any criterion fails, report the exact missing artifact or decision and return
to `/specify`.

## Slice shape

Prefer one end-to-end behavior over a horizontal layer. A slice description must
include:

| Item | Required content |
| --- | --- |
| Scope | `FR/NFR`, `ACPT-ID`, `SCN-ID`, in-scope outcome, explicit exclusions |
| Touch points | Expected files, interfaces, data, and migration |
| Tests | Scenario, boundary, failure, and regression evidence |
| Checks | Exact repository commands |
| Risks | Compatibility, security, privacy, rollback, external effects |
| Stop conditions | Spec conflict, new ADR, destructive migration, unavailable dependency |

## Authorization gates

1. **Local implementation:** `/deliver` authorizes the requested in-scope local
   code, test, and documentation work unless the user asks for plan/review only.
   Ask again only when scope is materially ambiguous or must expand.
2. **Decision approval:** accept new durable design choices through `/specify`.
3. **External action approval:** separately authorize commit, push, PR, migration,
   deployment, paid service, or production access.

Approval for one gate does not imply approval for later gates.

## Native task tracking

Use Claude Code's session-native tasks for implementation steps and dependencies.
Keep long-lived project truth in the document system. Do not create parallel WBS,
TaskMaster, hidden session, or context-report state.

## Handoff

Report traceability from requirement to files and tests, fresh check results,
unverified work, residual risk, and the precise `/verify` scope. Do not mark the
document-system artifact Approved as a side effect of implementation.
