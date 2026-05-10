---
name: sunnydata-auto-regen
description: Regenerate the 6 AI-AUTO files defined in OWNERSHIP-MATRIX.md (flow-index, traceability-matrix, project-structure, file-dependencies, class-relationships, frontend-route-map). These files are caches derived from authoritative sources (frontmatter scans, code, router config); they should never be hand-edited. Triggers on 'regenerate views', 'refresh flow-index', 'rebuild traceability', '重生視圖', 'auto-regen', 'update derived docs', 'refresh tier-5'.
stability-tier: tooling
---

# Auto-Regen Skill

## What this skill does

Regenerates the 6 files marked 🟩 AI-AUTO in `VibeCoding_Workflow_Templates/OWNERSHIP-MATRIX.md`:

| Target | Source of truth | Regeneration method |
|---|---|---|
| `docs/2-contracts/flow-index.md` | Frontmatter scan of all `flow-*.md` + `state-machine.*.md` | Aggregate id/status/owner/refs |
| `docs/2-contracts/traceability-matrix.md` | Cross-reference of Flow/Spec/API/TC IDs across docs + tests | Build coverage rows |
| `docs/5-views/project-structure.md` | `find src/ -type d` or `eza --tree src/` | Annotate per directory |
| `docs/5-views/file-dependencies.md` | Language-specific tool (`pyan` / `madge` / `go list`) | Render dependency graph |
| `docs/5-views/class-relationships.md` | UML extractor or AI full read | Mermaid classDiagram |
| `docs/5-views/frontend-route-map.md` | Router config + component graph | Per-route table |

## Usage rule (CRITICAL)

These targets are **never** hand-edited. If a generation produces wrong output, fix the generator's source detection — never patch the output directly. See `OWNERSHIP-MATRIX.md` § Anti-patterns.

## Procedure

### Step 1: Verify project layout

```bash
test -d docs/2-contracts || { echo "Project hasn't adopted v4 layered docs structure. See HOW-TO-INSTANTIATE.md"; exit 0; }
test -d docs/5-views      || mkdir -p docs/5-views
```

### Step 2: User selects targets (or "all")

If the user said "regen flow-index" → only that target.
If the user said "regen all" or "refresh views" → all 6.
Default: ask which targets if ambiguous.

### Step 3: Per-target regeneration

#### 3a. flow-index

```bash
# Inputs: every docs/2-contracts/flow-*.md + state-machine.*.md
# For each file, parse frontmatter:
#   - id: BF-NNNN | UF-NNNN | SF-NNNN | SM-NNNN
#   - status, owner, last_reviewed
#   - parent_business_flow (UF only)
#   - For SF: scan body for "Used By" links

# Build 4 tables (BF / UF / SF / SM) per the flow-index template structure
# Preserve the user-maintained sections:
#   - "Coverage View" (count rollup — recompute)
#   - "Deprecation / Supersession Ledger" (read frontmatter status + supersedes)
#   - "Open Questions Aggregation" (scan §Open Questions in each flow file)
```

Replace `docs/2-contracts/flow-index.md` wholesale. Stamp `last-synced-with: <HEAD>` and `synced-at: <today>`.

#### 3b. traceability-matrix

```bash
# Inputs: every docs/2-contracts/flow-*.md + functional-requirement.*.md + api-spec/*.md + tests/

# Per row construction:
# - Start from each BF in flow-index
# - For each BF, find related UFs (via parent_business_flow)
# - For each UF, find related SFs (mentioned in §8 Related Sub Flows)
# - For each UF/SF, find related FRs (mentioned in §11 / §10)
# - For each FR, find related APIs (§9)
# - For each API, find data entities (§10) and TC IDs (search tests/ for TC-NNNN)
# - For each TC, find CI job (search .github/workflows or equivalent)

# Build the main coverage matrix + NFR / Domain Event / External Dependency tables
```

Replace `docs/2-contracts/traceability-matrix.md` wholesale.

#### 3c. project-structure

```bash
cd src && (eza --tree --level=4 . 2>/dev/null || tree -L 4 . 2>/dev/null || find . -type d -maxdepth 4 | sort)
```

Convert tree output to the project-structure template's table format. Annotate each top-level directory with its purpose by reading any `README.md` or `__init__.py` docstring.

#### 3d. file-dependencies

Detect language and use the right tool:

```bash
if test -f pyproject.toml || ls *.py 2>/dev/null; then
    pyan src/ --uses --no-defines --colored --grouped > docs/5-views/_file-deps.svg
elif test -f package.json; then
    npx -y madge src/ --image docs/5-views/_file-deps.svg
elif test -f go.mod; then
    go list -deps ./... | <render>
fi
```

If no tool available, fall back to AI-driven full read producing a Mermaid graph.

#### 3e. class-relationships

For OO projects:
- Python: AST scan for class definitions + base classes
- TypeScript: tsserver query for classes + interfaces
- Java/Kotlin: javap + grep
- Generate Mermaid `classDiagram` syntax

Replace `docs/5-views/class-relationships.md`.

#### 3f. frontend-route-map

Detect router and extract:
- Next.js: `find app/ -name "page.tsx"` or `find pages/ -name "*.tsx"`
- React Router: AST scan for `<Route path="...">` patterns
- Vue Router: `routes:` array in `router/index.ts`

Build per-route table: URL pattern → component → guard → primary data sources.

### Step 4: Update frontmatter

Each regenerated file gets:

```yaml
last-synced-with: <git rev-parse HEAD>
synced-at: <today YYYY-MM-DD>
generated-by: sunnydata-auto-regen
generation-source: <the tool used, e.g. "pyan + frontmatter scan">
```

The `post-write` hook will also auto-update `last-synced-with` if the file's frontmatter has the field — the explicit set here is belt + suspenders.

### Step 5: Report

Output a single summary table:

| Target | Status | Source | Lines | Action |
|---|---|---|---|---|
| flow-index.md | ✅ regenerated | 18 flow files scanned | 142 | committed |
| traceability-matrix.md | ✅ regenerated | 18 flows × 6 TCs each | 108 | committed |
| project-structure.md | ✅ regenerated | eza tree, 4 levels | 67 | committed |
| file-dependencies.md | ⚠️ skipped | no language tool found | — | install pyan / madge |
| class-relationships.md | ✅ regenerated | AST scan | 89 | committed |
| frontend-route-map.md | ✅ regenerated | 12 Next.js pages | 45 | committed |

---

## What this skill does NOT do

- Does **not** regenerate 🟥 HUMAN-ONLY files (mission, glossary, module-boundary, etc.) — those have no derivable source
- Does **not** regenerate 🟨 HYBRID files (BF/UF/SF/FR/ADR/API spec) — those need human approval; use `vibecoding-write-*` skills instead
- Does **not** scan project files outside `docs/` and `src/`
- Does **not** auto-commit (proposes the diff; user commits)

## When to invoke

- After any large refactor (5+ file move/rename)
- Weekly maintenance pass alongside `sunnydata-doc-freshness` and `sunnydata-flow-audit`
- Before any release that depends on accurate views
- When `sunnydata-flow-audit` reports INDEX_DRIFT (this skill fixes that drift)

## Edge cases

- **No `docs/` folder yet**: nothing to regen; suggest `HOW-TO-INSTANTIATE.md` to bootstrap
- **No flow files exist**: skip flow-index + traceability; still regen 5-views from src/
- **Language tool missing**: skip that one target; report it clearly so user can install the tool
- **Generation produces empty output**: don't overwrite the existing file; report "no source detected" instead

## Output style

Single Markdown summary table after work. If a target was skipped, give the exact remediation command (e.g. `pip install pyan3`).

## See also

- `VibeCoding_Workflow_Templates/OWNERSHIP-MATRIX.md` — the 🟩 AI-AUTO list this skill implements
- `.claude/skills/sunnydata-flow-audit/SKILL.md` — surfaces INDEX_DRIFT this skill fixes
- `.claude/skills/sunnydata-doc-freshness/SKILL.md` — separate concern (contract sync)
- `.claude/rules/change-governance.md` — context-stability tier 5 mandate (regen, never hand-edit)
