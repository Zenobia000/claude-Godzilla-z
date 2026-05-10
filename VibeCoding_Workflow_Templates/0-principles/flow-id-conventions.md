# Flow ID Naming Conventions

> **Stability tier**: `0-principles` (highest). This is a project-wide naming invariant — once adopted, every Flow / Spec / API / Test / Decision artifact uses these IDs forever.
>
> **Why**: large systems can't use names like "the order flow" — front-stage? back-stage? payment? cancellation? Without IDs, traceability is impossible and AI cannot reliably reference what it changed.

---

## The 9 prefixes

| Prefix | Meaning | Lives in (typical) | Lifetime |
|---|---|---|---|
| **BF** | Business Flow | `docs/2-contracts/flow-business.<id>.md` | Long-lived; major rewrite is rare |
| **UF** | User / Role Flow | `docs/2-contracts/flow-user.<id>.md` | Medium; changes with feature evolution |
| **SF** | Sub Flow (reusable) | `docs/2-contracts/flow-sub.<id>.md` | Medium; shared across BF/UF |
| **FR** | Functional Requirement | `docs/2-contracts/fr.<id>.md` or grouped | Per-release |
| **NFR** | Non-Functional Requirement | `docs/0-principles/` (or grouped) | Long-lived |
| **API** | API Endpoint | `docs/2-contracts/api/openapi.yaml#operationId` | Tracks contract changes |
| **TC** | Test Case | tests/ source files; tracked in `traceability-matrix` | Per-feature |
| **ADR** | Architecture Decision Record | `docs/1-decisions/ADR-NNNN-*.md` | Append-only |
| **CR** | Change Request | `docs/4-exploration/CR-NNNN-*.md` | Per-change ephemeral |

---

## Numbering rules

- **4-digit zero-padded sequential**: `BF-0001`, `UF-0042`, `ADR-0007`
- **Sequential per prefix**, never reused, never renumbered
- **Numbers are immutable**; if you delete an artifact, the number is retired (don't reuse)
- **First-class IDs**: BF, UF, SF, ADR, CR. **Derived IDs**: FR, API, TC may use sub-numbering (e.g. `FR-0001.1`) when grouped

## Title format

Each artifact's title in the file uses both ID and human-readable name:

```markdown
# BF-0001: Order to Cash
```

Filenames mirror this: `flow-business.0001-order-to-cash.md`

## Cross-reference syntax

When one artifact references another, always use the ID:

- ✅ "Triggered by `BF-0001`"
- ✅ "Implements `FR-0023`, validated by `TC-0145`, exposed as `API-0008`"
- ❌ "Used in the order flow" *(which one?)*

In code comments and commit messages, the same convention:
```python
# Implements UF-0012 (admin review order)
```
```
fix(payment): handle duplicate callback per SF-0003 idempotency rule
```

---

## When a new ID is required

Allocate a new ID **before** writing the artifact. The allocation step is:

1. Open the relevant `<prefix>-INDEX.md` file (one per prefix, lives in same dir as the artifacts)
2. Take the next sequential number
3. Reserve it by adding the row (status: `draft`)
4. Write the artifact file using the reserved ID

This prevents the "two PRs allocated the same number" race.

---

## When IDs are NOT required

Tier 5 derived views (project-structure, dependency graph, class diagram) **do not** need Flow IDs — they're snapshots of code, not contracts. Their generators reference the source code directly.

Tier 0 product principles **do not** need IDs — they're a single document per project, not enumerated artifacts.

Tier 4 exploration drafts (PRD, brainstorm) **do not** need IDs *while exploring*; only when promoted to a tier-1/2 artifact does it get an ID.

---

## Example chain

A real change cuts across many IDs:

```
CR-0042 "Support partial order cancellation"
  ↓ touches
BF-0001 (Order to Cash) — adds partial-cancel branch
  ↓ adds
UF-0007 (Customer cancel order) — modifies main flow
  ↓ extracts
SF-0014 (Partial cancellation rule) — NEW reusable sub-flow
  ↓ requires
FR-0089 (Partial cancel calculation) — NEW functional rule
  ↓ exposed via
API-0034 (POST /orders/{id}/cancel) — schema change
  ↓ recorded as
ADR-0019 (Partial-cancel state machine choice)
  ↓ validated by
TC-0211 ~ TC-0218 (8 new test cases)
```

This chain becomes one row in `traceability-matrix.template.md`.

---

## See also

- `2-contracts/flow-business.template.md` — BF template
- `2-contracts/flow-user.template.md` — UF template
- `2-contracts/flow-sub.template.md` — SF template
- `2-contracts/traceability-matrix.template.md` — the Flow ID consumer
- `1-decisions/adr.template.md` — ADR template
- `4-exploration/change-impact-analysis.template.md` — CR-driven analysis using these IDs
