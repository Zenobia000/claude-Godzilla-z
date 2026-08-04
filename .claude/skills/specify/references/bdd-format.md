# BDD scenario format

Load this reference when `/specify` step 4 derives BDD scenarios. This is the
authoring format only; scenario responsibility (what BDD covers vs PRD/SAD) is
defined in [document-contract.md](document-contract.md).

## File placement and naming

- One file per approved feature scope: `docs/01_requirements/bdd-<scope-slug>.md`
  (or the project's existing BDD location when `docs/document-system/INDEX.md`
  identifies one).
- Scenario IDs use `SCN-<DOMAIN>-<NNN>` (e.g. `SCN-LOCK-001`), never recycled;
  superseded scenarios keep a tombstone with a `supersedes` link.

## Scenario shape

```gherkin
## SCN-LOCK-001 — 客戶授權後遠端上鎖
Traces: FR-AGT-001, ACPT-LOCK-001

Given 一個已綁定且在線的門鎖
  And 客戶已完成授權
When 客戶在 App 送出上鎖指令
Then 門鎖在 5 秒內回報「已上鎖」
  And 事件記錄包含操作者與時間
```

Rules:

- **Header carries the trace.** Every scenario names its `FR/NFR` and `ACPT-*`
  upstream IDs in a `Traces:` line; a scenario with no upstream ID is invented
  scope and must not exist.
- **Business-observable only.** Given/When/Then state what a user or external
  system can observe. No internal classes, tables, endpoints, or UI control
  names — that is L3 material (see `../../rules/language-register.md`).
- **One behavior per scenario.** Split "and also" behaviors into separate
  scenarios rather than stacking Then clauses for unrelated outcomes.
- **Concrete values over adjectives.** "within 5 seconds", not "quickly";
  values are proposals until the owner approves them.

## Coverage checklist

For each approved `ACPT-*`, cover what applies and mark the rest `N/A`:

- [ ] Primary path
- [ ] Boundary condition (limits, empty, max)
- [ ] Failure path (timeout, rejection, unavailable dependency)
- [ ] Permission / authorization variant
- [ ] Idempotency / retry behavior

Do not pad coverage: a scenario that restates the primary path with cosmetic
variation is noise, not coverage.
