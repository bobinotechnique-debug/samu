# Async and Background Jobs

## Purpose
Define the asynchronous execution model with job categories, queues, retry policies, and observability rules that avoid hidden side effects while honoring Phase 1 audit, ownership, and multi-tenancy constraints.

## Scope
- **In scope:** Job categories; async vs sync guidance; queue topology and naming; retry/backoff policies; idempotency and deduplication; ownership and auditability; observability expectations; failure handling and poison-message policies.
- **Out of scope:** Vendor/runtime selection (Celery/RQ/Arq/etc.), implementation of workers/schedulers/brokers, full notification system implementation.

## Inputs and Dependencies
- docs/specs/20_architecture_HLD.md
- docs/specs/21_architecture_LLD.md
- docs/specs/06_known_failure_patterns.md
- docs/specs/09_audit_and_traceability.md

## Definitions
- **Job:** An asynchronous unit of work executed by a worker.
- **Queue:** A named channel that carries jobs of a given category.
- **Attempt:** One execution try for a job.
- **Idempotency key:** A key used to ensure the job effect is applied at most once.
- **Poison message:** A job that repeatedly fails and must be quarantined.

## Principles
1. **Explicitness:** Any state change must be attributable to a request, actor, and job.
2. **Idempotency by default:** All jobs must be safe to retry.
3. **Isolation:** Jobs execute within `org_id` and project scope.
4. **Deterministic side effects:** External calls must be guarded with deduplication and timeouts.
5. **Visibility:** Every job is observable, traceable, and auditable.

## When to use async
- Use async when work exceeds API latency budgets (>300ms typical, >2s worst case), is I/O bound to external systems, aggregates or computes derived data, or must be retried without blocking the user.
- Do **not** use async when the user needs immediate consistency for a small write, the operation is a simple read, or the operation is a short deterministic write with minimal risk.

## Job categories
### 1) Notification jobs
Purpose: deliver email/SMS/push/in-app notifications.
- Must be idempotent per (`org_id`, recipient, template, `payload_hash`, `schedule_bucket`).
- Must not fail the core write path (notification is best-effort unless stated).
- Examples: notify collaborator assignment; notify run sheet update.

### 2) Audit enrichment jobs
Purpose: compute or enrich audit metadata without changing business state.
- Allowed to append audit events or enrich existing audit records.
- Must never mutate domain entities beyond audit tables.
- Example: derive human-readable diffs for run sheet changes.

### 3) Planning computation jobs
Purpose: compute suggestions, detect conflicts at scale, or prepare planning outputs.
- Must not write assignments unless explicitly authorized by a command plus policy.
- Must produce artifacts (results) that are referenceable and reviewable.
- Examples: conflict scans; auto-assign suggestion proposals with ranking.

### 4) Import/export jobs
Purpose: long-running file operations.
- Inputs must be stored with checksums.
- Output must be stored as an artifact with access control.
- Examples: export project planning to PDF/CSV; import collaborator availability.

### 5) Maintenance jobs
Purpose: scheduled housekeeping.
- Must be safe, bounded, and rate-limited.
- Must not violate retention rules.
- Examples: cleanup expired idempotency keys; rebuild search index (future).

## Queue topology
### Queue names
Queues are namespaced and stable:
- `q:critical`
- `q:default`
- `q:notifications`
- `q:planning`
- `q:exports`
- `q:maintenance`
- `q:deadletter`

### Routing rules
- User-facing write follow-ups go to `q:default` unless explicitly critical.
- Notification delivery goes to `q:notifications`.
- Planning computations go to `q:planning`.
- Exports/imports go to `q:exports`.
- Scheduled jobs go to `q:maintenance`.
- Poison jobs go to `q:deadletter`.

### Priority policy
- `q:critical` is reserved for jobs that unblock core flows and have strict SLOs.
- Avoid starving `q:default` by keeping `q:critical` small.

## Job contract
Every job payload MUST include:
- `job_id` (uuid)
- `job_type` (string)
- `org_id` (uuid)
- `project_id` (uuid, optional if not project-scoped)
- `actor_type` (`user` | `system` | `api_key`)
- `actor_id` (uuid|string)
- `request_id` (string)
- `correlation_id` (string)
- `idempotency_key` (string)
- `created_at` (RFC3339)
- `payload` (object)

Optional fields:
- `scheduled_for` (RFC3339)
- `traceparent` (W3C, if available)

## Idempotency and deduplication
### Rules
- A job MUST be idempotent across retries.
- A job MUST be deduplicated by `idempotency_key`.
- Idempotency scope is always within `org_id`.
- For project-scoped jobs, include `project_id` in the key.

### Idempotency key format
Recommended format:
- `<job_type>:<org_id>:<project_id?>:<stable_hash>`

`stable_hash` is derived from normalized inputs (sorted JSON, canonical timestamps).

### Storage and TTL
Idempotency keys must be stored with:
- `status` (`pending` | `running` | `succeeded` | `failed` | `dead`)
- `first_seen_at`
- `last_seen_at`
- `result_ref` (optional)
- `error_ref` (optional)

TTL depends on category:
- Notifications: 7 days
- Planning computations: 30 days
- Exports/imports: 30 days
- Maintenance: 7 days

## Retry and backoff policy
### Default retry policy
- Max attempts: 5
- Backoff: exponential with jitter
- Base delay: 5s
- Max delay: 5m

### Category overrides
- **Notifications:** max attempts 10; max delay 30m.
- **Planning:** max attempts 3; max delay 2m.
- **Exports:** max attempts 5; max delay 10m.

### Non-retryable errors
Do not retry when:
- Validation errors (malformed payload, missing required fields).
- Authorization/ownership violations.
- Business rule violations (conflict, forbidden state transition).

Retry when:
- Network timeouts, transient DB errors.
- External provider 5xx or rate-limit (with provider-specific backoff).

## Poison message and dead letter
A job is considered poison when it reaches max attempts or repeatedly fails with non-transient errors.
- Move to `q:deadletter`.
- Persist full error context (sanitized).
- Emit an alert event.
- Provide an operator action plan: replay, discard, or fix-forward.

## Consistency model
- Async jobs are eventually consistent.
- API writes must return success based on committed DB state only.
- Jobs may compute derived views; these must not be treated as authoritative writes unless explicitly stated.

## Ownership and security
- Jobs MUST enforce the same ownership rules as synchronous APIs.
- `org_id` boundary is mandatory and validated before execution.
- Any cross-tenant processing is forbidden.
- Secrets must not be embedded in job payloads.

## Audit and traceability
### Required audit events
Emit audit events for: `job.enqueued`, `job.started`, `job.succeeded`, `job.failed`, `job.deadlettered`, and optionally `job.retried`.

Each audit event must include: `org_id`, `project_id` (if relevant), `actor_type`, `actor_id`, `request_id`, `correlation_id`, `job_id`, `job_type`, `attempt`, and timestamps.

### Linking to Phase 1 audit model
Job events map to the audit and traceability contract defined in docs/specs/09_audit_and_traceability.md.

## Observability
### Logs
- Structured logs only.
- Include `request_id`, `correlation_id`, `job_id`, `job_type`, `org_id`, `project_id`.
- Never log secrets or PII beyond policy.

### Metrics
Minimum metrics:
- `jobs_enqueued_total{job_type,queue}`
- `jobs_started_total{job_type,queue}`
- `jobs_succeeded_total{job_type,queue}`
- `jobs_failed_total{job_type,queue,error_class}`
- `jobs_duration_seconds{job_type,queue}`
- `jobs_attempts_histogram{job_type}`
- `deadletter_total{job_type,queue}`

### Tracing
- Propagate trace context when available.
- Link spans from API request to worker execution.

## Scheduling
Scheduled jobs are allowed only for maintenance tasks or explicitly requested delayed notifications.
- `scheduled_for` must be explicit.
- Clock drift tolerance: 60s.
- Scheduled jobs must remain idempotent.

## Cancellation
Jobs may be cancellable when they have not started or are cooperative and can checkpoint.
- Cancel request creates an audit event.
- Worker checks cancellation token between steps.

## Acceptance criteria
- Defines job categories and queue names.
- Defines mandatory payload contract fields.
- Defines retry/backoff policies and non-retryable errors.
- Defines idempotency and deduplication rules.
- Aligns with audit and ownership constraints.
- Defines observability expectations.
- Defines poison/deadletter policy.

## Open questions (tracked, not blocking)
- Which runtime will be used for workers (Celery/RQ/Arq/etc.)?
- Where to store idempotency keys (DB vs Redis) per architecture constraints?
- What are the initial SLOs per queue?
