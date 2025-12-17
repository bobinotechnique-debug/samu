# Planning Page Contract (Phase 1 Step 16)

## Purpose
Provide a project-scoped planning surface that aligns missions, assignments, availability, and conflicts across time using only approved Phase 15 components.

## Layout and Zones
- Header: filter bar for timeframe, status, collaborator, and conflict toggles; avatar stack showing planning owners for quick context.
- Primary surface: timeline bar rendering missions and assignments within the selected timeframe; conflict badge overlays any band with detected conflicts.
- Side panel: data table listing missions and assignments in the current view; conflict badges display inline on impacted rows.

## Components Used
- Filter bar (Step 15) for all visible filters and search tokens.
- Timeline bar for mission and assignment bands.
- Data table for tabular mission/assignment lists and selection.
- Avatar stack for planners or owners.
- Conflict badge for any detected conflicts.

## Data Bindings (API Contract Names)
- GET /api/v1/projects/{project_id}/missions?timeframe_start&timeframe_end&status&owner&cursor&page_size
- GET /api/v1/projects/{project_id}/assignments?timeframe_start&timeframe_end&status&owner&cursor&page_size
- GET /api/v1/projects/{project_id}/conflicts?timeframe_start&timeframe_end
- Filters and pagination mirror Step 04 conventions; mission_id and assignment_id remain opaque; organization_id and project_id are required on every request.

## User Actions
- Adjust filters and timeframe via the filter bar; selections are encoded in the URL query per Step 04.
- Select a mission or assignment from the timeline bar or data table to sync selection across regions and expose inspection intents.
- Trigger manual refresh/retry per dataset; no silent retries.
- Request conflict drill-in by activating the conflict badge overlay or row-level indicator.

## Empty, Loading, Error States
- Loading: timeline bar shows loading bands; data table shows skeleton rows; controls disabled until both mission and assignment queries resolve.
- Empty: render empty-state guidance within timeline and data table encouraging filter or timeframe adjustments.
- Partial data: if one dataset fails, show loaded results with inline warning and disable conflict overlays tied to missing data.
- Error: map API errors to user-visible messages; retries are manual per dataset.
- Permission denied: display explicit denial messaging while keeping navigation shell and filter bar visible.

## Accessibility Rules
- Logical focus order: header filter bar -> timeline bar -> data table; keyboard navigation mirrors arrow/enter patterns from component contracts.
- Conflict badge activations expose readable summaries of conflict type, severity, and affected identifiers.
- All time values display in UTC with explicit labels; no implicit conversion.
- Deep links include selection and filter tokens so states are reproducible.
