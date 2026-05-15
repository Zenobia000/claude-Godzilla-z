---
name: sunnydata-code-review
description: Complete code review lifecycle — verify before claiming done, request structured reviews, and handle feedback with technical rigor. Use when completing tasks, before commits/PRs, or when receiving review feedback.
---

> **繁體中文說明**：此技能整合三個階段的完整程式碼審查流程：驗證完成前的正確性 (Verify) → 請求結構化審查 (Request) → 以技術嚴謹度回應審查意見 (Receive)。順序固定，不可跳過。

# Code Review

## Overview

Three phases, fixed order. The sequence is mandatory — not optional.

```
Verify → Request → Receive → Verify again → Done
```

**Why this order eliminates ambiguity:**
- You cannot claim completion without verification (Phase 1).
- You cannot request review of unverified work (Phase 2 depends on Phase 1).
- You cannot process feedback without first verifying your current state (Phase 3 loops back to Phase 1).

**Core principles across all phases:**
- Evidence before claims, always.
- Review early, review often.
- Technical correctness over social comfort.

---

## Phase 1: Verify Before Completion

### The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification command in this message, you cannot claim it passes.

**Violating the letter of this rule is violating the spirit of this rule.**

### The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

### Common Failures Table

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

### Rationalization Prevention Table

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is not compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion is not an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

### Red Flags — STOP Immediately

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports without checking VCS diff
- Relying on partial verification
- Thinking "just this once"
- ANY wording implying success without having run verification

### Key Verification Patterns

**Tests:**
```
CORRECT:   [Run test command] → [See: 34/34 pass] → "All tests pass"
INCORRECT: "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green cycle — mandatory):**
```
CORRECT:   Write test → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
INCORRECT: "I've written a regression test" (without completing the red-green cycle)
```

**Build:**
```
CORRECT:   [Run build] → [See: exit 0] → "Build passes"
INCORRECT: "Linter passed" (linter does not check compilation)
```

**Requirements:**
```
CORRECT:   Re-read plan → Create checklist → Verify each item → Report gaps or completion
INCORRECT: "Tests pass, phase complete"
```

**Agent delegation:**
```
CORRECT:   Agent reports success → Check VCS diff → Verify changes exist → Report actual state
INCORRECT: Trust agent report at face value
```

### When Phase 1 Applies

**ALWAYS before:**
- Any variation of success or completion claims
- Any expression of satisfaction
- Committing, PR creation, task completion
- Moving to next task
- Delegating to subagents

The rule applies to exact phrases, paraphrases, synonyms, and implications of success.

---

## Phase 2: Request Review

### When to Request

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature
- Before merge to main (typically after PR creation — `sunnydata-branch-lifecycle` invokes this skill post-PR for structured self-review)

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (establish baseline)
- After fixing a complex bug

### How to Request

**Step 1 — Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or use origin/main as base
HEAD_SHA=$(git rev-parse HEAD)
```

**Step 2 — Dispatch code-reviewer subagent:**

Use Agent tool with `code-quality-specialist` subagent type. Fill the template at `code-review/code-reviewer.md`.

Placeholders to fill:
- `{WHAT_WAS_IMPLEMENTED}` — What you just built
- `{PLAN_OR_REQUIREMENTS}` — What it should do (plan reference or requirements doc)
- `{BASE_SHA}` — Starting commit SHA
- `{HEAD_SHA}` — Ending commit SHA
- `{DESCRIPTION}` — Brief summary of the change

**Step 3 — Act on feedback (see Phase 3 below for full handling):**
- Fix Critical issues immediately, before proceeding to any next step
- Fix Important issues before moving to the next task
- Note Minor issues for later or address opportunistically

### Example Dispatch

```
[Just completed Task 2: Add verification function]

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code-quality-specialist subagent via Agent tool]
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

### Integration by Workflow Type

| Workflow | Review Cadence |
|----------|---------------|
| Subagent-Driven Development | After EACH task — catch issues before they compound |
| Executing Plans | After each batch of ~3 tasks |
| Ad-Hoc Development | Before merge; or when stuck |

### Red Flags for Phase 2

Never:
- Skip review because "it's simple"
- Ignore Critical issues and proceed
- Proceed with unfixed Important issues
- Argue with valid technical feedback without a technical counter-argument

If the reviewer is wrong: push back with technical reasoning, show tests or code that proves it works, and request clarification.

See reviewer template at: `code-review/code-reviewer.md`

---

## Phase 3: Receive and Respond to Feedback

### The Response Pattern

```
WHEN receiving code review feedback:

1. READ:      Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words — or ask
3. VERIFY:    Check against codebase reality
4. EVALUATE:  Technically sound for THIS codebase?
5. RESPOND:   Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

### Forbidden Response Phrases

**NEVER say:**
- "You're absolutely right!" (explicit violation)
- "Great point!" / "Excellent feedback!" (performative, not technical)
- "Let me implement that now" (before verification)
- "Thanks for catching that!" / "Thanks for [anything]" (actions speak, not gratitude)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions if unclear
- Push back with technical reasoning if the suggestion is wrong
- Just start working — actions over words

If you catch yourself about to write "Thanks": DELETE IT. State the fix instead.

### Handling Unclear Feedback

```
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on ALL unclear items

WHY: Items may be related. Partial understanding leads to wrong implementation.
```

Example:
```
Reviewer gives items 1-6. You understand 1,2,3,6. Unclear on 4,5.

WRONG: Implement 1,2,3,6 now, ask about 4,5 later
RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

### Source-Specific Handling

**From your human partner:**
- Trusted — implement after understanding
- Still ask if scope is unclear
- No performative agreement
- Skip to action or technical acknowledgment

**From external reviewers (subagent or external tool):**
```
BEFORE implementing any suggestion:
  1. Check: Is this technically correct for THIS codebase?
  2. Check: Does it break existing functionality?
  3. Check: Is there a reason for the current implementation?
  4. Check: Does it work on all required platforms/versions?
  5. Check: Does the reviewer understand the full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF you cannot easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF it conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

Rule: "External feedback — be skeptical, but check carefully."

### YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly" or adding infrastructure:
  grep codebase for actual usage of the endpoint/feature

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used:   Then implement properly
```

Rule: "You and reviewer both report to the human partner. If the feature isn't needed, don't add it."

### Implementation Order for Multi-Item Feedback

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (crashes, security, data loss)
     - Simple fixes (typos, imports, naming)
     - Complex fixes (refactoring, logic changes)
  3. Test each fix individually
  4. Verify no regressions (return to Phase 1 gate function)
```

### When to Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context of the codebase
- Violates YAGNI (unused feature being added)
- Technically incorrect for this stack
- Legacy or compatibility constraints exist
- Conflicts with your human partner's architectural decisions

How to push back:
- Use technical reasoning, not defensiveness
- Ask specific questions
- Reference working tests or code
- Involve your human partner if the issue is architectural

**Disagreement signal:** If you are uncomfortable pushing back explicitly, use the phrase: "Strange things are afoot at the Circle K" — this signals to your human partner that you have a disagreement you haven't stated directly.

### Acknowledging Correct Feedback

```
CORRECT:   "Fixed. [Brief description of what changed]"
CORRECT:   "Good catch — [specific issue]. Fixed in [location]."
CORRECT:   [Just fix it and show in the code]

INCORRECT: "You're absolutely right!"
INCORRECT: "Great point!"
INCORRECT: Any gratitude expression
```

### Correcting Your Own Pushback

If you pushed back and were wrong:
```
CORRECT:   "You were right — I checked [X] and it does [Y]. Implementing now."
CORRECT:   "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

INCORRECT: Long apology
INCORRECT: Defending why you pushed back
INCORRECT: Over-explaining
```

State the correction factually and move on.

### Common Mistakes Table

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if it breaks things |
| Avoiding pushback | Technical correctness over comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

### GitHub Inline Comment Replies

When replying to inline review comments on GitHub, reply in the comment thread — not as a top-level PR comment:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies \
  -f body="Your reply here"
```

### Real Examples

**Performative agreement (wrong):**
```
Reviewer: "Remove legacy code"
WRONG: "You're absolutely right! Let me remove that..."
```

**Technical verification (correct):**
```
Reviewer: "Remove legacy code"
CORRECT: "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat.
          Current impl has wrong bundle ID — fix it or drop pre-13 support?"
```

**YAGNI check (correct):**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
CORRECT: "Grepped codebase — nothing calls this endpoint. Remove it (YAGNI)?
          Or is there usage I'm missing?"
```

---

## Workflow Summary

```
START
  |
  v
[Phase 1: Verify]
  Run verification command → Check output
  |
  Fails? → Fix → Run again
  |
  Passes?
  |
  v
[Phase 2: Request Review]
  Get BASE_SHA + HEAD_SHA
  Dispatch code-reviewer subagent with template
  |
  v
[Phase 3: Receive Feedback]
  Read fully → Understand → Verify in codebase → Evaluate
  |
  Critical issues? → Fix immediately → back to Phase 1
  Important issues? → Fix before next task → back to Phase 1
  Minor issues? → Note or fix opportunistically
  |
  Unclear feedback? → Ask before implementing anything
  Wrong feedback? → Push back with technical reasoning
  |
  v
[Phase 1: Verify again after all fixes]
  |
  v
DONE — claim completion with evidence
```

The cycle is: **Verify → Request → Receive → Verify → Done.**

No phase is optional. No completion claim is valid without fresh verification evidence.
