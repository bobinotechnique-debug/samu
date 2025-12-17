# Planning Board View Specification

## Purpose
Describe the canonical board UX for mission planning and assignment coordination within a project prior to implementation.

## Scope
- Column-based mission board for status or phase-driven organization.
- Intent-level interactions for filtering, sorting, assignment inspection, and limited sequencing.
- Alignment with visual tokens in docs/specs/14_visual_language.md.

## Assumptions
- Phase 1 remains documentation-only; board behavior informs later implementation without prescribing libraries.
- RBAC and ownership constraints from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md apply to all actions and states.
- API interactions must follow docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md without introducing new patterns.

## Exclusions
- Drag-and-drop implementation, animation details, or real-time synchronization mechanics.
- Schema changes or new API endpoints beyond Step 04 conventions.

## User Goals
- Scan missions by status or phase to understand current throughput and blockers.
- Apply filters to focus on specific owners, collaborators, or priority ranges.
- Review mission details and assignments without leaving the board.
- Identify locked or forbidden missions quickly and understand next steps.

## Data Displayed
- Columns representing mission states or phases, with mission cards showing title, status, owner, due or milestone dates, organization and project identifiers, and last updated timestamp.
- Assignment summary per card: collaborator count, availability cues, and primary contact when provided.
- Inline indicators for locked missions, permission restrictions, and audit correlation identifiers when available.

## Actions (Intents)
- Filter board: intent to apply status, owner, collaborator, and priority filters using API-compliant query parameters.
- Sort columns or cards: intent to reorder by priority, due date, or last updated using supported API sort options; visual reordering MUST NOT imply server-side persistence without explicit APIs.
- Inspect mission: intent to open a detail panel with mission overview, assignments, and audit links.
- Request assignment change: intent to open an assignment editor flow (without defining the editor) respecting RBAC constraints.
- Switch grouping: intent to toggle between status-based and phase-based columns if supported by existing API fields.
- Refresh data: intent to request the latest board data using pagination or cursor tokens when provided.

## Drag and Drop Interaction Contract (Intent Only)
- Drag sources: mission cards and assignment chips embedded within cards. Collaborators or equipment are NOT draggable in Phase 1; parents MUST provide alternate intents for reassignment.
- Drop targets: board columns/lanes that share the same project_id; drops across organizations are forbidden. Timeline drop handoffs emit schedule_proposal intents only when the parent wires them to the planning timeline.
- Allowed vs forbidden: drops into locked or forbidden columns are blocked with tooltip messaging; RBAC checks must be performed by the parent before enabling drag handles. Conflicted cards may be dragged but MUST show a "conflict present" ghost label.
- Ghost preview and snap: dragged cards render a ghost showing mission title, status, and conflict/lock badges; ghost snaps to lane boundaries only, never between rows, and does not reorder cards until parent confirms.
- Multi-select drag: not supported in Phase 1; bulk actions must use the data table selection contract instead.
- Keyboard alternative: focusable drag handle supports Ctrl/Cmd+Arrow to propose moving to adjacent lanes; Enter confirms intent, Escape cancels. Screen readers announce current lane, target lane, and whether the drop is permitted.

## States
- Loading: skeleton columns and cards maintain layout; filters and sorting controls are disabled until data arrives.
- Empty: present guidance for filter resets or mission creation entry points; no auto-navigation occurs.
- Error: display inline banner using the error envelope from docs/specs/11_api_error_model.md with retry and correlation_id when provided.
- Forbidden: show a clear permission message and hide mission metadata except organization and project context headers.
- Locked: render locked badges on impacted cards; drag or reorder intents MUST be disabled while locked.

## Accessibility
- Keyboard navigation MUST allow column traversal and card focus using arrow keys or tab order that follows reading order.
- Focus indicators MUST follow docs/specs/14_visual_language.md; activation via Enter/Space MUST open the same intents as pointer input.
- Screen reader labels MUST include mission title, status, ownership context, and locked or forbidden states.

## API Linkage
- Filters and sorters MUST use parameters defined in docs/specs/10_api_conventions.md; client-side sorting MUST NOT conflict with server ordering indicators.
- Pagination or cursor tokens MUST follow docs/specs/10_api_conventions.md; partial reloads MUST honor server-provided cursors.
- Errors MUST follow docs/specs/11_api_error_model.md; forbidden and locked states MUST align with RBAC responses defined in docs/specs/08_rbac_model.md.

## Performance and Scale
- Boards with more than 50 cards per lane SHOULD enable virtualization or windowing without breaking keyboard traversal order; only rendered cards may be announced to assistive tech.
- Stale data indicators (timestamp supplied by parent) SHOULD appear in the header with a manual refresh intent; auto-refresh is forbidden in Phase 1.

## Ownership and Audit Notes
- Cards MUST display organization_id and project_id context; cross-organization mixing is forbidden.
- Audit links from mission cards SHOULD reference docs/specs/09_audit_and_traceability.md requirements without duplicating audit payloads.

## Component Cross-links
- Card-level collaborator display MUST follow docs/ux/components/03_avatar_stack.md.
- Inline conflict or restriction cues MUST use docs/ux/components/04_conflict_badge.md.
- Board filter controls MUST align with docs/ux/components/05_filter_bar.md and use only API-compliant parameters.
- Tabular mission details rendered from the board MUST apply docs/ux/components/01_data_table.md.
- Timeline previews or jumps from the board MUST use docs/ux/components/02_timeline_bar.md for consistent range depiction.
