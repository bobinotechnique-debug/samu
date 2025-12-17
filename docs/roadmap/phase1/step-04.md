# Phase 1 - Step 04: Authoritative API and Integration Conventions

## Purpose
Establish immutable API and integration conventions that bind all future backend and frontend work and prevent drift before implementation starts.

## Scope
- Documentation only; no backend, frontend, infrastructure, or CI modifications.
- API design principles, error model, versioning rules, identifier and time conventions.
- Index updates and roadmap registration for Step 04 outputs.

## Assumptions
- Phase 1 remains documentation-only and Steps 00-03 are validated baselines.
- CI must remain green with ASCII-only changes.
- Architecture, data ownership, and audit constraints from prior steps remain authoritative.

## Exclusions
- Implementing endpoints, clients, schemas, or infrastructure.
- Modifying CI workflows, guard scripts, or runtime configuration.
- Introducing experimental patterns outside the documented conventions.

## Objective
Define the authoritative API and integration conventions that will constrain all backend and frontend work in later phases, preventing drift and inconsistent behaviors.

## Deliverables
- docs/specs/10_api_conventions.md documenting REST principles, URL structure, HTTP verb usage, idempotency, filtering, sorting, pagination, and forbidden patterns.
- docs/specs/11_api_error_model.md defining the global error response format, error codes, validation and business error handling, authentication and authorization rules, example payloads, and error code stability.
- docs/specs/12_api_versioning.md establishing versioning strategy, backward compatibility rules, deprecation process, forbidden breaking changes, and minimum support windows.
- docs/specs/13_identifiers_and_time.md locking identifier formats, timezone rules, serialization formats, and forbidden patterns.
- Updated indexes: docs/roadmap/INDEX.md, docs/roadmap/next_steps.md, docs/roadmap/phase1/INDEX.md, docs/specs/INDEX.md, specs/INDEX.md.
- Cross-links from docs/specs/01_domain_model.md, docs/specs/07_data_ownership.md, and docs/specs/09_audit_and_traceability.md to the new specifications.

## Acceptance Criteria
- Every new document includes Purpose, Scope, Assumptions, and Exclusions sections with explicit MUST/MUST NOT rules.
- REST conventions enforce resource-oriented design with /api/v1/ URI structure, idempotent verb rules, and consistent filtering, sorting, and pagination.
- Error model prescribes a stable JSON envelope with contractual error codes, differentiates validation, business, authentication, and authorization failures, and includes text-only examples.
- Versioning rules enforce URI-based versions, backward compatibility expectations, deprecation timelines, forbidden breaking changes, and a minimum support window for prior versions.
- Identifier and time conventions require opaque IDs, UTC-only timestamps, ISO 8601 serialization, and ban client-generated authoritative identifiers and local time handling.
- All created files are indexed and cross-referenced with no TODO placeholders.

## Explicit Non-Goals
- Changing or implementing backend or frontend functionality.
- Altering CI pipelines or guard scripts.
- Designing feature-specific APIs beyond the documented conventions.

## Dependencies
- Step 02: Architecture guardrails, domain contracts, and failure pattern rules that constrain API design.
- Step 03: Data ownership, RBAC, and audit requirements that must be enforced by API conventions and error handling.
