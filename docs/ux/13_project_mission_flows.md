# Project Mission Flow Specification

## Purpose
Define the end-to-end UX flows for creating, reviewing, and progressing missions within a project while honoring Phase 1 constraints.

## Scope
- Mission lifecycle flows: creation, review, locking, publishing, and assignment checkpoints.
- User intents for navigation between mission views (timeline, board, detail) without prescribing components.
- Consistency with visual tokens in docs/specs/14_visual_language.md and API patterns from Step 04.

## Assumptions
- Phase 1 is documentation-only; flows inform later implementation without introducing new endpoints.
- RBAC and ownership rules from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md govern all transitions.
- API requests follow docs/specs/10_api_conventions.md and docs/specs/11_api_error_model.md for filters, sorting, pagination, and errors.

## Exclusions
- No detailed form schemas, validation regexes, or storage formats.
- No automation or background jobs beyond what Step 04 APIs already permit.

## User Goals
- Create missions within a project with clear ownership and scheduling context.
- Move missions through review, lock, and publish steps with audit traceability.
- Coordinate assignments and approvals without leaving project context.

## Data Displayed
- Mission metadata during flows: title, objectives, status, start/end dates, organization_id, project_id, mission_id.
- Assignment summaries: collaborators, roles, availability signals, and pending approvals when provided by APIs.
- Audit and correlation references to confirm traceability for transitions.

## Actions (Intents)
- Start mission creation: intent to open a guided flow that captures ownership and schedule; payload shape is defined by existing API contracts.
- Save draft: intent to persist mission drafts via POST following docs/specs/10_api_conventions.md without inventing fields.
- Submit for review: intent to update mission status via PATCH using existing status fields and error envelopes.
- Lock mission: intent to trigger lock status when approvals are pending; edit controls become read-only.
- Publish mission: intent to move mission to active/planned status using authorized endpoints.
- Manage assignments: intent to view, add, or reassign collaborators respecting RBAC; no new assignment schemas are defined here.
- View timeline/board: intent to navigate to timeline or board views for the current mission without duplicating data fetch rules.

## States
- Loading: forms and checklists display skeletons; submission buttons are disabled until data loads.
- Empty: when no missions exist for a project, show guidance to create a mission or adjust filters; avoid auto-creation.
- Error: show inline validation errors and API error envelopes with retry guidance; correlation_id must be visible when provided.
- Forbidden: block actions and mask mission metadata when roles lack permissions per docs/specs/08_rbac_model.md.
- Locked: display lock badges and read-only summaries; only unlock-capable roles may see unlock intents.

## Accessibility
- Keyboard access MUST support all critical intents (save, submit, navigate tabs); focus order MUST follow form and flow order.
- Labels and helper text MUST remain visible in read-only or locked states.
- Escape MUST close modal steps; tabbing MUST not trap users in any stepper or modal.

## API Linkage
- Creation, update, and status transitions MUST use the HTTP methods and patterns defined in docs/specs/10_api_conventions.md.
- Errors MUST follow docs/specs/11_api_error_model.md; validation feedback MUST avoid redefining error structures.
- Pagination and filtering for mission lists MUST reuse the same parameters documented in docs/specs/10_api_conventions.md.

## Ownership and Audit Notes
- Every flow step MUST display organization_id and project_id; mission_id MUST appear after creation.
- Audit visibility MUST align with docs/specs/09_audit_and_traceability.md; flows SHOULD surface correlation identifiers when provided.
