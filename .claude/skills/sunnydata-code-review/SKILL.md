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
- You cannot process feedback without first verifying your current state
  (Phase 3 loops back to Phase 1).

**Core principles across all phases:**
- Evidence before claims, always.
- Review early, review often.
- Technical correctness over social comfort.

## Phase 1: Verify Before Completion

### The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification command in this message, you cannot claim
it passes. **Violating the letter of this rule is violating the spirit of this
rule.** The rule applies to exact phrases, paraphrases, synonyms, and
implications of success.

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

**ALWAYS apply before:** any success or completion claim, any expression of
satisfaction, committing, PR creation, moving to the next task, or delegating
to subagents.

Read `references/verification-gates.md` before claiming any status: it holds
the common-failures table (what evidence each claim requires), the
rationalization-prevention table, the STOP red flags, and per-claim
verification patterns (tests, red-green regression cycle, build, requirements
checklist, agent delegation).

## Phase 2: Request Review

**Mandatory:** after each task in subagent-driven development, after completing
a major feature, before merge to main.

**Optional but valuable:** when stuck (fresh perspective), before refactoring
(establish baseline), after fixing a complex bug.

Review runs on **two axes**, as parallel sub-agents so neither pollutes the
other's context:

- **Standards** — does the diff follow this repo's documented standards, plus a
  Fowler smell baseline?
- **Spec** — does it faithfully implement the originating `FR`/`ACPT`/`SCN`?
  Missing, extra (scope creep), or implemented-but-wrong.

A change can pass one and fail the other, so the two reports stay **separate and
unranked** — merging them lets one axis mask the other. Read
`references/two-axis-review.md` when dispatching: it holds the fixed-point
protocol, both sub-agent briefs, the smell baseline to paste in, and the
aggregation rule.

Read `references/review-request.md` for the mechanics: SHA-capture commands,
dispatch template and placeholders, a full example, review cadence by workflow
type, and Phase 2 red flags (never skip review because "it's simple"; never
proceed past unfixed Critical or Important issues).

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

Read `references/feedback-handling.md` before responding to any feedback: it
holds the forbidden performative phrases, the unclear-feedback protocol
(clarify ALL items before implementing ANY), source-specific handling (human
partner vs external reviewer), the YAGNI check, implementation order for
multi-item feedback, when and how to push back, acknowledgment and
self-correction wording, GitHub inline reply mechanics, and real examples.

## Workflow Summary

```
START
  |
  v
[Phase 1: Verify]
  Run verification command → Check output
  Fails? → Fix → Run again
  |
  v
[Phase 2: Request Review]
  Pin fixed point → Dispatch Standards + Spec sub-agents in parallel
  → Report both axes separately, no cross-axis reranking
  |
  v
[Phase 3: Receive Feedback]
  Read fully → Understand → Verify in codebase → Evaluate
  Critical issues? → Fix immediately → back to Phase 1
  Important issues? → Fix before next task → back to Phase 1
  Minor issues? → Note or fix opportunistically
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

No phase is optional. No completion claim is valid without fresh verification
evidence.
