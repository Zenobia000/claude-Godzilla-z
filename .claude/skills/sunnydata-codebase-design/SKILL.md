---
name: sunnydata-codebase-design
description: Shared vocabulary for designing deep modules — module, interface, depth, seam, adapter, leverage, locality. Use when deciding where a seam goes, designing or improving a module's interface, judging whether an abstraction earns its keep, or when another skill needs this vocabulary (notably /specify when choosing test seams).
---

# Codebase Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. The aim is leverage for callers, locality for maintainers, and testability for everyone.

This skill is **vocabulary**, not a process. It has no steps — reach for it when the words are the problem, or when another skill pulls it in.

## Glossary

Use these terms exactly. Consistent language is the whole point — substituting "component", "service", or "boundary" reintroduces the ambiguity this glossary exists to remove.

| Term | Meaning | Avoid |
|---|---|---|
| **Module** | Anything with an interface and an implementation. Deliberately scale-agnostic: a function, class, package, or tier-spanning slice | unit, component, service |
| **Interface** | Everything a caller must know to use the module correctly — type signature, but also invariants, ordering constraints, error modes, required configuration, performance characteristics | API, signature (too narrow: type-level only) |
| **Implementation** | What is inside a module. Distinct from **Adapter**: a thing can be a small adapter with a large implementation (a Postgres repo) or a large adapter with a small implementation (an in-memory fake) | |
| **Depth** | Leverage at the interface — how much behaviour a caller or test can exercise per unit of interface it has to learn | |
| **Seam** | A place where you can alter behaviour without editing in that place; the *location* at which a module's interface lives. Where to put the seam is its own decision, separate from what goes behind it | boundary (overloaded with DDD's bounded context) |
| **Adapter** | A concrete thing satisfying an interface at a seam. Describes *role* (which slot it fills), not substance (what is inside) | |
| **Leverage** | What callers get from depth: more capability per unit of interface learned. One implementation pays back across N call sites and M tests | |
| **Locality** | What maintainers get from depth: change, bugs, knowledge, and verification concentrate in one place instead of spreading across callers | |

**Deep** = small interface, large implementation. **Shallow** = interface nearly as complex as the implementation. Shallow is the thing to avoid.

## Principles

**Depth is a property of the interface, not the implementation.** A deep module may be internally composed of small, swappable parts — they just are not part of its interface. A module can have **internal seams** (private, used by its own tests) as well as the **external seam** at its interface.

**The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep. Apply this to anything you suspect is shallow before proposing a refactor.

**The interface is the test surface.** Callers and tests cross the same seam. If you want to test *past* the interface, the module is the wrong shape — fix the shape rather than reaching around it.

**One adapter means a hypothetical seam. Two adapters means a real one.** Do not introduce a seam unless something actually varies across it. A seam with a single implementation is speculative generality wearing an architecture costume.

## Choosing where a seam goes

Whenever a design discussion has to pick seams — planning a feature, or before
writing the first test — four rules, in order:

1. **Prefer an existing seam** to a new one. A new seam is new interface surface to learn, maintain, and keep honest.
2. **Use the highest seam that can observe the behaviour.** Testing at the outermost interface that still sees the result gives the most leverage per test and survives the most refactors.
3. **Fewer seams is better. The ideal number is one.** Every seam is a place where the system can be observed *and* a place where it can drift.
4. **If a new seam is genuinely needed, propose it at the highest point you can** — and say what varies across it (rule: two adapters, not one).

Then **confirm the seams with the human before any test is written**. Testing effort lands on critical paths only if the seams are agreed up front; an unconfirmed seam produces tests nobody wanted.

## Designing for testability

Good interfaces make testing natural:

- **Accept dependencies, do not create them.** `processOrder(order, paymentGateway)` is testable; `processOrder(order)` that news up a `StripeGateway` inside is not.
- **Return results, do not produce side effects.** `calculateDiscount(cart): Discount` is testable; `applyDiscount(cart): void` that mutates `cart.total` is not.
- **Small surface area.** Fewer methods means fewer tests; fewer parameters means simpler setup.

## Relationships

- A **Module** has exactly one **Interface** — the surface it presents to callers and tests.
- **Depth** is a property of a **Module**, measured against its **Interface**.
- A **Seam** is where a **Module**'s **Interface** lives.
- An **Adapter** sits at a **Seam** and satisfies the **Interface**.
- **Depth** produces **Leverage** for callers and **Locality** for maintainers.

## Rejected framings

- **Depth as the ratio of implementation lines to interface lines.** Rewards padding the implementation. Use depth-as-leverage instead.
- **"Interface" as a language `interface` keyword or a class's public methods.** Too narrow — interface here includes every fact a caller must know, including error modes and ordering.
- **"Boundary"** as a synonym for seam. Overloaded with DDD's bounded context. Say **seam** or **interface**.

## Relationship to other skills

- **`sunnydata-design`** Phase 2 picks the seams while writing the plan, so every task in the plan knows where its tests go.
- **`sunnydata-testing`** places tests at those seams. An unconfirmed seam is not a valid test location — confirm before writing the first test, not after.
- **`sunnydata-architecture-review`** finds *where* the design hurts (smells → principles → fixes); this skill supplies the *words* to describe the fix. Run that one to survey, this one to design.

## Attribution

Vocabulary and principles adapted from [mattpocock/skills](https://github.com/mattpocock/skills) `codebase-design` (MIT, © 2026 Matt Pocock), itself drawing on John Ousterhout (*A Philosophy of Software Design*) and Michael Feathers (seams). The seam-selection rules are this project's addition.
