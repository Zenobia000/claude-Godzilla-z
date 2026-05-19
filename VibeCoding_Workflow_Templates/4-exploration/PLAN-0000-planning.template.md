---
id: PLAN-0000
title: "Planning — Roadmap + WBS"
status: active
tier: 4-exploration
owner: HYBRID
essence: specialized
absorbs: [RM-0000, WBS-0000]
last-updated: null
horizon-end: null
---

# PLAN-NNNN: Planning (Roadmap + WBS)

> **Tier**: 4-exploration · **Essence**: specialized — re-issued quarterly; archived after horizon-end.
>
> **Two horizons, one document**: §roadmap is the **outside view** (Now/Next/Later by theme); §wbs is the **inside view** (current quarter's items broken into tasks). They live together because they answer the same question at different zoom levels: "what are we doing and when?"

---

## §1 — Roadmap (§roadmap)

### §1.1 Horizon model

| Horizon | Window | Commitment | Detail |
|---|---|---|---|
| **Now** | This quarter (0–3 mo) | Building; PRD + WBS exist | Feature-level |
| **Next** | Next quarter (3–6 mo) | Intent; PRD drafted | Theme-level |
| **Later** | 6–12 mo | Direction; may change | Outcome-level only |
| **Not doing** | — | Explicit non-commitments | Sentence per item |

Item movement is one-way: Later → Next → Now. Backwards movement (Now → Next) is a re-prioritization event; document the reason in §1.5 change log.

### §1.2 Now horizon

| Item | Outcome (measurable) | Owner | Confidence | PRD |
|---|---|---|---|---|
| Smart triage v2 | p50 ticket resolution 4h → 2h | @support-eng | High | `PRD-NNNN` |
| Self-serve billing | billing tickets -30% | @billing | Med | `PRD-NNNN+1` |
| Mobile push | dormant reactivation 4.5%→5.0% | @growth | Med | `PRD-NNNN+2` |

### §1.3 Next horizon

| Theme | Outcome (hypothesis) | Likely owner | PRD status |
|---|---|---|---|
| Workspace collaboration | Multi-user editing on shared docs | @platform | Draft |
| AI knowledge assistant | KB search → conversational | @ai-team | Draft |

### §1.4 Later horizon (direction only)

| Outcome | Hypothesis |
|---|---|
| Enterprise SSO + audit | Unlocks $200k+ contracts (5 deals blocked) |
| Cross-region deploy | <100ms latency APAC; currently 350ms |

### §1.5 Not doing (explicit non-commitments)

| Item | Why not |
|---|---|
| Native mobile apps | Web responsive is 92% of mobile usage; native ROI undefined |
| Marketplace plugins | <50 enterprise customers; premature |
| On-prem | Eng cost > revenue ceiling at current size |

### §1.6 Outcome metrics format

Every Now-horizon item declares:
```
<metric>: <current_baseline> → <target> by <date>
```

A Now item with no measurable outcome → rejected; rewrite or demote.

### §1.7 Risk class

| Class | Probability | When to use |
|---|---|---|
| **Commitment** | > 80% | External promises; SLA-grade |
| **Initiative** | 50–80% | Planned; subject to discovery |
| **Bet** | < 50% | High variance; framed as experimental |

Healthy mix: 60% commitment / 30% initiative / 10% bet.

---

## §2 — Work Breakdown Structure (§wbs)

> Only fill for **Now-horizon items**. Past sprints archived; future sprints stub.

### §2.1 Item structure

```
EPIC: Smart triage v2 (linked to RM-NNNN Now §1.2 row 1)
├── Story: Triage classifier (5d)
│   ├── Task: Prompt design + eval datasets (2d) — @alice
│   ├── Task: Schema + retry loop (1d) — @alice
│   ├── Task: A/B against current rules (1d) — @bob
│   └── Task: Production rollout 10% → 100% (1d) — @bob
├── Story: Confidence-based handoff (3d)
│   ├── Task: Threshold tuning (1d) — @carol
│   └── Task: Human queue integration (2d) — @carol
└── Story: Operator dashboard (4d)
    └── Task: ... (etc)
```

### §2.2 Estimation rules

- **Days, not hours** — hours is false precision at planning level
- **Story = ≤ 5 days**; if larger, break into stories
- **Task = 0.5 to 2 days**; if larger, break into tasks
- **No 0.25-day estimates** — that's not planning, that's accounting

### §2.3 Capacity check

| Team | Headcount | Capacity (eng-weeks/q) | Allocated this quarter | Slack |
|---|---|---|---|---|
| Support eng | 4 | 48 | 38 | 10 (20%) |
| Billing | 3 | 36 | 32 | 4 (11%) — TIGHT |
| Growth | 2 | 24 | 18 | 6 (25%) |
| AI | 5 | 60 | 0 | 60 (ramping) |

**Rule**: allocated ≤ 80% of capacity. 20% slack absorbs: bugs, on-call, exploratory spikes, sick days.

Billing at 89% is overcommitted — either cut scope or accept Q-end slippage explicitly.

### §2.4 Dependencies

| Item | Depends on | Resolution date | Blocker? |
|---|---|---|---|
| Smart triage v2 | AI capacity budget `AI-NNNN §capacity` | 2026-06-01 | Resolved |
| Billing portal | Stripe v2 contract (`API-NNNN`) | 2026-06-15 | OPEN |
| AI KB assistant | RAG corpus complete | 2026-07-01 | OPEN (Next horizon) |

OPEN blockers on Now-horizon items → top of next standup.

### §2.5 Status (updated weekly)

| Item | % complete | Risk | Notes |
|---|---|---|---|
| Triage v2 | 60% | Green | Eval thresholds met; ramp this week |
| Billing portal | 30% | Yellow | Stripe API blocker; workaround in progress |
| Mobile push | 0% | Red | Headcount -1; demoted to Next |

---

## §3 — Cadence

| Cadence | Activity |
|---|---|
| Weekly | Owners report Now-horizon § progress against §1.6 metrics |
| Monthly | Trim Next horizon (move forward / push back) |
| Quarterly | Full re-issue — promote Later→Next, archive shipped Now items |

`last-updated` frontmatter bumps at every quarterly re-issue.

---

## §4 — Change log

| Date | Change | Reason |
|---|---|---|
| 2026-04-15 | Mobile push: Now → Next | Growth team -1 headcount |
| 2026-04-22 | AI KB assistant added to Next | `DISC` validated value |
| 2026-05-01 | On-prem added to Not-doing | Sales-eng review concluded |

---

## §5 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Roadmap = feature list | No outcomes; no commitment | §1.6 mandatory metrics |
| 100% commitments | Over-promised; team burns out | §1.7 mix 60/30/10 |
| 100% bets | Unsteerable; investors panic | Same §1.7 mix |
| Allocate at 100% capacity | First incident = quarter slips | §2.3 ≤80% rule |
| Hour-level WBS | False precision; rework constant | Days only §2.2 |
| Tasks no one owns | Drift; gets dropped | Every task @assignee |
| Status "looking good" | Vague = ungovernable | %, color (R/Y/G), specific blockers §2.5 |
| No "Not doing" section | Endless scope creep | §1.5 mandatory |
| Quarterly review skipped | Roadmap rots; team disengages | §3 cadence enforced |

---

## See also

- `PRD-0000-prd.template.md` — feature spec consumed by Now-horizon items
- `CIA-0000-change-impact-analysis.template.md` — mid-quarter scope changes
- `SRE-0000-reliability.template.md` §capacity — capacity feed informs §2.3
- `0-principles/PRIN-0000-product-principles.template.md` — north-star metric the roadmap serves
