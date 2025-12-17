# High Level Architecture (HLD)

## Purpose
Define the global technical shape of the SaaS platform using the locked stack (FastAPI, PostgreSQL, Redis, React/Vite/Tailwind, Docker Compose) while honoring Phase 1 ownership, RBAC, audit, and API conventions.

## Context Diagram (Narrative)
- **Clients:** Browsers interact with the frontend (React/Vite) which calls the API gateway under `/api/v1/` using organization-scoped tokens defined in Phase 1 security contracts.
- **API Layer:** FastAPI service exposes HTTP routes grouped by bounded contexts (organizations, projects, missions, assignments, collaborators) enforced by middleware for org_id/project_id validation and audit correlation IDs.
- **Async Workers:** Background workers subscribe to Redis-backed queues for long-running or retryable tasks (notifications, audit fan-out, search indexing) triggered explicitly by API handlers.
- **Persistence:** PostgreSQL holds authoritative data with schemas partitioned by organization_id and project_id; Redis provides ephemeral caching and work queues only.
- **Observability:** Centralized logging and metrics capture API calls, job executions, and security events with correlation to audit identifiers.

## Service Boundaries
- **Gateway/API service:** Single FastAPI application with modular routers per domain context; no hidden coupling across routers beyond shared domain services and auth middleware.
- **Worker service:** Shares domain models with the API but only consumes commands/events enqueued by API handlers; workers never mutate state outside audited commands.
- **Frontend client:** Pure presentation and orchestration of API calls; no business rules or authorization logic beyond token handling and routing guards.
- **Shared components:** Domain services (validation, authorization checks) and infrastructure adapters (database, cache, message bus) are reusable but must honor dependency direction defined in Phase 1 architecture principles.

## Sync vs Async Flows
- **Synchronous:** Request/response paths for CRUD operations, reads, and idempotent commands stay within API service and PostgreSQL transactions with audit logging.
- **Asynchronous:** Workloads exceeding request SLAs (notification fan-out, recalculations, imports) are enqueued to Redis queues with explicit job metadata (organization_id, project_id, correlation_id). API responses acknowledge enqueue actions only.
- **Idempotency:** Async jobs include deduplication keys derived from entity identifiers and timestamps to prevent duplicate effects.

## Trust Boundaries
- **External boundary:** Tokens validated at the edge; unauthenticated traffic rejected before hitting routers. CORS restricted to configured frontend origins.
- **Inter-service boundary:** Workers trust only signed job payloads emitted by the API and re-validate authorization context (organization_id, project_id, actor) before mutations.
- **Data boundary:** PostgreSQL schemas enforce organization_id/project_id foreign keys; caches are namespaced by organization_id to prevent cross-tenant leakage.

## Traceability
- All services emit correlation_id, organization_id, project_id, and actor identifiers into logs and metrics, aligning with Phase 1 audit and identifier rules.

## Alignment with Phase 1
- Adheres to REST conventions (docs/specs/10_api_conventions.md) and ownership contracts (docs/specs/07_data_ownership.md).
- Enforces RBAC evaluation order from docs/specs/08_rbac_model.md and audit fields from docs/specs/09_audit_and_traceability.md.
- Follows architecture principles in docs/specs/04_architecture_principles.md (no circular dependencies, explicit boundaries, ASCII-only tooling).
