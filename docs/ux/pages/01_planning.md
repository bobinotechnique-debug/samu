# Planning Page Contract (Phase 1 Step 07)

## 1. Overview
- Name: Planning
- Goal: Provide a project-scoped planning surface that aligns missions, assignments, and conflicts across time.
- Primary actors: Project planners, mission leads, viewers with project access.

## 2. URL and deep links
- Canonical route: /planning
- Query params: organization_id (required), project_id (required), timeframe_start (UTC ISO 8601), timeframe_end (UTC ISO 8601), filter tokens for status/owner/conflict, sort, page cursor, selection (mission_id or assignment_id).
- Anchor rules: Anchors reference structural regions (#header, #timeline, #list, #side-panel) and must remain stable.

## 3. Regions and required components
- Header: filter bar for visible filters and search; avatar stack showing primary planners for quick context.
- Primary surface: timeline bar visualizing missions and assignments within the selected timeframe; conflict badge overlays any band with detected conflicts.
- Side panel: data table listing missions/assignments matching current filters; conflict badge displayed within rows that carry conflicts.

## 4. Data model bindings
- Required API endpoints (convention reference):
  - GET /api/v1/projects/{project_id}/missions?timeframe_start&timeframe_end&status&owner&cursor&page_size
  - GET /api/v1/projects/{project_id}/assignments?timeframe_start&timeframe_end&status&owner&cursor&page_size
  - GET /api/v1/projects/{project_id}/conflicts?timeframe_start&timeframe_end
- Filters/sort/pagination mapping: filter bar maps to query params (status, owner_id, conflict flag); data table and timeline honor the same filters; pagination uses cursor per docs/specs/10_api_conventions.md.
- ID and time rules: mission_id and assignment_id are opaque; timeframe uses UTC ISO 8601 with no implicit conversion; organization_id and project_id required on all requests.

## 5. UI states
- Loading: timeline bar shows loading bars; data table shows skeleton rows; actions disabled until both mission and assignment queries resolve.
- Empty: timeline and data table show empty states with guidance to adjust filters or timeframe.
- Partial data: if missions load but assignments fail (or vice versa), render loaded dataset with inline warning banner; conflict badges only for datasets that loaded.
- Error: map API error codes to user messages; retries are manual per dataset.
- Permission denied: show explicit denial message; hide mission/assignment payloads but keep header for navigation.

## 6. Interactions
- Selection model: clicking a mission or assignment in timeline or data table syncs selection across both surfaces; selected item reflected in query param selection.
- Primary actions: open mission details via selection; initiate new planning action only when RBAC allows (control disabled otherwise).
- Bulk actions: multi-select in data table for bulk reassignment or schedule shift when RBAC permits; Shift+click extends ranges, Ctrl/Cmd+click toggles; conflicts or locks in the selection require an explicit confirmation step before mutation intents are sent.
- Drag and drop: mission cards from the board and mission/assignment bars in the timeline follow the Phase 1 DnD intent contract (no direct persistence). Drops into locked or forbidden slots are blocked; keyboard equivalents use focused handles with Ctrl/Cmd+Arrow and Enter to confirm.
- Keyboard accessibility baseline: tab order follows header -> timeline -> list; arrow keys navigate timeline focus; Enter activates selection.

## 7. RBAC and ownership
- View: users with project view permission (per docs/specs/08_rbac_model.md) scoped by organization_id and project_id.
- Edit: only planners or project owners can initiate planning actions; controls disabled with tooltip when lacking permissions.
- Redaction rules: collaborator names redacted if viewer lacks collaborator_view permission; avatar stack shows initials-only when redacted.

## 8. Audit and traceability
- User action events: page load, filter changes, timeframe shifts, selection changes, conflict badge expand events; include correlation_id.
- Mutation events: bulk operations or schedule changes emit audit records with mission_id/assignment_id lists and previous vs proposed timeframe when available.
- Correlation id propagation: pass correlation_id from API responses into subsequent mutation requests; include in navigation deep links when provided.

## 9. Forbidden patterns
- No hidden default filters; all applied filters must appear in the filter bar.
- No local conflict detection; rely on conflict endpoint and badges.
- No silent retries on failed datasets; retries must be explicit.
- No mixing data from multiple projects; project_id required on every query.
