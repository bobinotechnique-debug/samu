# Mission Page Contract (Phase 1 Step 07)

## 1. Overview
- Name: Mission
- Goal: Display a single mission's schedule, assignments, conflicts, and collaborator engagement with clear RBAC and audit coverage.
- Primary actors: Mission leads, project planners, collaborators assigned to the mission.

## 2. URL and deep links
- Canonical route: /mission
- Query params: organization_id (required), project_id (required), mission_id (required), timeframe_start/timeframe_end (optional for zoom), filter tokens for assignment status or role, selection (assignment_id), page cursor.
- Anchor rules: #header, #timeline, #assignments, #side-panel anchors must remain stable and map to structural regions.

## 3. Regions and required components
- Header: avatar stack representing mission leads and primary collaborators; conflict badge in header when mission has unresolved conflicts.
- Primary surface: timeline bar showing mission duration and assignment segments; conflict badge overlays conflicting windows.
- Side panel: data table of mission assignments with filter bar docked above it for status/role filters; rows may include avatar stack for assigned collaborators.

## 4. Data model bindings
- Required API endpoints (convention reference):
  - GET /api/v1/projects/{project_id}/missions/{mission_id}
  - GET /api/v1/projects/{project_id}/missions/{mission_id}/assignments?status&role&cursor&page_size
  - GET /api/v1/projects/{project_id}/missions/{mission_id}/conflicts?timeframe_start&timeframe_end
- Filters/sort/pagination mapping: filter bar maps to assignment status and role; data table uses cursor pagination and sortable columns aligned to docs/specs/10_api_conventions.md.
- ID and time rules: mission_id and assignment_id are opaque; times in UTC ISO 8601; organization_id and project_id required on all requests.

## 5. UI states
- Loading: header avatar stack shows placeholders; timeline bar and data table show skeletons; actions disabled.
- Empty: if no assignments exist, data table shows empty state; timeline shows mission window with no assignment bands.
- Partial data: if mission loads but assignments or conflicts fail, show mission metadata with inline warning; conflict badges only when conflict query succeeds.
- Error: map API errors to messages; allow manual retry per dataset.
- Permission denied: show denial message; hide assignment rows and mutation controls while preserving read-only mission summary if allowed.

## 6. Interactions
- Selection model: selecting an assignment in data table highlights corresponding timeline segment; timeline selection syncs back to table selection and query param.
- Primary actions: open collaborator profile via assignment row; edit assignment when RBAC allows (control disabled otherwise).
- Bulk actions: multi-select assignment rows for bulk status update; actions only available when RBAC permits.
- Keyboard accessibility baseline: tab order flows header -> filter bar -> data table -> timeline; Enter activates selection; space toggles row selection where supported.

## 7. RBAC and ownership
- View: users with mission_view scoped by organization_id and project_id.
- Edit: mission leads and project planners with mission_edit may modify assignments; unauthorized users see disabled controls with tooltips.
- Redaction rules: collaborator details redacted when collaborator_view is missing; avatar stack shows anonymized placeholders.

## 8. Audit and traceability
- User action events: page load, filter changes, selection changes, conflict badge opens.
- Mutation events: assignment edits and bulk status updates record mission_id, assignment_ids, previous and updated values, and timestamps.
- Correlation id propagation: carry correlation_id from mission fetch to assignment mutations and emitted audit records.

## 9. Forbidden patterns
- No client-side conflict resolution; rely on conflict endpoint.
- No hidden assignment filters; filter bar reflects all filters.
- No silent retries; retries require user initiation.
- No mixing mission data across projects or organizations.
