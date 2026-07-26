# Document-system contract

Load this reference when `docs/document-system` is absent or its index does not
define an equivalent convention.

## Conventional paths

Engineering documents follow the Word guide's ch15 folder layout (the same
taxonomy as `VibeCoding_Workflow_Templates/`); the document-system folder holds
only the meta layer (index, register, traceability, evidence):

```text
docs/
├── document-system/
│   ├── INDEX.md
│   ├── requirements/
│   │   └── requirements-register.md
│   ├── traceability.md
│   └── verification/            # evidence records
├── 01_requirements/             # prd, brd, srs, requirements tracker
├── 02_ux_ui/                    # ux research, information architecture, ui specs
├── 03_architecture/             # sad, adr/ADR-NNNN-*
├── 04_design/                   # api spec, openapi-*.yaml, db designs
├── 05_qa/                       # test plans, uat, qa tracker
└── 06_ops/                      # deployment, runbooks

Enterprise layers (00_strategy, 07_release, NFR/SDS/monitoring docs) are added
per the Word guide only when the project reaches that stage.
```

Create only required files and directories — the folders are a taxonomy, not a
quota. Existing repository conventions take precedence when `INDEX.md`
identifies them.

## Status model

- Requirements and specifications: `Draft → Review → Approved → Superseded`
- ADRs: `Proposed → Accepted → Superseded` or `Rejected`
- Only an identified responsible human may approve or accept.
- Record owner, status, revision date, source links, and replacement link.

## Artifact responsibilities

- **Requirements register:** workbook-derived facts, provenance, acceptance,
  assumptions, conflicts, and questions.
- **PRD:** problem, users, scope, goals, non-goals, outcomes, and product
  requirements; no component or framework design.
- **BDD:** observable examples derived from approved acceptance behavior.
- **SAD:** boundaries, responsibilities, interfaces, data ownership, deployment,
  quality attributes, failure handling, and migration.
- **ADR:** one durable technical decision, alternatives, rationale, and
  consequences.
- **Traceability:** joins the artifacts; it is not a second requirements source.

## Traceability row

The canonical full ID chain is `docs/document-system/architecture.md` §7.1.
Each traceability row records the project-visible span of that chain:

```text
SRC-ID(s) → REQ-ID → FR/NFR → ACPT-ID → Feature/SCN-ID
          → SAD element → ADR → delivery slice/task
          → code/test/evidence → status
```

Use `N/A` with a reason instead of leaving a link silently blank. Preserve
historical rows when an artifact is superseded.

## Conflict ownership

There is no single global ranking across product intent, technical decisions,
contracts, and evidence:

- Product/Business owns approved product behavior, scope, and acceptance.
- An Accepted ADR owns a technical decision within approved behavior and
  constraints; it cannot silently redefine product behavior.
- Approved SAD and interface contracts own the technical contract only after
  the relevant product and architecture decisions are accepted.
- Implementation and tests record observed reality and verification evidence;
  they do not rewrite approved intent merely by disagreeing with it.

When artifacts owned by different responsible parties conflict, stop only the
affected work, record the conflict and source locators, and ask those owners to
resolve it. Do not repair a cross-owner conflict by silently editing a
lower-level artifact.
