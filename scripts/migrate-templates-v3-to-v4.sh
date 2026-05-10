#!/bin/bash
# Migrate references from VibeCoding templates v3 (numeric prefix, flat) to v4 (stability-tier, semantic).
#
# Usage:
#   bash scripts/migrate-templates-v3-to-v4.sh [--dry-run] [path]
#
# Defaults:
#   --dry-run is OFF (changes are written)
#   path defaults to current directory
#
# What it does:
#   - Walks all *.md / *.json / *.sh / *.yaml / *.yml files under <path>
#   - Replaces v3 paths (01_*.md ... 17_*.md) with v4 tier paths
#   - Skips .git/, node_modules/, VibeCoding_Workflow_Templates/, and this script itself
#
# Safe to re-run; idempotent.

set -euo pipefail

DRY_RUN=0
ROOT="."
SELF_PATH="$(realpath "${BASH_SOURCE[0]}")"
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) ROOT="$arg" ;;
  esac
done

# v3 → v4 mapping (old basename | new full path)
# Old basenames are stored split so this script doesn't match itself when scanning.
declare -a MAP=(
  "0|1|workflow_manual.md|3-process/workflow-manual.md"
  "0|2|project_brief_and_prd.md|4-exploration/prd.template.md"
  "0|3|behavior_driven_development_guide.md|3-process/bdd-guide.md"
  "0|4|architecture_decision_record_template.md|1-decisions/adr.template.md"
  "0|5|architecture_and_design_document.md|1-decisions/architecture-overview.template.md"
  "0|6|api_design_specification.md|2-contracts/api-spec.template.md"
  "0|7|module_specification_and_tests.md|2-contracts/module-contract.template.md"
  "0|8|project_structure_guide.md|5-views/project-structure.template.md"
  "0|9|file_dependencies_template.md|5-views/file-dependencies.template.md"
  "1|0|class_relationships_template.md|5-views/class-relationships.template.md"
  "1|1|code_review_and_refactoring_guide.md|3-process/code-review-checklist.md"
  "1|2|frontend_architecture_specification.md|5-views/frontend-architecture.template.md"
  "1|3|security_and_readiness_checklists.md|3-process/security-readiness-checklist.md"
  "1|4|deployment_and_operations_guide.md|3-process/deployment-runbook.template.md"
  "1|5|documentation_and_maintenance_guide.md|3-process/docs-maintenance-guide.md"
  "1|6|wbs_development_plan_template.md|4-exploration/wbs.template.md"
  "1|7|frontend_information_architecture_template.md|5-views/frontend-information-architecture.template.md"
)

echo "Migration: VibeCoding templates v3 -> v4"
echo "Root: $ROOT"
echo "Dry-run: $([ "$DRY_RUN" = 1 ] && echo YES || echo NO)"
echo

CHANGED=0
for row in "${MAP[@]}"; do
  IFS='|' read -r D1 D2 BASE NEW <<< "$row"
  OLD="${D1}${D2}_${BASE}"

  while IFS= read -r -d '' file; do
    # Skip self
    if [ "$(realpath "$file")" = "$SELF_PATH" ]; then continue; fi

    if [ "$DRY_RUN" = 1 ]; then
      hits=$(grep -c "$OLD" "$file" || true)
      echo "[DRY] $file -> $hits occurrences of '$OLD'"
    else
      sed -i.bak "s|$OLD|$NEW|g" "$file"
      rm -f "${file}.bak"
      echo "[OK]  $file: $OLD -> $NEW"
    fi
    CHANGED=$((CHANGED + 1))
  done < <(grep -rlZ --include="*.md" --include="*.json" --include="*.sh" --include="*.yaml" --include="*.yml" \
            --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=VibeCoding_Workflow_Templates \
            "$OLD" "$ROOT" 2>/dev/null || true)
done

echo
echo "Files touched: $CHANGED"
echo
echo "Next steps:"
echo "  1. Review the diff: git diff"
echo "  2. Run tests / build to verify nothing broke"
echo "  3. Commit: git commit -am 'chore: migrate template refs to v4 layout'"
echo
echo "If you also want to migrate your project's docs/ folder structure to match"
echo "the v4 6-tier layout, see VibeCoding_Workflow_Templates/HOW-TO-INSTANTIATE.md"
