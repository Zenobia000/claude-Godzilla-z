# Dockerfile patterns and container security

Load this reference when writing or reviewing a Dockerfile, `.dockerignore`, or
container hardening configuration.

## Dockerfile Best Practices

One canonical multi-stage pattern per language. The `dev` stage is used by Compose; the `production` stage ships to production.

### Node.js

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

### Go

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

### Python

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

## .dockerignore

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

## Container Security

### Dockerfile Hardening

```dockerfile
# 1. Pin exact versions (never :latest)
FROM node:22.12-alpine3.20

# 2. Run as non-root
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
USER app

# 3. No secrets in image layers — use env vars or Docker secrets at runtime
```

### Compose Security Options

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

### Secret Management

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
