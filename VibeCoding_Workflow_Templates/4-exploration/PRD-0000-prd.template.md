---
id: PRD-0000
title: "Product Requirements Document — Discovery / Personas / Spec / Experiments / Launch"
status: active
tier: 4-exploration
owner: HYBRID
essence: specialized
absorbs: [DISC-0000-discovery-research, PERS-0000-persona-section, ABT-0000-ab-test, GTM-0000-go-to-market]
created: null
target-release: null
product-version: null
supersedes: null
superseded-by: null
---

# PRD-NNNN: Product Requirements Document

> **Tier**: 4-exploration · **Essence**: specialized — one PRD per feature; archived after launch.
>
> **One PRD, five sections** — write top-down: discover the problem (§1), define who you're solving for (§2), spec the solution (§3-§4), plan experiments (§5), prepare the launch (§6). Skip sections that don't apply (e.g. no §5 experiments if the feature isn't worth A/B-ing).

---

## §0 — Identity

| Field | Value |
|---|---|
| ID | `PRD-NNNN` |
| Title | Human-readable (≤ 7 words) |
| Status | `draft` / `accepted` / `shipped` / `archived` |
| Owner | PM + lead engineer + designer |
| Target release | `vX.Y.Z` or `2026-Q3` |
| Roadmap reference | `PLAN-NNNN §roadmap §1.2 Now` (which item this PRD implements) |
| Personas targeted | `PERS-NNNN` (in §2) |

---

## §1 — Discovery (§discovery, absorbs DISC-0000)

> Why we believe this feature is worth building. Fill before §3 solution.

### §1.1 Problem statement (1 paragraph)

What pain are we addressing? Who experiences it? How often? What's the cost of NOT addressing it?

Example: *"Support tickets pile up overnight. Our `PERS-0001` Alex (solo founder) wakes to 30 unread tickets and loses 2h every morning. We lose 12% of trial signups in the first week to slow first-response. Estimated revenue impact: $40k/yr."*

### §1.2 Hypotheses (≤ 3)

Format: "If we `<change>`, then `<metric>` will `<direction>` by `<magnitude>`, because `<causal story>`."

| ID | Hypothesis | Confidence | Evidence |
|---|---|---|---|
| H1 | If we triage tickets automatically with AI, then p50 first-response time will drop from 4h to 12min, because `PERS-0001` mentioned this pain in 7 of 8 interviews | Med-High | `docs/research/2026-04-interview-notes.md` |
| H2 | If triage is accurate to 92%, users will trust AI-drafted replies, because trust scales with predictability | Med | competitive analysis |

### §1.3 Competitive analysis

| Competitor | What they do | Where they fall short |
|---|---|---|
| Intercom Fin | Generic LLM over KB | Doesn't read YOUR KB; enterprise pricing |
| Zendesk AI | Triage + routing | $$$; over-engineered for solo founder |
| Email rules (status quo) | Free | Doesn't scale; no learning |

### §1.4 Opportunity sizing

| Metric | Today | Realistic target | Optimistic |
|---|---|---|---|
| Affected customers (paying) | 850 (60% of base) | 700 will adopt | 850 |
| Revenue impact | $0 retention lift | +$8k MRR / qtr | +$15k MRR / qtr |
| CAC payback shift | 3.7mo | 3.2mo | 2.9mo |

### §1.5 Research notes

| Date | Method | Participants | Key takeaway |
|---|---|---|---|
| 2026-04-10 | User interviews | 8 | Sleep-loss is THE pain |
| 2026-04-14 | Survey | 142 respondents | 78% would pay $20+ extra for this |

---

## §2 — Personas (§personas, absorbs PERS-0000)

> Who specifically benefits. Reference `PRIN-0000 §2` for global persona catalog; this PRD might serve a subset.

### §2.1 Primary persona for this feature

| Field | Value |
|---|---|
| ID | `PERS-0001 Alex the Solo Founder` |
| Segment size | 35% of MAU |
| Why this feature | JTBD-1: "midnight tickets → sleep" |
| Reachability | indie maker communities + Twitter |

### §2.2 Secondary persona

| ID | When relevant |
|---|---|
| `PERS-0002 Sara the Support Lead` | Small-team plan; uses triage at scale |

### §2.3 Anti-persona (NOT designing for)

`PERS-anti-001 Enterprise IT admin` — features they want (SSO, on-prem) are explicitly `PRIN-0000 §3` non-goal.

### §2.4 JTBD this feature serves

| JTBD ID | Job statement | Priority |
|---|---|---|
| JTBD-1 | "When tickets come in overnight, I want them triaged automatically, so I can sleep" | Must |
| JTBD-2 | "When I open the app, I want urgent tickets at the top, so I focus on impact" | Should |

---

## §3 — Spec (§spec)

### §3.1 What we're building (1 paragraph)

> The user-facing description in plain English. No buzzwords.

Example: *"Smart triage v2: when a support ticket arrives, AI reads it + relevant KB articles, classifies severity (P0-P3), drafts a suggested reply, and routes urgent tickets to the on-call queue. User can accept the draft, edit, or override classification."*

### §3.2 User stories + acceptance criteria

| US ID | Story (As / I want / So that) | Acceptance criteria | Linked artifacts |
|---|---|---|---|
| US-001 | As a solo founder, I want incoming tickets auto-classified, so I see urgent ones first | (1) New ticket arrives → severity set within 10s · (2) Severity visible in inbox · (3) Confidence < 0.4 → flagged for human | `FR-NNNN`, `AI-NNNN §prompt`, `TC-NNNN .feature` |
| US-002 | As a support lead, I want to override AI classification, so I trust the system | (1) Override button visible · (2) Override logged · (3) Override feeds back into eval dataset | `FR-NNNN+1`, `AI-NNNN §eval` |

Each AC is a testable statement → maps 1:1 to a Gherkin scenario in `TEST-NNNN §bdd`.

### §3.3 Scope & boundary

| In scope | Out of scope (this PRD) |
|---|---|
| Inbound email tickets | Voice / SMS channels |
| English + Traditional Chinese | Other languages (next PRD) |
| Severity P0-P3 + needs_human | Custom user-defined severity (deferred) |

### §3.4 Non-functional requirements

| Dimension | Requirement |
|---|---|
| Latency | p95 < 4s ticket-to-classification |
| Cost | $0.012 per ticket avg; budget $2k/mo (`AI-NNNN §capacity §5.2`) |
| Accuracy | Severity within ±1 level ≥ 95% (`AI-NNNN §eval §6`) |
| Adversarial | 100% block on prompt-injection eval set |
| Accessibility | Per `PRIN-0000 §6.4` |

### §3.5 Frontend IA (page contract pointer)

This feature touches pages `PC-A12 Inbox` + `PC-A14 Ticket Detail` — see `FR-NNNN §page-contract` per page.

### §3.6 Open questions

| ID | Question | Decision date | Decided |
|---|---|---|---|
| Q-001 | Auto-reply or draft-only? | 2026-05-20 | Draft-only for v1; auto-reply behind flag |
| Q-002 | How to handle multilingual training data? | 2026-05-25 | Pending |

---

## §4 — Risks & dependencies

| Risk | Likelihood | Mitigation |
|---|---|---|
| AI hallucinates customer ID | Med | Schema validation rejects unknown IDs; see `AI-NNNN §1.4` |
| Cost spike from verbose tickets | Med | Per-call token cap `AI-NNNN §5.1` |
| LLM provider outage | Low | Fallback model in `AI-NNNN §5.3` |
| PERS-0001 distrust ("AI is hype") | Med | Citations + audit trail visible in UI |

### Dependencies

- `AI-NNNN` capacity reserved $2k/mo  ← REQUIRED before launch
- KB indexed via `AI-NNNN §rag` — corpus must reach 90%+ coverage of common categories
- `API-NNNN` ticket-create endpoint must add `severity` field — see `CR-NNNN`

---

## §5 — Experiments (§experiments, absorbs ABT-0000)

> Use for any change worth A/B-testing. Skip for clearly-good additions (e.g. accessibility fixes).

### §5.1 Pre-registered hypothesis

> If we ship Smart triage v2, then p50 first-response time will drop ≥ 50% (4h → 2h or better), because automated classification removes the morning triage step.

Falsifiable: if p50 drops < 25% OR support-ticket NPS drops, hypothesis rejected.

### §5.2 Variants

| Variant | Description | Allocation |
|---|---|---|
| Control | Manual triage (current) | 50% |
| Treatment | Smart triage v2 active | 50% |

### §5.3 Primary metric (one)

`first_response_time_p50` measured over 7-day window post-treatment-exposure.

### §5.4 Guardrails (must not regress)

| Metric | Threshold |
|---|---|
| Support NPS | -3 points max |
| Misclassification rate | < 8% |
| Refund-rate | + 0% (false positive triage doesn't hurt revenue) |

### §5.5 Sample size + duration

| Variable | Value |
|---|---|
| Baseline | p50 = 4h |
| MDE | 25% relative |
| α / 1-β | 0.05 / 0.80 |
| N per arm | 850 customers ≈ 28d at current adoption |

### §5.6 Decision rule

| Result | Action |
|---|---|
| Treatment wins; guardrails pass; CI lower > 25% | Ship 100% |
| Inconclusive | Hold; iterate on prompt; do NOT retest same idea for 90 days |
| Guardrail breach | Ship control; investigate root cause |

Full methodology in `TEST-NNNN §experiment`.

---

## §6 — Launch (§launch, absorbs GTM-0000)

> Use when the feature is customer-visible. Skip for internal/infra features.

### §6.1 Positioning

| Field | Value |
|---|---|
| Category | "AI support triage" (NOT "AI for support" — too broad) |
| For whom | `PERS-0001` + `PERS-0002` |
| Versus status quo | Manual triage + email rules |
| Versus alternative | Intercom Fin / Zendesk AI (enterprise; expensive) |
| Unique credible claim | "Triage that reads YOUR KB — not generic LLM" |

### §6.2 Messaging

**Tagline** (≤ 8 words): "Triage tickets while you sleep."

**Hero copy** (≤ 3 sentences): "Stop waking up to 30 unread tickets. AI reads your KB, drafts replies, and wakes you only for urgent ones. Setup in 10 minutes; no card required."

**3 proof points** (concrete, citable):
1. "Triaged 12,000 tickets last week across 40 customers" (live counter)
2. "Cuts p50 first-response from 4h to 12min" (case study `caseStudy/acme.md`)
3. "Reads YOUR KB, not generic LLM — citations on every reply" (screenshot)

**Do NOT say**: "revolutionary", "powered by GPT-4", vague "AI-powered", feature-war comparisons we'd lose.

### §6.3 Channels (≤ 4, named owners)

| Channel | Cost | Owner | Expected outcome |
|---|---|---|---|
| Product Hunt launch | $0 + 2d prep | @growth | 200 trial, 30 paying in 30d |
| HN Show HN | $0 + 4h prep | @founder | 50-500 signups |
| Existing customer email (upgrade pitch) | $0 | @growth | 60 Starter → Pro |
| Targeted Google Ads | $4k/mo | @growth | CAC $80, 50 conv |

Forbidden: "let's do all channels."

### §6.4 Launch checklist (T-minus)

| T-minus | Item | Owner | ☐ |
|---|---|---|---|
| 30d | Landing page live + A/B variants | @design | ☐ |
| 14d | Case study published | @content | ☐ |
| 7d | Onboarding tested E2E with 3 alpha customers | @product | ☐ |
| 7d | Support team trained on top-10 FAQ | @support | ☐ |
| 3d | Status page + on-call ready for spike | @ops | ☐ |
| 3d | `SRE-NNNN` dashboards live for launch metrics | @data | ☐ |
| 0d | Launch — PH 12:01 PT; HN 09:00 PT next day | @founder | ☐ |
| +1d | Daily metrics review begins | @growth | ☐ |

### §6.5 Launch metrics

| Metric | T+1d | T+30d |
|---|---|---|
| Signups | 500 | 2,000 |
| Activated (used triage ≥ 1×) | 200 | 1,200 |
| Trial → paid | n/a | 12% |
| Net new ARR | n/a | $15k |
| Support ticket volume (internal) | < 50/d | < 80/d |

### §6.6 Post-launch retro (T+30d)

To be filled at T+30d:
- §5 experiment results
- §6.5 hit vs missed
- Which channel actually drove signups (often surprises)
- Customer feedback themes (feeds next `PRD-NNNN+1`)

---

## §7 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| §3 spec before §1-§2 | Solving wrong problem | Top-down order |
| AC like "should work" | Untestable | One ACTION + one ASSERTION per AC |
| 10 KPIs as "success metrics" | Optimize one, break two | One primary in §5.3 |
| §6 launch checklist with no owners | Falls through | Every row has @owner |
| "We'll measure later" | No post-mortem possible | §6.5 mandatory targets |
| §5 experiment "until significant" | Type-I rate → 30% | Pre-register §5.5 |
| Generic persona "user" | AI defaults to median; misses targets | §2 specific `PERS-NNNN` |

---

## See also

- `0-principles/PRIN-0000-product-principles.template.md` — §2 personas + §5 unit economics + §3 non-goals
- `4-exploration/PLAN-0000-planning.template.md` — roadmap horizon containing this PRD
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — if PRD scope changes mid-flight
- `2-contracts/FR-0000-functional-requirement.template.md` — §3.2 ACs map to FRs
- `2-contracts/AI-0000-ai-system-contract.template.md` — §3 AI implementation
- `2-contracts/SRE-0000-reliability.template.md` — §3.4 SLO ops; §6.5 dashboards
- `3-process/TEST-0000-testing-strategy.template.md` §experiment — §5 methodology
