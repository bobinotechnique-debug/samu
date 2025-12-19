# Phase 2 Step 20 - Consistency and Idempotency Strategy

## Goals
- Declare authoritative consistency, idempotency, retry, and concurrency rules for synchronous APIs and asynchronous jobs aligned with Phase 2 Steps 17 (rate limiting), 18 (circuit breakers), and 19 (caching).
- Prevent duplicate writes and cross-organization leakage by enforcing deterministic idempotency keys, optimistic locking, and replay-safe audit behavior across sync and async flows.
- Provide testable, enforceable guidance for API middleware, service layers, and worker wrappers without introducing runtime code changes.

## Definitions
- Consistency: Visibility of committed writes to authorized readers. Strong consistency applies within a single aggregate write path; eventual consistency applies to derived read models and async side effects.
- Idempotency: Repeating the same operation with the same identifiers and payload produces the same result and no additional side effects.
- Retry-safe: A failure class where retrying the operation will not violate idempotency or ordering rules (e.g., transient 503 with idempotent endpoint and stable payload).
- At-least-once: Delivery guarantee where a message or job may be processed one or more times; consumers must be idempotent.
- Exactly-once (emulated): Effect achieved through idempotency keys, deduplication, and optimistic locking even though the underlying transport is at-least-once.

## Scope Boundaries and Consistency Model
- Organization: Absolute security boundary; no cross-organization writes or reads. All keys include org_id.
- Project: Functional boundary for planning. Writes affecting a project are strongly consistent within the aggregate being mutated; derived projections may be eventually consistent.
- Mission and Assignment: Aggregates under a project. Commands targeting a single mission or assignment are strongly consistent for that aggregate. Dashboard summaries, notifications, and search indexes are eventually consistent via async jobs.
- Cross-aggregate effects: Any action affecting more than one aggregate is modeled as a command plus explicit async side effects; no multi-aggregate transactions.

## Write Patterns
- Allowed:
  - Single-aggregate synchronous writes (e.g., POST /v1/projects/{id}/missions) with optimistic locking and audit logging.
  - Command + async side effects pattern: write primary aggregate synchronously, enqueue outbox/event for notifications, search indexing, or read model fan-out.
  - Idempotent PUT/DELETE endpoints that replace or remove a single aggregate state under version control.
- Forbidden:
  - Multi-aggregate transactions spanning projects or organizations.
  - Hidden writes during read paths (GET endpoints must not mutate state or touch idempotency storage).
  - Cross-organization side effects or implicit fan-out beyond the caller org.

## API Idempotency Contract
- Header: `Idempotency-Key` is required for all non-GET writes (POST, PUT, PATCH, DELETE). Keys are ASCII, max 128 chars, opaque to clients.
- Scope: Key is scoped to `org_id + endpoint path template + canonical request body hash`. Canonical body uses stable field ordering and normalized types; clients must not embed timestamps or random data in the hash input.
- Replay rules:
  - Same key + same canonical payload: return original successful response (status, body, headers) without re-executing side effects; include `Idempotency-Replayed: true` header.
  - Same key + different payload: return HTTP 409 Conflict with machine code `idempotency.payload_mismatch` and no mutation.
- Storage model:
  - Durable table `idempotency_records` with optional Redis cache layer for fast lookup.
  - Recommended schema:
    | Column | Type | Constraints | Notes |
    | --- | --- | --- | --- |
    | org_id | uuid | part of PK, not null | Partitions keys per organization. |
    | endpoint | text | part of PK, not null | Path template, e.g., `/v1/projects/{project_id}/missions`. |
    | idempotency_key | text | part of PK, not null | Exact header value; max 128 chars. |
    | canonical_body_hash | text | not null | Stable hash (e.g., SHA256 hex). |
    | request_fingerprint | text | not null | Deterministic combination of method, endpoint, org_id, project_id/mission_id when applicable. |
    | response_status | int | not null | Stored HTTP status of the initial request. |
    | response_body | jsonb | not null | Full response payload for replay. |
    | response_headers | jsonb | not null | Whitelisted headers (content-type, etag, correlation ids). |
    | created_at | timestamptz | not null | Inserted on first successful write. |
    | expires_at | timestamptz | not null | TTL cutoff for cleanup and cache eviction alignment. |
  - Redis cache (optional): mirror durable records keyed by `idempo:{env}:{org_id}:{endpoint}:{idempotency_key}` with TTL matching `expires_at`; cache misses fall back to the table.
- TTL and cleanup:
  - Default TTL: 24h for successful writes; 4h for error responses to limit stale conflicts. No infinite retention.
  - Cleanup job runs hourly to purge expired records from table and Redis. Cleanup is idempotent and scoped by org_id.
- Error cases and status codes:
  - Missing header on write: 400 Bad Request (`idempotency.key_required`).
  - Payload mismatch on replay: 409 Conflict (`idempotency.payload_mismatch`).
  - Expired record replay: treat as new request; new record may be created if payload matches validation and locking rules.
  - Backend storage failure: 503 Service Unavailable; callers may retry with same key following backoff guidance.

## Retry Strategy
- Retryable failures: network timeouts, 502/503/504, and 429 when rate limit headers indicate a retry window. Retries must respect the endpoint idempotency contract and must not bypass optimistic locking.
- Non-retryable failures: 4xx validation errors (400/401/403/404/409 payload mismatch/version conflict), feature-disabled responses, and semantic errors.
- Backoff guidance:
  - Clients: exponential backoff with jitter, initial delay 200-500ms, max delay 5s, cap at 5 attempts. Respect `Retry-After` on 429/503.
  - Workers: bounded attempts (max 5) with exponential backoff starting at 1s, jittered up to 50 percent. Record attempt count in job metadata.
- Interaction rules:
  - Rate limiting (Step 17): retries must honor rate limit headers; do not retry before `Retry-After`. Idempotency keys remain stable across retries.
  - Circuit breakers (Step 18): when a breaker is open, do not enqueue new retries; return breaker-specific 503 and preserve idempotency record without side effects.
  - Caching (Step 19): cache entries must not be created or invalidated by failed or replayed writes; cache invalidation triggers only on successful primary writes.

## Async Jobs Idempotency
- Job idempotency key: `job:{org_id}:{queue}:{job_type}:{resource_id or hash}` generated at enqueue time; required for all job messages.
- Dedup strategy: workers first check a durable deduplication store (per org) before execution; if a record with the same key is complete, acknowledge without re-running side effects.
- Execution model: assume at-least-once delivery. Jobs must tolerate duplicate delivery by using idempotent writes, optimistic locking, and side-effect guards.
- Retry handling:
  - Retries reuse the same job key and carry forward attempt count and correlation ids.
  - Workers must isolate partial work by using transactional outbox patterns or unit-of-work boundaries; no partial commits without recorded completion.
- Poison and dead-letter policy (doc-only): mark jobs as poison after max attempts or non-retryable errors; route to dead-letter queue with error reason, payload hash, org_id, and correlation ids for audit.
- Visibility timeout / lease renewal (doc-only): workers acquire a lease per job; renew before 50 percent of lease duration; on lease expiration without completion marker, job becomes visible for retry.

## Concurrency Control
- Optimistic locking: every mutable aggregate includes a `version` (integer) or `updated_at` monotonic timestamp. Writes include the expected version; mismatches return 409 Conflict (`concurrency.version_mismatch`).
- Conflict semantics: the first valid write wins. Clients must refetch the latest state on 409 and reapply changes with a new idempotency key if the payload changes.
- Conflict handling matrix:
  | Operation | Conflict Trigger | Response | Client Action |
  | --- | --- | --- | --- |
  | Mission create | Duplicate idempotency key with different payload | 409 Conflict (`idempotency.payload_mismatch`) | Reissue with corrected payload and new key |
  | Assignment move | Version mismatch on assignment aggregate | 409 Conflict (`concurrency.version_mismatch`) | Refetch assignment, reapply move with new key and updated version |
  | Mission update | Simultaneous updates where optimistic lock fails | 409 Conflict (`concurrency.version_mismatch`) | Refetch mission, reconcile fields, retry with new key |

## Audit and Traceability
- Correlation ids: propagate `X-Request-ID` (sync) and `X-Correlation-ID` (async) end-to-end; persist both alongside idempotency records and job dedup entries.
- Idempotent replays: on replayed responses, do not create new audit records; instead, log an `audit.replay` event referencing the original audit id, correlation ids, and idempotency key.
- First execution logging: record audit events for the primary write, outbox enqueue, and any downstream job scheduling with org_id, actor, endpoint, payload hash, and version. Replays log only the replay marker plus access metadata.

## Implementation Hooks (Documentation Only)
- Enforcement placement:
  - API middleware handles `Idempotency-Key` validation, persistence lookup, and replay responses.
  - Service layer enforces optimistic locking, command validation, and explicit cache invalidation for successful writes only.
  - Worker wrapper validates job idempotency keys, manages leases, and records dedup completion markers before emitting side effects.
- Required test categories (names only, no code):
  - Unit: idempotency key parsing/validation, payload hash canonicalization, optimistic lock evaluator, replay response builder.
  - Integration: end-to-end POST with retry and replay semantics, conflict on mismatched payload, optimistic lock 409 path, worker retry with dedup store, visibility timeout lease renewal handling, cleanup job purging expired idempotency records.
  - Security: cross-org isolation of idempotency records and job dedup entries, header tampering rejection, inference prevention via key scoping.

## Security and Tenancy Constraints
- Idempotency keys must not leak org structure; keys are opaque and stored only alongside org_id and endpoint metadata. No client-visible reflection of raw hashes beyond conflict errors.
- Storage partitioning: all idempotency and dedup tables and caches include `org_id` in primary keys and indexes to prevent cross-organization lookups. Queries must filter by org_id first.
- Observability and rate limiting: structured logs and metrics include org_id, idempotency key hash (truncated), endpoint, status, and replay flag; metrics must not expose raw keys. Rate limiting decisions must be evaluated before idempotency persistence to avoid storing rejected requests beyond 429 needs.
