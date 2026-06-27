# Infrastructure

Docker Compose for local development lives at the repository root (`docker-compose.yml`).

Kubernetes Helm charts and production deployment configs will be added in **Phase 4 — Scale & Enterprise (v3.0)**.

## Local stack

| Service  | Port | Purpose        |
|----------|------|----------------|
| API      | 8000 | FastAPI backend |
| Postgres | 5432 | Primary database |
| Redis    | 6379 | Task queue broker |
