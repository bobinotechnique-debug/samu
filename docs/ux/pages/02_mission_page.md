# Mission Page Contract (Phase 1 Step 16)

## Purpose
Show a mission-centric view that links schedule, assignments, conflicts, and collaborators while honoring Phase 15 component rules.

## Layout and Zones
- Header: mission summary (name, status, timeframe) with avatar stack for mission leads; filter bar for assignment status, role, and timeframe refinements.
- Primary surface: timeline bar for mission schedule bands and assignment spans; conflict badges overlay affected spans.
- Detail panel: data table listing assignments for the mission with role, collaborator, and timeframe columns; conflict badges inline where overlaps occur.

## Components Used
- Filter bar for mission-level filters and search tokens.
- Timeline bar for mission and assignment visualization.
- Data table for assignment list and selection.
- Avatar stack for mission leads and key collaborators.
- Conflict badge for overlaps or rule violations.

## Data Bindings (API Contract Names)
- GET /api/v1/projects/{project_id}/missions/{mission_id}
- GET /api/v1/projects/{project_id}/missions/{mission_id}/assignments?status&role&cursor&page_size
- GET /api/v1/projects/{project_id}/missions/{mission_id}/conflicts?timeframe_start&timeframe_end
- All identifiers are opaque; timestamps use UTC ISO 8601; pagination and filtering follow Step 04 conventions.

## User Actions
- Adjust assignment filters via filter bar; reflect in query params and data table state.
- Select assignments in the timeline or data table to inspect; selection stays in sync across regions.
- Trigger retry on failed datasets; request conflict details through conflict badge activation.
- Initiate mission-level actions (edit metadata, propose schedule changes) as intents only; enforce RBAC before enabling controls.

## Empty, Loading, Error States
- Loading: show timeline loading bands and data table skeletons; disable mutation intents until data resolves.
- Empty: render empty copy for missions without assignments; suggest adding collaborators when permissions allow.
- Partial data: preserve whichever dataset loads; show inline warning when conflicts endpoint fails and suppress overlay until retry succeeds.
- Error: surface API error codes with retry; no silent retries or fallback data.
- Permission denied: display denial banner and keep navigation shell visible.

## Accessibility Rules
- Focus order: header (filter bar) -> timeline bar -> data table; keyboard navigation mirrors component contracts.
- Conflict badge details expose text summaries and affected assignment_ids for screen readers.
- All time displays remain in UTC with explicit labels; deep links include mission_id and filter tokens for reproducibility.
