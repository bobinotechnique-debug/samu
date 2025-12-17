# Planning Timeline View Specification

## Purpose
Define the authoritative timeline UX for viewing and coordinating mission schedules within a project before implementation begins.

## Scope
- Project-scoped mission timelines, milestones, and assignment windows.
- Read and adjust (intent-level) interactions for schedule navigation, filtering, and detail review.
- Visual and interaction alignment with docs/specs/14_visual_language.md.

## Assumptions
- Phase 1 documents behavior only; no frontend or backend code is modified.
- Data ownership and RBAC constraints from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md apply to all states.
- API requests use the filtering, sorting, pagination, and error envelopes defined in docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md.

## Exclusions
- No Gantt library selection, component implementation, or performance tuning decisions.
- No deviation from Step 04 API patterns; endpoints are referenced but not redesigned.

## User Goals
- Understand mission timelines, dependencies, and assignment windows for a specific project.
- Locate missions by status, owner, collaborator, or date range using filters.
- Inspect mission details, including objectives and audit traces, without leaving the timeline.

## Data Displayed
- Timeline grid with missions plotted by start and end dates, including phase markers or milestones.
- Mission metadata: title, status, owner, organization and project identifiers, last updated timestamp.
- Assignment windows and collaborator count per mission, showing availability cues when provided.
- Correlation or request identifiers when supplied by APIs for traceability.

## Actions (Intents)
- Adjust time range: intent to scroll or jump to date ranges without altering data.
- Filter missions: intent to apply filters (status, owner, collaborator, date range) using API-compliant query parameters.
- Sort missions: intent to reorder by start date, end date, status, or owner per API sort fields.
- Inspect mission: intent to open a side panel or modal with mission summary and audit trail links.
- Navigate to mission board: intent to open the related planning board for the selected mission.
- Export snapshot: intent to request an export using available API endpoints without redefining payloads.

## Drag and Drop Interaction Contract (Intent Only)
- Drag sources: mission bars and assignment segments originating from the timeline or handed off from the planning board; collaborator avatars are not draggable in Phase 1.
- Drop targets: timeline slots within the current project and timeframe; drops outside the visible range require a scroll or jump intent before acceptance. Table rows are NOT valid drop targets.
- Allowed vs forbidden: drops onto locked or forbidden missions are blocked; conflicted missions may accept drops but badge the ghost with the highest severity present. RBAC validation occurs before enabling drag handles.
- Ghost preview and snap: ghost shows mission title, new proposed start/end, and conflict/lock badges; snaps to nearest day boundary unless parent provides coarser granularity. No persistence occurs until parent confirms.
- Multi-select drag: not supported; sequencing changes must be requested through bulk intents in the data table.
- Keyboard alternative: Alt+Arrow proposes shifting the focused bar by the smallest granularity; Enter confirms intent, Escape cancels; screen readers announce proposed range and whether the drop is permitted.

## States
- Loading: skeleton timeline grid preserves column and row structure; filters are disabled until API responses return.
- Empty: when filters return no missions, show guidance to reset filters or create missions via designated flows.
- Error: inline banner referencing the API error envelope with retry and a link to refresh filters.
- Forbidden: display a permission notice aligned to docs/specs/08_rbac_model.md without exposing mission metadata.
- Locked: timeline shows read-only badges and disables rescheduling intents when missions are locked for review.

## Accessibility
- Keyboard navigation MUST allow moving across timeline items and filters in reading order; focus indicators MUST follow docs/specs/14_visual_language.md.
- Screen reader labels MUST describe mission title, date range, status, and ownership context.
- Escape MUST close detail overlays; tabbing MUST exit overlays without trapping focus.

## API Linkage
- Filters and sorters MUST pass query parameters defined in docs/specs/10_api_conventions.md and MUST NOT invent new fields.
- Pagination MUST follow the collection pagination contract from docs/specs/10_api_conventions.md; infinite scroll MUST honor server cursors if provided.
- Errors MUST display messages from docs/specs/11_api_error_model.md, including correlation_id when available.

## Performance, Scale, and Refresh
- Timeline rows MAY be virtualized when more than 40 missions are visible; virtualization MUST preserve keyboard traversal order and ensure off-screen rows are not announced to assistive tech.
- Large time ranges MUST chunk data per docs/specs/10_api_conventions.md pagination; auto-extend scrolling is forbidden unless driven by server cursors.
- Stale data indicators (last_refreshed timestamp supplied by parents) SHOULD appear above the timeline controls with a manual refresh intent; silent refresh loops are not allowed.

## Exports and Print
- Export snapshot intent produces a planning run sheet limited to the currently filtered missions and timeframe; export payloads MUST carry organization_id, project_id, timeframe, filter tokens, and generation timestamp.
- Audit stamp: export metadata MUST include correlation_id when supplied by APIs and the actor who initiated export; badge or footer text MUST display this information.
- Printable views MUST preserve color-independent indicators (icons and labels for conflicts/locks) to remain legible in grayscale.

## Ownership and Audit Notes
- All views MUST display organization_id and project_id context prominently.
- Mission selections SHOULD surface audit links aligned with docs/specs/09_audit_and_traceability.md without duplicating audit payloads.

## Component Cross-links
- Timeline bars MUST follow docs/ux/components/02_timeline_bar.md for rendering mission ranges and inspection intents.
- Filter controls MUST follow docs/ux/components/05_filter_bar.md for applying timeline filters without custom parameters.
- Inline conflict indicators MUST use docs/ux/components/04_conflict_badge.md.
- Mission detail tables or listings within the timeline context MUST apply docs/ux/components/01_data_table.md.
- Collaborator presence shown alongside missions MUST follow docs/ux/components/03_avatar_stack.md.
