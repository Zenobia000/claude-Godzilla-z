# Two-Axis Review

Load this when dispatching Phase 2. A change can pass one axis and fail the other:

- Follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Does exactly what the spec asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

## Dispatch

Run both axes as **parallel sub-agents** (`general-purpose`) in a single message, so neither pollutes the other's context. Pin the fixed point first — a commit SHA, branch, tag, or `main` — and confirm it resolves (`git rev-parse`) and the diff is non-empty **before** spawning anything. A bad ref should fail here, not inside two sub-agents.

Capture once and pass to both: `git diff <fixed-point>...HEAD` (three-dot, against the merge-base) and `git log <fixed-point>..HEAD --oneline`.

### Standards sub-agent

Give it: the diff command, the commit list, the repo's documented standards files (`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `.claude/rules/`, and any filled `VibeCoding_Workflow_Templates/11_code_review_and_refactoring_guide.md`), **and the smell baseline below pasted in full** — the sub-agent has no other access to it.

Brief: report per file/hunk (a) every place the diff violates a documented standard, citing the standard; (b) any baseline smell, named, with the hunk quoted. Distinguish hard violations from judgement calls. Skip anything tooling already enforces. Under 400 words.

### Spec sub-agent

Give it: the diff command, the commit list, and the originating spec — resolved in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`).
2. A path the user passed as an argument.
3. A plan or spec under `docs/`, matching the branch name or feature — including a `sunnydata-design` Phase 1 spec or Phase 2 plan.
4. A filled template under `VibeCoding_Workflow_Templates/` (typically `02_project_brief_and_prd`).
5. Ask the user.

Brief: report (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff nobody asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line or ID for each finding. Under 400 words.

If no spec exists, skip this axis and say so — do not substitute your own judgement of what the code should do.

## Smell baseline

Applies even when the repo documents nothing. Two rules bind it: **the repo overrides** (a documented standard always wins), and **every smell is a judgement call** — a labelled heuristic ("possible Feature Envy"), never a hard violation.

| Smell | What it is | Fix |
|---|---|---|
| Mysterious Name | Name doesn't reveal what it does or holds | Rename; if no honest name comes, the design is murky |
| Duplicated Code | Same logic shape in more than one hunk or file | Extract the shared shape, call it from both |
| Feature Envy | A method reaches into another object's data more than its own | Move the method onto the data it envies |
| Data Clumps | The same few fields keep travelling together | Bundle them into one type |
| Primitive Obsession | A primitive standing in for a domain concept | Give the concept its own small type |
| Repeated Switches | Same switch/if-cascade on the same type recurs | Replace with polymorphism, or one shared map |
| Shotgun Surgery | One logical change forces scattered edits across many files | Gather what changes together into one module |
| Divergent Change | One module edited for several unrelated reasons | Split so each changes for one reason |
| Speculative Generality | Abstraction or hooks for needs the spec doesn't have | Delete it; inline back until a real need shows |
| Message Chains | Long `a.b().c().d()` the caller shouldn't depend on | Hide the walk behind one method |
| Middle Man | A class or function that mostly just delegates | Cut it, call the real target |
| Refused Bequest | A subclass ignoring most of what it inherits | Drop inheritance, use composition |

## Aggregate

Present both reports under `## Standards` and `## Spec`, verbatim or lightly cleaned. **Do not merge or rerank findings** — the axes are deliberately separate.

End with one line: total findings per axis, and the worst issue *within each axis*. Do not pick a single winner across axes — that cross-axis reranking is exactly what the separation exists to prevent.

## Attribution

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `code-review` (MIT, © 2026 Matt Pocock). Smell list from Martin Fowler, *Refactoring* ch.3.
