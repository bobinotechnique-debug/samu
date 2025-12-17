# Specs Documentation Index

This index mirrors the authoritative specs/INDEX.md and is maintained by the Docs Agent.

## Catalog
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

## Rules
- Primary specifications live in specs/INDEX.md.
- Updates must respect AGENT.md stop conditions and roadmap linkage.
- ASCII-only content is enforced by guard scripts.
