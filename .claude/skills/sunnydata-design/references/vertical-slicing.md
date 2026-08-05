# Vertical Slicing

Load this in Phase 2, before breaking the work into tasks. The pointer lives in
`SKILL.md`; this file holds the rules.

Before breaking the work into steps, break it into **tracer-bullet slices**.

**Vertical, not horizontal.** Each slice cuts a narrow but *complete* path
through every layer it touches (schema → API → UI → tests), rather than doing all
of one layer. A horizontal slice cannot be verified until every other layer
lands; a vertical one can be demoed on its own.

Four tests, all four must hold:

1. **Complete** — a narrow path through every layer involved.
2. **Verifiable alone** — demoable, or produces evidence, without waiting on a
   slice that isn't done.
3. **Fits one fresh context window** — a clean session can read its plan, make
   its changes, and run its tests. If it doesn't fit, the slice is too coarse.
   Re-slice; don't push through.
4. **Seam already chosen** — you know where its tests go before you start (see
   `sunnydata-codebase-design`).

**Prefactoring goes first.** "Make the change easy, then make the easy change" —
reshaping, extracting, renaming to make later slices tractable is its own slice,
and it comes before them.

**Declare blocking edges.** For each slice, list the slices that must finish
first. List only what genuinely gates it — "would be tidier afterwards" is not a
dependency, and writing it down needlessly narrows what can be worked in parallel.

**Wide refactors are the exception.** A change whose blast radius fans across the
whole codebase — renaming a shared column, retyping a common symbol — breaks
thousands of call sites at once, and no vertical slice can land green. Sequence it
as **expand → migrate in batches → contract**: add the new form beside the old so
nothing breaks; migrate call sites in batches sized by blast radius, each batch
its own slice kept green by the old form still existing; delete the old form once
no caller remains.

Present the slices as a numbered list — title, what end-to-end behavior it
delivers, what blocks it — and confirm granularity and dependencies before
writing any tasks.

## Attribution

Slice criteria and the expand–contract sequence adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) `to-tickets`
(MIT, © 2026 Matt Pocock).
