# CI Gates — Contract Enforcement Workflows

> **Tier**: 3-process · **Layer mapping**: implements §3 cells of [`PRIN-0003-engineering-contract-stack.md`](../../0-principles/PRIN-0003-engineering-contract-stack.md)
>
> **Why this directory exists**: contracts that aren't enforced by CI rot in 6 months. Every layer in `PRIN-0003` claims a CI gate; this directory holds the reference workflow stubs that prove it.

---

## §1 Reference platform

All 10 gates are written as **GitHub Actions** workflows (`.workflow.yml`). The shell logic in each is portable — translating to GitLab CI / Bitbucket Pipelines / Jenkins is mechanical (copy the script body, swap the `on:` block).

When instantiating a project:
1. Copy needed `CIG-NNNN-*.workflow.yml` to `.github/workflows/<name>.yml` (rename, drop `.workflow` suffix).
2. Fill the `# TODO: configure` blocks (paths, secrets, version pins).
3. Verify with `actionlint .github/workflows/<name>.yml` locally.

---

## §2 Gate inventory

| ID | Gate | Layer | Trigger | Required-or-Advisory |
|---|---|---|---|---|
| `CIG-0001` | OpenAPI spec-lint (Spectral) | L1.1, L1.3 | PR | **Required** |
| `CIG-0002` | API types sync (OpenAPI → TS) | L1.1, L5.3 | PR | **Required** |
| `CIG-0003` | AsyncAPI validate | L1.2 | PR | **Required** if async exists |
| `CIG-0004` | Schemathesis contract test | L1.1, L4.1 | PR + nightly | **Required** |
| `CIG-0005` | i18n keys sync | L4.3, L5.4 | PR | **Required** if frontend |
| `CIG-0006` | Test case coverage | L4.2 | PR | **Required** |
| `CIG-0007` | Doc freshness (last-synced-with) | all tier-2 | PR + weekly | **Required** |
| `CIG-0008` | Orphan check (Flow ID refs) | L4.4 | PR | **Required** |
| `CIG-0009` | Reverse-import-lint | L3.1 | PR | **Required** if policy module |
| `CIG-0010` | Mock server smoke | L1.1 | PR | Advisory |

---

## §3 Composition

Run order matters. A typical PR pipeline:

```
on: pull_request
  ↓
1. CIG-0001 spec-lint        (cheap, fails fast)
2. CIG-0003 asyncapi-validate (cheap)
3. CIG-0002 api-types-sync   (compiles TS — medium)
4. CIG-0005 i18n-keys-sync   (compiles JSON — medium)
5. CIG-0008 orphan-check     (greps repo)
6. CIG-0009 reverse-import   (parses imports)
7. CIG-0007 doc-freshness    (queries git log)
   ↓ (only if above pass)
8. CIG-0004 schemathesis      (boots service — expensive)
9. CIG-0010 mock-smoke         (advisory)
   ↓
10. CIG-0006 test-case-coverage (final coverage check)
```

Gates 1-7 are pure-static and should complete in < 60s.
Gates 8-10 boot the service and take 2-10 min.

---

## §4 Dependencies on skills

| Gate | Skill it pairs with |
|---|---|
| `CIG-0001` | `vibecoding-write-api-contract` (authoring) |
| `CIG-0003` | `vibecoding-write-api-contract` (async extension) |
| `CIG-0004` | `vibecoding-write-integration-tests`, `sunnydata-testing` |
| `CIG-0006` | `vibecoding-write-bdd` |
| `CIG-0007` | `sunnydata-doc-freshness` |
| `CIG-0008` | `sunnydata-flow-audit` |
| (all) | `sunnydata-contract-stack-audit` — periodic super-check |

---

## §5 Adding a new gate

1. Pick the next `CIG-NNNN` from `PRIN-0001 §extended prefixes`.
2. Add a workflow file `CIG-NNNN-<slug>.workflow.yml` here.
3. Update §2 inventory above.
4. Register the gate in `QG-0000-quality-gates.md` (which stage it enforces).
5. Update `PRIN-0003 §3` cell for the affected layer.

---

## §6 What this directory does NOT cover

- **Deploy / release pipelines** — see `PROC-0005-deployment-runbook.template.md` + `PROC-0011-gitops-runbook.template.md`.
- **Infrastructure provisioning** — see `ARCH-0003-infra-architecture.template.md`.
- **Security scans** (SAST / dependency / SBOM) — those have their own gate convention; add as a CIG when needed.
- **Performance budgets** (Lighthouse CI, k6) — future CIG-0011+.

---

## See also

- `0-principles/PRIN-0003-engineering-contract-stack.md` — the layer map these gates implement
- `3-process/QG-0000-quality-gates.md` — stage prerequisites
- `.claude/skills/sunnydata-contract-stack-audit/SKILL.md` — verifies each layer has at least one gate wired
