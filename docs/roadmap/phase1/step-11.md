# Phase 1 - Step 11: Cross-Domain Read Models and Integration Rules (Active)

## Purpose
Document authoritative cross-domain read models and integration guardrails that let Planning, Inventory, Finance, and Operations share read-only projections without violating Phase 1 constraints.

## Scope
- Documentation only; no backend, frontend, infrastructure, or CI modifications.
- Cross-domain read model definitions, versioning rules, and provenance requirements.
- Integration guardrails that prevent hidden coupling across projects, missions, and operational domains.
- Index updates and roadmap registration for Step 11 outputs.

## Assumptions
- Phase 1 remains documentation-only with Steps 02-04 establishing architecture, ownership, RBAC, audit, identifier, and API conventions.
- Organization and project scopes are mandatory; missions inherit project scope and cannot cross organizations.
- Cross-domain projections are GET-only and never emit client-generated authoritative identifiers.

## Exclusions
- Implementing endpoints, pipelines, ETL jobs, or replication services.
- Introducing mutable cross-domain workflows, schedulers, or automation triggers.
- Changing CI workflows, guard scripts, infrastructure, or runtime configuration.

## Objective
Publish read-only contracts that enable safe cross-domain insights while keeping domains decoupled until implementation planning begins.

## Deliverables
- docs/specs/18_cross_domain_read_models.md capturing read-only projections across Planning, Inventory, Finance, and Operations.
- docs/specs/19_domain_integration_rules.md defining integration guardrails that bind cross-domain reads to Phase 1 constraints.
- Updated indexes: docs/roadmap/INDEX.md, docs/roadmap/phase1/INDEX.md, docs/roadmap/next_steps.md, docs/specs/INDEX.md, specs/INDEX.md.
- Roadmap registration marking Step 11 as Active within Phase 1 sequencing.

## Acceptance Criteria
- Read models enumerate required fields, scopes, provenance, freshness, and versioning rules, all bound to organization_id and project_id with mission inheritance.
- Integration guardrails define allowed cross-domain joins, aggregation limits, and API alignment with explicit RBAC and audit references.
- Contracts remain GET-only, forbid cross-organization visibility, and cite identifier/time conventions to prevent drift.
- Documentation is ASCII-only, indexed, and contains no TODO placeholders.

## Explicit Non-Goals
- Building synchronization engines, event streams, or background workers to populate read models.
- Allowing write paths, cross-organization aggregation, or client-side authoritative identifiers.

## Dependencies
- Steps 02-04 for architecture guardrails, ownership, RBAC, audit, identifier/time, and API conventions that govern cross-domain reads and integrations.
