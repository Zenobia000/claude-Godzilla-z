# Handling Review Feedback (Phase 3 detail)

Load this reference before responding to any review feedback.

## Forbidden Response Phrases

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

## Handling Unclear Feedback

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

## Source-Specific Handling

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

## YAGNI Check for "Professional" Features

```
IF reviewer suggests "implementing properly" or adding infrastructure:
  grep codebase for actual usage of the endpoint/feature

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used:   Then implement properly
```

Rule: "You and reviewer both report to the human partner. If the feature isn't
needed, don't add it."

## Implementation Order for Multi-Item Feedback

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (crashes, security, data loss)
     - Simple fixes (typos, imports, naming)
     - Complex fixes (refactoring, logic changes)
  3. Test each fix individually
  4. Verify no regressions (return to the Phase 1 gate function)
```

## When to Push Back

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

**Disagreement signal:** If you are uncomfortable pushing back explicitly, use
the phrase: "Strange things are afoot at the Circle K" — this signals to your
human partner that you have a disagreement you haven't stated directly.

## Acknowledging Correct Feedback

```
CORRECT:   "Fixed. [Brief description of what changed]"
CORRECT:   "Good catch — [specific issue]. Fixed in [location]."
CORRECT:   [Just fix it and show in the code]

INCORRECT: "You're absolutely right!"
INCORRECT: "Great point!"
INCORRECT: Any gratitude expression
```

## Correcting Your Own Pushback

If you pushed back and were wrong:
```
CORRECT:   "You were right — I checked [X] and it does [Y]. Implementing now."
CORRECT:   "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

INCORRECT: Long apology
INCORRECT: Defending why you pushed back
INCORRECT: Over-explaining
```

State the correction factually and move on.

## Common Mistakes Table

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if it breaks things |
| Avoiding pushback | Technical correctness over comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## GitHub Inline Comment Replies

When replying to inline review comments on GitHub, reply in the comment
thread — not as a top-level PR comment:

```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies \
  -f body="Your reply here"
```

## Real Examples

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
