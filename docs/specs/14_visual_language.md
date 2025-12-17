# Visual Language and Interaction Tokens

## Purpose
Lock semantic visual language rules that keep UX views consistent across planning workflows before implementation begins.

## Scope
- Semantic tokens for layout, spacing, typography, color roles, surfaces, and status feedback.
- Interaction and affordance conventions that guide view specifications in docs/ux/.
- State treatments (loading, empty, error, forbidden, locked, success) for read and edit contexts.

## Assumptions
- Phase 1 is documentation-only; tokens are conceptual and not yet mapped to design systems or code.
- API behavior, error envelopes, and pagination follow docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md.
- Domain boundaries from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md remain authoritative.

## Exclusions
- No hex values, font files, CSS variables, or component implementations.
- No override of API contracts defined in Step 04; only visual usage guidance is provided.
- No accessibility audit tooling or keyboard implementation details.

## Semantic Token Rules
- Surfaces: use layered semantic surfaces (base, raised, overlay). Base surfaces MUST handle primary reading areas; overlays MUST reserve higher contrast for dialogs and critical system banners.
- Color roles: success, warning, danger, info, and neutral roles MUST remain distinct; danger MUST be reserved for destructive or irreversible intents.
- Text: primary text MUST be used for core content; secondary text for supportive metadata; disabled text for non-actionable states; link text MUST be visually distinct and keyboard focusable.
- Spacing: small, medium, and large spacing tokens MUST be reused across layouts; padding and margin MUST NOT be hard-coded per view.
- Borders and dividers: subtle dividers MAY segment dense lists; prominent borders MUST be reserved for alerts, locked banners, and forbidden notices.
- Elevation: shadows or elevation cues MUST only indicate interactivity or layering, not decoration.

## Layout and Density
- Grid: planning surfaces SHOULD align content to a predictable grid; cards or rows MUST align with column headers for scanability.
- Density: timeline and board views MUST support high-density modes without hiding critical labels; truncation MUST provide tooltips or detail affordances.
- Responsiveness: layouts MUST degrade gracefully to narrow viewports by stacking filters above content and preserving sticky headers for context.

## Typography and Iconography
- Hierarchy: headings MUST follow a consistent descending hierarchy; do not skip levels within a view.
- Labels: field and column labels MUST use sentence case and MUST remain visible in read-only and locked states.
- Icons: status icons MUST map to semantic color roles; decorative icons MUST NOT appear without accessible labels.

## Interaction and Focus Rules
- Focus: every actionable element MUST show a visible focus ring; focus order MUST follow reading order.
- Keyboard: primary actions MUST be reachable via keyboard; escape MUST dismiss overlays; tabbing MUST not trap users in components unless modal.
- Hover and active states MUST be distinct from default and disabled states; disabled elements MUST NOT trigger actions.
- Notifications: toast or inline confirmations MUST use semantic roles and MUST expire or provide manual dismissal without blocking navigation.

## State Treatments
- Loading: skeletons or progress indicators MUST reserve space to prevent layout shift; repeat user actions MUST be prevented while loading.
- Empty: empty states MUST describe the expected data and the next available intent (e.g., filter adjustment or create request) without auto-navigation.
- Error: inline errors MUST reference the API error envelope from docs/specs/11_api_error_model.md and provide retry where safe.
- Forbidden: forbidden states MUST cite missing permissions aligned to docs/specs/08_rbac_model.md and MUST avoid exposing sensitive metadata.
- Locked: locked states MUST convey the locking condition (e.g., mission frozen for review) and provide a read-only summary without edit controls.
- Success: confirmations MUST be concise, reversible where possible, and MUST log correlation identifiers when provided by APIs.

## Data and Ownership Cues
- Ownership: organization and project identifiers MUST be visible in headers or context bars when viewing missions or assignments.
- Traceability: correlation or request identifiers surfaced by APIs MAY appear in audit drawers; visual cues MUST NOT leak cross-organization data.
- Inline metadata such as updated_at and owner names MUST use neutral text and consistent placement near titles or summary rows.

## Usage Constraints
- Visual language tokens MUST be reused across all UX view specs; bespoke styling per view is forbidden.
- Status colors and icons MUST align with the semantic token rules above; mixing warning and danger roles is forbidden.
- Filters, sorters, and pagination controls MUST follow placement and labeling patterns set here and MUST respect docs/specs/10_api_conventions.md.
