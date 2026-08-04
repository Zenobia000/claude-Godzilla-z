# Docker Compose for local development

Load this reference when setting up or debugging a Compose-based local
development environment.

## Standard Web App Stack

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

## Override Files

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

## Service Discovery and Networking

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

## Volume Strategies

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

## Debugging

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
