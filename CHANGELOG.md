# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Generation: run `/release <version>` command — orchestrates [`sunnydata-changelog-sync`](.claude/skills/sunnydata-changelog-sync/SKILL.md) skill, tag creation, and GitHub Release.

## [Unreleased]

(awaiting next `/release` invocation)

---

## [v5.5] - 2026-05-11

### Added
- Template compliance sweep: 14 templates got v5 frontmatter; 1 file got WORKED EXAMPLE banner
- `sunnydata-changelog-sync` skill — Keep-a-Changelog generator
- `/release` command — full release pipeline orchestration
- `CHANGELOG.md` at project root + GitHub Actions auto-release workflow

### Fixed
- Frontmatter field naming inconsistencies (`last_updated` → `last_reviewed`, `owners` → `owner`)
- Missing `target_release`, `supersedes`, `superseded_by` chains on legacy templates

## [v5.4] - 2026-05-10

### Changed
- Frontend templates segregated to `extras/web-frontend/` — keeps core tiers domain-neutral
- 14 templates with worked examples gained `⚠️ WORKED EXAMPLE — DELETE BEFORE USE` banner — preserves AI few-shot value while marking examples as illustrative

### Added
- `extras/README.md` — explains domain-bound template segregation
- ADR-0001 / CR-0001 dogfood example demonstrating CIA → ADR workflow (later removed)

## [v5.3] - 2026-05-10

### Added
- `2-contracts/flow-index.template.md` — project-wide Flow aggregation view
- `sunnydata-flow-audit` skill — detects broken refs, orphans, layering violations, stale flows, index drift in the Flow ecosystem
- `OWNERSHIP-MATRIX.md` — human vs AI division of labor (16 HUMAN-ONLY / 12 HYBRID / 6 AI-AUTO)
- `sunnydata-auto-regen` skill — regenerates 6 AI-AUTO files from authoritative sources

### Changed
- INDEX.md now points to OWNERSHIP-MATRIX as the entry point for human architects

## [v5.2] - 2026-05-10

### Added
- ERP-class foundation:
  - `0-principles/glossary.template.md` — business terminology source of truth
  - `1-decisions/module-boundary.template.md` — per-module charter (owns / does NOT own)
  - `1-decisions/domain-model.template.md` — per-bounded-context DDD model
  - `2-contracts/state-machine.template.md` — extracted state machines for complex entities (≥5 states)
  - `2-contracts/master-data-specification.template.md` — master entity governance

## [v5.1] - 2026-05-10

### Added
- `2-contracts/functional-requirement.template.md` — FR independent template (decouples rules from Flow per "one doc, one question" principle)
- `3-process/test-plan.template.md` — strategic test document (quality targets, test pyramid, stages, data strategy, CI gate spec, risk register)
- `3-process/vendor-api-test-requirement.template.md` — per-vendor test prerequisites

## [v5.0] - 2026-05-10

### Added
- Change Governance hard gate:
  - `0-principles/flow-id-conventions.md` — 9-prefix Flow ID system (BF/UF/SF/FR/NFR/API/TC/ADR/CR)
  - 3-tier Flow templates (BF/UF/SF) in `2-contracts/`
  - `4-exploration/change-impact-analysis.template.md` (CIA) — per-change ephemeral
  - `2-contracts/traceability-matrix.template.md` — Flow→Spec→API→Data→TC→CI coverage map
  - `3-process/quality-gates.md` — Gate 0-4 stage prerequisites
  - `.claude/rules/change-governance.md` — hard gate enforcing CIA before code changes
  - `sunnydata-change-impact-analysis` skill
- Lifecycle frontmatter: `status` (draft/active/deprecated/superseded/archived), `supersedes`, `superseded_by`
- `sunnydata-doc-freshness` skill — detects stale tier-2 contracts

## [v4.0] - 2026-05-10

### Changed (Breaking)
- Stability-tier layout: templates organized by `0-principles` → `5-views` (was phase-based `01_` to `17_`)
- `.template.md` naming convention (was numeric prefix)
- `output-styles/01-14` migrated to `vibecoding-*` skills (was system-prompt-replacement mode)

### Added
- 6-tier README files describing each tier's policy
- `HOW-TO-INSTANTIATE.md` — recommended `docs/` layout for end-user projects
- `LEGACY-INDEX.md` — v3 phase-based view preserved for downstream forks
- Sync mechanism: `post-write` hook auto-updates `last-synced-with` frontmatter on tier-2 contract edits
- `.claude/rules/context-stability.md` — what AI loads per tier
- `.claude/rules/primitive-selection.md` — command/skill/output-style decision rule

### Removed
- 14 task-template output-styles (migrated to skills; `15-Vision-output` retained)
- 6 pure-indirection commands (`/plan`, `/tdd`, `/e2e`, `/review-code`, `/hub-delegate`, `/check-quality`)
- `VibeCoding_Workflow_Templates/output_style.md` — contradicted v4 design
- `.claude/plugins/`, `.claude/custom-rule&skill/`, `statusline-go.exe` — dead code

### Fixed
- `post-write` hook matcher broadened from `Write` to `Write|Edit|MultiEdit|NotebookEdit`

## [v3.0] - 2026-03-16

### Changed
- Phase-based numbering (01-17), unified zh-TW, removed cookbook duplicate

## [v2.1] - 2025-10-03

### Added
- Frontend Information Architecture template (17)

## [v2.0] - 2025-10-03

### Changed
- Reorganized template numbering
- Added INDEX

## [v1.0] - 2025-10-01

### Added
- Initial template set

---

[Unreleased]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.5...HEAD
[v5.5]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.4...v5.5
[v5.4]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.3...v5.4
[v5.3]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.2...v5.3
[v5.2]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.1...v5.2
[v5.1]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v5.0...v5.1
[v5.0]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v4.0...v5.0
[v4.0]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v3.0...v4.0
[v3.0]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v2.1...v3.0
[v2.1]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v2.0...v2.1
[v2.0]: https://github.com/Zenobia000/claude-Godzilla-z/compare/v1.0...v2.0
[v1.0]: https://github.com/Zenobia000/claude-Godzilla-z/releases/tag/v1.0
