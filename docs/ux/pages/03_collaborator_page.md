# Collaborator Page Contract (Phase 1 Step 16)

## Purpose
Provide a collaborator-centric view that surfaces assignments, availability, and conflicts to support staffing decisions.

## Layout and Zones
- Header: collaborator identity with avatar stack (initials-only when redacted) and filter bar for timeframe, role, and mission status.
- Primary surface: timeline bar showing assignments and availability blocks; conflict badges overlay overlapping or over-capacity spans.
- Detail panel: data table listing assignments with mission, role, timeframe, and status columns; conflict badges inline for impacted rows.

## Components Used
- Avatar stack for collaborator identity and delegates.
- Filter bar for timeframe and role/status filters.
- Timeline bar for assignment and availability visualization.
- Data table for assignment list and selection.
- Conflict badge for double-bookings or rule violations.

## Data Bindings (API Contract Names)
- GET /api/v1/collaborators/{collaborator_id}
- GET /api/v1/collaborators/{collaborator_id}/assignments?timeframe_start&timeframe_end&status&role&cursor&page_size
- GET /api/v1/collaborators/{collaborator_id}/availability?timeframe_start&timeframe_end
- GET /api/v1/collaborators/{collaborator_id}/conflicts?timeframe_start&timeframe_end
- All identifiers are opaque; organization_id context required; timestamps use UTC ISO 8601; pagination follows Step 04.

## User Actions
- Filter assignments by timeframe, mission status, or role; filters are reflected in URL query params.
- Select assignments via timeline or data table for inspection; selection syncs across regions.
- Trigger retry per dataset and request conflict details from conflict badges.
- Intent-only actions: propose reassignment or schedule adjustment when RBAC allows; disabled otherwise with tooltip reason.

## Empty, Loading, Error States
- Loading: timeline and data table show loading states; actions disabled until assignments load.
- Empty: display empty-state copy when no assignments or availability exist in range; suggest adjusting filters.
- Partial data: show loaded datasets with inline warning if availability or conflicts fail; hide conflict overlays tied to missing data until retry succeeds.
- Error: surface API error messages; manual retry only; no fallback data.
- Permission denied: show denial banner while keeping navigation shell and filter bar visible.

## Accessibility Rules
- Focus order: header (filters and avatar) -> timeline -> data table.
- Conflict badges expose textual summaries of conflict type, severity, and impacted assignment_ids for screen readers.
- All time displays are UTC with clear labels; deep links include collaborator_id, timeframe, and filter tokens to restore state.
