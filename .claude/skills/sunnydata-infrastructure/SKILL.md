---
name: sunnydata-infrastructure
description: Docker containerization and deployment patterns — Dockerfile best practices, Compose for local dev, CI/CD pipelines, deployment strategies (Rolling/Blue-Green/Canary), health checks, and production readiness. Use when containerizing apps, setting up local dev environments, or planning deployments.
---

> **繁體中文說明**：此技能整合 docker-patterns 與 deployment-patterns，涵蓋從本機容器化到正式環境部署的完整工作流程。

# Infrastructure

## Overview

Single skill for "how code runs" — from local Docker to production deployment.
Merged from `docker-patterns` (container dev workflow) and `deployment-patterns` (CI/CD, release strategy).

Activate when:
- Containerizing an application (Dockerfile, .dockerignore)
- Setting up Docker Compose for local development
- Designing multi-container or multi-network architectures
- Establishing a CI/CD pipeline
- Planning a deployment strategy (Rolling, Blue-Green, Canary)
- Implementing health checks or Kubernetes probes
- Preparing a production release checklist

## Core Principles

- **One canonical multi-stage Dockerfile per language.** The `dev` stage is used
  by Compose; the `production` stage ships to production — minimal, non-root,
  exact pinned base versions, HEALTHCHECK built in, secrets never baked into
  image layers.
- **12-Factor configuration.** All config via environment variables, never
  hardcoded; validate at startup and fail fast if config is wrong.
- **One health endpoint per service.** Simple `/health` liveness plus a detailed
  readiness check that probes real dependencies (database, cache, external APIs).
- **Every deploy has a tested rollback path.** Backward-compatible migrations,
  tagged previous artifacts, feature flags that disable without a deploy.
- **Build once, promote the artifact.** The same image digest moves
  dev → staging → production through evidence gates; only environment variables
  and secrets differ per environment. Never rebuild for production.

## Workflow

1. **Containerize.** Read `references/dockerfile-patterns.md` when writing or
   reviewing a Dockerfile — it holds the canonical Node.js/Go/Python multi-stage
   patterns, the shared `.dockerignore`, and container security hardening
   (non-root, capability drops, secret management).
2. **Local development.** Read `references/compose-local-dev.md` when setting up
   or debugging Docker Compose — standard web app stack (app/db/redis/mailpit),
   override files, service discovery and network isolation, volume strategies,
   and the debugging command reference.
3. **Pipeline and release.** Read `references/cicd-deployment.md` when building
   CI/CD or planning a release — GitHub Actions pipeline, deployment strategy
   details, health endpoints and Kubernetes probes, environment validation,
   environment promotion gates (dev → staging → production, migration
   ordering), rollback procedures, and the production readiness checklist.

## Deployment Strategy Decision

| Scenario | Strategy |
|---|---|
| Standard backward-compatible change | Rolling |
| Critical service, instant rollback required | Blue-Green |
| High-risk change, need real-traffic validation | Canary |
| Database schema change (additive only) | Rolling with migration guard |

One-line summaries (full traffic diagrams and trade-offs in
`references/cicd-deployment.md`):

- **Rolling (default):** replace instances one at a time; zero downtime, but two
  versions run simultaneously — changes must be backward-compatible.
- **Blue-Green:** two identical environments, atomic traffic switch; instant
  rollback at the cost of 2x infrastructure during deployment.
- **Canary:** route a small traffic percentage to the new version first; catches
  issues with real traffic but requires traffic-splitting and monitoring.

## Pipeline Stages

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → unit tests → integration tests → build image → deploy staging → smoke tests → deploy production
```

## Production Gate

Before any production release, run the production readiness checklist in
`references/cicd-deployment.md` (application, infrastructure, monitoring,
operations). For the security portion, load `sunnydata-security` for the
technology-specific checklist (secrets, CORS, rate limiting, auth, security
headers, CVE scanning).
