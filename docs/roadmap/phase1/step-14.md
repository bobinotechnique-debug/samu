# Phase 1 - Step 14: Global Lock and Non-Regression Charter (Locked)

## Purpose

Formally lock Phase 1 as the authoritative specification baseline, prevent scope drift, and define how later phases may reference Phase 1 artifacts. Phase 1 becomes immutable after this step and any change requires a formal amendment.

## Scope

- Governance, authority, and agent orchestration (Steps 00-01).
- Core domain definitions and ownership (Steps 02-03).
- API and integration conventions (Step 04).
- UI component and page contracts (Steps 06-07).
- Operational run sheets (Step 08).
- Inventory and equipment contracts (Step 09).
- Finance and accounting contracts (Step 10).
- Cross-domain read models (Step 11).
- Locations and maps contracts (Step 12).
- Notifications and messaging contracts (Step 13).

## Immutability Rules

1. No Phase 1 file may be modified in later phases.
2. Corrections require a formal amendment that includes a new spec file, an explicit reference to the locked Phase 1 artifact, and rationale plus migration notes.
3. No silent edits, rewrites, or reinterpretations are permitted.

## Non-Regression Guardrails

- All Phase 2+ implementations MUST conform to Phase 1 contracts.
- CI and guards must fail if implementation violates ownership or RBAC rules, API conventions, UI contracts, or audit requirements.

## Allowed Evolutions

- Additive extensions in Phase 2+ that do not alter Phase 1 meaning.
- New modules that reference Phase 1 contracts.
- Read-only projections built from Phase 1 models.

## Forbidden Evolutions

- Changing identifiers, ownership, or scoping rules.
- Introducing cross-organization shortcuts.
- Embedding business logic in the frontend.
- Bypassing audit or RBAC rules.

## Enforcement

- AGENT.md must declare Phase 1 as LOCKED and replicate stop conditions.
- Any violation triggers STOP and requires human validation.
- Phase 1 amendments follow the formal correction path with explicit references and migration notes.

## Acceptance Criteria

- All Phase 1 steps are indexed and referenced.
- Roadmap marks Phase 1 as LOCKED.
- AGENT.md updated accordingly.
- No TODO placeholders remain.
