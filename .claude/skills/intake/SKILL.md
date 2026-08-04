---
name: intake
description: Inspect an Excel requirements workbook without modifying it, determine whether it is an authored source or generated snapshot, and derive a traceable requirements register with source locations, acceptance criteria, assumptions, and open questions.
disable-model-invocation: true
argument-hint: "<workbook.xlsx> [--source-key KEY] [--output docs/document-system/requirements/requirements-register.md]"
---

# Requirements Intake

Treat `$ARGUMENTS` as the source workbook, optional immutable source key, output
path, and scope. This action creates or updates derived project documentation; it
never writes to the workbook.

Write in the business register (L1) defined in
[../../rules/language-register.md](../../rules/language-register.md): describe
requirements in the interviewee's domain language and observable outcomes. Do not
introduce schemas, identifiers, or implementation terms at intake.

## Guardrails

- Do not infer authority from the `.xlsx` format alone. Read the document-system
  authority matrix: an interview/control workbook may own business fields, while
  a published workbook may be a generated snapshot.
- Treat authored Excel business fields and visual annotations as authoritative
  when the matrix assigns them to Excel. Never treat generated contract cells as
  human-editable SSOT.
- Do not edit, resave, normalize, rename, move, or generate a replacement
  workbook.
- Treat layout, merged cells, hidden rows or sheets, comments, formulas, colors,
  and proximity as possible business meaning. Do not infer solely from flattened
  cell text.
- Separate confirmed requirements, assumptions, conflicts, and open questions.
  Never silently resolve ambiguity.
- Preserve existing `REQ-ID` and `SRC-ID` values. Never recycle identifiers.
- Do not start specification or implementation work.

## Workflow

1. **Resolve inputs and authority.** Require one `.xlsx` or `.xlsm` path. Read
   `docs/document-system/INDEX.md` and its authority links when present. Ask for an immutable
   source key if the default filename-derived key could collide. Reject legacy
   `.xls` rather than converting it.
2. **Locate document governance.** Classify the workbook as `Authored source`,
   `Controlled working copy`, or `Generated snapshot`. If governance is absent,
   record the classification as `Pending` and do not silently assign ownership.
   Use
   `docs/document-system/requirements/requirements-register.md` as the derived
   register path unless the arguments specify another path.
3. **Inspect structure read-only.** Run:

   ```bash
   python .claude/skills/intake/scripts/inspect_workbook.py "<workbook>" \
     --source-key "<key>" --pretty
   ```

   Use `--sheet "<name>"` to narrow a large workbook. The script reports OOXML
   structure and raw values; it does not render Excel.
4. **Inspect visually.** Use an available spreadsheet viewer or workbook-capable
   tool to inspect relevant sheets, formatting, comments, charts, and displayed
   formula results. If visual inspection is unavailable, record that limitation
   and do not claim visual semantics were verified.
5. **Build source records.** For every candidate requirement, record
   `source_file`, `sheet`, `row`, `cell` or range, and deterministic `SRC-ID`
   using [references/requirements-contract.md](references/requirements-contract.md).
6. **Normalize without rewriting intent.** For authored business fields, assign
   stable `REQ-ID` values; for generated snapshots, retain existing IDs and trace
   back to their declared canonical source. Capture
   the requirement statement, rationale, priority if stated, acceptance criteria,
   assumptions, conflicts, and questions. Quote only short source fragments.
7. **Reconcile.** Link duplicate or conflicting source records instead of
   deleting them. Ask the responsible owner to resolve material product
   conflicts in the authoritative source or explicitly approve a derived
   interpretation.
8. **Write the derived register.** Preserve unrelated content and existing IDs.
   Mark its status `Draft` or `Review`; never `Approved` without explicit human
   approval.
9. **Report evidence.** State workbook hash, sheets inspected structurally and
   visually, output path, counts by status, unresolved questions, and any
   unsupported workbook features.

## Seed the requirement decisions

Alongside the derived register, seed or update the project's requirements
tracker (`requirements_tracker.xlsx`, sheet ①需求決策 — the requirement-decision
authority; see `docs/document-system/workbook-guide.md`). Create one `DEC-*` row
per requirement candidate carrying the business-language VOC. Leave the
owner-decision columns — priority, scope in/out, milestone, business acceptance,
核准 — **empty or marked pending owner input**. Never auto-derive or guess these;
they are the product owner's decisions and pre-filling them defeats the
intake→specify boundary.

## Human Gate

Stop after producing the draft register and seeded decision rows. Present
conflicts, assumptions, and questions for review. From the Pilot stage onward,
continue to `/specify` only after the owner-approval checklist in
`VibeCoding_Workflow_Templates/_meta/workflow_manual.md` §8 — the single
authority for this gate — passes; in the prototype stage a skeleton `DEC-*` row
is enough.

## Completion

- The workbook hash is unchanged before and after inspection, and its authority
  classification is recorded.
- Every derived requirement has at least one source location or is explicitly
  labeled `Derived`.
- Assumptions and questions are not presented as approved facts.
- The register can trace `source location → SRC-ID → REQ-ID`.
