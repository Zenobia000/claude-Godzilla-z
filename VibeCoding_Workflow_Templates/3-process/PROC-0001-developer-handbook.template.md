---
id: PROC-0001
title: "Developer Handbook — Onboarding / Workflow / Code Review / Security / BDD"
status: active
tier: 3-process
owner: HUMAN-ONLY
essence: bedrock
absorbs: [PROC-0001-workflow, PROC-0002-bdd, PROC-0003-code-review, PROC-0004-security, PROC-0008-frontend-pre-merge, ONBOARD-0000]
last-reviewed: null
---

# PROC-0001: Developer Handbook

> **Tier**: 3-process · **Essence**: bedrock — how engineers actually ship.
>
> **One handbook, five sections** — read in order on Day 1, refer back when stuck. Replaces the previous PROC-0001 workflow-manual + PROC-0002 BDD guide + PROC-0003 code-review checklist + PROC-0004 security checklist + PROC-0008 frontend pre-merge + ONBOARD team onboarding.

---

## §1 — Onboarding (Day 1–30)

### §1.1 Day 1 (≤ 4h to first PR)

| Step | Owner | Output |
|---|---|---|
| Access provisioned (GitHub, cloud, Slack, vault, on-call rotation read-only) | IT | All green checks |
| Clone repo + run `make bootstrap` | New hire | App boots locally |
| Read `BEDROCK.md` + `PRIN-0000` + `ARCH-0000` (90 min) | New hire | Mental model |
| Pair with buddy on one micro-task | Buddy | First PR opened |

If Day 1 takes > 4h to first PR → onboarding is broken; investigate.

### §1.2 Week 1

- Pair on 3 PRs (2 fixes + 1 small feature)
- Shadow 1 on-call rotation (read-only)
- Read this handbook end-to-end
- Read `PROC-0002 §incident` playbook

### §1.3 Week 2–4

- Solo PRs (buddy reviews)
- Own one Now-horizon `PLAN-NNNN §wbs` task
- Add 1 row to relevant `EDGE-0000` catalog from observed pain
- Shadow 1 customer-facing call (support / sales)

### §1.4 Offboarding (mirror)

| Item | Action |
|---|---|
| In-flight work | Hand off to named successor; document state in PR draft |
| Knowledge dump | 30-min recorded session; commit to `docs/handoff/<name>-YYYY-MM-DD.md` |
| Access | Revoke at exit interview; final commit window 24h |
| Open items | Each open issue assigned or closed with reason |

---

## §2 — Daily workflow (§workflow)

### §2.1 Branch protocol (HARD rule)

```
git branch --show-current        # always run before editing
git status
```

| State | Action |
|---|---|
| On `main`/`master` | **STOP.** Ask user → new branch or switch to feature branch |
| On feature branch with uncommitted changes | **STOP.** Commit OR stash explicitly |
| On feature branch, clean | Continue |
| User says "edit X" without branch context | **STOP.** Ask for branch |

Forbidden: `git stash` as workflow (it's a temporary tool); mixing tasks in one branch; direct commits to protected branches.

### §2.2 Feature implementation order

1. **Research & reuse** — search GitHub / docs / npm before coding. Reuse > re-invent.
2. **Plan** — load `sunnydata-design` skill if non-trivial; explore intent before code.
3. **TDD** — red → green → refactor; see `TEST-0000`.
4. **Self code-review** — see §3.
5. **Commit** — see §2.4.
6. **Branch lifecycle** — load `sunnydata-branch-lifecycle` skill to close out.

### §2.3 Change-governance gate

If your change touches **flow / contract / data / architecture**, you MUST first invoke `sunnydata-change-impact-analysis` skill → produces `CIA-NNNN`. No CIA → no code.

Touches the gate include: new/changed BF/UF/SF, API endpoint, DB schema, external integration, test plan, architecture boundary.

Exempt: typo / comment / format / pure internal refactor with test coverage / bug fix in single function with no contract impact.

### §2.4 Commit message format

```
<type>(<scope>): <subject>

<WHY — background and motivation>

<WHAT — key decisions and tradeoffs>

<IMPACT — affected modules + breaking changes>
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`.

Subject: imperative, ≤ 72 chars. **Forbidden**: `fix`, `update`, `misc`, `wip`.

Body discipline by type:
- `feat` / breaking → full WHY/WHAT/IMPACT
- `fix` → WHY + one-line root cause
- `refactor` → WHY only
- `perf` → before/after numbers
- `docs` / `test` / `chore` / `ci` → subject line only

One commit = one logical change. Squash before merge if commits are scratch work.

---

## §3 — Code review (§code-review)

### §3.1 Self-review checklist (before opening PR)

| Check | Pass criteria |
|---|---|
| Diff < 400 lines OR split into multiple PRs | Yes |
| No debug prints / `console.log` / TODO hacks / commented-out code | Yes |
| All tests pass locally (unit + integration) | Yes |
| New code has tests (or explicit justification why not) | Yes |
| Type checker clean | Yes |
| No secrets in diff (`.env`, `credentials.json`, API keys) | Yes |
| Commit history readable (squash if needed) | Yes |
| PR title + description follow §2.4 format | Yes |

### §3.2 Reviewer checklist

| Pass | Criteria |
|---|---|
| Architecture | Does it fit the boundary in `ARCH-0000 §modules`? |
| Business logic | Does it correctly implement `FR-NNNN`? Reference cited? |
| Tests | Cover new behavior + edge cases (`EDGE-NNNN` row added if needed)? |
| Security | §4 checklist passes? |
| Performance | No N+1 queries; no unbounded loops; no synchronous I/O in hot path? |
| Maintainability | Will another engineer understand this in 6mo without help? |
| Public API | Contract docs (`API-0000` / `MC-0000`) updated? |

### §3.3 Review tone

- Critique code, not the person.
- Suggest, don't command — except for security / correctness blockers.
- Praise what's good — silent acceptance kills motivation.
- < 24h turnaround on first review; < 4h on hot fixes.

### §3.4 Approval rules

| Type | Approvers required |
|---|---|
| Standard feature | 1 |
| Touching `2-contracts/` (any) | 1 + contract owner |
| Touching `0-principles/` or `1-decisions/ADR-NNNN` | 2 (governance) |
| Touching `policy/`, `aisafe`, `iam` | 1 + security lead |
| Hotfix to main | 1 + post-fact PM notification |

---

## §4 — Security review (§security-review)

### §4.1 Per-PR security checklist

- [ ] No hardcoded secrets (API keys, passwords, tokens)
- [ ] All user input validated (length, type, schema, encoding)
- [ ] SQL: parameterized queries only (no string interpolation)
- [ ] XSS: HTML output is escaped or sanitized
- [ ] CSRF: state-changing endpoints protected (token / SameSite)
- [ ] AuthN/AuthZ: every endpoint passes through middleware
- [ ] Rate limiting: configured for public endpoints
- [ ] Error messages: no internal stack info leaking to caller
- [ ] Secrets: `.env` / `credentials.json` in `.gitignore`
- [ ] Dependencies: `npm audit` / `pip audit` / `cargo audit` clean

### §4.2 Pre-launch security review

A larger feature / new attack surface triggers:
- Threat model (1-page; STRIDE walkthrough)
- Pen-test or `sunnydata-security` skill audit
- OPA policy update (`ARCH-0000 §security`)
- `AI-0000 §safety` (if AI feature)

### §4.3 Security incident response

1. **Stop** — no patches under pressure
2. Load `sunnydata-security` skill
3. Contain (rotate secrets, disable affected endpoints)
4. Investigate root cause
5. Patch + add regression test + `EDGE-NNNN` row
6. Post-mortem within 48h (severity-dependent — see `PROC-0002 §incident`)

### §4.4 Forbidden patterns

| Pattern | Why |
|---|---|
| `eval(user_input)` | Anything |
| `os.system(user_input)` | Command injection |
| Storing passwords plaintext | Use Argon2 / bcrypt |
| JWT with `alg: none` | Auth bypass |
| Cors `*` on credentialed endpoints | CSRF + token theft |
| Sending PII to LLM without redaction | `AI-0000 §safety` Layer 1 |

---

## §5 — BDD (§bdd) — when to use it

Use BDD when the requirement is **business-rule heavy** (refund policy, eligibility, pricing) — the Gherkin scenarios become the shared contract with PM.

Don't force BDD for pure technical work (refactor, infra, library code) — that's `TEST-0000 §unit` / `§contract` territory.

### §5.1 BDD flow

```
1. PM + eng + QA write feature file together (≤ 30min)
2. Engineer implements step definitions; tests are red
3. Engineer implements production code; tests turn green
4. PM reviews feature file; sign-off
5. Feature file lives at tests/features/<feature>.feature (versioned with code)
```

### §5.2 Format

See `TEST-0000 §bdd` for Gherkin format + discipline rules + CI wiring.

---

## §6 — Communication norms

| Norm | Detail |
|---|---|
| Default async | Slack / GitHub / docs > synchronous meetings |
| Decisions written | If it matters, capture in ADR / CR / commit message |
| 24h response SLA | Reviews, questions, blockers |
| RFC for non-trivial change | Draft → `4-exploration/` → review → ADR |
| Disagree commit (Linus rule) | Push back hard on technical issues; once decided, execute fully |

---

## §7 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| "I'll add the test later" | Later = never | TDD red→green, not green→add-test |
| Hot-fix on main without branch | History pollution; rollback impossible | Always branch |
| Commit "wip" with mixed changes | Unreviewable; unrevertable | One commit = one change |
| Force-push to shared branch | Destroys collaborators' work | Forbidden on shared; rebase your own only |
| PR > 400 lines | Reviewer effort vs quality drops cliff | Split |
| Review approval without reading | False signal; quality erodes | Run checklist §3.2 |
| Security check skipped because "small change" | First exploit comes from "small change" | §4.1 mandatory always |
| New hire onboarding > 1 day to first PR | Repo or process broken | Fix repo / process |

---

## See also

- `BEDROCK.md` — entry point new hires read first
- `0-principles/PRIN-0000-product-principles.template.md` — mission + non-goals
- `1-decisions/ARCH-0000-architecture-overview.template.md` §security — OPA policy
- `2-contracts/API-0000-api-spec.template.md` — wire contract
- `3-process/TEST-0000-testing-strategy.template.md` — test pyramid + BDD format
- `3-process/PROC-0002-ops-runbook.template.md` — production operations + incident
- `3-process/QG-0000-quality-gates.md` — stage prerequisites
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — change-governance hard gate
