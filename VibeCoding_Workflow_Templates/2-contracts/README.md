# Tier 2 — Contracts

> The boundary layer. Documents here describe **interfaces between systems, modules, or teams** — and they MUST stay synchronized with code.

## What lives here

- API specifications (OpenAPI, GraphQL schema)
- Module contracts (Design-by-Contract, public function signatures, invariants)
- Data schemas (DB tables, message envelopes, file formats)

## What does NOT live here

- Internal implementation → tier 5 (views, derivable from code)
- Why we chose this contract shape → tier 1 (decisions)
- Workflow for evolving a contract → tier 3 (process)

## How AI should use this tier

These documents are either **source-of-truth** (contract-first projects) or **mirror-of-truth** (code-first projects).

**Always check the `sync-source` frontmatter** of the instance file:
- `sync-source: doc` → the doc is authoritative, code follows
- `sync-source: code` → the code is authoritative, doc may be stale

When in doubt, run the `/check-doc-freshness` skill before treating a contract doc as ground truth.

## How humans should maintain this tier

Every instance file in `docs/2-contracts/` MUST carry frontmatter:

```yaml
---
last-synced-with: <git-commit-sha>   # the HEAD when this doc was last verified
sync-source: code | doc              # which side is authoritative
source-paths:                        # the code paths this contract describes
  - src/api/users.py
  - src/models/user.py
synced-at: 2026-05-10
---
```

The `post-write` hook updates `last-synced-with` and `synced-at` automatically when you edit the file. The `/check-doc-freshness` skill compares `last-synced-with` against the latest commit on each `source-path` and warns if the source has moved on.

## Files

| File | Purpose |
|---|---|
| `api-spec.template.md` | REST/GraphQL API contract (endpoints, schemas, errors, versioning) |
| `module-contract.template.md` | Module/class public contract (DbC pre/post-conditions, invariants, test cases) |
