# Timeline Bar Component Contract

## Purpose
Visualize mission duration blocks, milestones, and availability windows along a time axis for project planning contexts.

## Scope
- Timeline rows and bars used within planning timelines and mission flow summaries.
- Intent-level interactions for range navigation, item focus, and detail inspection.

## Assumptions
- Time ranges and mission metadata are provided by parent views; the component does not calculate schedules.
- Time zones and ISO formatting are handled upstream per docs/specs/13_identifiers_and_time.md.
- Visual tokens follow docs/specs/14_visual_language.md.

## Exclusions
- No drag-and-drop rescheduling, collision detection, or dependency calculations.
- No live updates or animation rules.

## Responsibilities
- Render bars representing mission start/end, milestones, and lock or forbidden badges.
- Convey ownership context (organization_id, project_id) and mission identifiers when provided.
- Expose intents for navigation, inspection, and range adjustments without altering data.

## Inputs (Conceptual Props)
- timeline_range: start and end boundaries prepared by the parent in UTC.
- items: list of missions or milestones with id, label, start, end, status, lock/forbidden flags, and ownership context.
- focus: currently highlighted item id (optional).
- state: loading | empty | error | forbidden | disabled | read-only | locked with error details and correlation_id when provided.

## Outputs (Events as Intents Only)
- range_change_requested(new_start, new_end)
- item_focus_requested(item_id)
- item_inspect_requested(item_id)
- item_scroll_requested(direction or jump_target)
- retry_requested()

## States
- Loading: skeleton bars aligned to expected positions; navigation controls disabled.
- Empty: axis and labels remain visible with guidance; no automatic refresh is triggered.
- Error: inline banner referencing docs/specs/11_api_error_model.md with correlation_id; retry intent available.
- Disabled: all interactions suppressed with reason visible.
- Read-only: bars are focusable; no mutation intents emitted.
- Forbidden: mask item details, showing only organization_id and project_id headers when applicable.
- Locked: display lock badges on affected items; range change intents still allowed if read-only-safe.

## Accessibility Rules
- Keyboard navigation MUST allow moving between items and along the timeline using arrow keys or tab order matching visual order.
- Each bar MUST provide an accessible name including label, date range, status, and lock/forbidden state.
- Focus indicators MUST follow docs/specs/14_visual_language.md; Escape MUST close overlays triggered by inspection intents.

## Allowed Usage Contexts
- Planning timeline view bars, mission flow summaries, and board-to-timeline navigation previews.

## Forbidden Usage Contexts
- Financial reporting timelines or any non-project-scoped visualization.
- Direct scheduling editors that require mutation logic.

## Explicit MUST/MUST NOT
- MUST accept precomputed UTC ranges; MUST NOT adjust time zones internally.
- MUST surface lock and forbidden states visually and via accessible labels.
- MUST NOT perform dependency calculations or persist range changes.
- MUST NOT fetch mission data or invoke API calls.
