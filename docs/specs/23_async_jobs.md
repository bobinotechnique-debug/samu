# Async and Background Jobs

## Purpose
Define the asynchronous execution model to support long-running or reliability-critical work without violating auditability or organization isolation.

## Job Types
- **Notification dispatch:** Fan-out of mission/assignment events to channels (email/webhook) with per-organization templates.
- **Search indexing:** Project and mission indexing into search backends with idempotent upserts.
- **Data imports/exports:** Controlled ingestion of mission timelines or collaborator rosters with validation and audit logging.
- **Audit replication:** Forwarding audit events to cold storage or observability pipelines.

## Queues and Topology
- Single Redis broker with namespaced queues per organization (e.g., `org:{id}:notifications`, `org:{id}:backfill`).
- Workers subscribe to specific queue groups based on job type to reduce contention and blast radius.
- Dead letter queues capture exhausted retries with metadata for operators.

## Retry and Idempotency
- Exponential backoff with jitter and a maximum retry count per job type; notification retries lower than data sync retries.
- Idempotency keys derived from entity identifiers and correlation_id; workers must check prior completion markers before side effects.
- Poison message detection moves jobs to dead letter with structured error payloads.

## Observability
- Metrics: queue depth, processing latency, success/failure counts, retry counts per job type.
- Logs include organization_id, project_id, correlation_id, job_type, attempt, and actor_id when available.
- Alerts trigger on sustained queue growth or repeated failures for a single organization.

## Safety and Isolation
- Workers re-validate organization_id/project_id and authorization context before mutating state.
- No implicit reads across organizations; caches are scoped to the queue namespace.
- Jobs must emit audit events when mutating domain entities to satisfy docs/specs/09_audit_and_traceability.md.

## Alignment with Phase 1
- Avoids hidden coupling per docs/specs/06_known_failure_patterns.md by keeping explicit job metadata.
- Honors ownership and RBAC rules from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md during worker execution.
- Uses API conventions for any callbacks, keeping routes under `/api/v1/` with organization scoping (docs/specs/10_api_conventions.md).
