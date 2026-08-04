# Verification evidence contract

Load this reference before running checks or issuing a verdict.

## Gate states

| State | Meaning |
| --- | --- |
| `PASS` | Fresh, in-scope evidence satisfies the gate |
| `FAIL` | Fresh evidence shows a blocking mismatch or failed check |
| `NOT RUN` | Applicable but unavailable, unsafe, unknown, or not executed |
| `N/A` | Not applicable, with a recorded reason |

Never convert `NOT RUN` into `PASS`.

## Minimum evidence

For every executed command record:

- exact command and working directory;
- relevant environment assumptions;
- start or observation time when useful;
- exit code;
- concise result and artifact location;
- requirements or scenarios supported by the result.

For document inspection record file path, status, revision, and relevant section
or trace row. For manual observations distinguish observed fact from inference.

## Gate expectations

- **Build:** configured build completes with exit code zero.
- **Type:** configured type checker reports no in-scope error.
- **Lint:** check-only formatter/linter reports no blocking finding.
- **Test:** risk-appropriate suites pass and approved scenarios have mapped
  evidence.
- **Security:** no unresolved blocking exposure in changed trust boundaries;
  configured scans succeed when safely runnable.
- **Traceability:** every in-scope approved behavior reaches implementation and
  test evidence, and no implementation behavior lacks an approved source.

## Verdicts

- `PASS`: every applicable required gate passes; no blocking finding or unknown.
- `CONDITIONAL PASS`: no known blocking failure, but explicitly accepted
  `NOT RUN` gates or non-blocking risks remain.
- `FAIL`: any required gate fails, a blocking trace/spec mismatch exists, or
  available evidence contradicts the claimed behavior.

## Finding format

```text
[severity] [gate] title
Evidence: file:line or command + exit code
Requirement/Scenario: identifier
Impact: observable consequence
Next action: bounded recommendation
```

Verification reports findings only. Repair requires separate authorization.
