# Data Table Component Contract

## Purpose
Provide a structured tabular presentation of mission, project, or assignment data aligned to planning views without embedding business logic.

## Scope
- Read-only or read-mostly tables used in planning timeline, board details, and mission flow summaries.
- Intent-level interactions for sorting, pagination, selection, and basic filtering consistent with Step 04 API patterns.

## Assumptions
- Data is supplied by parent views; the component never fetches or mutates server state.
- Column definitions map to existing API fields; no derived fields beyond what parents supply.
- Visual styling follows docs/specs/14_visual_language.md.

## Exclusions
- No inline editing, bulk mutation logic, or custom export routines.
- No schema inference or automatic column generation.

## Responsibilities
- Render rows with clear ownership context (organization_id, project_id) when present.
- Expose intents for sorting, pagination, row selection, and row inspection without performing the actions.
- Display stateful cues for loading, empty, error, forbidden, disabled, and read-only modes.

## Inputs (Conceptual Props)
- columns: ordered definitions including header label, field key, optional alignment, and sortability flag.
- rows: array of row data objects already sanitized for display, including identifiers and ownership context.
- pagination: page number, page size, total count or cursor tokens consistent with docs/specs/10_api_conventions.md.
- sorting: active sort field and direction constrained to API-supported options.
- selection: currently selected row identifiers (if applicable) with read-only toggle.
- state: loading | empty | error | forbidden | disabled | read-only | locked (optional) with error details and correlation_id when provided.

## Outputs (Events as Intents Only)
- sort_requested(field, direction)
- page_requested(page_number or cursor)
- page_size_requested(size)
- row_selected(row_id)
- row_inspect_requested(row_id)
- retry_requested()

## Selection and Bulk Actions
- Selection modes: single-select by default; multi-select enabled only when parent passes a selectable flag. Shift-click extends a contiguous range, Ctrl/Cmd-click toggles individual rows, and keyboard users can use Space to toggle and Shift+Arrow to extend range.
- Bulk actions: component exposes a bulk_action_requested(action_id, row_ids) intent when parents register available bulk actions; actions MUST be disabled when RBAC or lock flags are present in selection metadata.
- Confirmation and conflicts: parents MUST surface confirmation copy and conflict summaries before executing bulk intents; the table only surfaces a conflict-present indicator when selection contains rows flagged as conflicted or locked.

## States
- Loading: skeleton headers and rows; interaction controls disabled.
- Empty: table chrome persists with guidance text; no automatic data fetch is triggered.
- Error: inline banner with error message and correlation_id; retry intent available.
- Disabled: all controls inert with reason visible.
- Read-only: selection intents disabled; inspection remains available.
- Forbidden: hide row content while showing ownership headers only.
- Locked: show lock indicators on affected rows; mutation intents suppressed.

## Accessibility Rules
- Table headers and cells MUST expose appropriate header associations for screen readers.
- Focus order MUST follow row and column order; keyboard shortcuts MUST cover sorting and pagination intents.
- Error and state messages MUST be announced to assistive technologies.

## Integration Notes
- Sorting, pagination, and filtering tokens MUST match docs/specs/10_api_conventions.md without adding derived fields or client-only parameters.
- Ownership context (organization_id, project_id) MUST be visible when provided and masked only by parent RBAC decisions.
- correlation_id from docs/specs/11_api_error_model.md MUST be displayed when supplied; retry intents MUST not mutate state directly.
- Time fields or identifiers shown in rows MUST honor docs/specs/13_identifiers_and_time.md formatting and cannot be reformatted locally.

## Performance and Scale
- Pagination remains authoritative; virtualization MAY be used for visible rows but MUST preserve keyboard focus order and announce only rendered rows to assistive technologies.
- Stale data cues (last_refreshed timestamp provided by parent) SHOULD appear above the table when available; refresh_requested intents are not emitted by the component.

## Allowed Usage Contexts
- Mission detail drawers, planning board cards expanding into tables, timeline side panels, and mission flow summaries.

## Forbidden Usage Contexts
- Payment, authentication, or organization-switching flows.
- Any context requiring inline editing or real-time synchronization without explicit parent orchestration.

## Explicit MUST/MUST NOT
- MUST display organization_id and project_id when present in rows.
- MUST respect parent-provided sorting and pagination tokens without modification.
- MUST NOT fetch or mutate data.
- MUST NOT introduce columns or filters beyond parent definitions.
- MUST NOT hide correlation identifiers supplied for auditing.
