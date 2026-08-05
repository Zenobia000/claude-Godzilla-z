---
name: sunnydata-testing
description: Risk-based test development workflow with unit, integration, and E2E patterns. Use Red-Green-Refactor where it improves feedback, and apply project-defined coverage and evidence thresholds when writing features, fixing bugs, or setting up test infrastructure.
origin: merged(tdd-workflow + e2e-testing)
---

> **繁體中文說明**：此技能整合 TDD 與 Playwright E2E，依風險選擇單元、整合、E2E 層級；覆蓋率門檻由專案政策與關鍵行為決定。

# Testing

> Project-wide evidence rules are in `.claude/rules/golden-rules.md`; this Skill
> owns testing methods. Discover thresholds from project configuration, CI, NFRs,
> or approved quality policy instead of inventing a universal percentage.

## Overview

Prefer a failing test or reproducible check before implementation when practical,
then implement and refactor with feedback. Choose the test layers needed to cover
approved behavior and material risk:

- **Unit tests** — individual functions, utilities, components
- **Integration tests** — API endpoints, database operations, service interactions
- **E2E tests** — critical user flows via Playwright browser automation

## TDD Workflow (Red-Green-Refactor)

### When to Apply

- Writing new features or functionality
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing code
- Adding API endpoints or new components

### The 7-Step Cycle

1. **Write user journey** — `As a [role], I want to [action], so that [benefit]`
2. **Derive test cases** — happy path, empty input, fallback behavior, ordering
3. **Run tests (RED)** — they must fail; the implementation does not exist yet
4. **Implement minimal code** — only enough to make tests pass
5. **Run tests (GREEN)** — they must all pass
6. **Refactor** — remove duplication, improve naming, optimize; keep tests green
7. **Verify coverage** — compare with the repository's configured thresholds and
   changed-risk areas

Read `references/unit-and-tdd-patterns.md` when executing the cycle: it holds
the full step-by-step code examples, the optional coverage-threshold policy
example, watch mode and pre-commit setup, unit test patterns
(Jest/Vitest + Testing Library), and mocks for external services
(Supabase, Redis, OpenAI).

## Seams — where tests go

A **seam** is the public boundary you test at: the interface where you observe
behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** Before writing any test, write down the seams
under test and confirm them. No test is written at an unconfirmed seam. You
cannot test everything — agreeing the seams up front is how testing effort lands
on critical paths and complex logic instead of every edge case.

Four rules for picking one, in order: prefer an existing seam; use the highest
seam that can still observe the behavior; fewer is better (the ideal number is
one); if a new seam is genuinely needed, propose it at the highest point you can.
Load `sunnydata-codebase-design` for the vocabulary and the reasoning behind each.

Ask: "What's the public interface, and which seams should we test?"

## Anti-Patterns

Three ways a test suite rots. Each has a tell:

- **Implementation-coupled** — mocks internal collaborators, tests private
  methods, or verifies through a side channel (querying the database instead of
  using the interface). *Tell:* the test breaks when you refactor but behavior
  hasn't changed.
- **Tautological** — the assertion recomputes the expected value the way the code
  does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way,
  a constant asserted equal to itself), so it passes by construction and can never
  disagree with the code. *Fix:* expected values must come from an independent
  source — a known-good literal, a worked example, the spec.
- **Horizontal slicing** — writing all tests first, then all implementation. Bulk
  tests verify *imagined* behavior: you test the shape of things rather than
  user-facing behavior, and you commit to test structure before understanding the
  implementation. *Fix:* vertical slices — one test → one implementation →
  repeat, each test a tracer bullet responding to what the last cycle taught you.

## Choosing and Writing Test Layers

- **Unit** — Read `references/unit-and-tdd-patterns.md` when testing functions,
  utilities, or components in isolation, or mocking external services.
- **Integration and E2E** — Read `references/integration-e2e-patterns.md` when
  testing API endpoints, writing Playwright flows with the Page Object Model,
  diagnosing flaky tests, or covering Web3/wallet and financial high-risk flows.
- **Infrastructure** — Read `references/test-infrastructure.md` when setting up
  test directory structure, Playwright configuration, artifact capture
  (screenshots, traces, video), or CI/CD workflows for E2E and coverage upload.

## Non-Negotiables

Full before/after code examples for each rule live in the references noted:

- **Test behavior, not implementation details** — assert what users see, not
  internal state (`unit-and-tdd-patterns.md`)
- **Isolate every test** — each test owns its data; no shared-state chains
  (`unit-and-tdd-patterns.md`)
- **Test error paths, not just happy paths** — null input, empty arrays, network
  failures, boundary values (`unit-and-tdd-patterns.md`)
- **Use semantic selectors** — `data-testid` or role/text, never brittle CSS
  classes (`integration-e2e-patterns.md`)
- **Never use arbitrary timeouts** — wait for a deterministic network or
  visibility condition (`integration-e2e-patterns.md`)

## Success Metrics

- Project-defined coverage gates pass, with critical paths and changed risk
  directly exercised
- All applicable tests pass; skipped or disabled tests have an explicit reason
- Test feedback time meets the repository or CI budget
- E2E tests cover all critical user flows
- No flaky tests in CI (quarantine with tracked issue if needed)
- Tests catch regressions before production
