# Ownership Matrix — Human vs AI Division of Labor

> **Why this exists**: 52 templates is a lot. Human architects shouldn't have to fill all of them. This matrix tells you **which files demand a human decision**, **which AI drafts and you approve**, and **which AI auto-manages without you ever opening them**.
>
> **Reading rule**: focus your attention on 🟥 HUMAN-ONLY files first. 🟨 HYBRID files come to you when AI proposes. 🟩 AI-AUTO files you should rarely if ever open.

---

## The 3 ownership modes

| Mode | Who creates | Who edits | Human action required |
|---|---|---|---|
| 🟥 **HUMAN-ONLY** | Human | Human | Always — these are decisions / governance / strategy |
| 🟨 **HYBRID** (AI-DRAFTS, HUMAN-APPROVES) | AI | AI drafts → Human reviews + commits | Approve / amend / reject |
| 🟩 **AI-AUTO** | AI | AI regenerates from source | None (read when curious) |

---

## Per-file ownership

### 🟥 HUMAN-ONLY (23 files) — your real workload

These encode strategy / governance / domain knowledge. AI must not silently modify them.

| File | Why human-only |
|---|---|
| `0-principles/PRIN-0000-product-principles.template.md` | Mission, non-goals — strategic invariants |
| `0-principles/PRIN-0001-flow-id-conventions.md` | Naming convention — once set, immutable |
| `0-principles/GLOS-0000-glossary.template.md` | Business terminology — definitional |
| `0-principles/PRIN-0002-frontend-quality-attributes.template.md` | Quality bars — performance/a11y/browser support targets |
| `1-decisions/ARCH-0001-module-boundary.template.md` | Architectural charter — what each module owns / does NOT own |
| `1-decisions/DDD-0000-domain-model.template.md` | DDD model — aggregate boundaries, invariants |
| `1-decisions/ARCH-0002-frontend-tech-stack.template.md` | Framework / build tooling choice |
| `2-contracts/MDS-0000-master-data.template.md` | Master data governance — DQ rules, lifecycle, GDPR |
| `3-process/PROC-0001-workflow-manual.md` | Process choice — full vs MVP mode |
| `3-process/PROC-0002-bdd-guide.md` | Methodology |
| `3-process/PROC-0003-code-review-checklist.md` | Process gate |
| `3-process/PROC-0004-security-readiness-checklist.md` | Pre-launch gate |
| `3-process/PROC-0005-deployment-runbook.template.md` | Ops procedures — humans run these |
| `3-process/PROC-0006-docs-maintenance-guide.md` | Process |
| `3-process/QG-0000-quality-gates.md` | Stage prerequisites — gate definition |
| `3-process/TP-0000-test-plan.template.md` | Test strategy — coverage targets, risk areas |
| `3-process/PROC-0007-vendor-api-test.template.md` | Per-vendor decisions |
| `3-process/PROC-0008-frontend-pre-merge.template.md` | Gate |
| `3-process/PROC-0009-incident-response.template.md` | Incident severity + on-call + comms — org-specific decisions |
| `3-process/PROC-0010-chaos-engineering.template.md` | Game day scope + blast radius — requires human judgment |
| `3-process/PROC-0011-gitops-runbook.template.md` | Ops procedures — environment promotion policy |
| `3-process/PROC-0012-deprecation-playbook.template.md` | Sunset lifecycle — compatibility windows, migration paths |
| `3-process/ONBOARD-0000-team-onboarding.template.md` | Onboarding/offboarding — org-specific access, mentorship |

**Total decisions you own**: ~23 files for a typical project. Some you fill once (product-principles, glossary), some grow over time (one master-data-spec per master entity).

### 🟨 HYBRID (23 files) — AI proposes, you decide

AI drafts these from intent + context. You read, amend, approve. Once approved, they become contracts that AI must honor.

| File | AI's role | Your role | Trigger |
|---|---|---|---|
| `1-decisions/ADR-0000-adr.template.md` | Draft from CIA outcomes | Accept / Reject; once Accepted = append-only | After CR resolved |
| `1-decisions/ADR-0001-frontend-template-tier-realignment.md` | — (human-authored) | Append-only once accepted | — |
| `1-decisions/ARCH-0000-architecture-overview.template.md` | Maintain C4 / DDD diagrams | Accept structural changes | Quarterly or per major feature |
| `2-contracts/API-0000-api-spec.template.md` | Generate from code (code-first) or scaffold from intent (contract-first) | Approve schema, error codes | Per endpoint change |
| `2-contracts/MC-0000-module-contract.template.md` | Generate DbC pre/post-conditions from code | Approve invariants | Per module |
| `2-contracts/BF-0000-flow-business.template.md` | Draft BF from intent | Approve actors, scope, exception flow | Per business capability |
| `2-contracts/UF-0000-flow-user.template.md` | Draft UF from BF | Approve actor flow, AC | Per user-facing feature |
| `2-contracts/SF-0000-flow-sub.template.md` | Extract reusable sub-flow | Approve idempotency, side effects | When 2+ flows share logic |
| `2-contracts/FR-0000-functional-requirement.template.md` | Draft FR rules + AC | Approve MUST/SHALL rules | Per business rule |
| `2-contracts/SM-0000-state-machine.template.md` | Draft state catalog + transitions | Approve forbidden transitions | Per stateful entity |
| `2-contracts/PC-0000-page-contract.template.md` | Draft from route + component scan | Approve auth, data sources | Per route |
| `2-contracts/DS-0000-frontend-design-system.template.md` | Generate token tables from CSS / Figma export | Approve component contracts | Per design system change |
| `4-exploration/PRD-0000-prd.template.md` | Draft from brief | Approve scope, metrics | Per feature |
| `4-exploration/WBS-0000-wbs.template.md` | Draft from PRD | Approve sequencing | Per sprint/release |
| `4-exploration/CIA-0000-change-impact-analysis.template.md` | Generate §1-§7 (affected artifacts, suggested order) | **Decide §8 (Human Decisions Required)** — AI cannot proceed without your decisions | Auto-fired by CIA gate |
| `1-decisions/ARCH-0003-infra-architecture.template.md` | Draft VPC / compute / IaC / DR sections from infra scan | Approve network topology, scaling policy, DR tier | Per infra change |
| `2-contracts/SLO-0000-slo-spec.template.md` | Draft SLI definitions + burn-rate alerts from metrics | Approve SLO targets, error budget policy | Per service |
| `2-contracts/PIPE-0000-pipeline-contract.template.md` | Draft pipeline I/O schema + DQ gates from code | Approve SLA, blast radius, DQ thresholds | Per pipeline |
| `2-contracts/MODEL-0000-model-card.template.md` | Draft model metrics + lineage from training artifacts | Approve bias analysis, deployment constraints | Per model version |
| `4-exploration/EXP-0000-experiment-log.template.md` | Draft hypothesis + metrics from experiment config | Approve experiment design, success criteria | Per experiment |
| `2-contracts/OBS-0000-observability-spec.template.md` | Draft metrics/logs/traces spec from infra scan | Approve retention policy, alerting strategy | Per service |
| `2-contracts/CAP-0000-capacity-planning.template.md` | Draft resource model + cost projection from cloud billing | Approve budget thresholds, scaling policy | Quarterly |
| `4-exploration/DISC-0000-discovery-research.template.md` | Draft hypotheses + competitive analysis from brief | Approve research design, go/no-go criteria | Per feature discovery |

**Your action when AI proposes**: read the diff, check §8 if CIA, accept or amend.

### 🟩 AI-AUTO (6 files) — you almost never open these

AI regenerates these from authoritative sources. They are **caches**, not source of truth. If you find yourself hand-editing one, the regeneration tooling is missing — file an issue, don't keep editing.

| File | Source of truth | Regenerated by |
|---|---|---|
| `2-contracts/FI-0000-flow-index.template.md` | Frontmatter scan of all `flow-*.md` files | `sunnydata-auto-regen` skill |
| `2-contracts/TM-0000-traceability-matrix.template.md` | Cross-reference of Flow ID mentions across docs + tests | `sunnydata-auto-regen` skill |
| `5-views/VIEW-0001-project-structure.template.md` | `tree` / `eza --tree` of `src/` | `sunnydata-auto-regen` skill |
| `5-views/VIEW-0002-file-dependencies.template.md` | Language-specific (`pyan` / `madge` / `go list`) | `sunnydata-auto-regen` skill |
| `5-views/VIEW-0003-class-relationships.template.md` | UML extractor or AI full-read | `sunnydata-auto-regen` skill |
| `5-views/VIEW-0004-frontend-route-map.template.md` | Router config + component graph | `sunnydata-auto-regen` skill |

**Your action**: never. If you need a current view, run `sunnydata-auto-regen` skill. AI handles the rest.

---

## What you actually do — the cockpit view

### Daily (when working on a feature)
- Open the relevant **🟥 product-principles** to remind yourself of constraints
- Open the relevant **🟥 module-boundary** for the module you're touching
- AI invokes **🟨 sunnydata-change-impact-analysis** if needed
  - You read the CIA, decide §8, approve §9 implementation order
- AI proposes **🟨 hybrid contracts** as it implements
  - You review the diff before AI commits
- AI runs **🟩 sunnydata-flow-audit** weekly to catch decay (no action needed unless red)

### Weekly (maintenance)
- Run `sunnydata-doc-freshness` — fix any STALE / SUPERSEDED rows it surfaces
- Run `sunnydata-flow-audit` — fix any BROKEN_REF / LAYERING_VIOLATION
- Run `sunnydata-auto-regen` — refresh tier-5 views and aggregation indices

### Per-project (one-time setup)
- Fill **🟥 product-principles** (mission, non-goals, quality bars)
- Fill **🟥 glossary** (5-10 core terms; grows over time)
- Fill **🟥 module-boundary** for each module (1 doc per module)
- Decide **🟥 quality-gates** policy (defaults usually fine)

### Per-quarter (stewardship)
- Review **🟥 architecture-overview** for drift
- Review **🟥 master-data-specification** for governance changes
- Review **🟥 vendor-api-test-requirement** for vendor SLA changes

---

## What AI auto-handles for you (you may not even notice)

| Mechanism | Triggered when | What it does |
|---|---|---|
| `post-write` hook | Any Write/Edit on tier-2 doc | Updates `last-synced-with` and `synced-at` frontmatter automatically |
| `change-governance` rule | AI about to mutate code touching flow/contract/data/architecture | Forces CIA before code changes |
| `sunnydata-doc-freshness` skill | On-demand | Reports stale / deprecated / superseded contract docs |
| `sunnydata-flow-audit` skill | On-demand or weekly | Catches broken refs, orphans, layering violations, index drift |
| `sunnydata-auto-regen` skill | On-demand or after refactor | Regenerates 🟩 AI-AUTO files (flow-index, traceability, 5-views) |

You don't run these manually unless asked. AI invokes them by trigger words or at natural breakpoints.

---

## Anti-patterns to refuse

| Anti-pattern | Why bad | Correct behavior |
|---|---|---|
| AI silently editing 🟥 HUMAN-ONLY files | Steals your decisions | AI must propose change as a CR + ADR, get your approval |
| Human hand-editing 🟩 AI-AUTO files | Edits get overwritten next regen | Run regen instead; if it produces wrong output, fix the generator |
| Skipping §8 of a CIA "to save time" | Defeats the gate's purpose | CIA without decisions = no implementation |
| Editing accepted ADR | Loses history | Write new ADR with `supersedes: ADR-NNNN` |

---

## TL;DR — three lines

1. **You touch ~23 🟥 HUMAN-ONLY files** (strategy, governance, decisions). That's your real cockpit.
2. **AI proposes ~23 🟨 HYBRID files** for your approval. Read the diff, decide, commit.
3. **AI auto-manages 6 🟩 AI-AUTO files** invisibly. Never hand-edit them.

If a file isn't in this matrix, it's a guide / README / index — read once, refer occasionally, don't fill.

---

## See also

- `INDEX.md` — full template catalog
- `HOW-TO-INSTANTIATE.md` — recommended `docs/` layout for end-user projects
- `.claude/rules/change-governance.md` — when CIA must fire
- `.claude/skills/sunnydata-auto-regen/SKILL.md` — how 🟩 AI-AUTO regeneration works
- `.claude/skills/sunnydata-flow-audit/SKILL.md` — Flow ID consistency monitoring
- `.claude/skills/sunnydata-doc-freshness/SKILL.md` — tier-2 contract drift monitoring
