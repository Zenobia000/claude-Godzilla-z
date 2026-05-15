# Primitive Selection Rule

> Why this rule exists: the harness offers three primitives — **command**, **skill**, **output-style** — with overlapping capabilities. Without a clear rule, both AI and humans end up with mode-switching fatigue ("which entry point do I pick for code review?"). Good design doesn't require constant mode switching; this rule encodes the selection so it's mechanical, not judgment.

## TL;DR — three lines

1. **Default to `skill`.**
2. **Use `command` only when the action touches system state** (taskmaster, session, time-log, learn) **or carries a unique procedural sequence the AI shouldn't free-form** (build-fix, verify, refactor-clean, template-check).
3. **Use `output-style` only for persistent persona/voice shifts across the entire session** (e.g. visualization-first mode); never for task templates.

## Decision tree

```
                 ┌──────────────────────────────┐
                 │  user wants to do something  │
                 └──────────────┬───────────────┘
                                │
        ┌───────────────────────┼─────────────────────────┐
        ▼                       ▼                         ▼
   touches system          persistent persona         everything else
   state? (taskmaster,     shift across the           (default)
   session, time-log,      whole session?
   learn)                  e.g. visualization-first,
        │                  socratic-tutor mode
        ▼                          │                       │
    command                        ▼                       ▼
    e.g. /save-session         output-style              skill
                               e.g. /output-style       (auto-load
                               Vision-output         or via
                                                        Skill tool)
```

## What each primitive *is*

| Primitive | Triggered by | Lifetime | Authority over AI |
|---|---|---|---|
| **command** | User types `/<name>` | One-shot | Strong — explicit instruction |
| **skill** | AI auto-detects from request OR user explicit via Skill tool OR natural-language match against the skill description | Loaded on demand, released after | Medium — procedural guide |
| **output-style** | User types `/output-style <name>` | Whole session, until switched | Strongest — replaces system prompt |

## When to use each — the policy

### command
**Use when**:
- The action mutates persistent project state (taskmaster files, session snapshot, time-log, learned patterns)
- The action carries a unique procedural sequence (build tool detection, dead-code scanner table) that an AI without the command would have to re-derive

**Don't use when**:
- The command is a thin wrapper that just routes to an agent or skill — delete it; let the user describe intent in natural language and let the harness pick the skill or agent.

### skill
**Use when**:
- This is anything procedural the AI might want to load: writing PRDs, designing APIs, code review, debugging, security audit, frontend design, etc.
- **Default for every task** that doesn't touch system state or require persona shift.

**Don't use when**:
- (No good reason to avoid skills — they're cheap, on-demand, composable.)

### output-style
**Use when**:
- You genuinely want the *whole session* to behave differently — every response in a different voice or format.
- Example: `/output-style Vision-output` makes Claude prefer ASCII diagrams over code for the rest of the session.

**Don't use when**:
- Encoding a task template (PRD, ADR, API spec). Those are skills now. The user shouldn't have to switch session mode just to draft one document.

## How AI signals primitive awareness

When responding, name the primitive you're using if non-obvious:

- ✅ "This is procedural — invoking `vibecoding-code-review` skill."
- ✅ "This needs to mutate session state — using `/save-session` command."
- ✅ "User wants visualization mode for the rest of the chat — `/output-style Vision-output`."
- ❌ "Switching to `/output-style 01-prd-product-spec` mode" *(deprecated; that's now `vibecoding-write-prd` skill)*
- ❌ Implicitly switching modes mid-conversation without telling the user.

## Anti-patterns to refuse

| Anti-pattern | Why bad | What to do instead |
|---|---|---|
| Adding a `/foo` command that just calls "the foo agent" | Indirection without value; user has to know two names instead of one | Let the user describe intent; harness finds the skill/agent |
| Using `/output-style` for a task template ("PRD mode", "ADR mode") | Forces session-wide mode change for one-shot work | Make it a skill; keep session mode neutral |
| Multiple skills with overlapping triggers but no clear "use when" boundary | Decision fatigue | Document the boundary in each skill's description, OR consolidate |
| Renaming a skill but keeping the old name as a redirect | Old name silently rots | Delete cleanly; update all references in one commit |

## Cleanup history

- **2026-05-10** — Removed 6 pure-indirection commands: `/plan`, `/tdd`, `/e2e`, `/review-code`, `/hub-delegate`, `/check-quality`. Replacements are skills (vibecoding-*, sunnydata-*) or the Agent tool itself.
- **2026-05-10** — Removed `VibeCoding_Workflow_Templates/output_style.md` (424-line stale design doc that contradicted v4 by promoting output-styles for task templates).
- **2026-05-10** — Removed 14 task-template output-styles; migrated to `vibecoding-*` skills. Only `Vision-output.md` remains as a legitimate session-wide persona mode.

## See also

- `.claude/rules/context-stability.md` — when AI should load which docs (tier-based)
- `.claude/output-styles/README.md` — what truly belongs in `output-styles/`
- `.claude/WORKFLOW.md` — concrete workflow showing all three primitives in use
