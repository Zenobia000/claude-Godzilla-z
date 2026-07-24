# Requirements intake contract

Load this reference when creating or updating a derived requirements register.

## Authority

- Classify each workbook as `Authored source`, `Controlled working copy`, or
  `Generated snapshot`; file format alone does not establish authority.
- In an authored source, fields assigned to Excel by the authority matrix are
  the business and visual source of truth.
- In a generated snapshot, contract and derived cells project their declared
  Markdown, code, or evidence source and are not independently authoritative.
- The requirements register is a traceable, reviewable projection for delivery.
- A derived document never overwrites or silently corrects the workbook.
- Record workbook revisions by SHA-256 and inspection date.

## Source identity

Assign an immutable, project-unique `source_key` to each workbook. Prefer a short
business identifier such as `CRM-2026`; do not depend on a temporary upload name.

Create one identifier per source cell or anchor:

```text
SRC-{SOURCE_KEY}-{SHEET_KEY}-R{ROW}-C{COLUMN_NUMBER}
```

Example:

```text
source_file: 客戶系統需求.xlsx
sheet: 核心需求
row: 18
cell: D18
SRC-ID: SRC-CRM-2026-CORE-R18-C4
```

For a merged cell or range, keep one anchor `SRC-ID` and record the full range.
If one requirement has several sources, link all `SRC-ID` values. If a sheet is
renamed or rows move, preserve old IDs through an alias/history entry rather than
reusing them.

## Requirement identity

Use stable, never-recycled IDs:

```text
REQ-0001
ACPT-0001
```

Do not encode priority, state, or implementation module in `REQ-ID`; those
attributes change over time. New source evidence may link to an existing
requirement without changing its ID.

## Minimum register fields

| Field | Meaning |
| --- | --- |
| `REQ-ID` | Stable requirement identifier |
| Statement | Normalized user or business outcome |
| Rationale | Why it matters, when stated |
| Source | `SRC-ID` links plus file/sheet/row/cell or range |
| Kind | Functional, quality, constraint, business rule, or derived |
| Priority | Source-stated value or `Unspecified` |
| Status | Draft, Review, Approved, Rejected, or Superseded |
| Acceptance | Observable results with `ACPT-*` IDs |
| Assumptions | Unverified statements; never hidden in the requirement |
| Questions | Owner and resolution state |
| Conflicts | Other source or requirement IDs in tension |
| Revision | Workbook hash and last reconciliation date |

## Reconciliation rules

- Preserve source wording in a short excerpt only when it prevents semantic loss.
- Record one normalized requirement for one independently testable outcome.
- Link duplicates; do not discard their provenance.
- When an authoritative source and derived interpretation conflict, the
  authoritative source wins until its owner explicitly approves a correction.
- When a generated snapshot conflicts with its canonical source, report
  generator drift; do not overwrite the canonical source from the snapshot.
- Mark requirements `Approved` only with identifiable human approval evidence.
- Never treat color or layout as decoration until visually inspected.

## Script limitations

`inspect_workbook.py` reads OOXML structure, raw or cached values, formulas, style
IDs, merged ranges, and hidden structure. It does not render formatting, evaluate
formulas, interpret charts, inspect macros, or guarantee displayed date/number
formatting. Pair it with visual inspection.
