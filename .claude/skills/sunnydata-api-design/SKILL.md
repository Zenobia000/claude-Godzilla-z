---
name: sunnydata-api-design
description: REST API design patterns including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production APIs.
origin: ECC
---

# API Design Patterns

Conventions and best practices for designing consistent, developer-friendly REST APIs.

## When to Activate

- Designing new API endpoints
- Reviewing existing API contracts
- Adding pagination, filtering, or sorting
- Implementing error handling for APIs
- Planning API versioning strategy
- Building public or partner-facing APIs

## Core Rules

- Resources are nouns, plural, lowercase, kebab-case; verbs only for actions
  that don't map to CRUD (e.g. `POST /api/v1/orders/:id/cancel`).
- Use HTTP status codes semantically — never 200 for everything, 201 with a
  `Location` header for creation, 400/422 for validation, never 500 for
  client errors.
- Every error response carries a machine-readable `code`, a human `message`,
  and field-level `details` for validation failures.
- Paginate every list endpoint: cursor-based for scale and feeds, offset-based
  where users expect page numbers.
- Require authentication by default; check authorization at the resource level
  (ownership) and role level (permissions).
- Version in the URL path (`/api/v1/`); only breaking changes get a new
  version, and at most two versions stay active.

## References

Load the reference matching the task; each holds the full patterns, tables,
and good/bad examples.

- Read `references/resources-and-naming.md` when designing endpoint URLs,
  choosing HTTP methods, or reviewing naming — URL structure, naming rules,
  method semantics (idempotency/safety).
- Read `references/errors-and-responses.md` when defining response shapes or
  error handling — status code reference, common status-code mistakes,
  success/collection/error response formats, envelope variants.
- Read `references/pagination-auth-versioning.md` when adding list endpoints,
  query capabilities, or API lifecycle policy — offset vs cursor pagination,
  filtering/sorting/search/sparse fieldsets, token auth and authorization
  patterns, rate limit headers and tiers, versioning strategy and deprecation
  timeline.
- Read `references/implementation-examples.md` when implementing endpoints —
  validated-create examples for TypeScript (Next.js), Python (DRF), and
  Go (net/http).

## API Design Checklist

Before shipping a new endpoint:

- [ ] Resource URL follows naming conventions (plural, kebab-case, no verbs)
- [ ] Correct HTTP method used (GET for reads, POST for creates, etc.)
- [ ] Appropriate status codes returned (not 200 for everything)
- [ ] Input validated with schema (Zod, Pydantic, Bean Validation)
- [ ] Error responses follow standard format with codes and messages
- [ ] Pagination implemented for list endpoints (cursor or offset)
- [ ] Authentication required (or explicitly marked as public)
- [ ] Authorization checked (user can only access their own resources)
- [ ] Rate limiting configured
- [ ] Response does not leak internal details (stack traces, SQL errors)
- [ ] Consistent naming with existing endpoints (camelCase vs snake_case)
- [ ] Documented (OpenAPI/Swagger spec updated)
