# Project Page Contract (Phase 1 Step 16)

## Purpose
Deliver a project-level overview that aggregates missions, assignments, team visibility, and conflicts without duplicating business logic.

## Layout and Zones
- Header: project summary with key dates and avatar stack for project owners; filter bar for mission status, phase, and timeframe.
- Primary surface: timeline bar showing mission phases and key milestones; conflict badges overlay bands with scheduling conflicts.
- Detail panel: data table listing missions with status, timeframe, lead, and risk/conflict indicators; row-level conflict badges for impacted missions.

## Components Used
- Filter bar for visible filters and search tokens.
- Timeline bar for mission/milestone visualization.
- Data table for mission list and selection.
- Avatar stack for owners and core team.
- Conflict badge for mission-level conflicts or schedule risks.

## Data Bindings (API Contract Names)
- GET /api/v1/projects/{project_id}
- GET /api/v1/projects/{project_id}/missions?status&phase&timeframe_start&timeframe_end&cursor&page_size
- GET /api/v1/projects/{project_id}/conflicts?timeframe_start&timeframe_end
- Identifiers remain opaque; timestamps use UTC ISO 8601; filters, pagination, and sorting follow Step 04 conventions; organization_id and project_id required.

## User Actions
- Filter missions by status, phase, or timeframe; filter tokens persist in URL query params.
- Select missions from the timeline or data table to inspect details; selection remains synchronized across regions.
- Activate conflict badges to review conflict type, scope, and suggested remediation; manual retry available on failures.
- Intent-only actions: propose new mission, adjust dates, or reassign leads subject to RBAC; disabled controls expose tooltip rationale when forbidden.

## Empty, Loading, Error States
- Loading: timeline shows loading bands; data table shows skeleton rows; mutation intents disabled until data resolves.
- Empty: render empty-state guidance when no missions match filters; suggest adjusting filters or timeframe.
- Partial data: preserve loaded datasets even if conflicts endpoint fails; show inline warning and suppress conflict overlays tied to missing data until retry succeeds.
- Error: display API error messages with retry controls; no silent retries.
- Permission denied: show denial banner while keeping navigation shell and filter bar visible.

## Accessibility Rules
- Focus order: header (filter bar and avatar stack) -> timeline bar -> data table; keyboard navigation mirrors component contracts.
- Conflict badges expose textual summaries with mission_id references for screen readers.
- All dates/times shown in UTC with clear labels; deep links include project_id and filter tokens to restore state.
