# UI Component Contracts

## Purpose
Lock a minimal, reusable design system through authoritative UI component contracts that align with Phase 1 constraints and the immutable API conventions from Step 04 and UX visual language from Step 05.

## Scope
- Documentation-only rules for cross-view components used in planning surfaces (timeline, board, project/mission flows).
- Global component behaviors, state model, accessibility baseline, and forbidden patterns.
- References for UX component specifications under docs/ux/components/.

## Assumptions
- Phase 1 prohibits implementation; contracts describe behavior and structure without code or library choices.
- All API interactions follow docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md without deviation.
- Visual semantics are governed by docs/specs/14_visual_language.md and cannot be altered here.

## Exclusions
- No component theming systems, styling tokens, or CSS frameworks.
- No business logic, data fetching, or storage rules inside components.
- No new API endpoints or payload shapes.

## Global Component Rules
- Components MUST remain stateless UI contracts; data loading, mutation, and orchestration belong to their parent views.
- Inputs MUST be explicit, typed conceptual props (no implicit global state). Outputs MUST be emitted as intent events, not coupled to API calls.
- Organization_id and project_id context MUST be displayed whenever domain data is shown; cross-organization data mixing is forbidden.
- RBAC, audit, and ownership cues MUST follow docs/specs/07_data_ownership.md, docs/specs/08_rbac_model.md, and docs/specs/09_audit_and_traceability.md.
- Visual states MUST align with docs/specs/14_visual_language.md; components MUST NOT redefine colors, spacing, or focus rules.
- Pagination, sorting, and filtering controls MUST follow docs/specs/10_api_conventions.md and MUST NOT invent new parameters.

## State Model
- Loading: visual skeletons preserve layout without implying final data; interactive controls are disabled until data arrives.
- Empty: explicit guidance text; no auto-navigation or implicit creation occurs.
- Error: inline message uses the error envelope from docs/specs/11_api_error_model.md with correlation_id when provided; retry is an intent only.
- Disabled: component ignores interaction and communicates why; visual treatment follows docs/specs/14_visual_language.md.
- Read-only: content is focusable and navigable but non-editable; labels remain visible.
- Forbidden: mask protected data, showing only organization_id and project_id context where applicable.
- Locked: show lock badges and suppress mutation intents while preserving inspection intents.

## Accessibility Baseline
- Keyboard access MUST cover all intents; focus order follows reading order with visible indicators per docs/specs/14_visual_language.md.
- Screen reader labels MUST describe primary content, ownership context, and state (loading, locked, forbidden, error).
- Escape MUST close overlays; tabbing MUST exit overlays without trapping focus.
- Text alternatives MUST exist for icons and badges conveying status or conflict.

## Forbidden Patterns
- Components MUST NOT fetch data, manage authentication, or enforce business rules.
- Components MUST NOT manipulate time zones, identifiers, or RBAC decisions; they only display provided results and intents.
- Components MUST NOT mutate server state directly; outputs are intents for parent handlers.
- Components MUST NOT introduce new query parameters, headers, or storage mechanisms.
- Components MUST NOT hide correlation identifiers or audit cues when provided by parent contexts.

## Cross-References
- Component contracts are detailed per component under docs/ux/components/.
- View specifications (docs/ux/11_planning_timeline.md, docs/ux/12_planning_board.md, docs/ux/13_project_mission_flows.md) MUST reference these contracts when embedding components.
