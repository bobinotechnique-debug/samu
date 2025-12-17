# Project Page Contract (Phase 1 Step 07)

## 1. Overview
- Name: Project
- Goal: Provide a project summary surface that exposes missions, collaborators, timelines, and conflict signals for project owners and contributors.
- Primary actors: Project owners, planners, mission leads, stakeholders with view access.

## 2. URL and deep links
- Canonical route: /project
- Query params: organization_id (required), project_id (required), timeframe_start/timeframe_end (optional), mission_status filter, collaborator filter, selection (mission_id), page cursor.
- Anchor rules: #header, #timeline, #missions, #side-panel anchors remain stable for deep links.

## 3. Regions and required components
- Header: avatar stack showing project owners and planners; filter bar for mission status and collaborator filters; conflict badge when project has open conflicts.
- Primary surface: timeline bar displaying missions across the selected timeframe; conflict badges overlay conflicting mission windows.
- Side panel: data table of missions with status, owner, timeframe columns; avatar stack in rows for mission leads; conflict badge per row when applicable.

## 4. Data model bindings
- Required API endpoints (convention reference):
  - GET /api/v1/projects/{project_id}
  - GET /api/v1/projects/{project_id}/missions?status&collaborator_id&timeframe_start&timeframe_end&cursor&page_size
  - GET /api/v1/projects/{project_id}/conflicts?timeframe_start&timeframe_end
- Filters/sort/pagination mapping: filter bar sets mission status and collaborator filters; data table uses cursor pagination and sortable columns per docs/specs/10_api_conventions.md; timeline respects the same filters and timeframe.
- ID and time rules: project_id and mission_id opaque; organization_id required; times in UTC ISO 8601.

## 5. UI states
- Loading: header avatar stack placeholders; timeline and data table skeletons; actions disabled until project and mission queries resolve.
- Empty: timeline and data table show empty states if no missions match filters; guidance to adjust filters/timeframe.
- Partial data: project metadata loads while missions or conflicts fail; render available data with inline warning; conflict badges only on successful conflict fetch.
- Error: map errors via docs/specs/11_api_error_model.md; retries manual per dataset.
- Permission denied: explicit denial; hide mission data and mutation controls; header remains for navigation context.

## 6. Interactions
- Selection model: selecting a mission in timeline highlights corresponding row in data table and syncs selection query param.
- Primary actions: open mission page from selection; initiate project-level planning actions when RBAC permits.
- Bulk actions: multi-select missions in data table for bulk status changes when authorized.
- Keyboard accessibility baseline: tab order header -> filter bar -> data table -> timeline; arrow keys navigate timeline focus; Enter activates selection; space toggles multi-select.

## 7. RBAC and ownership
- View: users with project_view scoped by organization_id and project_id.
- Edit: project owners and planners with project_edit may change mission metadata or create missions; disabled controls show permission tooltips when not allowed.
- Redaction rules: collaborator details redacted if viewer lacks collaborator_view; avatar stack uses anonymized placeholders when redacted.

## 8. Audit and traceability
- User action events: page load, filter changes, selection changes, conflict badge expansion.
- Mutation events: mission edits, bulk updates, and project-level planning actions record project_id, mission_ids, prior and updated states, timestamps, and actor identifiers.
- Correlation id propagation: propagate correlation_id from project fetch to subsequent mission mutations and audit events.

## 9. Forbidden patterns
- No hidden mission filters; filter bar must reflect defaults.
- No client-derived conflict logic; rely on conflict endpoint and conflict badge.
- No silent retries; retries initiated by the user.
- No cross-project data mixing on this page.
