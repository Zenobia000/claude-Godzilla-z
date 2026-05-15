# Tier 1 — Decisions

> Append-only. Each entry captures a moment of architectural judgment that future-self (and future-AI) needs to honor or knowingly override.

## What lives here

- ADRs (Architecture Decision Records) — one file per decision, numbered
- Architecture overviews — the C4 / DDD level snapshots that ADRs reference

## What does NOT live here

- Implementation details → tier 2 (contracts) or tier 5 (views)
- Process for *making* decisions → tier 3 (process)
- Open questions that haven't been resolved → tier 4 (exploration)

## How AI should use this tier

**Read before proposing architectural changes.** ADRs encode the team's history with each tradeoff — proposing a solution that was already rejected (and the reasons captured here) is the single most common form of AI slop.

When generating new ADRs, AI should:
1. Search this directory first for related prior decisions
2. Reference superseded ADRs explicitly (`Supersedes: ADR-0007`)
3. Never silently contradict an Accepted ADR — escalate to the human

## How humans should maintain this tier

- ADRs are **immutable once Accepted**. To change a decision, write a new ADR that supersedes the old one
- Never delete ADRs, even Rejected or Superseded ones — they preserve the rationale trail
- Number sequentially (ADR-0001, ADR-0002, …); never reuse numbers

## Files

| File | Purpose |
|---|---|
| `ADR-0000-adr.template.md` | Single-decision record (status, context, decision, consequences) |
| `ADR-0001-frontend-template-tier-realignment.md` | Decision record for splitting monolithic frontend-architecture.template.md into 6 tier-aligned files |
| `ARCH-0000-architecture-overview.template.md` | C4 / DDD level architecture snapshot |
| `ARCH-0001-module-boundary.template.md` | Per-module charter — what it owns, what it explicitly does NOT own, dependencies, ACL with neighbors. **Critical for ERP** (prevents god-modules) |
| `ARCH-0002-frontend-tech-stack.template.md` | Frontend technology stack decision record (framework, state management, styling) |
| `ARCH-0003-infra-architecture.template.md` | Infrastructure architecture — VPC topology, compute scaling, IaC strategy, secrets management, DR. **Profile: `platform-infra`** |
| `DDD-0000-domain-model.template.md` | Per-bounded-context DDD model — aggregate roots, entities, value objects, invariants, ERD, domain events. **Critical for ERP** (accounting model is the foundation) |

## Frontmatter Schema

All files in this tier MUST carry this frontmatter:

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | YES | string | `ADR-NNNN`, `ARCH-NNNN`, or `DDD-NNNN` |
| `title` | YES | string | Human-readable title |
| `status` | YES | enum | `draft` / `active` / `deprecated` / `superseded` |
| `tier` | YES | const | `1-decisions` |
| `owner` | YES | enum | `HUMAN-ONLY` / `HYBRID` / `AI-AUTO` |
| `last-reviewed` | YES | date | `YYYY-MM-DD` |
| `date` | YES | date | Decision date |
| `decider` | YES | string | Person or team |
| `product-version` | opt | string | Product version this doc applies to |
| `supersedes` | opt | string | ID of predecessor |
| `superseded-by` | opt | string | ID of successor |
