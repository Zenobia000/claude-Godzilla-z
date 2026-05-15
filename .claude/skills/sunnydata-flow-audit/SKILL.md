---
name: sunnydata-flow-audit
description: Audit the project's Flow ecosystem (BF/UF/SF/SM/FR/API IDs across docs/2-contracts/) for consistency violations. Detects broken refs, orphan flows, layering violations, stale flows, and flow-index drift. Triggers on 'audit flows', 'check flow consistency', 'find broken refs', '稽核 flow', 'flow 一致性檢查', 'is flow-index up to date'. Reports only — does not modify files.
stability-tier: tooling
---

# Flow Audit

## What this skill does

Walks `docs/2-contracts/flow-*.md` + `docs/2-contracts/state-machine.*.md` + `docs/2-contracts/flow-index.md` and reports five classes of decay:

1. **BROKEN REF** — a Flow doc references an ID (BF-NNNN / UF-NNNN / SF-NNNN / SM-NNNN / FR-NNNN / API-NNNN) that doesn't exist in any file
2. **ORPHAN** — an SF or SM that no BF/UF references (candidate for archival)
3. **LAYERING VIOLATION** — Flow doc contains "MUST / SHALL / MUST NOT" rule wording that belongs in an FR (`functional-requirement.template.md`)
4. **STALE FLOW** — `status: active` but `last_reviewed` > 6 months ago
5. **INDEX DRIFT** — `flow-index.md` lists IDs that don't have corresponding files, or files exist that aren't in the index

This skill **only reports**; it never modifies files. Remediation is delegated to `vibecoding-write-*` skills or human review.

## When to invoke

- Weekly maintenance pass
- Before any release / deployment
- After a major refactor that moved/renamed Flow files
- When `vibecoding-write-flow` (if present) is about to add a new ID — to warn if numbering would collide
- When `sunnydata-change-impact-analysis` writes a CR that touches Flows — to spot pre-existing decay

## Procedure

### Step 1: Verify location

```bash
test -d docs/2-contracts || { echo "Project hasn't adopted v4 layered docs structure. See HOW-TO-INSTANTIATE.md"; exit 0; }
```

### Step 2: Enumerate Flow universe

```bash
# Flow files
FLOW_FILES=$(find docs/2-contracts -type f \( \
  -name "flow-business.*.md" -o \
  -name "flow-user.*.md" -o \
  -name "flow-sub.*.md" -o \
  -name "state-machine.*.md" -o \
  -name "functional-requirement.*.md" -o \
  -name "api-spec.*.yaml" -o \
  -name "api-spec.*.md" \
\))

# Index file
INDEX="docs/2-contracts/flow-index.md"
```

### Step 3: Build the ID universe

Extract every defined ID from frontmatter `id:` field across all files. Build a set:

```
DEFINED = {
  "BF-0001": "docs/2-contracts/flow-business.0001-order-to-cash.md",
  "UF-0001": "docs/2-contracts/flow-user.0001-customer-create-order.md",
  "SF-0001": "docs/2-contracts/flow-sub.0001-inventory-validation.md",
  "SM-0001": "docs/2-contracts/state-machine.order.md",
  …
}
```

### Step 4: Build the reference universe

Scan every Flow file's body for ID-shaped tokens (`(BF|UF|SF|SM|FR|NFR|API|TC|ADR|CR)-\d{3,4}`). Track per-file which IDs are referenced.

### Step 5: Run the 5 audits

#### 5a. Broken refs
```
For each ID in REFERENCES but not in DEFINED:
  emit BROKEN_REF { ref: ID, in_file: path, line: N }
```

#### 5b. Orphans
```
For each SF or SM in DEFINED:
  consumers = [file for file in FLOW_FILES if id in REFERENCES[file]]
  if consumers is empty:
    emit ORPHAN { id: ID, file: path, suggest: "archive or delete" }
```

#### 5c. Layering violations
```
For each flow-business.* or flow-user.* or flow-sub.* file:
  scan body for /\b(MUST|SHALL|MUST NOT|SHALL NOT)\b/ outside code blocks
  if matches found AND no link to a corresponding FR-NNNN exists:
    emit LAYERING_VIOLATION { file: path, lines: [N], suggest: "extract rules to FR template" }
```

Exception: phrases like "MUST be authenticated" in §Pre-conditions are OK if they describe a precondition state. Heuristic: violations are MUST/SHALL inside §Main Flow / §Exception Flow / §Acceptance Criteria sections.

#### 5d. Stale flows
```
For each file with status: active in frontmatter:
  if last_reviewed > 180 days ago:
    emit STALE { id: ID, file: path, days_since_review: N, suggest: "review or mark deprecated" }
```

#### 5e. Index drift
```
If INDEX exists:
  index_ids = parse rows in BF/UF/SF/SM tables
  defined_ids = set(DEFINED.keys())

  for id in index_ids - defined_ids:
    emit INDEX_DRIFT { type: "phantom_in_index", id: ID, suggest: "remove from index or create file" }
  for id in defined_ids - index_ids:
    emit INDEX_DRIFT { type: "missing_from_index", id: ID, file: path, suggest: "add to flow-index" }

If INDEX missing:
  if count(DEFINED) > 5:
    emit INDEX_DRIFT { type: "index_missing", suggest: "create docs/2-contracts/flow-index.md" }
```

### Step 6: Output

Single Markdown table sorted by severity (BROKEN > LAYERING > INDEX_DRIFT > ORPHAN > STALE):

| Severity | Type | ID / File | Detail | Suggested Action |
|---|---|---|---|---|
| 🔴 BROKEN | broken_ref | `SF-0099` referenced in `flow-business.0001-order-to-cash.md:142` | ID not defined anywhere | Create SF-0099 or fix the ref |
| 🟠 LAYERING | layering_violation | `flow-user.0003-customer-pay-order.md:67` | "system MUST validate signature" found in §Main Flow without FR link | Extract to `functional-requirement.NNNN.md` |
| 🟠 INDEX_DRIFT | phantom_in_index | `BF-0099` in flow-index but no file | Remove from index or create file |
| 🟠 INDEX_DRIFT | missing_from_index | `SF-0014` exists at `flow-sub.0014-partial-cancel.md` | Add row to flow-index |
| 🟡 ORPHAN | orphan | `SF-0007` in `flow-sub.0007-…md` | No BF/UF references it | Archive or check if planned |
| 🟡 STALE | stale | `BF-0002` in `flow-business.0002-…md` | last_reviewed: 245 days ago | Review or mark deprecated |
| 🟢 OK | — | — | No issues | — |

If no issues: single line "All Flow audits pass — N flows / M references checked, 0 issues."

End the response with summary stats:
```
Audited: 23 Flow files (4 BF, 8 UF, 7 SF, 3 SM, 1 index)
References scanned: 187
  Defined: 23
  References to defined: 142
  References to undefined: 3 (BROKEN)
  Orphans: 2
  Layering violations: 1
  Stale: 4
  Index drift: 0
```

## What this skill does NOT do

- Does NOT modify files (audit only)
- Does NOT create FR docs to fix layering violations (that's `vibecoding-write-prd` / future `vibecoding-write-fr`)
- Does NOT auto-update flow-index (delegate to human or write-flow skill)
- Does NOT scan tier-3+ docs (this is Flow-specific; use `sunnydata-doc-freshness` for tier-2 contracts in general)
- Does NOT enforce — just surfaces. The remediation decisions belong to humans

## Why audit-only (no auto-fix)

Auto-fixing flow audit findings is dangerous:
- Auto-deleting "orphans" can remove valid SFs that are about to be wired up
- Auto-extracting layering violations into FRs needs human judgment on what's actually a rule vs descriptive prose
- Auto-creating missing IDs from index drift can mask intent (was the ID a typo or did the file get deleted?)

Pattern matches `sunnydata-doc-freshness` — both are reporting tools; remediation goes through dedicated write skills.

## Output style

Single Markdown table + summary stats. No preamble. If clean, single-line OK. Match the format of `sunnydata-doc-freshness` for visual consistency.

## See also

- `VibeCoding_Workflow_Templates/0-principles/PRIN-0001-flow-id-conventions.md` — ID semantics this skill enforces
- `VibeCoding_Workflow_Templates/2-contracts/FI-0000-flow-index.template.md` — the index this skill cross-checks
- `.claude/skills/sunnydata-doc-freshness/SKILL.md` — tier-2 contract sync (different audit dimension)
- `.claude/skills/sunnydata-change-impact-analysis/SKILL.md` — when CIA fires, run this first to surface pre-existing decay
- `.claude/rules/change-governance.md` — rule that mandates Flow IDs being usable
