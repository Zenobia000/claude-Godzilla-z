---
name: sunnydata-contract-stack-audit
description: Audit the project's engineering contract stack (10 layers per PRIN-0003) for coverage gaps. Verifies (1) every layer has at least one contract doc, (2) every machine-readable contract has its sibling example file, (3) every layer is enforced by at least one CI gate. Composes sunnydata-flow-audit + sunnydata-doc-freshness with three unique checks they cannot do alone. Triggers on 'audit contract stack', 'check layer coverage', '稽核契約完整度', 'is the contract stack sealed', 'contract stack audit'. Reports only — does not modify files.
stability-tier: tooling
---

# Contract Stack Audit

## What this skill does

Walks the repo and answers: **"is this project's engineering contract stack actually wired, or are some L1–L5 layers floating without enforcement?"**

It runs three checks the existing audits cannot:

1. **Layer coverage** — every layer cell in `PRIN-0003-engineering-contract-stack.md §3` (19 cells: L1×3 + L2×4 + L3×4 + L4×4 + L5×4) must have at least one corresponding instance in `docs/2-contracts/` (or be explicitly waived in `HOW-TO-INSTANTIATE.md` per profile).
2. **Machine-readable presence** — every contract type that requires a sibling `.example.<format>` file (SM, DS, MIG, POL, ASYNC per PRIN-0003) must actually have it next to the markdown.
3. **CI gate wiring** — every layer cell that claims a `CIG-NNNN` in PRIN-0003 §3 must have a corresponding workflow file in `.github/workflows/` (or `3-process/ci-gates/` for the template repo).

It **delegates** the underlying ID-reference and freshness checks to:
- `sunnydata-flow-audit` — for orphan / broken-ref / layering violations (re-runs and includes summary)
- `sunnydata-doc-freshness` — for `last-synced-with` drift (re-runs and includes summary)

This skill **only reports**; it never modifies files. Remediation is delegated to `vibecoding-write-*` skills or human review.

## When to invoke

- **Release gate** — required by `QG-0000 Gate 5 — Release Ready` before tagging a release.
- Quarterly audits.
- Before adopting a new profile (`web-product` → `web-product + data-ml`) — ensures incoming layers are wired.
- After a major refactor that moved/renamed contracts.
- When `sunnydata-change-impact-analysis` produces a CR that adds a new layer instance — verify it didn't orphan an existing one.

## Procedure

1. **Load the layer map**: parse `VibeCoding_Workflow_Templates/0-principles/PRIN-0003-engineering-contract-stack.md §3` to extract the 19 layer cells. Each cell has: `layer_id` (e.g. `L1.1`), `template_id`, `machine_readable` (yes/no/N/A), `ci_gate` (`CIG-NNNN` or `none`).

2. **Load the profile**: parse `HOW-TO-INSTANTIATE.md` to find which layers are required for the project's selected profile. Layers waived by the profile are reported as `WAIVED`, not `MISSING`.

3. **Check #1 — Layer coverage**:
   - For each required cell, glob `docs/2-contracts/<prefix>-*.md` (excluding `-0000` templates).
   - At least one instance must exist with `status: active`.
   - Output: `LAYER_UNCOVERED` if zero instances; `LAYER_DRAFT` if only draft instances.

4. **Check #2 — Machine-readable presence**:
   - For each markdown file at `docs/2-contracts/SM-NNNN-*.md`, `DS-NNNN-*.md`, `MIG-NNNN-*.md`, `POL-NNNN-*.md`, `ASYNC-NNNN-*.md`, check the sibling `<ID>-<slug>.example.<format>.<ext>` exists.
   - Output: `MACHINE_READABLE_MISSING` if absent.

5. **Check #3 — CI gate wiring**:
   - For each cell claiming a `CIG-NNNN`, verify a workflow file matching the pattern exists either:
     - `.github/workflows/<name>.yml` for instantiated projects, OR
     - `3-process/ci-gates/CIG-NNNN-*.workflow.yml` for the template repo itself.
   - Output: `GATE_UNWIRED` if absent.

6. **Delegate #1 — Flow audit**:
   - Invoke `sunnydata-flow-audit` skill. Include its 5-class summary in this report.

7. **Delegate #2 — Doc freshness**:
   - Invoke `sunnydata-doc-freshness` skill. Include stale-doc summary in this report.

8. **Compose final report** in `audit.json` (machine-readable) + `audit.md` (human-readable).

## Output schema (`audit.json`)

```json
{
  "audited_at": "2026-05-16T14:00:00Z",
  "profile": "web-product",
  "summary": {
    "layers_total": 19,
    "layers_covered": 17,
    "layers_uncovered": 1,
    "layers_waived": 1,
    "machine_readable_total": 5,
    "machine_readable_present": 4,
    "ci_gates_total": 10,
    "ci_gates_wired": 9
  },
  "layers": [
    {
      "id": "L1.1",
      "name": "REST API",
      "template": "API-0000",
      "instances": ["API-0001", "API-0002"],
      "status": "COVERED",
      "machine_readable": "openapi.yaml present",
      "gates": ["CIG-0001", "CIG-0002", "CIG-0004"]
    }
    // ... 18 more
  ],
  "findings": [
    { "severity": "ERROR", "kind": "GATE_UNWIRED", "layer": "L3.1", "detail": "POL-0001 exists but CIG-0009 reverse-import-lint workflow not deployed" },
    { "severity": "WARNING", "kind": "MACHINE_READABLE_MISSING", "file": "docs/2-contracts/SM-0002-payment.md", "missing": "SM-0002-payment.example.xstate.json" }
  ],
  "delegated": {
    "flow_audit": { /* summary from sunnydata-flow-audit */ },
    "doc_freshness": { /* summary from sunnydata-doc-freshness */ }
  }
}
```

## Severity rules

| Severity | When |
|---|---|
| `ERROR` | Layer required by profile, no instance exists; OR claimed CI gate has no workflow file |
| `WARNING` | Machine-readable sibling missing; OR layer only has draft instances |
| `INFO` | Layer waived per profile (no action needed) |

## Anti-patterns this skill catches

- **"Spec without lint"** — `openapi.yaml` exists, `CIG-0001` workflow missing → `GATE_UNWIRED`
- **"Markdown SM with no xstate"** — `SM-0002.md` exists but `SM-0002.example.xstate.json` absent → `MACHINE_READABLE_MISSING`
- **"Layer claimed but uninstantiated"** — `PRIN-0003 §L3.1` says POL exists; no `POL-NNNN-*.md` matches → `LAYER_UNCOVERED`
- **"Profile incomplete"** — project selected `web-product` but skipped L5.4 design tokens → `LAYER_UNCOVERED` (not waived; profile requires it)
- **"Audit-skill recursion"** — this skill MUST NOT call itself; if a previous run's `audit.json` exists, treat as cache only

## What this skill is NOT

- Not a fixer — it doesn't write contracts. Use `vibecoding-write-*` skills for that.
- Not a code-quality checker — `sunnydata-code-review` owns that lane.
- Not a security audit — `sunnydata-security` owns that.

## Integration points

| Wired to | Where | When |
|---|---|---|
| `QG-0000 Gate 5` | `3-process/QG-0000-quality-gates.md` | Pre-release blocker |
| `change-governance.md` | rules | Auto-suggested after large CIA |
| `.github/workflows/release.yml` | release pipeline | Optional CI step |

## See also

- `VibeCoding_Workflow_Templates/0-principles/PRIN-0003-engineering-contract-stack.md` — the layer map this skill audits against
- `VibeCoding_Workflow_Templates/3-process/QG-0000-quality-gates.md` §Gate 5
- `VibeCoding_Workflow_Templates/3-process/ci-gates/README.md` — CIG inventory
- `.claude/skills/sunnydata-flow-audit/SKILL.md` — delegated flow audit
- `.claude/skills/sunnydata-doc-freshness/SKILL.md` — delegated freshness audit
- `.claude/skills/sunnydata-auto-regen/SKILL.md` — companion regen skill
