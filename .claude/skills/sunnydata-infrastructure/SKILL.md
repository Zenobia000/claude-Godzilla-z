---
name: sunnydata-infrastructure
description: Docker containerization and deployment patterns — Dockerfile best practices, Compose for local dev, CI/CD pipelines, deployment strategies (Rolling/Blue-Green/Canary), health checks, and production readiness. Use when containerizing apps, setting up local dev environments, or planning deployments.
---

<!-- 繁體中文說明：此技能整合 docker-patterns 與 deployment-patterns，涵蓋從本機容器化到正式環境部署的完整工作流程。 -->

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

---

## Part 1: Containers (Docker)

### Dockerfile Best Practices

One canonical multi-stage pattern per language. The `dev` stage is used by Compose; the `production` stage ships to production.

#### Node.js

```dockerfile
# Stage: dependencies
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Stage: dev (hot reload — used by Compose)
FROM node:22-alpine AS dev
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Stage: build
FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build && npm prune --production

# Stage: production (minimal, non-root)
FROM node:22-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && adduser -S appuser -u 1001
USER appuser
COPY --from=build --chown=appuser:appgroup /app/dist ./dist
COPY --from=build --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=build --chown=appuser:appgroup /app/package.json ./
ENV NODE_ENV=production
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

#### Go

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

FROM alpine:3.19 AS production
RUN apk --no-cache add ca-certificates
RUN adduser -D -u 1001 appuser
USER appuser
COPY --from=builder /server /server
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["/server"]
```

#### Python

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

FROM python:3.12-slim AS production
WORKDIR /app
RUN useradd -r -u 1001 appuser
USER appuser
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### .dockerignore

Defined once — apply to all projects:

```
node_modules
.git
.env
.env.*
dist
coverage
*.log
.next
.cache
docker-compose*.yml
Dockerfile*
README.md
tests/
```

### Docker Compose (Local Development)

#### Standard Web App Stack

```yaml
# docker-compose.yml
services:
  app:
    build:
      context: .
      target: dev                     # Use dev stage of multi-stage Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - .:/app                        # Bind mount for hot reload
      - /app/node_modules             # Anonymous volume — preserves container deps
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379/0
      - NODE_ENV=development
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: npm run dev

  db:
    image: postgres:16-alpine
    ports:
      - "127.0.0.1:5432:5432"        # Localhost-only; omit entirely in production
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app_dev
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

  mailpit:                            # Local email testing
    image: axllent/mailpit
    ports:
      - "8025:8025"                   # Web UI
      - "1025:1025"                   # SMTP

volumes:
  pgdata:
  redisdata:
```

#### Override Files

```yaml
# docker-compose.override.yml — auto-loaded in development
services:
  app:
    environment:
      - DEBUG=app:*
      - LOG_LEVEL=debug
    ports:
      - "9229:9229"                   # Node.js debugger

# docker-compose.prod.yml — explicit for production
services:
  app:
    build:
      target: production
    restart: always
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
```

```bash
# Development (auto-loads override)
docker compose up

# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

#### Service Discovery and Networking

Services in the same Compose network resolve by service name:

```
# From "app" container:
postgres://postgres:postgres@db:5432/app_dev    # "db" resolves to the db container
redis://redis:6379/0                             # "redis" resolves to the redis container
```

Custom networks for isolation:

```yaml
services:
  frontend:
    networks: [frontend-net]

  api:
    networks: [frontend-net, backend-net]

  db:
    networks: [backend-net]           # Only reachable from api, not frontend

networks:
  frontend-net:
  backend-net:
```

#### Volume Strategies

```yaml
services:
  app:
    volumes:
      - .:/app                        # Bind mount: source code, enables hot reload
      - /app/node_modules             # Anonymous: protect container deps from host overlay
      - /app/.next                    # Anonymous: protect build cache

  db:
    volumes:
      - pgdata:/var/lib/postgresql/data                          # Named: persists across restarts
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql # Bind: init script
```

### Container Security

#### Dockerfile Hardening

```dockerfile
# 1. Pin exact versions (never :latest)
FROM node:22.12-alpine3.20

# 2. Run as non-root
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
USER app

# 3. No secrets in image layers — use env vars or Docker secrets at runtime
```

#### Compose Security Options

```yaml
services:
  app:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /app/.cache
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE              # Only if binding to ports < 1024
```

#### Secret Management

```yaml
# GOOD: env_file (never commit .env)
services:
  app:
    env_file:
      - .env
    environment:
      - API_KEY                       # Inherits from host environment

# GOOD: Docker secrets (Swarm mode)
secrets:
  db_password:
    file: ./secrets/db_password.txt

services:
  db:
    secrets: [db_password]

# BAD:
# ENV API_KEY=sk-proj-xxxxx          # Never hardcode secrets in image
```

### Debugging

```bash
# Logs
docker compose logs -f app
docker compose logs --tail=50 db

# Shell into container
docker compose exec app sh
docker compose exec db psql -U postgres

# Inspect
docker compose ps
docker compose top
docker stats

# Rebuild
docker compose up --build
docker compose build --no-cache app

# Teardown
docker compose down
docker compose down -v                # Also removes volumes — DESTRUCTIVE
docker system prune

# Network diagnosis
docker compose exec app nslookup db
docker compose exec app wget -qO- http://api:3000/health
docker network ls
docker network inspect <project>_default
```

---

## Part 2: Deployment

### CI/CD Pipeline

#### GitHub Actions (Standard Pipeline)

```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage
          path: coverage/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy to production
        run: |
          # Platform-specific deployment command:
          # Railway:  railway up
          # Vercel:   vercel --prod
          # K8s:      kubectl set image deployment/app app=ghcr.io/${{ github.repository }}:${{ github.sha }}
          echo "Deploying ${{ github.sha }}"
```

#### Pipeline Stages

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → unit tests → integration tests → build image → deploy staging → smoke tests → deploy production
```

### Deployment Strategies

#### Rolling (Default)

Replace instances one at a time — old and new versions run simultaneously during rollout.

```
Instance 1: v1 → v2
Instance 2: v1
Instance 3: v1

Instance 1: v2
Instance 2: v1 → v2
Instance 3: v1

Instance 1: v2
Instance 2: v2
Instance 3: v1 → v2
```

**Pros:** Zero downtime, gradual rollout
**Cons:** Two versions run simultaneously — changes must be backward-compatible
**Use when:** Standard deployments

#### Blue-Green

Two identical environments; switch traffic atomically.

```
Blue  (v1) ← traffic
Green (v2)   idle, running new version

# After verification:
Blue  (v1)   idle (standby for rollback)
Green (v2) ← traffic
```

**Pros:** Instant rollback (switch back to blue), clean cutover
**Cons:** Requires 2x infrastructure during deployment
**Use when:** Critical services, zero-tolerance for issues

#### Canary

Route a small percentage of traffic to the new version first.

```
v1: 95% of traffic
v2:  5% of traffic   (canary)

# If metrics look good:
v1: 50%  →  v2: 50%

# Final:
v2: 100% of traffic
```

**Pros:** Catches issues with real traffic before full rollout
**Cons:** Requires traffic-splitting infrastructure and monitoring
**Use when:** High-traffic services, risky changes, feature flags

#### Decision Matrix

| Scenario | Strategy |
|---|---|
| Standard backward-compatible change | Rolling |
| Critical service, instant rollback required | Blue-Green |
| High-risk change, need real-traffic validation | Canary |
| Database schema change (additive only) | Rolling with migration guard |

### Health Checks and Probes

#### Health Endpoint (define once per service)

```typescript
// Simple liveness check
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

// Detailed check (internal monitoring / readiness)
app.get("/health/detailed", async (req, res) => {
  const checks = {
    database: await checkDatabase(),
    redis: await checkRedis(),
    externalApi: await checkExternalApi(),
  };

  const allHealthy = Object.values(checks).every(c => c.status === "ok");

  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? "ok" : "degraded",
    timestamp: new Date().toISOString(),
    version: process.env.APP_VERSION || "unknown",
    uptime: process.uptime(),
    checks,
  });
});

async function checkDatabase(): Promise<HealthCheck> {
  try {
    await db.query("SELECT 1");
    return { status: "ok", latency_ms: 2 };
  } catch (err) {
    return { status: "error", message: "Database unreachable" };
  }
}
```

#### Kubernetes Probes

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 30
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 2

startupProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 0
  periodSeconds: 5
  failureThreshold: 30              # 30 * 5s = 150s max startup time
```

### Environment Configuration

```bash
# All config via environment variables — never hardcoded (12-Factor)
DATABASE_URL=postgres://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
API_KEY=${API_KEY}                  # Injected by secrets manager
LOG_LEVEL=info
PORT=3000
NODE_ENV=production
```

```typescript
// Validate at startup — fail fast if config is wrong
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "staging", "production"]),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

export const env = envSchema.parse(process.env);
```

### Rollback Strategy

```bash
# Kubernetes
kubectl rollout undo deployment/app

# Vercel
vercel rollback

# Railway
railway up --commit <previous-sha>

# Database migration rollback (if reversible)
npx prisma migrate resolve --rolled-back <migration-name>
```

**Rollback prerequisites:**
- [ ] Previous image/artifact is available and tagged
- [ ] Database migrations are backward-compatible (no destructive changes)
- [ ] Feature flags can disable new features without a deploy
- [ ] Monitoring alerts configured for error rate spikes
- [ ] Rollback procedure tested in staging before production release

### Production Readiness Checklist

#### Application
- [ ] All tests pass (unit, integration, E2E)
- [ ] Error handling covers all edge cases
- [ ] Logging is structured (JSON) and does not contain PII
- [ ] Health check endpoint returns meaningful status
- [ ] Environment variables validated at startup (fail fast)

#### Infrastructure
- [ ] Docker image builds reproducibly (pinned versions)
- [ ] Resource limits set (CPU, memory)
- [ ] Horizontal scaling configured (min/max instances)
- [ ] SSL/TLS enabled on all endpoints

#### Security
> Load `sunnydata-security` for the technology-specific checklist (secrets,
> CORS, rate limiting, auth, security headers, CVE scanning).

#### Monitoring
- [ ] Application metrics exported (request rate, latency, error rate)
- [ ] Alerts configured for error rate above threshold
- [ ] Log aggregation set up (structured, searchable)
- [ ] Uptime monitoring on `/health` endpoint

#### Operations
- [ ] Rollback plan documented and tested
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios
- [ ] On-call rotation and escalation path defined
