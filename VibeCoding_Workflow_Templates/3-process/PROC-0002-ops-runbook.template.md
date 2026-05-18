---
id: PROC-0002
title: "Ops Runbook — Deploy / GitOps / Incident / Chaos / Deprecation"
status: active
tier: 3-process
owner: HUMAN-ONLY
essence: specialized
specialty: ops-production
absorbs: [PROC-0005-deploy, PROC-0006-docs, PROC-0009-incident, PROC-0010-chaos, PROC-0011-gitops, PROC-0012-deprecation]
last-reviewed: null
---

# PROC-0002: Ops Runbook

> **Tier**: 3-process · **Essence**: specialized — required when serving production traffic. Solo dev / dev-only projects can skip.
>
> **One runbook, five sections** — read on-call rotation start; refer back when alerts fire.

---

## §1 — Deploy (§deploy)

### §1.1 Environments

| Env | Purpose | Promotion source |
|---|---|---|
| `dev` | Engineer's local | — |
| `staging` | Mirror of prod (smaller); E2E target | merge to `main` |
| `prod` | Real traffic | tag `vX.Y.Z` |

### §1.2 Release flow

```
PR merged to main
  ↓
CI runs: tests, lint, security scan, contract tests (CIG-*)
  ↓
Auto-deploy to staging
  ↓
Smoke tests on staging (5min)
  ↓
Manual approval → tag vX.Y.Z
  ↓
Production deploy (rolling / blue-green / canary — choose one per service)
  ↓
Post-deploy health check (15min)
  ↓
Auto-rollback if SLO burn > 2× normal
```

### §1.3 Strategy by service tier

| Tier | Strategy | Rollback time |
|---|---|---|
| T0 (revenue-critical) | Canary 1% → 10% → 100% over 30min | < 5min |
| T1 (user-facing) | Blue-green | < 10min |
| T2 (internal) | Rolling | < 15min |
| T3 (batch) | Recreate | next run |

### §1.4 Pre-deploy checklist

- [ ] CHANGELOG updated (per `sunnydata-changelog-sync` skill)
- [ ] All `CIG-*` workflows green
- [ ] `QG-0000 Gate 5` passes (release-ready)
- [ ] On-call notified (Slack #deploys with link to changelog)
- [ ] No customer-facing migration in this window without `CR-NNNN`
- [ ] Rollback plan stated (which previous tag?)

### §1.5 Forbidden

- Friday deploy after 14:00 local (you wreck the weekend)
- Deploy during incident (one fire at a time)
- Skip staging unless emergency hotfix with documented approver
- Manual SQL on production (everything is migration)

---

## §2 — GitOps (§gitops)

### §2.1 Pattern

```
Source of truth = git repo (`infra/` or separate `*-infra` repo)
  ↓
ArgoCD / Flux watches repo
  ↓
Drift detection: cluster state vs git
  ↓
Auto-sync OR manual approval (per environment)
```

### §2.2 Environment promotion

```
PR to infra-repo: bump image tag in staging/values.yaml
  ↓ auto-sync
staging applies
  ↓ smoke OK
PR: bump tag in prod/values.yaml
  ↓ manual approval gate
prod applies
```

### §2.3 Drift detection

| Drift | Detection | Response |
|---|---|---|
| Manual kubectl edit | ArgoCD sync status: out-of-sync | Auto-revert OR alert (per env policy) |
| Secret rotated outside git | Vault diff alert | Update git ref to new secret name |
| Resource manually scaled | HPA shows ≠ desired | Investigate; either update git or accept HPA |

### §2.4 Forbidden

- `kubectl apply` directly in prod (always via git)
- Editing live resources for "quick fixes" (drift compounds)
- Sealed secrets not committed (Vault has its own ref; commit the ref)

---

## §3 — Incident response (§incident)

### §3.1 Severity ladder

| SEV | Definition | Response | Postmortem |
|---|---|---|---|
| **SEV-1** | Customer-impacting outage; revenue loss; security breach | Page primary + secondary; war room within 15min | < 48h, public |
| **SEV-2** | Major degradation; some users impacted; data integrity risk | Page primary; war room within 1h | < 1wk, internal |
| **SEV-3** | Minor degradation; workaround exists | Notify in #ops; fix next business day | Optional |
| **SEV-4** | Cosmetic / non-customer | Ticket; sprint backlog | None |

### §3.2 War room protocol

1. **Incident commander** (IC) declared — owns coordination, NOT debugging
2. **Comms lead** — owns external comms (status page, customer support)
3. **Eng investigators** — debug; do NOT update status page
4. **Scribe** — Slack thread; every action timestamped

```
12:03 SEV-1 declared — payment success rate dropped to 0%
12:04 IC: @alice. Comms: @bob. Eng: @carol, @dave
12:05 Status page updated: "Investigating issue with payments"
12:08 Carol: Stripe webhook receiving but processor failing on validation
12:12 Dave: rolled back to v3.4.1 — success rate recovering
12:18 Recovery confirmed; status page: "Resolved"
12:20 IC declares stand-down. Postmortem scheduled for tomorrow.
```

### §3.3 Communication discipline

| Audience | Channel | Cadence |
|---|---|---|
| Customers | Status page | Initial < 15min, updates every 30min |
| Internal eng | Slack #incident-NNN | Continuous |
| Leadership | Slack DM from IC | At declaration + every 1h |
| Affected customers (post) | Email | Within 24h with RCA summary |

### §3.4 Postmortem format

| Section | Content |
|---|---|
| Summary | 1 paragraph what happened |
| Timeline | Every notable event timestamped |
| Root cause | "5 whys" — go deep |
| What went well | Recovery patterns to keep |
| What went poorly | Process / tool / human factors |
| Action items | Specific, owned, dated; tracked to closure |
| Detection gap? | Why did this not alert sooner? → new alert / metric |
| EDGE row | Add to relevant `EDGE-NNNN` catalog |

**Blameless** — focus on systems, not people. The system let humans make the mistake; fix the system.

### §3.5 On-call rotation

| Property | Value |
|---|---|
| Rotation length | 1 week |
| Primary + secondary | Two engineers per rotation |
| Handoff | Friday EOD; documented in #ops |
| Compensation | TOIL or stipend (org policy) |
| Carry pager | Yes; offline-acknowledge possible |

---

## §4 — Chaos engineering (§chaos)

### §4.1 Why

Test failure modes **before** they happen for real. The first time you discover the failover doesn't work is during a real outage; the second time is during chaos day.

### §4.2 Game day cadence

| Frequency | Scope | Blast radius |
|---|---|---|
| Monthly | One service in staging | Staging only |
| Quarterly | One service in prod (off-hours) | <5% traffic |
| Annually | Full DR exercise | Full prod (announced window) |

### §4.3 Pre-game-day

- [ ] Document hypothesis ("if X fails, Y should happen because Z")
- [ ] Blast radius: which services / which % of traffic
- [ ] Abort criteria ("if real-customer error rate > 1%, abort")
- [ ] Rollback plan (1-button)
- [ ] Stakeholders notified

### §4.4 Common experiments

| Experiment | Hypothesis | Success criterion |
|---|---|---|
| Kill primary DB | RR promoted; reads unaffected | < 30s RTO |
| Drop region us-east-1 | us-west-2 absorbs traffic | < 1% error spike |
| Network partition between services | Circuit breaker engages | No cascading failure |
| 10× traffic spike | Auto-scaler keeps up | p99 < 2× target |
| Disk fills | Alerts fire; cleanup auto-runs | Manual action < 30min |

### §4.5 Forbidden

- Chaos experiment during active incident
- Chaos in prod without rollback button
- Repeating same experiment monthly (test new failure modes)

---

## §5 — Deprecation (§deprecation)

### §5.1 When to deprecate

| Trigger | Action |
|---|---|
| New version supersedes old | Deprecate old immediately on new release |
| Vendor sunsets dependency | Plan migration > sunset date |
| Compliance requires removal | Deadline = compliance date |
| < 5% usage of feature | Consider; not automatic |
| Tech debt only | Don't deprecate; refactor |

### §5.2 Compatibility windows

| Audience | Minimum notice |
|---|---|
| Internal API | 30 days |
| External API (public) | 6 months (more if SLA) |
| SDK | 12 months for 2 major versions back |
| Data format | 12 months (let users export/migrate) |

### §5.3 Sunset checklist

- [ ] Deprecation announced (changelog, status page, email to users)
- [ ] Deprecated endpoints emit `Sunset` HTTP header + log warning
- [ ] Migration guide written (in `docs/migration/<feature>.md`)
- [ ] Usage telemetry tracked; alert when usage drops to plan-removable level
- [ ] Final cutoff date set + communicated
- [ ] On cutoff: return `410 Gone` with migration link
- [ ] After 30d grace: remove code
- [ ] `EDGE-NNNN` row added for "expected `410 Gone` after <date>"

### §5.4 Data retention on deprecation

| Data class | Retention after deprecation |
|---|---|
| Audit logs | per `DATA-NNNN §master-data §retention` |
| User-generated content | Provide export; delete after 90d post-cutoff |
| Configuration | Archive; delete after 1y |
| Telemetry | Aggregate to 5-views; raw deleted after 30d |

---

## §6 — Docs maintenance (§docs-maintenance)

### §6.1 Sync discipline

- `tier-2/` contracts MUST update `last-synced-with` frontmatter on source change
- `post-write` hook auto-updates timestamp
- `sunnydata-doc-freshness` skill weekly catches drift
- `CIG-0007` blocks PR if source moved but contract didn't

### §6.2 Generated docs (auto-regen)

Tier-5 used to exist; now removed. Generation on demand via `sunnydata-auto-regen`:

| What | Source | Command |
|---|---|---|
| Flow index | frontmatter scan | `sunnydata-auto-regen flow-index` |
| Traceability matrix | flow + test refs | `sunnydata-auto-regen traceability` |
| Project structure | `tree src/` | `sunnydata-auto-regen project-structure` |
| Class relationships | AST extraction | `sunnydata-auto-regen class-graph` |
| Frontend routes | router config | `sunnydata-auto-regen frontend-routes` |

These are outputs, not artifacts — never hand-edit.

### §6.3 Release notes

Use `sunnydata-changelog-sync` skill. Conventional Commits drive section structure; ADRs + CRs feed the "What changed" body.

---

## §7 — Anti-patterns

| Anti-pattern | Why bad | Fix |
|---|---|---|
| Friday deploy | Weekend = no eyes | §1.5 forbidden |
| Manual prod edit | Drift; unreproducible | GitOps everything |
| SEV-1 declared by eng only | Comms miss; customer rage | IC + Comms roles split |
| Blameful postmortem | Engineers hide problems | §3.4 blameless rule |
| Chaos without abort criteria | Real outage masqueraded as drill | §4.3 mandatory |
| Deprecation < 30d notice | Customers churn out of anger | §5.2 minimums |
| "We'll write the runbook later" | First incident = no plan | This template IS the runbook |
| One-person on-call | Burnout; single point of failure | §3.5 primary + secondary |

---

## See also

- `BEDROCK.md` — onboarding entry point
- `2-contracts/SRE-0000-reliability.template.md` — SLO + observability + capacity
- `2-contracts/API-0000-api-spec.template.md` — wire surface
- `2-contracts/DATA-0000-data-contract.template.md` §migration — schema change procedures
- `3-process/PROC-0001-developer-handbook.template.md` §security — pre-deploy security
- `3-process/QG-0000-quality-gates.md` Gate 5 — release-ready
- `3-process/TEST-0000-testing-strategy.template.md` — load testing feeds §4 chaos
- `4-exploration/CIA-0000-change-impact-analysis.template.md` — change governance
