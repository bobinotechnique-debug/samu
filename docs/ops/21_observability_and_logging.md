# Phase 2 Step 14 - Observability, Logging, and Audit Hooks

## Purpose
Provide an authoritative observability contract for structured logging, correlation, and audit hooks that aligns with Phase 1 error, audit, multi-tenancy, and API conventions while integrating Phase 2 security, testing, and deployment deliverables.

## Scope
Applies to all services (API, workers, scripts) and environments (dev, CI, staging, production). Covers log schema, level policy, correlation propagation, audit hooks, redaction, and doc-level verification. Metrics, tracing vendor, and alert thresholds are out of scope.

## Definitions
- request_id: Stable identifier per inbound request or command invocation; echoed across downstream calls.
- trace_id: W3C trace identifier spanning hops (API -> service -> job).
- correlation_id: Alias for trace_id when external clients do not supply tracing headers; may be generated from request_id.
- actor_id/actor_type: Authenticated subject identifiers (user, service principal) per docs/specs/03_multi_tenancy_and_security.md.
- org_id/project_id: Tenant and project boundaries; never nullable for org_id.
- audit event: Immutable record of security-sensitive actions per docs/specs/09_audit_and_traceability.md.

## Principles
- Structured logs only (JSON).
- ASCII-only payloads.
- No secrets and no PII.
- Tenant safety and isolation.
- Determinism (stable keys, stable error codes).

## Log Schema (Authoritative)

| Field | Type/Format | Constraints |
| --- | --- | --- |
| timestamp_utc | string, ISO8601 UTC with milliseconds (e.g., 2026-01-09T12:00:00.123Z) | Required; UTC only; no timezone offsets other than Z |
| level | string enum | Required; one of: debug, info, warn, error, critical; lowercase |
| service | string | Required; service name (api, worker, script); ASCII letters, digits, hyphen |
| module | string | Required; module or file path emitting the log; use dotted module path |
| operation | string | Required; logical operation or use case; stable identifiers (e.g., create_mission) |
| request_id | string | Required for inbound requests; ASCII only; generate if missing; length <= 128 |
| trace_id | string | Required when tracing enabled; W3C trace id (32 hex) preferred; mirror request_id if tracing disabled |
| org_id | string (UUID) | Required for tenant-aware paths per docs/specs/03_multi_tenancy_and_security.md |
| project_id | string (UUID) | Nullable; include when project scoped |
| actor_id | string (UUID) | Nullable; present when authenticated |
| actor_type | string enum | Nullable; user, service, job |
| http_method | string | Nullable; uppercase HTTP verb |
| http_path | string | Nullable; templated path (no raw user segments or query params) |
| status_code | integer | Nullable; HTTP status or synthetic job status code; 100-599 for HTTP |
| error_code | string | Nullable; stable code per docs/specs/11_api_error_model.md; lowercase with dots |
| duration_ms | integer | Nullable; execution duration rounded to ms; non-negative |
| message | string | Required; concise ASCII summary without secrets or PII |

### JSON examples
- Successful API request
```
{"timestamp_utc":"2026-01-09T12:00:00.123Z","level":"info","service":"api","module":"routes.missions","operation":"create_mission","request_id":"req-123","trace_id":"trace-abc","org_id":"org-001","project_id":"proj-100","actor_id":"user-777","actor_type":"user","http_method":"POST","http_path":"/api/v1/projects/{project_id}/missions","status_code":201,"duration_ms":142,"message":"mission created"}
```
- Validation failure
```
{"timestamp_utc":"2026-01-09T12:00:01.010Z","level":"warn","service":"api","module":"validators.mission","operation":"validate_mission","request_id":"req-124","trace_id":"trace-abc","org_id":"org-001","project_id":"proj-100","actor_id":"user-777","actor_type":"user","http_method":"POST","http_path":"/api/v1/projects/{project_id}/missions","status_code":422,"error_code":"validation.error","message":"payload validation failed"}
```
- Authorization failure
```
{"timestamp_utc":"2026-01-09T12:00:02.000Z","level":"warn","service":"api","module":"authz.rbac","operation":"enforce_project_role","request_id":"req-125","trace_id":"trace-abc","org_id":"org-001","project_id":"proj-100","actor_id":"user-888","actor_type":"user","http_method":"GET","http_path":"/api/v1/projects/{project_id}/missions","status_code":403,"error_code":"auth.forbidden","message":"role insufficient for project"}
```
- Database constraint error
```
{"timestamp_utc":"2026-01-09T12:00:03.500Z","level":"error","service":"api","module":"repos.missions","operation":"insert_mission","request_id":"req-126","trace_id":"trace-abc","org_id":"org-001","project_id":"proj-100","actor_id":"user-777","actor_type":"user","http_method":"POST","http_path":"/api/v1/projects/{project_id}/missions","status_code":409,"error_code":"db.constraint_violation","message":"unique mission code violation"}
```
- Background job retry
```
{"timestamp_utc":"2026-01-09T12:05:00.000Z","level":"warn","service":"worker","module":"jobs.sync_assignments","operation":"sync_assignment","request_id":"job-req-200","trace_id":"trace-job-200","org_id":"org-001","project_id":"proj-100","actor_id":null,"actor_type":"job","status_code":503,"error_code":"job.retry","duration_ms":1200,"message":"retrying due to downstream timeout"}
```

## Log Levels Policy
- DEBUG: Internal diagnostics without secrets; allowed only locally. Not emitted in CI or production.
- INFO: Successful operations, state transitions, startup/shutdown, background job completion. Allowed in all environments with sampling in production if volume requires.
- WARN: Validation issues, throttling, retries, authz denials without security incident indicators. Allowed in all environments; CI should assert presence of required fields.
- ERROR: Unexpected exceptions, failed dependencies, database constraint violations mapped to 4xx/5xx. Must include error_code. Production and staging always emit; CI allowed when tests assert behavior.
- CRITICAL: System-wide failures, data loss risk, security incidents. Emits pager integrations when alerting exists. Never sampled.

Environment rules: dev allows DEBUG/INFO; CI defaults to INFO/WARN/ERROR only; staging and production exclude DEBUG and require WARN+ for policy enforcement.

## Correlation and Propagation
- request_id: Generated per inbound HTTP request; preserved through service calls and injected into background job payloads/metadata. Scripts use a synthetic request_id per execution.
- trace_id: Prefer W3C Trace Context. When absent, derive from request_id. Must be forwarded across API -> worker boundaries and stored on job retry attempts.
- Correlation headers: Accept X-Request-Id and W3C Trace Context; respond with both request_id and trace_id. Background jobs log upstream request_id and trace_id for stitching.
- Idempotency and jobs: Idempotency keys (per docs/specs/23_async_jobs.md) must be logged under operation context and linked to request_id/trace_id to dedupe retries.

## Audit Events (Authoritative)
- Distinguish logs vs audits: logs capture operational context; audit events are immutable, security-grade records stored separately per docs/specs/09_audit_and_traceability.md.
- Audit schema:

| Field | Type/Format | Constraints |
| --- | --- | --- |
| timestamp_utc | ISO8601 UTC | Required |
| event_type | string enum | Required; categorized per MUST list |
| actor_id | string (UUID) | Required when authenticated; else service principal id |
| actor_type | string enum | user, service, job |
| org_id | string (UUID) | Required |
| project_id | string (UUID) | Nullable; include when scoped |
| target_id | string | Nullable; mission, assignment, project, org identifiers |
| request_id | string | Required to bind to logs |
| trace_id | string | Required when tracing enabled |
| metadata | object | Required; structured, no secrets or PII |

- MUST-audit actions: authentication success/failure, org lifecycle (create/update/archive), project lifecycle, mission CRUD, assignment changes, RBAC changes, imports/exports, file attachments for mission run sheets, and any data access scope elevation.
- Emission points: service layer hooks right after authorization and before persistence commits; retries must avoid duplicate audit records by using idempotency keys.

## Error Observability Mapping
- Align with docs/specs/11_api_error_model.md:
  - validation.error -> WARN log with error_code and 422 status; no audit unless access policy changed.
  - auth.unauthenticated -> WARN log; audit authentication failure.
  - auth.forbidden -> WARN log; audit authorization denial when policy would otherwise allow change.
  - conflict.* (e.g., db.constraint_violation) -> ERROR log with 409 status; audit when data integrity change fails after authorization.
  - server.error.* -> ERROR or CRITICAL depending on blast radius; audit when incident involves data loss risk.
- Audit categories: authentication events, authorization denials involving privileged operations, data lifecycle changes (org/project/mission/assignment), RBAC mutations, import/export, and file attachment actions.

## Redaction Rules
- Strip secrets, tokens, passwords, raw headers, and PII (names, emails, phone numbers). Do not log payload bodies.
- Safe identifiers: org_id, project_id, mission_id, assignment_id, request_id, trace_id, job identifiers, and stable error codes.
- Normalize http_path to templated routes; never include raw IDs or user-provided path segments unless templated.

## Testing and Verification (Doc-level)
- Future CI checks: static lint to enforce presence of required fields in log factories; schema snapshot tests for logging middleware; contract tests that assert error_code mapping for Phase 1 error model; audit hook tests to ensure required event types are emitted on CRUD and RBAC changes.

## Out of Scope
- Metrics vendor selection.
- Tracing vendor selection.
- Alerting thresholds and dashboards.
