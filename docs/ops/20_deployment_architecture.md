# Deployment and Environments

## Purpose
Define how the system runs across environments with reproducible local and CI setups using the locked stack (Docker Compose, GitHub Actions, PowerShell scripts).

## Environments
- **Local:** Docker Compose orchestrates API, worker, PostgreSQL, Redis, and frontend dev server; seeded org/project data via seed.ps1.
- **CI:** GitHub Actions executes guards.ps1 and test suites with ephemeral PostgreSQL/Redis services; artifacts published for preview environments.
- **Staging:** Parity with production topology using Compose or orchestrator; feature flags enabled for experimental APIs.
- **Production:** Hardened network boundaries, managed PostgreSQL/Redis services, autoscaled API/worker replicas, CDN for frontend assets.

## Configuration
- Environment variables supplied via `.env` files for local and secrets managers for CI/staging/production.
- Strongly typed configuration module reads required settings (database URL, Redis URL, JWT keys, OIDC endpoints, CORS origins) with validation at startup.
- Per-environment overrides stored separately; no defaults that infer organization context.

## Secrets Management
- Secrets stored in GitHub Actions secrets for CI, Vault/KeyVault/SSM for staging/production; never committed.
- Rotation runbooks define cadence and rely on migrate.ps1/dev_up.ps1 to reload services without downtime.

## Deployment Topology
- API and worker images built from the same codebase with different entrypoints; tagged builds per commit.
- Frontend built into static assets served by CDN or edge cache with immutable versioning per commit hash.
- Reverse proxy terminates TLS and forwards to FastAPI; rate limiting and WAF rules applied at the edge.

## Observability and Operations
- Centralized logging with correlation_id, organization_id, project_id injected by middleware.
- Metrics scraped for API latency, worker throughput, queue depth, and database health; alerts configured per environment.
- Backups scheduled for PostgreSQL with restore drills; Redis persistence limited to queues/caches per design.

## Reproducibility Guarantees
- dev_up.ps1/dev_down.ps1 provide deterministic startup/teardown for local.
- validate.ps1 orchestrates guards and tests before deployment.
- Migration and seed scripts are idempotent and organization-scoped to avoid cross-tenant bleed.
