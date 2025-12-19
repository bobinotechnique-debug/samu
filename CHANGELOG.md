# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Phase 2 Step 20 documentation for consistency, idempotency, retries, and concurrency control, including new specification, roadmap entry, and index updates.

## [2026-01-12] - Phase 2 Step 17 Rate Limiting and Quotas

### Added
- docs/specs/25_rate_limiting_and_quotas.md detailing organization-first rate limiting and quota strategy, scope dimensions, Redis keying guidance, enforcement placement, headers/error mapping, audit/observability integration, and failure/fallback behavior for Phase 2 Step 17.
- Roadmap entry for Phase 2 Step 17 capturing objectives, dependencies, acceptance criteria, and exclusions for the documentation-first delivery.
- Index updates registering the new specification within docs/specs/INDEX.md, specs/INDEX.md, and roadmap navigation.

## [2026-01-11] - Phase 2 Step 16 Feature Flags and Configuration Toggles

### Added
- docs/specs/26_feature_flags.md outlining feature flag and configuration toggle scope, precedence, naming, storage, logging guidance, forbidden patterns, and future extensions for Phase 2 Step 16.
- Feature flag scaffolding in the backend, including models, provider interface, loader utilities, injectable service, and configuration example for env/global/org overrides without business logic branching.
- Index, roadmap, and changelog updates registering Phase 2 Step 16 alongside unit tests covering precedence, parsing, and decision sources.

## [2026-01-10] - Phase 2 Step 15 Resilience and Rate Limiting

### Added
- docs/specs/25_resilience_and_error_handling.md capturing error categories, retry/timeout ownership, idempotency expectations, degraded mode behavior, and conceptual circuit breaker rules.
- docs/specs/26_rate_limiting_and_abuse_protection.md defining rate limit scopes, abuse protections, throttle responses, and observability requirements aligned to the API error model.
- Index and roadmap updates registering Phase 2 Step 15 specifications across docs/specs/INDEX.md, specs/INDEX.md, and roadmap navigation.

## [2026-01-09] - Phase 2 Step 14 Observability and Logging

### Added
- docs/ops/21_observability_and_logging.md documenting structured logging schema, correlation rules, log level policy, audit hook schema, and redaction guidance aligned to Phase 1 contracts.
- Roadmap and ops index updates registering Phase 2 Step 14 observability and logging deliverables, including roadmap step file and next steps note.

## [2026-01-08] - Phase 2 Step 13 Testing Strategy

### Added
- docs/specs/25_testing_strategy.md documenting the backend test pyramid, isolation practices, and forbidden testing patterns for Step 13.
- Pytest harness fixtures for FastAPI app setup, database session rollback, fake auth context overrides, and a healthcheck probe test to keep CI green.

## [2026-01-07] - Onboarding and CI improvements

### Added
- Getting started guidance, prerequisites, and navigation updates to simplify contributor onboarding.
- Cross-platform guard suite, sample backend and frontend tests under tests/, and roadmap diagrams for every phase.
- CI pipeline covering linting, guards, and tests across Linux, macOS, and Windows plus a release workflow for semantic versioning.

### Changed
- Introduced tables of contents for AGENT.md and README.md and reformatted this changelog to the Keep a Changelog convention.

## [2026-01-06] - Phase 2 Step 11 First Vertical Slice

### Added
- Auth + organization context slice with bearer token lookup, principal context, RBAC hooks, and org/membership CRUD APIs.
- Persistence models, alembic migration, seed script, docker compose updates, and backend/frontend tests for scoped access and error model enforcement.
- Roadmap, API and ops indexes, and new local run documentation for Step 11.

## [2026-01-05] - Phase 2 Step 10 Implementation Bootstrap

### Added
- Backend and frontend runnable scaffolding with FastAPI, routing, health probes, and React shell aligned to Phase 2 architecture docs.
- Docker Compose baseline, environment samples, and roadmap/doc index updates for Step 10 while keeping guards/tests green.

## [2026-01-04] - Phase 2 Step 09 Observability and Operations Baseline

### Added
- docs/ops/21_observability.md to lock logging, metrics, tracing, health checks, alerting, and runbooks for Phase 2 Step 09.
- Phase 2 Step 09 registration in roadmap indexes to keep navigation aligned with the new observability baseline.

## [2026-01-03] - Phase 2 Step 08 Deployment and Environments

### Added
- docs/ops/20_deployment_architecture.md with authoritative environment, configuration, secrets, and deployment topology contract for Phase 2 Step 08.
- Alignment with locked stack decisions, Windows-first reproducibility, and existing architecture/security specs.

## [2026-01-02] - Phase 2 Step 06 Security and Trust Model

### Added
- docs/specs/24_security_model.md detailing auth flows, token scopes, RBAC enforcement, and data isolation rules for Phase 2 Step 06.
- Specs and indexes updated to honor Phase 1 security, ownership, RBAC, and audit dependencies.

## [2026-01-01] - Phase 2 Step 05 Async and Background Jobs

### Added
- docs/specs/23_async_jobs.md covering asynchronous execution model, queues, payload contract, idempotency, retry/backoff, observability, and dead letter handling.
- Roadmap and status references for Phase 2 Step 05 while keeping existing architecture indexes intact.

## [2025-12-31] - Phase 2 Step 04 API Architecture and Routing

### Added
- docs/api/20_api_architecture.md with FastAPI routing, versioning, dependency, error mapping, and pagination scaffolds aligned to Phase 1 contracts and Phase 2 wiring goals.
- docs/api/INDEX.md updates to register the Phase 2 routing scaffold and cross-cutting middleware and dependency conventions.

## [2025-12-30] - Phase 2 Step 03 Persistence and Data Model

### Added
- docs/specs/22_persistence_model.md capturing PostgreSQL table, index, isolation, and soft delete design covering all Phase 1 entities.
- Audit/outbox persistence skeletons, integrity invariants, and retention policies to guide later implementation without semantic drift.

## [2025-12-29] - Phase 2 Step 02 Low Level Architecture

### Added
- docs/specs/21_architecture_LLD.md elaborating per-module layering, dependency rules, and async/job boundaries aligned to Phase 1 contracts.
- Backend package layout and cross-cutting rules for IDs, time, RBAC, audit, and repository/UoW patterns for services.

## [2025-12-28] - Phase 2 Architecture Kickoff

### Added
- Phase 2 roadmap with Steps 01-08 covering HLD, LLD, persistence, API architecture, async jobs, security, frontend architecture, and deployment environments.
- Phase 2 architecture specifications and index updates aligning Phase 2 documentation with Phase 1 contracts.

## [2025-12-27] - Phase 1 Step 16 UI Page Contracts and Roadmap Reconciliation

### Added
- Roadmap entries for Steps 15 and 16 plus reconciliation notes for the Step 07 numbering gap.
- Roadmap updates for Step 16 UI page contracts covering planning, mission, collaborator, and project pages and UX index updates.

## [2025-12-26] - Phase 1 Repo Consistency

### Added
- Missing step/spec/index files for Phase 1 Steps 01 and 13 to restore roadmap consistency.

## [2025-12-25] - Phase 1 Lock Charter and AGENT 2.5.0

### Added
- docs/roadmap/phase1/step-14.md to seal Phase 1 with immutability, amendment, and non-regression rules.
- Roadmap indexes and next steps updated to mark Phase 1 as LOCKED and register Step 14 navigation.
- AGENT.md version 2.5.0 declaration locking Phase 1 baseline and enforcement rules.

## [2025-12-24] - Phase 1 Step 11 Roadmap Registration

### Added
- docs/roadmap/phase1/step-11.md to log scope, deliverables, and acceptance criteria for cross-domain read models and integration guardrails.
- Roadmap and specs indexes updated to register Step 11 navigation alongside existing Phase 1 sequencing.

## [2025-12-23] - Phase 1 Step 11 Cross-Domain Read Models and Integration Rules

### Added
- docs/specs/18_cross_domain_read_models.md documenting authoritative read-only projections across Planning, Inventory, Finance, and Operations with snapshot and versioning requirements.
- docs/specs/19_domain_integration_rules.md capturing read-layer integration guardrails to prevent hidden coupling and enforce Phase 1 constraints.
- Roadmap and specs indexes updated to register Step 11 deliverables alongside existing Phase 1 navigation and sequencing.

## [2025-12-22] - Phase 1 Extended Domain Specifications (Proposed Steps 08-10)

### Added
- docs/specs/17_phase1_extended_domains.md capturing roadmap execution, inventory/equipment, and finance/accounting contracts under documentation-only scope.
- Phase 1 roadmap Steps 08-10 registered as Proposed with dedicated step files and index updates for navigation and dependencies.
- Roadmap next steps updated to include extended domains while honoring Phase 1 constraints and sequencing.

## [2025-12-21] - Phase 1 Step 07 UI Page Contracts Registration

### Added
- Phase 1 Step 07 roadmap entry with status Done and linked deliverables.
- Roadmap indexes and next steps updated to include the Step 07 UI page contracts alongside prior steps.
- Catalog references for docs/specs/16_ui_page_contracts.md and UX page contract indexes to keep Step 07 discoverable.

## [2025-12-20] - Phase 1 Step 06 UI Component Contracts

### Added
- Phase 1 Step 06 roadmap completion with authoritative UI component contracts.
- docs/specs/15_ui_component_contracts.md expansions with catalog, integration guardrails, and alignment to prior specs.
- Integration notes across docs/ux/components/ contracts to lock API, RBAC, ownership, and audit expectations.

## [2025-12-19] - Phase 1 Step 03 Data Ownership, RBAC, and Audit Rules

### Added
- Phase 1 Step 03 roadmap entry to lock data ownership, RBAC, and audit constraints.
- Authoritative data ownership, RBAC, and audit/traceability specifications under docs/specs/ with index updates.
- Roadmap navigation and cross-links updated to reference the new rules.

## [2025-12-18] - Phase 1 Step 02 Documentation Guardrails

### Added
- Phase 1 Step 02 roadmap entry covering architecture principles, domain contracts, and failure patterns.
- Architecture principles, domain interaction contracts, and known failure patterns published under docs/specs/ with index updates.
- Agent contracts updated to enforce alignment with new guardrails and recorded roadmap navigation updates.

## [2025-12-17] - Phase 1 Initiation

### Added
- Phase 0 closure after completing docs/roadmap/phase0/step-01-harden-bootstrap.md and sealing guardrail validation.
- Phase 1 roadmap kickoff (docs/roadmap/phase1/step-00.md) focused on foundational documentation with Phase 1 constraints.
- Agent contracts aligned with Phase 1 documentation-only scope.
- Restored authoritative Phase 0 bootstrap step at roadmap/phase0/step-00-bootstrap.md to satisfy roadmap guard coverage.

## [2025-02-21] - Phase 0 Step 01

### Added
- Phase 0 validation hardening via enforceable guards, CI validation, and roadmap updates (roadmap: docs/roadmap/phase0/step-01-harden-bootstrap).

## [2025-02-20] - Version 2.4.0 (Phase 0 Hardening)

### Added
- Sealed Phase 0 by enforcing guardrails, navigation indexes, and stop conditions (roadmap: phase0/step-00-bootstrap).
- Elevated AGENT.md to ROOT OFFICIAL with version bump and explicit update rules.
- Required documentation indexes, guard scripts, and agent precedence confirmations.

## [2025-02-19] - Phase 0 Bootstrap Initialization

### Added
- Initial Phase 0 orchestration skeleton and documentation scaffolding (roadmap step: phase0/step-00-bootstrap).
