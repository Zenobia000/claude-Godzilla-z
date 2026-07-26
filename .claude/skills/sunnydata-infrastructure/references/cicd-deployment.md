# CI/CD, deployment strategies, and production readiness

Load this reference when building a pipeline, choosing or executing a deployment
strategy, wiring health checks, or preparing a production release.

## CI/CD Pipeline

### GitHub Actions (Standard Pipeline)

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

### Pipeline Stages

```
PR opened:
  lint → typecheck → unit tests → integration tests → preview deploy

Merged to main:
  lint → typecheck → unit tests → integration tests → build image → deploy staging → smoke tests → deploy production
```

## Deployment Strategies

### Rolling (Default)

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

### Blue-Green

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

### Canary

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

### Decision Matrix

| Scenario | Strategy |
|---|---|
| Standard backward-compatible change | Rolling |
| Critical service, instant rollback required | Blue-Green |
| High-risk change, need real-traffic validation | Canary |
| Database schema change (additive only) | Rolling with migration guard |

## Health Checks and Probes

### Health Endpoint (define once per service)

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

### Kubernetes Probes

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

## Environment Configuration

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

## Environment Promotion (dev → staging → production)

Promotion is an artifact moving through gates, not a rebuild per environment.

- **Build once, promote the artifact.** The image built on merge is the only
  artifact that ever reaches production: tag it immutably (git SHA + semver),
  deploy that exact digest to staging, and promote the same digest to
  production. Rebuilding for production means testing one artifact and shipping
  another — never do it. Only environment variables and injected secrets differ
  between environments.
- **Each environment is a gate with an owner.** An environment promotion is a
  release decision, not a pipeline side effect:

  | Promotion | Required evidence | Approver |
  |---|---|---|
  | dev → staging | CI green (lint, typecheck, unit, integration) | automatic |
  | staging → production | staging smoke + E2E green, security scan clean, rollback path verified | named release owner — record who and when |

  Evidence must be fresh output from the pipeline run of the promoted digest;
  a green run of a different commit proves nothing.
- **Migrations gate the promotion, not the deploy.** Schema changes ship
  expand-contract: the expand migration (additive, backward-compatible) runs
  and is verified in staging **before** the app version that depends on it is
  promoted; the contract migration (dropping old columns/paths) is a separate
  later promotion, only after the old app version is no longer deployable as a
  rollback target. A promotion whose rollback would break against the current
  schema is not ready.
- **Track release state separately.** Which digest is in which environment is
  release status — its own axis, never merged into requirement, code, or
  verification status.

## Rollback Strategy

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

## Production Readiness Checklist

### Application
- [ ] All tests pass (unit, integration, E2E)
- [ ] Error handling covers all edge cases
- [ ] Logging is structured (JSON) and does not contain PII
- [ ] Health check endpoint returns meaningful status
- [ ] Environment variables validated at startup (fail fast)

### Infrastructure
- [ ] Docker image builds reproducibly (pinned versions)
- [ ] Resource limits set (CPU, memory)
- [ ] Horizontal scaling configured (min/max instances)
- [ ] SSL/TLS enabled on all endpoints

### Security
> Load `sunnydata-security` for the technology-specific checklist (secrets,
> CORS, rate limiting, auth, security headers, CVE scanning).

### Monitoring
- [ ] Application metrics exported (request rate, latency, error rate)
- [ ] Alerts configured for error rate above threshold
- [ ] Log aggregation set up (structured, searchable)
- [ ] Uptime monitoring on `/health` endpoint

### Operations
- [ ] Rollback plan documented and tested
- [ ] Database migration tested against production-sized data
- [ ] Runbook for common failure scenarios
- [ ] On-call rotation and escalation path defined
