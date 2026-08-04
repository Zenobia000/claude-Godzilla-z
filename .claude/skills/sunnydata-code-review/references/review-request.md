# Requesting Review (Phase 2 detail)

Load this reference when dispatching a review after verified work.

## How to Request

**Step 1 — Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or use origin/main as base
HEAD_SHA=$(git rev-parse HEAD)
```

**Step 2 — Dispatch code-reviewer subagent:**

Use Task tool with `superpowers:code-reviewer` type. Fill the template at
`code-review/code-reviewer.md`.

Placeholders to fill:
- `{WHAT_WAS_IMPLEMENTED}` — What you just built
- `{PLAN_OR_REQUIREMENTS}` — What it should do (plan reference or requirements doc)
- `{BASE_SHA}` — Starting commit SHA
- `{HEAD_SHA}` — Ending commit SHA
- `{DESCRIPTION}` — Brief summary of the change

**Step 3 — Act on feedback (see `feedback-handling.md` for full handling):**
- Fix Critical issues immediately, before proceeding to any next step
- Fix Important issues before moving to the next task
- Note Minor issues for later or address opportunistically

## Example Dispatch

```
[Just completed Task 2: Add verification function]

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

[Fix Important issues → Phase 1 verify again → Continue to Task 3]
```

## Integration by Workflow Type

| Workflow | Review Cadence |
|----------|---------------|
| Subagent-Driven Development | After EACH task — catch issues before they compound |
| Executing Plans | After each batch of ~3 tasks |
| Ad-Hoc Development | Before merge; or when stuck |

## Red Flags for Phase 2

Never:
- Skip review because "it's simple"
- Ignore Critical issues and proceed
- Proceed with unfixed Important issues
- Argue with valid technical feedback without a technical counter-argument

If the reviewer is wrong: push back with technical reasoning, show tests or
code that proves it works, and request clarification.

See reviewer template at: `code-review/code-reviewer.md`
