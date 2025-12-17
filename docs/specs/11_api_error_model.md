# API Error Model

## Purpose
Define a contractual JSON error model with stable codes and semantics to guarantee predictable handling across clients and services.

## Scope
- Applies to every HTTP error response under /api/v1/.
- Covers error envelope structure, code stability, validation vs business logic failures, and authentication/authorization errors.
- Binding for backend implementations and frontend error handling in future phases.

## Assumptions
- All APIs follow the REST conventions in docs/specs/10_api_conventions.md.
- Authentication and authorization enforce organization boundaries as defined in prior specs.
- Phase 1 documents behavior; runtime implementations will adhere in later phases.

## Exclusions
- Transport-specific retry policies or circuit breaking behaviors.
- Localized error messages or client-side presentation rules.
- Out-of-band logging and monitoring pipelines.

## Global Error Envelope
- Errors MUST be returned as application/json with the following top-level fields:
  - error.code: stable, unique, machine-readable string; treated as part of the public contract.
  - error.message: human-readable summary in English; MUST NOT leak secrets or internal stack traces.
  - error.details: optional array of detail objects describing field-level or rule-level issues.
  - error.request_id: server-generated correlation identifier; MUST be present for every error response.
  - error.timestamp: UTC timestamp in ISO 8601 format as defined in docs/specs/13_identifiers_and_time.md.
- Additional fields MUST NOT be added without a versioned contract change.

## Error Codes and HTTP Status Codes
- HTTP status codes MUST align with semantics: 400 for validation errors, 401 for authentication failures, 403 for authorization denials, 404 for missing resources, 409 for conflict, 422 for business rule violations when distinct from validation, 429 for throttling, 500+ for server errors.
- Error codes MUST remain stable across versions; deprecations require a documented migration path in docs/specs/12_api_versioning.md.
- Codes MUST be namespaced by domain or concern (e.g., auth.invalid_token, project.conflict, validation.required_field).

## Validation Errors vs Business Rule Violations
- Validation errors (HTTP 400) MUST describe malformed input, missing required fields, or invalid formats; each detail entry SHOULD include field, issue, and expected format.
- Business rule violations (HTTP 422) MUST represent well-formed requests that break domain rules (e.g., scheduling conflicts, ownership violations) and MUST include a domain-specific code.
- Validation and business rule errors MUST NOT be merged under a single generic code; clients rely on separation for UX and retries.

## Authentication and Authorization Errors
- Authentication failures MUST return 401 with codes such as auth.missing_token or auth.invalid_token and MUST NOT disclose whether the user exists.
- Authorization failures MUST return 403 with codes such as auth.insufficient_scope or auth.forbidden_org and MUST include the organization_id context when safe.
- Rate limiting or session expiration MUST NOT be signaled with 500-series codes; appropriate 401, 403, or 429 responses MUST be used.

## Example Error Payloads
- Validation error (HTTP 400):
  - {"error": {"code": "validation.required_field", "message": "project_id is required", "details": [{"field": "project_id", "issue": "missing", "expected": "UUID"}], "request_id": "rq_123", "timestamp": "2025-01-01T00:00:00Z"}}
- Business rule violation (HTTP 422):
  - {"error": {"code": "mission.conflict", "message": "Mission overlaps with existing window", "details": [{"field": "time_window", "issue": "overlap", "expected": "non-overlapping"}], "request_id": "rq_456", "timestamp": "2025-01-01T00:00:00Z"}}
- Authentication error (HTTP 401):
  - {"error": {"code": "auth.invalid_token", "message": "Authentication failed", "details": [], "request_id": "rq_789", "timestamp": "2025-01-01T00:00:00Z"}}
- Authorization error (HTTP 403):
  - {"error": {"code": "auth.forbidden_org", "message": "Access to organization is forbidden", "details": [], "request_id": "rq_987", "timestamp": "2025-01-01T00:00:00Z"}}

## Stability Rules
- Error codes are part of the public contract and MUST NOT change semantics without a documented migration path and version bump.
- New error codes MUST be additive and documented; removals or renames MUST follow the deprecation process in docs/specs/12_api_versioning.md.
- Error payload shape MUST remain backward compatible within a version; clients MUST NOT be forced to handle breaking changes within the same major version.
