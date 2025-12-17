# Avatar Stack Component Contract

## Purpose
Display grouped collaborator presence and availability cues for missions or assignments without performing access control or scheduling logic.

## Scope
- Compact avatar clusters used in boards, timelines, and mission summaries.
- Optional badges for availability, role, or primary contact markers supplied by parents.

## Assumptions
- Collaborator identities, roles, and availability indicators are provided by parent views.
- Images or initials are resolved upstream; this contract only states display and intent behavior.
- Visual tokens and spacing follow docs/specs/14_visual_language.md.

## Exclusions
- No avatar upload, cropping, or image fetching logic.
- No presence polling or status computation.

## Responsibilities
- Render collaborator avatars with clear ownership context when relevant to the view.
- Convey availability or conflict cues supplied by parents.
- Expose intents for viewing collaborator details or assignment summaries.

## Inputs (Conceptual Props)
- collaborators: ordered list of items with id, display label, visual token (initials or resolved image), role tag, availability indicator, and optional primary_contact flag.
- overflow: maximum visible avatars and overflow count behavior.
- state: loading | empty | error | forbidden | disabled | read-only | locked with error details and correlation_id when provided.

## Outputs (Events as Intents Only)
- collaborator_inspect_requested(collaborator_id)
- overflow_expand_requested()
- retry_requested()

## Stacking, Overflow, and Identity Rules
- Stacking order follows collaborator priority provided by parents; primary_contact pins to the front and retains a role badge even in overflow.
- Overflow indicator displays "+N" with a tooltip listing hidden collaborator labels when permitted by RBAC; keyboard focus MUST be able to reach overflow and expand details.
- Fallback visuals: when images are missing, two-letter initials use deterministic background colors derived from collaborator_id to avoid accidental role encoding; forbidden states replace initials with anonymized silhouettes.
- Role and availability badges remain visible on each avatar; privacy constraints from parents dictate whether roles are replaced with generic placeholders when collaborator_view is missing.

## States
- Loading: placeholder circles with consistent sizing; interactions disabled.
- Empty: placeholder avatar silhouette with guidance text; no auto-fetch occurs.
- Error: inline message with correlation_id if provided; retry intent available.
- Disabled: avatars visually muted; interactions suppressed with visible reason.
- Read-only: intents remain for inspection; no assignment mutation intents are emitted.
- Forbidden: hide collaborator identities; display only ownership context allowed by the parent.
- Locked: show lock badge when assignments are locked; interactions limited to inspection intents if permitted.

## Accessibility Rules
- Each avatar MUST have an accessible name including collaborator label and availability or conflict cues when provided.
- Focus order MUST respect visual order; keyboard activation MUST trigger inspection intents.
- Overflow indicators MUST be reachable via keyboard and announce the number of hidden collaborators.

## Integration Notes
- Collaborator attributes (roles, availability, conflicts) MUST originate from parent views that enforce docs/specs/08_rbac_model.md; the component MUST NOT infer or recalc permissions.
- correlation_id or audit cues associated with assignment issues MUST be shown when provided and follow docs/specs/11_api_error_model.md messaging.
- Ownership context MUST be displayed when available; masking rules for forbidden states are determined by the parent view.
- Image resolution, CDN choices, and caching strategies are entirely upstream; this contract only renders supplied tokens.

## Allowed Usage Contexts
- Mission cards on the planning board, timeline row headers, mission detail side panels, and assignment summary sections.

## Forbidden Usage Contexts
- Authentication, billing, or organization-switching interfaces.
- Any context requiring real-time presence computation.

## Explicit MUST/MUST NOT
- MUST show availability or conflict indicators exactly as provided; MUST NOT infer or transform statuses.
- MUST NOT fetch collaborator data or alter assignments.
- MUST NOT hide primary_contact markers supplied by the parent view.
