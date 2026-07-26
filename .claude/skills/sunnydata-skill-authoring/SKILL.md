---
name: sunnydata-skill-authoring
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

> **繁體中文說明**：見 [SUPERPOWERS-EXTRAS-USAGE-zh-TW.md](../SUPERPOWERS-EXTRAS-USAGE-zh-TW.md)（全系列 `sp-*` 摘要）。

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Personal skills live in agent-specific directories (`~/.claude/skills` for Claude Code, `~/.agents/skills/` for Codex)**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand superpowers:sunnydata-testing before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

**Official guidance:** For Anthropic's official skill authoring best practices, see anthropic-best-practices.md. This document provides additional patterns and guidelines that complement the TDD-focused approach in this skill.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

**Skill types:** Technique (concrete method with steps, e.g. condition-based-waiting), Pattern (way of thinking, e.g. flatten-with-flags), Reference (API docs, syntax guides, tool documentation).

## When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (if it's enforceable with regex/validation, automate it—save documentation for judgment calls)

## TDD Mapping for Skills

| TDD Concept | Skill Creation |
|-------------|----------------|
| **Test case** | Pressure scenario with subagent |
| **Production code** | Skill document (SKILL.md) |
| **Test fails (RED)** | Agent violates rule without skill (baseline) |
| **Test passes (GREEN)** | Agent complies with skill present |
| **Refactor** | Close loopholes while maintaining compliance |
| **Write test first** | Run baseline scenario BEFORE writing skill |
| **Watch it fail** | Document exact rationalizations agent uses |
| **Minimal code** | Write skill addressing those specific violations |
| **Watch it pass** | Verify agent now complies |
| **Refactor cycle** | Find new rationalizations → plug → re-verify |

## The Iron Law (Same as TDD)

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.
Edit skill without testing? Same violation.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Don't "adapt" while running tests
- Delete means delete

## Workflow: RED-GREEN-REFACTOR

1. **RED — Write failing test (baseline).** Run pressure scenarios with a subagent
   WITHOUT the skill. Document exact behavior and verbatim rationalizations.
   Read `references/testing-and-bulletproofing.md` before designing scenarios —
   each skill type (discipline, technique, pattern, reference) needs a different
   test approach.
2. **GREEN — Write minimal skill.** Address the specific baseline failures; skip
   hypothetical cases. Read `references/skill-structure.md` when laying out
   frontmatter, directory structure, flowcharts, and code examples. Read
   `references/writing-for-agents.md` when writing the description and prose —
   discovery (CSO), token efficiency, and steering language live there. Re-run
   the same scenarios WITH the skill; the agent should now comply.
3. **REFACTOR — Close loopholes.** Agent found a new rationalization? Add an
   explicit counter, build the rationalization table, create a red-flags list.
   Re-test until bulletproof. Read `references/testing-and-bulletproofing.md`
   for loophole-closing patterns and the full deployment checklist.

**Testing methodology:** See @testing-skills-with-subagents.md for pressure
scenario design, pressure types, and meta-testing techniques.

## Writing Principles

- **Lead with words, not lectures.** Steer behavior with compact concepts the
  model already knows — "seam", "tracer bullet", "red", "tight feedback loop" —
  and repeat them as tokens, not sentences: "keep the loop _tight_" beats
  re-explaining "fast, deterministic, low-overhead" every time.
- **Prompt the positive.** State what TO do; a "don't" plants the very image you
  want avoided. Reserve "never / do not" for hard gates like the Iron Law.
- **One excellent example beats many mediocre ones.** Complete, runnable,
  commented for WHY, from a real scenario. You're good at porting.
- **Description = when to use, NOT what the skill does.** A workflow summary in
  the description becomes a shortcut that replaces reading the skill body.

Details and worked examples: `references/writing-for-agents.md`.

## STOP: Before Moving to Next Skill

**After writing ANY skill, you MUST STOP and complete the deployment process.**

Test each skill before starting the next — verify the current one, then move on;
"batching is more efficient" is how untested skills ship. The deployment
checklist in `references/testing-and-bulletproofing.md` is MANDATORY for EACH
skill. Deploying untested skills = deploying untested code.

## The Bottom Line

**Creating skills IS TDD for process documentation.**

Same Iron Law: No skill without failing test first.
Same cycle: RED (baseline) → GREEN (write skill) → REFACTOR (close loopholes).
Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation.
