# Specs Documentation Index

This index mirrors the authoritative specs/INDEX.md and is maintained by the Docs Agent.

## Status Summary
- See docs/STATUS_SUMMARY.md for cross-area status and inventory.

## Catalog
### Phase 1 (Locked)
- docs/specs/00_glossary.md - terminology grounding for the planning platform.
- docs/specs/01_domain_model.md - high-level entities and relationships.
- docs/specs/02_project_mission_model.md - project and mission structuring rules.
- docs/specs/03_multi_tenancy_and_security.md - tenancy and security guidance.
- docs/specs/04_architecture_principles.md - authoritative architecture rules and enforcement tests.
- docs/specs/05_domain_contracts.md - explicit inputs/outputs/ownership for core domain interactions.
- docs/specs/06_known_failure_patterns.md - detection and prevention rules for recurrent errors and drifts.
- docs/specs/07_data_ownership.md - authoritative ownership boundaries and required identifiers.
- docs/specs/08_rbac_model.md - enforceable role definitions, permissions, and evaluation order.
- docs/specs/09_audit_and_traceability.md - mandatory audit coverage, fields, retention, and correlation rules.
- docs/specs/10_api_conventions.md - authoritative REST design, URL structure, and pagination rules.
- docs/specs/11_api_error_model.md - contractual error envelope and code stability guarantees.
- docs/specs/12_api_versioning.md - versioning strategy, compatibility, and deprecation governance.
- docs/specs/13_identifiers_and_time.md - opaque identifier rules and UTC/ISO 8601 time handling.
- docs/specs/14_visual_language.md - semantic visual tokens and state rules for consistent UX surfaces.
- docs/specs/15_ui_component_contracts.md - global UI component rules, state model, accessibility, and forbidden patterns.
- docs/specs/16_ui_page_contracts.md - page-level contracts assembling approved components with navigation, RBAC, and audit rules.
- docs/specs/17_phase1_extended_domains.md - extended Phase 1 contracts for roadmap execution, inventory/equipment, and finance/accounting domains (Proposed Steps 08-10).
- docs/specs/18_cross_domain_read_models.md - cross-domain read-only projections for Planning, Inventory, Finance, and Operations (Phase 1 Step 11).
- docs/specs/19_domain_integration_rules.md - integration guardrails preventing hidden coupling across domains at the read layer (Phase 1 Step 11).
- docs/specs/20_location_and_maps_contracts.md - location identifiers, hierarchy, and read-only map references for Phase 1 Step 12.
- docs/specs/21_notifications_and_messaging_contracts.md - notification and messaging contracts for Phase 1 Step 13 (Proposed).
- docs/specs/25_mission_run_sheet.md - operational run sheet (call sheet) structure, lifecycle, attachments, and governance for missions in Phase 1.
- docs/specs/27_comptabilite.md - accounting scope covering invoices, bills, expenses, budget lines, payments, exports, permissions, and audit expectations for Phase 1 extension (Proposed).
- docs/specs/28_contrats.md - contracts scope for intermittent/CDDU, artist, vendor, and client agreements with lifecycle, templates, attachments, permissions, and audit rules for Phase 1 extension (Proposed).

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

## Rules
- Primary specifications live in specs/INDEX.md.
- Updates must respect AGENT.md stop conditions and roadmap linkage.
- ASCII-only content is enforced by guard scripts.
