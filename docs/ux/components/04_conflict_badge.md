# Conflict Badge Component Contract

## Purpose
Surface conflicts or alerts (e.g., overlapping assignments, permission restrictions) as concise badges without embedding resolution logic.

## Scope
- Inline badges attached to mission cards, timeline bars, or detail panels.
- Visual and textual cues for conflict type and severity provided by parent contexts.

## Assumptions
- Conflict detection and severity scoring are performed upstream; the component only renders supplied data.
- Visual tokens follow docs/specs/14_visual_language.md for color and icon semantics.

## Exclusions
- No conflict detection algorithms or resolution workflows.
- No badge stacking logic beyond what parents supply.

## Responsibilities
- Display conflict label, severity, and optional correlation_id link supplied by parents.
- Indicate lock or forbidden states when conflicts prevent actions.
- Expose intent to view conflict details.

## Inputs (Conceptual Props)
- conflict: id, label, severity level, optional correlation_id, ownership context, and lock/forbidden flags.
- state: loading | empty | error | forbidden | disabled | read-only | locked with error details when provided.

## Outputs (Events as Intents Only)
- conflict_inspect_requested(conflict_id)
- retry_requested()

## Conflict Types and Severity
- Supported types: assignment_overlap, over_capacity, missing_clearance (RBAC restriction), schedule_lock_violation, data_stale, and dependency_blocked. Parents MAY provide additional display labels but MUST map them to one of these types for consistent iconography.
- Severity levels: info, warning, critical. Critical MUST render the lock overlay when lock/forbidden flags are present; warning shows striped highlight; info uses neutral outline only.
- Badge highlight rules: conflict badges inherit severity color tokens and MUST never rely solely on color; include iconography and text labels.

## Conflict Panel Behavior
- Inspection intent opens a parent-controlled panel that lists conflict type, severity, affected mission/assignment ids, and correlation_id when available; badge only emits the intent.
- Resolution hints are read-only: badge tooltip and inspection panel may show "contact planner" or "review mission lock" notes supplied by parents; no remediation controls or auto-resolution are permitted.
- When multiple conflicts are aggregated on a single badge, parent MUST provide a count; badge cycles through labels with left/right keyboard controls and announces the active conflict to assistive tech.

## States
- Loading: placeholder badge with neutral styling; interactions disabled.
- Empty: no badge rendered; optional guidance text from parent.
- Error: inline message in badge area referencing docs/specs/11_api_error_model.md with correlation_id when available.
- Disabled: badge muted; interactions suppressed with reason visible.
- Read-only: badge remains readable; inspection intent still available.
- Forbidden: badge text limited to generic permission notice; underlying data is masked.
- Locked: lock indicator overlays the badge; mutation intents are suppressed.

## Accessibility Rules
- Badge MUST include accessible text describing the conflict, severity, and state (locked/forbidden) when present.
- Keyboard activation MUST trigger inspection intent; focus indicator MUST follow docs/specs/14_visual_language.md.

## Integration Notes
- Conflict detection sources MUST conform to docs/specs/10_api_conventions.md payloads; the badge displays supplied severity without remapping.
- correlation_id and audit cues MUST be displayed when provided to align with docs/specs/11_api_error_model.md and docs/specs/09_audit_and_traceability.md.
- RBAC and ownership masking rules remain parent responsibilities; the badge only renders permissible labels and states provided upstream.
- The badge MUST NOT trigger remediation or mutation flows; inspection intents route to parent-controlled experiences.

## Allowed Usage Contexts
- Mission board cards, timeline bars, data table cells, and mission detail headers.

## Forbidden Usage Contexts
- Non-project alerts (billing, authentication) or contexts lacking project scope.
- Any view that requires resolving conflicts directly within the badge.

## Explicit MUST/MUST NOT
- MUST display severity exactly as provided; MUST NOT reclassify or reorder conflicts.
- MUST NOT fetch conflict data or initiate remediation flows.
- MUST NOT conceal correlation identifiers provided by parents.
