# UI Page Contracts (Phase 1 Step 07)

## Purpose
Lock page-level contracts that assemble approved Phase 1 components into authoritative surfaces. Prevent drift during Phase 2+ implementation by defining navigation, data bindings, RBAC, audit hooks, and shared states that every page must honor.

## Inputs
- Phase 1 Step 04 conventions: API envelopes, pagination, filters, identifiers, and time handling.
- Phase 1 Step 06 components: data table, timeline bar, avatar stack, conflict badge, filter bar, and global component rules in docs/specs/15_ui_component_contracts.md.

## Scope
- Documentation only; no frontend or backend implementation.
- Applies to Planning, Mission, Collaborator, and Project pages.
- Pages may only assemble approved Step 06 components.

## Global Rules
- Every page uses the contract template defined in Phase 1 Step 07 (sections 1-9).
- Routes, query params, and anchors must follow Step 04 URL conventions; identifiers are opaque and scoped by organization_id and project_id as applicable.
- API bindings reference convention-aligned endpoints (marked "convention reference") and must respect pagination, filtering, and error envelopes from docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md.
- Time values are UTC ISO 8601 without implicit conversion (docs/specs/13_identifiers_and_time.md).
- Only the approved Step 06 components are allowed on these pages; no bespoke widgets.
- Loading/empty/error/permission states must be explicit and aligned with component state contracts (docs/specs/15_ui_component_contracts.md).
- Conflict display always uses the conflict badge with source metadata.
- Navigation between pages must preserve context via query params (e.g., project_id, mission_id, collaborator_id).

## Shared Page State Model
- Loading: show skeleton or loading state per component; actions disabled until data present.
- Empty: render empty-state copy inside the primary component (data table empty slot or timeline bar empty band) with guidance to adjust filters.
- Partial data: show available rows/bands with inline warnings where dependent queries fail; never hide partial results.
- Error: map API error codes to UI-visible messages per docs/specs/11_api_error_model.md; provide retry control without auto-retries.
- Permission denied: render explicit denial message and suppress data payload; maintain navigation shell to allow back navigation.

## Navigation and Deep Links
- Canonical routes must be stable and singular per page; query params carry selection, filter, sort, page cursor, and timeframe.
- Anchors target structural regions (header, primary surface, side panels) and must not depend on client-only IDs; deep link anchors for mission_id, assignment_id, and conflict_id MUST map to visible UI elements.
- Deep links preserve filters and time ranges so other users can reproduce the view state; saved view identifiers, when present, MUST also be encoded.
- State restore: navigating back to a page MUST reapply the last known selection and filter tokens from the URL or saved view; transient modal state (e.g., inspection drawer) is not restored automatically.

## Audit and RBAC Binding Rules
- RBAC decisions follow docs/specs/08_rbac_model.md with explicit organization_id and project_id gating.
- Viewability and editability must be checked before rendering editable controls; disabled states still display ownership context.
- Audit hooks capture view events (page load, filter changes), selection changes, and mutation intents (create/update/delete) with correlation_id propagation (docs/specs/09_audit_and_traceability.md).

## Forbidden Page Patterns
- No local business rules or derived permissions in the client; defer to API responses and RBAC evaluation order.
- No silent retries or hidden refresh loops; retries must be user-triggered.
- No hidden filters; default filters are visible and editable through the filter bar.
- No implicit timezone shifts; display and input in UTC with explicit offset when shown.
- No mixing of data from different organizations or projects in a single page view.

## Page Contracts
The following documents apply these rules using the shared template:
- docs/ux/pages/01_planning.md
- docs/ux/pages/02_mission.md
- docs/ux/pages/03_collaborator.md
- docs/ux/pages/04_project.md
