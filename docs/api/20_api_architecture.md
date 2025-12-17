# API Architecture and Routing

## Purpose
Define practical API wiring for Phase 2 using Phase 1 conventions (docs/specs/10_api_conventions.md, docs/specs/11_api_error_model.md, docs/specs/12_api_versioning.md).

## Route Groups
- **/api/v1/organizations**: organization management, member provisioning, and settings.
- **/api/v1/projects**: CRUD with organization scoping; includes project status transitions and archival routes.
- **/api/v1/missions**: mission lifecycle endpoints keyed by project_id; includes scheduling and status changes.
- **/api/v1/assignments**: assignment creation, allocation updates, and conflict checks.
- **/api/v1/collaborators**: collaborator profiles, availability, and role mappings.
- **/api/v1/audit-events**: read-only access with filtering by organization_id, project_id, correlation_id.

## Versioning
- Stable base path `/api/v1/` with compatibility guarantees; breaking changes require `/api/v2/` and deprecation notices.
- Feature flags enable preview endpoints under `/api/v1/experimental/` gated by organization.

## Error Mapping
- Standard error envelope from docs/specs/11_api_error_model.md with codes per domain (e.g., `project.not_found`, `mission.conflict`).
- Validation errors return 400 with field-level messages; authorization failures return 403 with audit hooks.
- Async enqueue responses return 202 with job reference and correlation_id.

## Pagination and Filtering
- Cursor-based pagination default; limit/offset allowed for admin-only list endpoints.
- Filters require explicit organization_id and optional project_id; sorting limited to allowlisted fields.
- List endpoints return total counts when performant, otherwise include `has_more` flag.

## Middleware and Cross-Cutting Concerns
- Authentication middleware validates tokens and injects organization_id/project_id context.
- Request ID and correlation_id generation at ingress; echoed in responses and logs.
- Rate limiting per organization and actor, with 429 mapped to error envelope.

## Alignment with Phase 1
- Respects REST constraints and forbidden patterns from docs/specs/10_api_conventions.md (no verb-named routes, no implicit org context).
- Uses audit requirements from docs/specs/09_audit_and_traceability.md for mutating endpoints.
- Applies ownership and RBAC rules from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md at route handlers.
