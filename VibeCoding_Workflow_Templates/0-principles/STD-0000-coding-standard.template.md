---
id: STD-0000
title: "Coding Standard — Team Divergences"
status: active
tier: 0-principles
owner: HUMAN-ONLY
essence: bedrock
last-reviewed: 2026-05-17
product-version: null
supersedes: null
superseded-by: null
---
# Coding Standard — `<PROJECT_NAME>`

> **Tier**: 0-principles — encodes the team's *deviations from textbook defaults* so AI does not have to guess them every conversation.
>
> **Scope rule**: this doc is NOT a programming tutorial. It records **where this team disagrees with the language's mainstream style guide and why**. If a rule is identical to the mainstream guide, do not list it here — link the upstream guide instead.

---

## 1. Why this document exists

AI assistants default to the mainstream style of whatever language they were trained on. That default is usually fine, but every mature team has 5-15 rules that diverge — and those divergences cause the most painful AI slop (a refactor that "looks right" but violates an unspoken team convention).

This file is the **convention contract**. Filling it once means AI stops re-deriving the team's instincts on every PR.

---

## 2. Upstream baselines

State which mainstream guides we *inherit by default*. The rest of this doc records only the overrides.

| Language / area | Upstream guide we follow | Link |
|---|---|---|
| Python | PEP 8 + Black formatting | https://peps.python.org/pep-0008/ |
| TypeScript | Airbnb style + Prettier | https://github.com/airbnb/javascript |
| Go | gofmt + Effective Go | https://go.dev/doc/effective_go |
| SQL | <pick one: Mozilla / Simon Holywell> | — |
| Commit messages | Conventional Commits | https://www.conventionalcommits.org/ |

If a language is not listed, AI must ask before assuming a style.

---

## 3. Team-specific overrides

For each rule that diverges from the upstream guide, give: **the rule**, **why we diverge**, and **one example**. Without the *why*, the rule will be discarded as soon as someone forgets the history.

### 3.1 Layer interaction (what may import what)
> Link to `ARCH-0001-module-boundary` for the authoritative list. Repeat the top 3 rules here so AI sees them at tier-0 load time.

- **Domain layer NEVER imports infrastructure layer.** Reason: keeps domain unit-testable without DB. Violation example: importing `sqlalchemy.Session` inside `domain/order.py` = blocked.
- **UI components NEVER call API clients directly.** Reason: testability + retry/auth concerns belong in a hook layer. Violation example: `fetch()` inside a `.tsx` render function.
- **Add the third rule that bit you most recently.**

### 3.2 Naming conventions where we diverge
| What | Mainstream default | Our rule | Why |
|---|---|---|---|
| Test file location | `tests/` mirror tree | Adjacent `*.test.ts` next to source | Discoverability outweighs separation |
| Boolean variables | `is_*` / `has_*` | (state) | (state) |
| (add more) | | | |

### 3.3 Error handling patterns
- **Never silently swallow errors.** `try: ... except: pass` is banned. Reason: bit us in incident INC-XXXX where a swallowed timeout looked like success for 3 hours.
- **Errors crossing module boundary MUST be typed.** Internal exceptions stay internal; public API surfaces wrap them in `<DomainError | InfraError>` discriminated union.
- **At system boundaries, validate. Inside, trust.** No defensive `if user is None` chains within a single module.

### 3.4 State / immutability rules
- **Default to immutable data.** Mutate only inside the owning aggregate.
- **No global mutable state.** Module-level mutable variables = blocked. Reason: kills test parallelism.
- **Function arguments are read-only.** Returning a new value beats mutating an input.

### 3.5 Testing layer assignment (which test type owns which concern)
> Detailed strategy lives in `3-process/TP-0000-test-plan`. List the top-3 boundaries here so AI does not test the wrong layer (the #4 anti-slop symptom).

| Concern | Owned by | Not by |
|---|---|---|
| Business invariants | Unit test on domain aggregate | E2E |
| HTTP contract | Contract test against OpenAPI | Unit |
| User-visible flow | E2E (Playwright/Cypress) | Unit |

### 3.6 Comment policy
- **Default: write no comment.** Names carry intent.
- **Allowed: explain WHY when non-obvious.** Hidden constraint, workaround for a specific bug, surprising invariant.
- **Banned: comments restating the code.** `# increment i` above `i += 1` = noise.
- **Banned: AI-style "this function does X by doing Y and Z" multi-paragraph docstrings.** One sentence max unless this is a public API.

### 3.7 Dependency policy
- **Adding a runtime dependency requires:** active maintenance (commit in last 6 months), no known CVE, license compatible (`<pick: MIT/Apache-2.0/BSD>`), one team member sign-off.
- **Lock files are committed.** `package-lock.json` / `poetry.lock` / `go.sum` go in version control.
- **Pinning policy:** runtime deps use exact version; dev deps use `^` minor range.

---

## 4. Anti-patterns we explicitly reject

| Anti-pattern | Why we reject | What to do instead |
|---|---|---|
| Premature abstraction | Three similar lines is fine; abstract on the *third* use case, not the first | Repeat once, extract on third occurrence (Rule of Three) |
| Catch-all base classes / mega-utils | Becomes a junk drawer | One module per cohesive concern; refuse "utils" with > 5 unrelated functions |
| Speculative `**kwargs` / `extends` for "future flexibility" | YAGNI | Add the parameter when the second caller needs it |
| Wrapping every primitive in a class for "type safety" | Cognitive overhead > safety win at our scale | Use type aliases (`UserId = NewType('UserId', int)`) instead |
| (add the one your team keeps re-inventing) | | |

---

## 5. Tooling enforcement

A rule that is not enforced is a wish.

| Rule from §3 | Enforced by | Where it runs |
|---|---|---|
| Formatting | Black / Prettier / gofmt | pre-commit hook + CI |
| Linting | ruff / eslint / golangci-lint | pre-commit hook + CI |
| Type checking | mypy --strict / tsc --strict | CI |
| Import boundary (§3.1) | <import-linter / dependency-cruiser / depguard> | CI |
| No-swallow-errors (§3.3) | <custom lint rule / grep CI step> | CI |
| Commit message format | commitlint | commit-msg hook |

If a rule has no row in this table, treat it as aspirational, not binding. **Either tool-enforce it or delete it.**

---

## 6. AI-specific guidance

This section addresses the failure modes specific to LLM-generated code. Update when you observe a new pattern.

- **No "for future flexibility" abstractions.** If the second use case does not exist *today*, do not add a parameter / interface / strategy class for it.
- **No backward-compatibility shims when changing internal code.** If the only caller is in this repo, just change the call site.
- **No fallback error handlers around code that cannot reach the error path.** Trust internal guarantees; validate only at system boundaries.
- **Hallucinated APIs are a stop-the-line bug.** Every external function / library call must be grep-verified in the dependency before being shipped.
- **Tests that always pass are worse than no tests.** A test that has never failed since being written is suspect — verify it actually exercises the assertion.

---

## 7. Out-of-Date Indicators

Re-review this doc immediately if ANY is true:

- [ ] A new language / framework joined the stack with no row in §2
- [ ] A code-review comment had to explain the same convention twice in one month
- [ ] An incident post-mortem named "we don't have a rule for X" as a root cause
- [ ] An ADR overrode something in §3 without a corresponding edit here
- [ ] CI added a new lint rule with no row in §5

---

## 8. Relationship to other documents

| If you want… | Read… |
|---|---|
| Why a specific module exists at all | `ARCH-0001-module-boundary` (tier 1) |
| What a module promises externally | `MC-0000-module-contract` (tier 2) |
| Which tests cover which behavior | `TP-0000-test-plan` (tier 3) |
| The reasoning behind a one-off override | The relevant `ADR-NNNN` (tier 1) |

This document tells AI **how** to write code; the others tell it **what** and **why**.

---

**Maintained by**: `<owner>`
**Last reviewed**: `<YYYY-MM-DD>`
**Next review due**: `<YYYY-MM-DD + 6 months>`
