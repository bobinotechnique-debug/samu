# Specs Index

## Purpose
Catalog technical and product specifications that guide implementation.

## Expected Documents
### Phase 1 (Locked)
- docs/specs/00_glossary.md - Glossary for shared terminology.
- docs/specs/01_domain_model.md - Domain entity relationships and boundaries.
- docs/specs/02_project_mission_model.md - Project and mission structure guidelines.
- docs/specs/03_multi_tenancy_and_security.md - Multi-tenancy and security expectations.
- docs/specs/04_architecture_principles.md - Authoritative architecture principles and enforcement tests.
- docs/specs/05_domain_contracts.md - Contracts covering inputs, outputs, ownership, and forbidden dependencies across domains.
- docs/specs/06_known_failure_patterns.md - Catalog of detection and prevention rules for recurrent failures.
- docs/specs/07_data_ownership.md - Authoritative ownership boundaries and required identifiers.
- docs/specs/08_rbac_model.md - Enforceable roles, permissions, and evaluation order.
- docs/specs/09_audit_and_traceability.md - Mandatory audit coverage, required fields, retention, and correlation guidance.
- docs/specs/10_api_conventions.md - Authoritative REST design, URL structure, and pagination rules.
- docs/specs/11_api_error_model.md - Contractual error envelope and code stability guarantees.
- docs/specs/12_api_versioning.md - Versioning strategy, compatibility, and deprecation governance.
- docs/specs/13_identifiers_and_time.md - Opaque identifier rules and UTC/ISO 8601 time handling.
- docs/specs/14_visual_language.md - Semantic visual language and interaction tokens for UX surfaces.
- docs/specs/15_ui_component_contracts.md - UI component rules, state model, and accessibility baseline aligned to visual language and API conventions.
- docs/specs/16_ui_page_contracts.md - UI page contract rules, navigation, shared state, and forbidden patterns.
- docs/specs/17_phase1_extended_domains.md - Extended Phase 1 contracts for roadmap execution, inventory/equipment, and finance/accounting domains (Proposed Steps 08-10).
- docs/specs/18_cross_domain_read_models.md - Cross-domain read-only projections for Planning, Inventory, Finance, and Operations (Phase 1 Step 11).
- docs/specs/19_domain_integration_rules.md - Integration guardrails preventing hidden coupling across domains at the read layer (Phase 1 Step 11).
- docs/specs/20_location_and_maps_contracts.md - Location identifiers, hierarchy, and read-only map references for Phase 1 Step 12.
- docs/specs/21_notifications_and_messaging_contracts.md - Notification and messaging contracts for Phase 1 Step 13 (Proposed).
- docs/specs/25_mission_run_sheet.md - Operational run sheet (call sheet) structure, lifecycle, attachments, and governance for missions in Phase 1.
- docs/specs/27_comptabilite.md - Accounting scope covering invoices, bills, expenses, budget lines, payments, exports, permissions, and audit expectations for Phase 1 extension (Proposed).
- docs/specs/28_contrats.md - Contracts scope for intermittent/CDDU, artist, vendor, and client agreements with lifecycle, templates, attachments, permissions, and audit rules for Phase 1 extension (Proposed).
- docs/specs/29_planning_cost_view.md - Planning-derived cost views per day, mission, and project with display-only, reproducible estimates (Phase 1 extension).
- docs/specs/30_contract_assignment_link.md - Contract-to-assignment linkage rules, lifecycle, and non-blocking completeness alerts for planning coherence (Phase 1 extension).
- docs/specs/31_cost_centers.md - Project and mission-scoped cost center classification for derived planning reports without accounting ledgers (Phase 1 extension).
- docs/specs/32_engagement_acceptance_and_notifications.md - Engagement ladder, enriched acceptance, declarative reminders/escalations, engagement timeline, execution documents, and audit journal for Phase 1 extension.

### Coherence Audits
- docs/specs/phase1_coherence_audit_engagement_acceptance.md - Audit confirming alignment of engagement, acceptance, reminders, and audit timeline scope with Phase 1 constraints.

### Phase 2 (In Progress)
- docs/specs/20_architecture_HLD.md - High Level Architecture (context, boundaries, sync/async flows, trust boundaries) for Phase 2 Step 01.
- docs/specs/21_architecture_LLD.md - Low Level Architecture (package layout, layering, dependency rules) for Phase 2 Step 02.
- docs/specs/22_persistence_model.md - Persistence model with tables, relations, indexes, and soft delete rules for Phase 2 Step 03.
- docs/specs/23_async_jobs.md - Async job model covering job types, queues, and retry policies for Phase 2 Step 05.
- docs/specs/24_security_model.md - Security and trust model with auth flows, token scopes, and data isolation for Phase 2 Step 06.
- docs/specs/25_execution_invariants.md - Execution governance rules, enforcement matrix, and stop conditions for Phase 2 Step 12.
- docs/specs/25_testing_strategy.md - Backend testing pyramid, isolation rules, and pytest harness guardrails for Phase 2 Step 13.
- docs/specs/25_resilience_and_error_handling.md - Resilience model for error propagation, retries, timeouts, idempotency, degraded modes, and circuit breaker expectations for Phase 2 Step 15.
- docs/specs/25_rate_limiting_and_quotas.md - Organization-first rate limiting and quota strategy with enforcement placement, headers, and failure behavior for Phase 2 Step 17.
- docs/specs/25_consistency_and_idempotency.md - Consistency model for writes, idempotency contracts for sync and async flows, retry safety, concurrency conflict handling, and audit/trace propagation for Phase 2 Step 20.
- docs/specs/26_feature_flags.md - Feature flag and configuration toggle scaffolding, precedence, naming, storage, and logging guidance for Phase 2 Step 16.
- docs/specs/26_rate_limiting_and_abuse_protection.md - Rate limiting scopes, throttling rules, headers, and abuse protection expectations for Phase 2 Step 15.
- docs/specs/26_resilience_and_circuit_breakers.md - Circuit breaker, retry, timeout, and resilience policies to prevent cascading failures for Phase 2 Step 18.
- docs/specs/26_caching_strategy.md - Caching strategy, key format, TTL rules, invalidation, observability, and safety constraints for Phase 2 Step 19.
- docs/specs/33_assignment_engagement_states.md - Assignment engagement state machine, transitions, invariants, and audit rules for Phase 2 Step 21.
- docs/specs/34_notifications_and_acceptance.md - Notification model, payload contract, acceptance flow, and forbidden patterns for Phase 2 Step 21.
- docs/specs/35_contract_generation_pipeline.md - Event-driven contract generation pipeline with idempotency, auditability, and alerting for Phase 2 Step 21.

## Ownership
Docs Agent in collaboration with Backend and DevOps Agents
