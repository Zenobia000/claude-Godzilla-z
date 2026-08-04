# Verification Gates (Phase 1 detail)

Load this reference before claiming any status, completion, or success.

## Common Failures Table

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Rationalization Prevention Table

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

## Red Flags — STOP Immediately

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports without checking VCS diff
- Relying on partial verification
- Thinking "just this once"
- ANY wording implying success without having run verification

## Key Verification Patterns

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
