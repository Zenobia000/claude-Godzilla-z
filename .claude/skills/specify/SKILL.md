---
name: specify
description: Generate or minimally update PRD, BDD, SAD, ADR, and traceability artifacts from approved requirements while preserving document status, ownership, and source links.
disable-model-invocation: true
argument-hint: "<approved-requirements> [--artifacts prd,bdd,sad,adr,srs,brd,api,db,lld,ui,traceability] [--update]"
---

# Specify Approved Requirements

Treat `$ARGUMENTS` as the approved requirement scope, requested artifact set, and
update mode. This action writes specifications, not production code.

This action is the bridge register (L2) in
[../../rules/language-register.md](../../rules/language-register.md): it is the
only legal channel translating business language (L1) into engineering language
(L3). State each business term beside its engineering ID, and never let an
engineering artifact assert business intent that no source ID backs.

**Thinking mode** (see [../../rules/thinking-boundary.md](../../rules/thinking-boundary.md)).
Architectural judgment (VOC→FR/NFR translation, component/design/tech trade-offs)
is a user growth area. **速通 is the default**: recommend one option plus a
one-line trade-off for a fast human pick, keep it lean, and defer exhaustive
regulatory/permission/edge-case analysis to a later production-bound pass. Switch
to **深思 mode only when the user asks** — then do not auto-translate or
auto-decide: present options with trade-offs and the key open questions, let the
human make the call, and record it as an ADR. At a clearly high-risk or
irreversible point you may ask once whether to go 深思, but do not switch on your
own.

## Inputs and authority

1. Read `docs/document-system/INDEX.md` when present, then only the approved
   requirements and directly related artifacts.
2. If the document system does not exist, follow
   [references/document-contract.md](references/document-contract.md) and create
   only the paths required by this invocation.
3. **Hard gate — owner requirement decisions (binds from the Pilot stage).**
   Before engineering any in-scope item, walk the release checklist in
   `VibeCoding_Workflow_Templates/_meta/workflow_manual.md` §8 — the single
   authority for this gate — against the requirements tracker
   (`requirements_tracker.xlsx` ①需求決策／③Gate). Requirement decisions are
   the product owner's; never auto-derive or infer them to get past the gate.
   If any checklist item fails, stop and route back to the owner. A draft
   register may be summarized, but it must not be converted into an approved
   specification. In the prototype stage the gate relaxes to "a skeleton
   `DEC-*` row exists" — do not block fast iteration with approval ceremony
   before the project reaches Pilot.
4. Follow the field-level authority matrix. Preserve authored Excel business
   fields and visual annotations; treat generated workbook cells as projections
   of their declared canonical source. Never edit source workbooks.

## Template routing

Route through `VibeCoding_Workflow_Templates/INDEX.md` — the folder taxonomy
mirrors the Word documentation guide, so pick templates by the layer the gap
lives in. Core set for most invocations:

- PRD (problem, scope, FR/NFR, ACPT in Given/When/Then):
  `VibeCoding_Workflow_Templates/01_requirements/prd.md`
- SAD: `VibeCoding_Workflow_Templates/03_architecture/sad.md`
- ADR: `VibeCoding_Workflow_Templates/03_architecture/adr.md`
- Mode and gates: `VibeCoding_Workflow_Templates/_meta/workflow_manual.md`

Add by risk and affected contracts: `srs`/`brd` (formal or process-heavy
requirements), `api_spec`+`openapi.yaml` (interface contracts), `db_design`
(schema), `lld` (code map and state machines, AS-BUILT),
`ux_research_and_journey`/`information_architecture`/`ui_spec`
(UX/IA/UI), `test_plan`/`uat_plan` (formal acceptance),
`deployment_and_operations`/`runbook` (ops). The bundle
stops at these Pilot-core 15; enterprise documents (NFR, SDS, event
spec/AsyncAPI, monitoring, postmortem, WBS/CR/release notes) have no bundled
template — create them per the Word guide only when the project actually
needs them.

Do not copy an entire template. Retain only sections justified by the approved
scope, risks, NFRs, or existing document convention.

## Workflow

1. **Select artifacts.** Default to the smallest artifact set named in the
   arguments. If none is named, propose the set and wait for confirmation.
2. **Check consistency.** Identify missing acceptance behavior, conflicting
   requirements, unknown NFRs, or decisions without an owner. Stop affected work
   rather than choosing silently.
3. **Write or update PRD.** Map approved `DEC-*`/`REQ-ID` decisions to stable
   engineering `FR-*` and `NFR-*` IDs, and write those `FR-*`/`NFR-*` back into the
   Requirement Decision Record's `對應工程ID` column to keep `DEC → FR/NFR`
   traceable. Define problem, users, goals, non-goals,
   scope, measurable success, and observable `ACPT-*` results. Keep
   implementation choices out.
4. **Derive BDD.** Write scenarios in the format defined by
   [references/bdd-format.md](references/bdd-format.md). Map each scenario to
   `FR/NFR` and `ACPT-ID`. Cover the primary path plus applicable boundary,
   failure, permission, and idempotency behavior. Avoid internal classes,
   tables, or UI controls.
5. **Design SAD.** Trace components, interfaces, data ownership, deployment,
   failure handling, privacy, security, reliability, and migration decisions to
   requirements or NFRs. Separate current, transition, and target states.
6. **Record ADRs.** Create one ADR per significant durable decision. Use
   `Proposed` until the named decision owner explicitly accepts it; link
   superseded decisions.
7. **Update traceability.** Maintain
   `SRC-ID → REQ-ID → FR/NFR → ACPT → SCN → SAD element/ADR`. Do not leave new approved
   behavior untraced.
8. **Update the document index.** Record path, purpose, owner, status, revision,
   and replacement links without creating a second source of truth.
9. **Review the diff.** Check links, placeholders, status claims, contradictions,
   and unrequested scope.

## Human Gate

Present changed artifacts, decisions, assumptions, and unresolved questions.
Only the responsible human may move a document or decision to `Approved` or
`Accepted`. Do not start `/deliver` until the relevant PRD/BDD/SAD and required
ADRs are approved.

## Completion

- Every new statement is traced to approved input or labeled as a proposal.
- BDD and SAD do not invent product scope.
- ADR status reflects actual human decisions.
- Traceability and `docs/document-system/INDEX.md` agree with the artifacts.
