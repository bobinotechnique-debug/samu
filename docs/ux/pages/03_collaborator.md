# Collaborator Page Contract (Phase 1 Step 07)

## 1. Overview
- Name: Collaborator
- Goal: Show a collaborator's assignments, availability, and conflicts across projects within the organization.
- Primary actors: Collaborators, project planners, staffing coordinators.

## 2. URL and deep links
- Canonical route: /collaborator
- Query params: organization_id (required), collaborator_id (required), project_id (optional filter), timeframe_start/timeframe_end (optional), status filter, selection (assignment_id), page cursor.
- Anchor rules: #header, #timeline, #assignments, #side-panel anchors are stable for deep linking.

## 3. Regions and required components
- Header: avatar stack for collaborator and backup contacts; filter bar for timeframe/project/status filters; conflict badge when collaborator has active conflicts.
- Primary surface: timeline bar showing assignments for the collaborator across projects within timeframe; conflict badge overlays over-allocations.
- Side panel: data table of assignments with project and mission columns; rows may show avatar stack for co-assignees; filter bar controls above the table manage visible filters.

## 4. Data model bindings
- Required API endpoints (convention reference):
  - GET /api/v1/collaborators/{collaborator_id}
  - GET /api/v1/collaborators/{collaborator_id}/assignments?project_id&status&timeframe_start&timeframe_end&cursor&page_size
  - GET /api/v1/collaborators/{collaborator_id}/conflicts?timeframe_start&timeframe_end
- Filters/sort/pagination mapping: filter bar sets project_id, status, timeframe; data table uses cursor pagination and sortable columns per docs/specs/10_api_conventions.md.
- ID and time rules: collaborator_id and assignment_id opaque; organization_id required on all requests; times in UTC ISO 8601 with no implicit conversion.

## 5. UI states
- Loading: avatar stack placeholders; timeline and data table skeletons; actions disabled.
- Empty: no assignments show empty state in timeline and table with prompt to adjust filters/timeframe.
- Partial data: collaborator profile loads while assignments or conflicts fail; render available data with inline warning banner and omit conflict badges until conflict query succeeds.
- Error: map API errors to messages; retries manual per dataset.
- Permission denied: explicit denial message; hide assignment details; maintain header to allow navigation away.

## 6. Interactions
- Selection model: selecting an assignment in timeline highlights row in data table and syncs selection query param.
- Primary actions: open project or mission via assignment row; request reassignment when RBAC allows (control disabled otherwise).
- Bulk actions: multi-select assignments for bulk status update or removal when permitted by RBAC.
- Keyboard accessibility baseline: tab order header -> filter bar -> data table -> timeline; arrow navigation in timeline; Enter activates row actions; space toggles selection.

## 7. RBAC and ownership
- View: users with collaborator_view scoped by organization_id; project filter restricted to projects the viewer can access.
- Edit: staffing coordinators or project planners with collaborator_edit may change assignments; controls disabled and annotated when lacking permission.
- Redaction rules: hide project names when viewer lacks project_view for that project; show anonymized labels while preserving row count.

## 8. Audit and traceability
- User action events: page load, filter updates, selection changes, conflict badge opens.
- Mutation events: reassignment requests and bulk updates record collaborator_id, assignment_ids, prior vs requested state, and timestamps.
- Correlation id propagation: use correlation_id from collaborator fetch and pass into mutation requests and emitted audit entries.

## 9. Forbidden patterns
- No cross-organization data mixing; collaborator scope is organization-bounded.
- No hidden project filters; project filter defaults must appear in the filter bar.
- No silent retries for failed datasets.
- No client-side conflict inference; use conflict endpoint only.
