---
name: verify
description: Perform a read-only-by-default evidence gate across build, type checking, lint, tests, security, and requirement traceability, and issue a supported PASS, CONDITIONAL PASS, or FAIL without fixing findings.
disable-model-invocation: true
argument-hint: "<change-range|FR-ID|NFR-ID|SCN-ID|path> [--baseline ref] [--checks build,type,lint,test,security,traceability]"
---

# Verify with Evidence

Treat `$ARGUMENTS` as the comparison range, requirement scope, paths, and
requested gates. Read
[references/evidence-contract.md](references/evidence-contract.md) before
issuing a verdict.

Report in the engineering register (L3) defined in
[../../rules/language-register.md](../../rules/language-register.md): state facts
and evidence only, without embellishment.

## Default posture

- Remain read-only: do not fix code, update docs, rewrite snapshots, change
  baselines, install dependencies, commit, or push.
- Existing non-destructive project checks may create ordinary temporary build or
  coverage artifacts. Report material side effects and never run destructive,
  paid, production, or credentialed checks without explicit approval.
- Use repository-defined commands. Never invent a command or infer a pass from a
  different check.
- Fresh command output, inspected artifacts, and trace links are evidence.
  Confidence, previous logs, and agent reports are not.

## Workflow

1. **Establish scope.** Resolve baseline, changed files, affected interfaces,
   target `FR/NFR`, `ACPT-ID` and `SCN-ID`. If the baseline or acceptance behavior cannot
   be identified, mark the affected gate `NOT RUN` and explain why.
2. **Read authority.** Read `docs/document-system/INDEX.md`, traceability, and
   only the approved artifacts relevant to the change.
3. **Discover commands.** Use `CLAUDE.md`, package manifests, CI, and project
   scripts to identify exact build, type, lint, test, and security commands.
4. **Build gate.** Run the applicable build command and capture command, exit
   code, and concise output.
5. **Type gate.** Run the repository type checker when defined. Do not substitute
   lint for type checking.
6. **Lint gate.** Run configured formatting or lint checks in check-only mode.
   Do not auto-fix.
7. **Test gate.** Run risk-appropriate unit, integration, and E2E suites. Map
   approved scenarios to test evidence; passing unrelated tests is insufficient.
8. **Security gate.** Inspect changed trust boundaries, secrets, input handling,
   dependencies, and data exposure. Run only configured non-destructive security
   checks; invoke `sunnydata-security` when deeper review is warranted.
9. **Traceability gate.** Verify the chain from source to evidence
   (`SRC → REQ → FR/NFR → ACPT/SCN → SAD/ADR → implementation → test/evidence`;
   the canonical full chain is `docs/document-system/architecture.md` §7.1).
   Flag undocumented behavior and dead trace links.
10. **Regression review.** Inspect the diff for architecture drift, compatibility
    changes, data migration risk, and unrelated modifications.
11. **Verdict.** Classify each gate as `PASS`, `FAIL`, `NOT RUN`, or `N/A`, then
    issue `PASS`, `CONDITIONAL PASS`, or `FAIL` using the evidence contract.

## Reporting

List scope and baseline, exact commands, exit codes, mapped requirements and
scenarios, blocking and non-blocking findings with file locations, unverified
items, and residual risk. Do not modify findings unless the user separately
invokes `/deliver` or otherwise authorizes a fix.
