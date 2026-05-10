# Tier 0 — Principles

> The least-volatile layer. Changes once per major version, if that.

## What lives here

Documents that define **what this product is** and **what it refuses to be**:
- Product mission and non-goals
- Quality bars (performance, security, a11y)
- Technical invariants that survive across features

## What does NOT live here

- Specific features → tier 4 (exploration / PRD)
- API shapes → tier 2 (contracts)
- Why we picked PostgreSQL → tier 1 (decisions)

## How AI should use this tier

**Always read first** in any new conversation about this project. These documents establish the worldview that constrains every other decision. If a generated feature violates a principle, the principle wins.

## How humans should maintain this tier

- Review once every 6 months minimum
- A change here is a major event — usually requires a team discussion, not a PR review
- If you find yourself updating this monthly, the document is the wrong shape (it's probably exploration, not principle)

## Files

| File | Purpose |
|---|---|
| `product-principles.template.md` | Mission, personas, non-goals, quality bars, technical invariants |
