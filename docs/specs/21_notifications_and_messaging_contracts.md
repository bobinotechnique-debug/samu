# Notifications and Messaging Contracts

## Status
Proposed (Phase 1 Step 13).

## Purpose
Document notification and messaging contracts so future implementations can deliver consistent, auditable communications without altering runtime behavior in Phase 1.

## Scope
- Applies to notification definitions, templates, delivery metadata, and read-only status reporting.
- Covers email and in-app notification channels that surface planning and mission events to collaborators.
- Aligns with Phase 1 API conventions (docs/specs/10_api_conventions.md), error model (docs/specs/11_api_error_model.md), and identifier/time rules (docs/specs/13_identifiers_and_time.md).

## Assumptions
- Organization is the hard security boundary; project is the planning boundary.
- Missions inherit project scope; cross-organization visibility is forbidden.
- Notifications are GET-only in Phase 1; no delivery pipelines or schedulers exist yet.

## Exclusions
- Implementing notification services, queues, or schedulers.
- Adding UI components or pages beyond existing Phase 1 contracts.
- Integrating third-party messaging providers or modifying runtime configuration.

## Contracts and Rules
- **Triggers**: Notifications may be registered for mission assignment changes, mission schedule updates, conflict flags, and audit-significant events. Every trigger must capture organization_id and project_id, with mission_id when applicable.
- **Envelope**: Each notification payload MUST include a stable notification_id (opaque), recipient collaborator_id, organization_id, project_id, trigger type, created_at (UTC ISO 8601), and delivery channel. No client-generated identifiers are allowed.
- **Templates**: Templates define subject/title, body/summary, contextual links (using Step 04 routing conventions), and must reference the visual language tokens from docs/specs/14_visual_language.md for in-app surfaces.
- **RBAC**: Delivery eligibility MUST evaluate the RBAC model (docs/specs/08_rbac_model.md) before enqueueing. Default-deny applies; recipients require explicit permission for the underlying event.
- **Audit**: Every notification generation event records correlation_id, actor, trigger source, and delivery channel. Read receipts are out of scope, but delivery attempt logs must be auditable as read-only records.
- **Delivery Status**: Status values are read-only (queued, sent, failed) and follow docs/specs/11_api_error_model.md for failure codes. Retrying or state mutation is outside Phase 1 scope.
- **Localization and Accessibility**: Templates declare locale and accessibility notes (ARIA text for in-app banners/toasts) but do not ship assets; rendering details defer to component contracts in docs/specs/15_ui_component_contracts.md.

## Forbidden Patterns
- Cross-organization notifications or aggregation of recipients outside organization boundaries.
- Client-generated identifiers or client-side delivery state authority.
- Embedding executable links or instructions that bypass API contracts defined in docs/specs/10_api_conventions.md.
- Implicit RBAC bypass or UI-only gating without server-side enforcement.

## Cross-References
- Step 04 API conventions and error model for envelope, pagination, and error handling.
- Step 05/06 visual language and component rules for in-app display alignment.
- Step 03 ownership, RBAC, and audit specs for scoping and mandatory logging.
