# Phase 2 Step 15 - Resilience and Error Handling

## Purpose
Define an enforceable resilience model that keeps API behavior predictable under failures, load, and misuse while aligning with the existing API conventions, error envelope, async job policies, audit, and observability contracts.

## Scope
- Applies to synchronous HTTP APIs, background workers, and supporting services within the platform topology described in docs/ops/20_deployment_architecture.md.
- Governs error propagation, retries, timeouts, idempotency, degraded modes, and conceptual circuit breaker expectations.
- Documentation only; no runtime behavior changes are implemented here.

## Authoritative inputs
- docs/specs/10_api_conventions.md
- docs/specs/11_api_error_model.md
- docs/specs/23_async_jobs.md
- docs/specs/09_audit_and_traceability.md
- docs/ops/20_deployment_architecture.md
- docs/ops/21_observability_and_logging.md

## Error categories and propagation
Error categories align to the global error envelope in docs/specs/11_api_error_model.md and MUST remain stable:
- Client errors: malformed payloads, missing fields, invalid formats. Use HTTP 400 with validation.* codes; propagate details to the caller without retries.
- Authentication errors: missing or invalid credentials. Use HTTP 401 with auth.* codes; do not disclose principal existence; no retries unless client refreshes credentials explicitly.
- Authorization errors: insufficient scope or cross-organization access. Use HTTP 403 with auth.* codes; never retried automatically; MUST include org boundary context when safe.
- Domain errors: business rule violations or conflicts. Use HTTP 409 or 422 with domain-scoped codes; never retried automatically.
- Infrastructure errors: database, cache, or internal service failures. Map to HTTP 500-range codes prefixed with server.*; callers MAY retry only when the operation is idempotent.
- Dependency errors: failures from external providers or downstream services. Map to HTTP 502/503/504 with dependency.* codes; retries follow the policy matrix below and MUST be observable.

Propagation rules:
- Do not downgrade or mask errors; preserve category semantics and error.code values.
- Every error response MUST include request_id and timestamp fields per docs/specs/11_api_error_model.md to support audit and tracing.
- Logs MUST include error_code and correlation identifiers per docs/ops/21_observability_and_logging.md; audit events MUST record failures that impact authorization, data integrity, or security posture.

## Retry policy matrix
- Synchronous API clients: No automatic retries by the frontend. Server-side retries MUST be explicit, bounded, and only for idempotent operations (GET, HEAD, safe PUT/DELETE) when the failure is transient (timeout, 5xx). Use exponential backoff with jitter and emit job.retry logs. No silent retries.
- Background jobs: Follow docs/specs/23_async_jobs.md defaults (max attempts, exponential backoff with jitter) and category overrides. Non-retryable classes remain validation, authorization, and domain rule violations. Poison jobs move to deadletter with alerts.
- Integrations with external providers: Retries are allowed only when the provider signals transient errors (5xx or 429) and when the call is idempotent; backoff MUST respect provider guidance and stop after bounded attempts.
- Database and cache operations: Rely on service-layer retries for transient connection failures only; avoid retrying statement-level conflicts that would violate idempotency.

## Timeout ownership
- API boundary: Request-level timeouts are owned by the API service and MUST fit within user-facing latency budgets; when a timeout fires, return a dependency.* or server.timeout code with 504 or 503 status.
- Service layer: Each internal call (database, cache, queue) sets its own timeout shorter than the request timeout to avoid cascading failures; timeouts MUST be logged with error_code and correlation identifiers.
- External dependencies: Callers define explicit timeouts per provider; never rely on provider defaults. Timeout values and categories MUST be documented and tested; exceedance leads to dependency.* errors surfaced to the API or job layer.

## Idempotency expectations
- All background jobs MUST honor idempotency keys as defined in docs/specs/23_async_jobs.md and remain safe under retries within the same org boundary.
- Synchronous APIs that mutate state MUST declare idempotency behavior: PUT/DELETE endpoints are idempotent by contract; POST endpoints requiring idempotency MUST accept an Idempotency-Key header scoped to org_id and project_id when applicable.
- Idempotent operations MUST record and reuse request_id and idempotency_key to avoid duplicate side effects across retries and circuit transitions.

## Degraded mode principles
- Prefer explicit read-only modes over silent partial writes; when write paths are unavailable, return clear error codes and communicate read-only state in responses.
- Partial availability is allowed only when isolated dependencies fail (e.g., notification provider); core domain writes MUST NOT proceed if integrity cannot be enforced.
- Derived or cached data MUST NOT be silently served as authoritative when primary stores are degraded; surface the degradation through headers and logs.
- Recovery from degraded mode MUST be observable via metrics and audit events where applicable.

## Circuit breaker expectations (conceptual)
- Circuit breakers wrap external dependencies and non-core internal services to prevent cascade failures. They monitor failure rates, timeouts, and concurrency saturation.
- States: closed (normal), open (fail fast with dependency.circuit_open errors), half-open (probe with limited concurrent requests).
- Breaker decisions MUST be driven by metrics and logs defined in docs/ops/21_observability_and_logging.md; events SHOULD emit audit records when breaker states change for org-affecting operations.
- Breakers MUST NOT introduce alternative data sources or hidden fallbacks; they fail fast with documented error codes.

## Non-goals and forbidden patterns
- No hidden fallbacks to stale data or alternate providers without explicit contract changes.
- No infinite or unbounded retries; every retry strategy must be capped and observable.
- No client-side retry loops outside documented idempotent cases; frontend MUST follow guidance in API documentation.
- No swallowing exceptions or returning generic 500 errors without structured error_code and correlation identifiers.
- No cross-organization spillover during failover or retries; org boundary remains the primary safety and rate limit boundary.
