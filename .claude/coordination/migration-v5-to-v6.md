# Migration Guide — VibeCoding Templates v5.x → v6.0

> **What changed**: 71 templates collapsed to 20 (-72%). Deleted templates merged into §sections of canonical templates.
>
> **Why**: v5.8 reached 84% contract coverage but onboarding took 2 days. v6.0 is the Linus-minimum convergence — readable in 30 min, AI no longer overwhelmed by cross-reference graph.

---

## TL;DR — what to do if you're a fork

1. **If you have NOT instantiated any templates yet** → just `git pull` and start from `BEDROCK.md`. Nothing to migrate.

2. **If you have instantiated v5.x templates in your project's `docs/`**:
   - Templates that survived to v6.0 (`API`, `MC`, `FR`, `ARCH-0000`, `PRD`, `EDGE`, `QG`, `CIA`, `PRIN-0000/0001/0003`, `ADR`) — keep your instances; the v6.0 templates are supersets.
   - Templates that were deleted — use this mapping table to find which v6.0 §section to migrate content into.

3. **AI assistants**: invoke `sunnydata-contract-stack-audit` skill to verify your instantiated set still satisfies the 10-layer map after migration.

---

## Mapping table — 51 deleted templates and where they went

### Tier 0 (2 deleted)

| v5.x file | v6.0 location |
|---|---|
| `GLOS-0000-glossary.template.md` | `PRIN-0000 §terminology (§4)` |
| `PRIN-0002-frontend-quality-attributes.template.md` | `PRIN-0000 §quality-bars (§6.1-§6.5)` |

### Tier 1 (4 deleted)

| v5.x file | v6.0 location |
|---|---|
| `ARCH-0001-module-boundary.template.md` | `ARCH-0000 §modules (§2)` |
| `ARCH-0002-frontend-tech-stack.template.md` | `ARCH-0000 §stack (§4)` + `ARCH-0000 §frontend (§6)` |
| `ARCH-0003-infra-architecture.template.md` | `ARCH-0000 §infrastructure (§5)` |
| `DDD-0000-domain-model.template.md` | `ARCH-0000 §domain-model (§3)` |
| `ADR-0001-frontend-template-tier-realignment.md` | archived (historical) |

### Tier 2 (22 deleted)

| v5.x file | v6.0 location |
|---|---|
| `BF-0000-flow-business.template.md` | `FLOW-0000 §1 BF` (instance-numbered: `FLOW-NNNN-<slug>.md` with §1 marker) |
| `UF-0000-flow-user.template.md` | `FLOW-0000 §2 UF` |
| `SF-0000-flow-sub.template.md` | `FLOW-0000 §3 SF` |
| `ERR-0000-error-envelope.template.md` | `API-0000 §6 Problem schema + error code registry` |
| `ASYNC-0000-async-api.template.md` + `.example.asyncapi.yaml` | `API-0000 §7 Async API` |
| `SM-0000-state-machine.template.md` | `MC-0000 §3 state-machine` |
| `SM-0000-state-machine.example.xstate.json` | renamed to `MC-0000-module-contract.example.xstate.json` (kept as MC sibling) |
| `PC-0000-page-contract.template.md` | `FR-0000 §page-contract` (appended) |
| `MDS-0000-master-data.template.md` | `DATA-0000 §1 master-data` |
| `MIG-0000-schema-migration.template.md` + `.example.alembic-env.py` | `DATA-0000 §2 migration` (example dropped; restore from git if needed) |
| `PIPE-0000-pipeline-contract.template.md` | `DATA-0000 §3 pipeline` |
| `MODEL-0000-model-card.template.md` | `DATA-0000 §4 model-card` |
| `PROMPT-0000-prompt-contract.template.md` | `AI-0000 §1 prompt` |
| `AGENT-0000-agent-contract.template.md` | `AI-0000 §2 agent` |
| `RAG-0000-retrieval-architecture.template.md` | `AI-0000 §3 rag` |
| `AISAFE-0000-ai-safety-policy.template.md` | `AI-0000 §4 safety` |
| `AICAP-0000-ai-capacity.template.md` | `AI-0000 §5 capacity` |
| `SLO-0000-slo-spec.template.md` | `SRE-0000 §1 slo` |
| `OBS-0000-observability-spec.template.md` | `SRE-0000 §2 observability` |
| `CAP-0000-capacity-planning.template.md` | `SRE-0000 §3 capacity` |
| `POL-0000-policy-as-code.template.md` + `.example.rego` | `ARCH-0000 §8 security` (Rego example dropped) |
| `DS-0000-frontend-design-system.template.md` + `.example.style-dictionary.json` | `ARCH-0000 §6 frontend` (Style Dictionary example dropped) |
| `FI-0000-flow-index.template.md` | Removed — regenerate via `sunnydata-auto-regen flow-index` |
| `TM-0000-traceability-matrix.template.md` | Removed — regenerate via `sunnydata-auto-regen traceability` |
| `UE-0000-unit-economics.template.md` | `PRIN-0000 §unit-economics (§5)` |
| `PERS-0000-persona.template.md` | `PRD-0000 §personas (§2)` |
| `EST-0000-capacity-estimation.template.md` | `ARCH-0000 §capacity-estimation (§7)` |
| `CT-0000-contract-test.template.md` | `TEST-0000 §3 contract` |

### Tier 3 (14 deleted)

| v5.x file | v6.0 location |
|---|---|
| `PROC-0001-workflow-manual.md` | `PROC-0001-developer-handbook.template.md §2 workflow` (rewritten) |
| `PROC-0002-bdd-guide.md` | `PROC-0001 §5 bdd` + `TEST-0000 §4 bdd` |
| `PROC-0003-code-review-checklist.md` | `PROC-0001 §3 code-review` |
| `PROC-0004-security-readiness-checklist.md` | `PROC-0001 §4 security-review` |
| `PROC-0007-vendor-api-test.template.md` | `API-0000 §vendor-test (callout)` |
| `PROC-0008-frontend-pre-merge.template.md` | `PROC-0001 §3 code-review` |
| `ONBOARD-0000-team-onboarding.template.md` | `PROC-0001 §1 onboarding` |
| `PROC-0005-deployment-runbook.template.md` | `PROC-0002 §1 deploy` |
| `PROC-0006-docs-maintenance-guide.md` | `PROC-0002 §6 docs-maintenance` |
| `PROC-0009-incident-response.template.md` | `PROC-0002 §3 incident` |
| `PROC-0010-chaos-engineering.template.md` | `PROC-0002 §4 chaos` |
| `PROC-0011-gitops-runbook.template.md` | `PROC-0002 §2 gitops` |
| `PROC-0012-deprecation-playbook.template.md` | `PROC-0002 §5 deprecation` |
| `TP-0000-test-plan.template.md` | `TEST-0000` (entire doc reorganized) |
| `LLMEVAL-0000-eval-harness.template.md` | `TEST-0000 §5 llm-eval` |

### Tier 4 (7 deleted)

| v5.x file | v6.0 location |
|---|---|
| `DISC-0000-discovery-research.template.md` | `PRD-0000 §1 discovery` |
| `EXP-0000-experiment-log.template.md` | `TEST-0000 §6 experiment` (works for ML AND product) |
| `ABT-0000-ab-test.template.md` | `PRD-0000 §5 experiments` + `TEST-0000 §6 experiment` |
| `GTM-0000-go-to-market.template.md` | `PRD-0000 §6 launch` |
| `RM-0000-roadmap.template.md` | `PLAN-0000 §1 roadmap` |
| `WBS-0000-wbs.template.md` | `PLAN-0000 §2 wbs` |
| `EST-0000-capacity-estimation.template.md` (already in tier 2 above) | `ARCH-0000 §7 capacity-estimation` |

### Tier 5 (4 deleted — entire directory)

| v5.x file | v6.0 replacement |
|---|---|
| `VIEW-0001-project-structure.template.md` | `sunnydata-auto-regen project-structure` |
| `VIEW-0002-file-dependencies.template.md` | `sunnydata-auto-regen file-dependencies` |
| `VIEW-0003-class-relationships.template.md` | `sunnydata-auto-regen class-graph` |
| `VIEW-0004-frontend-route-map.template.md` | `sunnydata-auto-regen frontend-routes` |

---

## ID prefix changes (PRIN-0001)

**Retired prefixes**: BF, UF, SF, GLOS, DDD, MDS, MIG, PIPE, MODEL, ERR, ASYNC, SLO, OBS, CAP, POL, DS, FI, TM, PROMPT, AGENT, RAG, AISAFE, AICAP, PERS, UE, EST, CT, LLMEVAL, ONBOARD, TP, DISC, EXP, ABT, GTM, RM, WBS, VIEW, SM, PC.

**Kept prefixes (15)**: PRIN, ARCH, ADR, FLOW (new), API, MC, FR, DATA (new), AI (new), SRE (new), EDGE, PROC, QG, TEST (new), CIG, PRD, PLAN (new), CIA.

Sub-prefixes that survive *as ID references* (no standalone files): BF, UF, SF (within FLOW §1/§2/§3), TC (in test files), CR (in 4-exploration), PC (in FR §section), SM (in MC §section).

---

## Skills updated

The following skills had references to retired templates and were updated to point to v6.0:

- `sunnydata-contract-stack-audit` — checks new 20-template canon
- `sunnydata-flow-audit` — looks for FLOW-NNNN instances (was BF/UF/SF separately)
- `sunnydata-doc-freshness` — same logic, fewer template paths to scan
- `sunnydata-auto-regen` — same outputs; replaces tier-5 files

The 14 `vibecoding-write-*` skills mostly remain useful but reference §sections now (e.g. `vibecoding-write-api-contract` now produces API-NNNN with §async + §errors inline).

---

## Verification after migration

```
# Check structure
ls VibeCoding_Workflow_Templates/0-principles/    # expect 3 files + README
ls VibeCoding_Workflow_Templates/1-decisions/     # expect 2 files + README
ls VibeCoding_Workflow_Templates/2-contracts/     # expect 8 files + README + xstate sibling
ls VibeCoding_Workflow_Templates/3-process/       # expect 4 files + ci-gates/ + README
ls VibeCoding_Workflow_Templates/4-exploration/   # expect 3 files + README

# No tier-5
test ! -d VibeCoding_Workflow_Templates/5-views/  # should be true

# Total canonical templates
find VibeCoding_Workflow_Templates -name "*.template.md" -o -name "QG-0000*.md" -o -name "PRIN-000*.md" -o -name "ADR-0000*.md" | wc -l
# expected: 20 (or 21 if you count the xstate JSON sibling)
```

---

## What if you depended on a deleted template's URL?

v6.0 is a clean break (per user instruction). v5.x files do NOT remain as `status: deprecated` redirects. If your bookmarks / external docs / Slack threads link to deleted templates, they 404.

Recommended: search-and-replace in your team's wiki / Notion / Confluence using the table above.

---

## Need to revert?

The v5.8 state lives at git tag `v5.8` (if your fork tagged it). Run:

```bash
git checkout v5.8 -- VibeCoding_Workflow_Templates/
```

Then re-do the v5→v6 mapping manually for the templates you want.
