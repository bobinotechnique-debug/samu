# Phase 1 - Step 10: Finance and Accounting (Proposed)

## Purpose
Capture finance and accounting documentation—cost tracking, rates and budgets, invoicing exports, and accounting read models—before any code or integration work begins.

## Scope
- Documentation only; no backend, frontend, infrastructure, or CI modifications.
- Cost tracking for projects and missions, rate/budget/forecast rules, invoicing/export contracts, and accounting read models.
- Alignment with Phase 1 API conventions, ownership, RBAC, audit, identifier, and time constraints.

## Assumptions
- Phase 1 remains documentation-only with Steps 00-07 established as baselines.
- All finance artifacts are scoped by organization_id and project_id; missions inherit project scope.
- Currency and precision rules follow documented contracts and forbid client-generated authoritative identifiers.

## Exclusions
- Implementing billing pipelines, payment processing, or ledger integrations.
- Generating live invoices, budget adjustments, or forecast calculations.
- Modifying CI, guard scripts, or operational infrastructure.

## Objective
Define authoritative finance and accounting contracts to inform later implementation without permitting runtime changes.

## Deliverables
- Finance and accounting contracts captured in docs/specs/17_phase1_extended_domains.md under the Step 10 domain.
- Updated indexes: docs/roadmap/INDEX.md, docs/roadmap/phase1/INDEX.md, docs/roadmap/next_steps.md, docs/specs/INDEX.md, specs/INDEX.md.
- Roadmap registration marking Step 10 as Proposed within Phase 1 sequencing.

## Acceptance Criteria
- Cost tracking contracts enumerate required data points per project/mission and align them with mission milestones and assignments.
- Rate, budget, and forecast contracts define effective dates, currency/precision rules, and snapshot expectations without prescribing implementation.
- Invoicing and export contracts remain read-only, align to API conventions, and ban payment processing or ledger mutations in Phase 1.
- Accounting read models list provenance and versioning requirements with RBAC, audit, and organization/project scoping.
- Documentation is ASCII-only, indexed, and cites Phase 1 constraints with no TODO placeholders.

## Explicit Non-Goals
- Implementing financial calculations, payment flows, or accounting system integrations.
- Introducing cross-organization finance visibility or multi-tenant ledger shortcuts.

## Dependencies
- Steps 02-04 for ownership, RBAC, audit, identifier/time, and API conventions that govern finance contracts.
