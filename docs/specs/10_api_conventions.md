# API Design Conventions

## Purpose
Define authoritative REST API design conventions that prevent drift, ensure consistency, and constrain backend and frontend integration work.

## Scope
- Applies to all HTTP APIs under /api/v1/ exposed by the platform.
- Covers resource orientation, URL structure, HTTP verb semantics, idempotency, filtering, sorting, and pagination.
- Binding for backend implementation and frontend consumption in subsequent phases.

## Assumptions
- Phase 1 is documentation-only; no endpoints or schemas are implemented yet.
- Architecture and domain guardrails from prior steps remain authoritative.
- Multi-tenancy and data ownership rules mandate explicit organization context in every call.

## Exclusions
- Concrete endpoint payload schemas and field-level definitions.
- Protocols beyond HTTP/HTTPS.
- Client SDK design and language-specific idioms.

## REST Principles
- APIs MUST be resource-oriented; RPC-style verb nouns (e.g., /runReport) MUST NOT be introduced.
- Resources MUST be pluralized consistently (e.g., /projects, /missions) and MUST align with domain terminology.
- Nested resources MAY be used when enforcing ownership context (e.g., /organizations/{org_id}/projects/{project_id}/missions/{mission_id}).
- Every resource operation MUST include explicit organization context either in the URI or enforced through token claims; implicit context is forbidden.

## URL Structure
- All endpoints MUST live under the /api/v1/ prefix; future versions MUST use /api/{version}/.
- Resource identifiers in paths MUST be opaque IDs defined in docs/specs/13_identifiers_and_time.md.
- Collection endpoints MUST use plural nouns (e.g., /api/v1/projects) and item endpoints MUST append the opaque identifier (e.g., /api/v1/projects/{project_id}).
- Nested paths MUST preserve ownership ordering: /api/v1/organizations/{org_id}/projects/{project_id}/missions/{mission_id}.
- Query parameters MUST be used for filtering, sorting, and pagination; path segments MUST NOT encode these concerns.

## HTTP Verbs and Idempotency
- GET MUST be safe and idempotent, returning the current representation without side effects.
- POST MUST be used to create resources or trigger non-idempotent actions; duplicate POSTs MUST be guarded by idempotency keys when clients may retry.
- PUT MUST fully replace the target resource representation and MUST be idempotent.
- PATCH MUST perform partial updates and MUST be idempotent in effect; patch semantics MUST define deterministic merge behavior.
- DELETE MUST be idempotent; repeated deletes MUST return success with no side effects beyond the first removal.
- OPTIONS and HEAD MAY be exposed for discovery and lightweight checks and MUST be side-effect free.

## Filtering, Sorting, and Pagination
- Filtering MUST use query parameters prefixed with filter[attribute], such as filter[status]=active; multiple filters MUST be ANDed unless documented otherwise.
- Sorting MUST use a sort parameter with comma-separated fields; descending order MUST be indicated with a leading dash (e.g., sort=-created_at,name).
- Pagination MUST use page[number] and page[size] query parameters; defaults MUST be documented per resource and MUST cap maximum sizes server-side.
- Collection responses MUST include pagination metadata (page number, page size, total count, total pages) alongside data arrays.
- Servers MUST reject unknown filter or sort fields with a validation error defined in docs/specs/11_api_error_model.md.

## Forbidden Patterns
- Verbs in URLs (e.g., /api/v1/projects/create, /api/v1/projects/{id}/delete) are forbidden; HTTP verbs MUST convey action semantics.
- Mixed pluralization or inconsistent resource naming across endpoints MUST NOT occur.
- Implicit organization or project context derived solely from authentication tokens MUST NOT replace explicit scoping enforced in URIs or validated claims.
- Query-parameter overloading (e.g., using a single q parameter for unrelated filters) MUST NOT be used.
- Side-effectful GET, HEAD, or OPTIONS requests are forbidden.
