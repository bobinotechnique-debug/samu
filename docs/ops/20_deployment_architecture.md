# Phase 2 Step 08 - Deployment and Environments

Status: Starting

## Objective

Define how the system runs across environments with configuration, secrets management, and reproducible local/CI setups aligned to locked technology stack decisions.

This document is documentation-only. It defines contracts and expectations. It does not implement infrastructure.

## Scope

In scope:

* Environment matrix (local, CI, staging, production).
* Configuration strategy (settings model, precedence, validation).
* Secrets handling (what is a secret, where it lives, rotation expectations).
* Deployment topology (services, dependencies, ports, network boundaries).
* Reproducible developer setup (Windows-first PowerShell workflow) and CI alignment.
* Operational guardrails (health checks, readiness, migrations, rollback strategy).

Out of scope:

* Choosing a cloud provider.
* Writing Terraform/Ansible/Kubernetes manifests.
* Implementing runtime logic.

## Non-goals

* No ad-hoc per-developer configuration.
* No plaintext secrets in Git.
* No environment-specific behavior inside business logic.

## Authoritative inputs

This doc must remain consistent with:

* docs/specs/20_architecture_HLD.md
* docs/specs/21_architecture_LLD.md
* docs/specs/22_persistence_model.md
* docs/api/20_api_architecture.md
* docs/specs/23_async_jobs.md
* docs/specs/24_security_model.md
* docs/ux/20_frontend_architecture.md
* AGENT.md (locked stack, Windows-first, ASCII-only, CI green)

If a conflict is found, raise an issue and stop; do not silently diverge.

## Definitions

* Environment: a named runtime context with specific config values and secrets.
* Config: non-secret settings (URLs, feature flags, limits) that can be stored in plain text.
* Secret: any value that grants access or can be used to impersonate (tokens, passwords, private keys, API keys).
* Reproducible: a clean machine can reach a working state from docs + scripts with no manual hidden steps.

## Environment matrix

The system supports four environments.

### 1) local

Purpose: developer workstation for iterative work.
Characteristics:

* Docker Compose is the default orchestration.
* Uses .env.local (uncommitted) for local overrides.
* Uses seeded data optionally.
* Debug logging enabled.

### 2) ci

Purpose: deterministic builds and tests in GitHub Actions.
Characteristics:

* No interactive steps.
* Uses ephemeral databases/redis.
* Uses minimal secrets (only what CI needs).
* Produces build artifacts (if configured), but does not deploy by default.

### 3) staging

Purpose: pre-production validation.
Characteristics:

* Mirrors production topology as closely as possible.
* Uses real external integrations only if safe and isolated.
* Strict migrations policy (forward-only, automated).

### 4) production

Purpose: real users.
Characteristics:

* Secrets stored in a dedicated secret store.
* Strict logging and monitoring.
* Hardening enabled (secure headers, rate limits, least privilege).

## Service topology

This section defines the logical services and their dependencies.

### Services

* api: FastAPI application (HTTP)
* db: PostgreSQL
* cache: Redis (queues, rate limits, caching)
* worker: background job workers
* scheduler: optional periodic job runner (or worker mode with beat-like scheduler)
* web: frontend static build served via a web server (or node dev server in local)

Notes:

* The exact split between worker and scheduler depends on the async model in docs/specs/23_async_jobs.md.
* If running as a single worker process with scheduled triggers, document that explicitly in ops runbooks.

### Dependency graph

* api depends on db, cache
* worker depends on db, cache
* scheduler depends on db, cache
* web depends on api (at runtime for API calls)

### Network boundaries

* db and cache are private to the internal network.
* api is public (behind reverse proxy in staging/prod).
* web is public (served behind reverse proxy/CDN in staging/prod).

### Ports (default, local)

These are local-only defaults; they must be overrideable.

* api: 8000
* web: 5173 (dev) or 80 (static)
* db: 5432
* redis: 6379

## Configuration strategy

### Principles

* Single settings model per service.
* Validation on boot; fail fast if required config is missing.
* No secret values in logs.
* Default values exist only for safe local development.
* All config keys are documented.

### Precedence order

Highest to lowest:

1. Explicit environment variables
2. .env file (local only)
3. Built-in defaults (local-safe only)

CI, staging, production MUST NOT rely on defaults for critical settings.

### Settings naming

* Use uppercase snake case for environment variables.
* Prefix by service boundary when shared repo is used.
  Example:

  * API__DATABASE_URL
  * API__REDIS_URL
  * API__JWT_ISSUER
  * WEB__PUBLIC_API_BASE_URL

### Configuration categories

* Runtime: ports, hostnames, URLs
* Database: URLs, pool sizes
* Security: JWT issuer/audience, token lifetimes, CORS origins
* Observability: log level, tracing endpoint
* Feature flags: explicit toggles (default off in production unless specified)
* Limits: pagination max, upload size max

### Required settings

The following MUST be explicitly provided outside local:

* Database connection string
* Redis connection string
* Auth/JWT material (issuer, signing keys, audience)
* CORS allowlist (if applicable)
* External integration keys (if enabled)

## Secrets handling

### What counts as a secret

* Any password, token, private key, signing key, API key.
* Database credentials if not using a managed identity.
* Encryption keys for at-rest or field-level encryption.

### Rules

* No secrets in Git history.
* No secrets in logs.
* No secrets in front-end bundles.
* Rotation must be possible without code changes.

### Storage expectations per environment

* local: .env.local (uncommitted). Optionally a local secret manager.
* ci: GitHub Actions secrets (minimal). Use OIDC to cloud secret manager if available.
* staging/prod: dedicated secret store (cloud-native secret manager or vault). Inject as env vars at runtime.

### Key rotation and versioning

* Signing keys MUST support rotation (kid-based) when JWT is used.
* Database passwords: rotate using dual credentials window where possible.
* Any integration tokens: rotate by creating a new token, updating secret store, then revoking old.

## Build and release artifacts

### Backend

* Build artifact is a container image tagged with:

  * immutable git SHA tag
  * optional semantic tag (if release)

### Frontend

* Build output is static assets (dist) packaged into:

  * a container image serving static files, OR
  * an object storage + CDN deployment (provider-specific, not specified here)

### Version stamping

* Expose build metadata:

  * GIT_SHA
  * BUILD_DATE
  * APP_VERSION

These must be present in:

* api /health or /version endpoint
* web footer or about screen (read-only)

## CI alignment

### CI goals

* Deterministic, reproducible runs.
* Same docker-compose service graph as local when feasible.
* No reliance on developer machine state.

### Minimum CI pipeline expectations

* Lint + type checks (backend and frontend)
* Unit tests (backend and frontend)
* Contract checks for docs guards (ASCII, indices, roadmap)
* Database migration checks (alembic head present, no divergence)

### Caching

* Allow caching of dependencies (pip, node_modules) but must not alter correctness.

## Data and migrations

### Migration policy

* Migrations are forward-only.
* Staging runs migrations automatically during deploy.
* Production migrations:

  * either automated with a guarded job
  * or manual step with a documented runbook

### Rollback strategy

* Prefer rolling forward with a corrective migration.
* Application rollback is allowed only if schema is backward compatible.

### Seed data

* local only by default.
* staging may have synthetic data seeded for demos.
* production seeding is prohibited except through controlled admin flows.

## Health, readiness, and startup ordering

### Endpoints

* /health: process alive
* /ready: dependencies reachable (db, cache)

### Startup ordering

* db and cache must be reachable before api/worker become ready.
* web can start independently but must point to correct API base.

## Logging and observability

### Logging

* Structured logs (JSON recommended) in staging/prod.
* Correlation ids propagated from ingress to workers.
* Audit logs follow docs/specs/09_audit_and_traceability.md constraints.

### Metrics and tracing

* Expose basic metrics (latency, error rates, queue depth).
* Tracing is optional but recommended for async chains.

## Local developer workflow (Windows-first)

### Expected entry points

* PowerShell scripts under a single folder (as defined in AGENT.md).
* Commands must be ASCII-only.
* One-command up/down for local stack.

### Local stack expectations

* docker compose up starts db, cache, api, worker, web.
* hot reload enabled for api and web.
* ability to reset local db without deleting unrelated docker volumes.

### Files

* .env.example committed with non-secret placeholders.
* .env.local ignored by git.

## Deployment topology (staging/prod)

This section remains provider-agnostic.

### Reverse proxy / ingress

* Terminates TLS.
* Routes /api to api service.
* Serves web static assets.

### Scaling

* api: scale horizontally.
* worker: scale by queue depth.
* db: managed service recommended (not required by this doc).
* cache: managed service recommended.

### Isolation

* Separate staging and production resources.
* Separate databases per environment.
* No cross-environment credential reuse.

## Security hardening notes

* Enforce least privilege for service accounts.
* Strict CORS allowlist.
* Secure headers for web.
* Rate limiting at edge and/or api.
* Dependency pinning and SBOM generation (optional but recommended).

## Acceptance criteria

* Environment matrix is explicit and complete.
* Config precedence and naming conventions are explicit.
* Secrets rules are explicit and forbid plaintext in Git.
* Deployment topology is provider-agnostic and consistent with HLD/LLD.
* Local and CI expectations align (compose graph, reproducibility).

## Appendix A - Example configuration keys (non-exhaustive)

API:

* API__ENV
* API__BASE_URL
* API__DATABASE_URL (secret)
* API__REDIS_URL (secret)
* API__JWT_ISSUER
* API__JWT_AUDIENCE
* API__JWT_PRIVATE_KEY (secret)
* API__CORS_ORIGINS
* API__LOG_LEVEL

WEB:

* WEB__PUBLIC_API_BASE_URL
* WEB__LOG_LEVEL

WORKER:

* WORKER__DATABASE_URL (secret)
* WORKER__REDIS_URL (secret)
* WORKER__CONCURRENCY

## Appendix B - Deployment checklist (high level)

* Validate config and secrets present.
* Run migrations (staging always, prod per policy).
* Deploy api.
* Deploy worker/scheduler.
* Deploy web.
* Run smoke checks (/health, /ready, core flows).
* Monitor error rates and queue depth.
* Record deployment in audit/release log.
