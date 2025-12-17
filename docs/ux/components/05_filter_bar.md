# Filter Bar Component Contract

## Purpose
Provide consistent filter controls for planning views without embedding filtering logic or API calls.

## Scope
- Horizontal or vertical filter bars used on planning timeline, board, data tables, and mission flow summaries.
- Intent-level interactions for filter application, reset, and search aligned with Step 04 API conventions.

## Assumptions
- Available filter fields and allowed values are supplied by parent views.
- Query composition and execution are handled by parents following docs/specs/10_api_conventions.md.
- Visual tokens and focus styles follow docs/specs/14_visual_language.md.

## Exclusions
- No server-side query construction or caching.
- No autosave or persistence of filter presets.

## Responsibilities
- Render filter controls (dropdowns, chips, toggles) consistent with provided field definitions.
- Display active filters and expose clear reset intents.
- Reflect loading, error, forbidden, and locked states without altering data.

## Inputs (Conceptual Props)
- fields: list of filter field definitions with id, label, type, allowed values, multi-select flag, and default selection.
- active_filters: current applied values prepared by the parent.
- search_term: optional free text provided by parent; no debouncing logic inside the component.
- state: loading | empty | error | forbidden | disabled | read-only | locked with error details and correlation_id when provided.

## Outputs (Events as Intents Only)
- filter_changed(field_id, value)
- filters_reset_requested()
- search_requested(term)
- retry_requested()
- saved_view_requested(view_id) (optional, when enabled by parent)
- save_view_requested(name, filters) (optional, when enabled by parent)

## Saved Views and URL State
- Saved view intents are optional and scoped to Phase 1 documentation: when parents enable them, the component exposes saved_view_requested(view_id) and save_view_requested(name, filters) intents while rendering owner badges provided by the parent.
- Ownership and sharing: saved views default to private ownership; parents MUST enforce RBAC before exposing shared views and indicate sharing status via labels; component MUST NOT persist or fetch views directly.
- URL/deep link mapping: every active filter, search term, and saved_view_id MUST be representable in query params supplied by the parent to allow reproducible links; reset controls clear the params and revert to parent-provided defaults.

## States
- Loading: controls show skeletons or disabled placeholders; no filter events emitted.
- Empty: when no fields are available, present guidance text; no automatic field requests occur.
- Error: inline message referencing docs/specs/11_api_error_model.md with correlation_id when available; retry intent available.
- Disabled: controls inert with reason visible.
- Read-only: controls visible and focusable; changes are suppressed and no events emitted.
- Forbidden: hide sensitive filters; show permission notice where appropriate.
- Locked: lock badge present; only inspection of active filters allowed.

## Accessibility Rules
- All controls MUST be reachable via keyboard; labels MUST remain visible in all states.
- Screen readers MUST announce field labels, selected values, and state (disabled, read-only, locked, forbidden).
- Clear reset control MUST be focusable and announce the consequence of resetting filters.

## Integration Notes
- Filter definitions MUST mirror docs/specs/10_api_conventions.md query parameters; the component MUST NOT invent or reorder filters beyond parent instructions.
- Ownership and RBAC-sensitive filter options MUST be masked by parents; the component displays only what is allowed and never infers permissions.
- Error displays MUST surface correlation_id when provided to align with docs/specs/11_api_error_model.md and audit requirements.
- Time and identifier fields MUST retain formatting from docs/specs/13_identifiers_and_time.md; the component MUST NOT localize or coerce values.

## Allowed Usage Contexts
- Planning timeline headers, board filter panels, data table toolbars, and mission flow entry points.

## Forbidden Usage Contexts
- Authentication, billing, or organization-switching flows.
- Any context requiring implicit filter persistence or background fetches.

## Explicit MUST/MUST NOT
- MUST emit filter changes as intents only; parents perform actual filtering.
- MUST NOT invent query parameters or override parent-provided defaults.
- MUST NOT cache or persist filter values beyond current render lifecycle.
