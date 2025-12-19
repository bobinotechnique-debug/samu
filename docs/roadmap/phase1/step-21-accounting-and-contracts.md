# Phase 1 - Step 21: Accounting and Contracts Extension (Amendment)

## Purpose
Extend the sealed Phase 1 documentation with accounting and contract scopes through the Step 14 amendment path without altering locked artifacts.

## Status
Proposed (documentation-only amendment aligned to Step 14 rules).

## Objectives
- Publish Phase 1 specifications for accounting (invoices, bills, expenses, budget lines, payments, attachments) and contracts (intermittent/CDDU, artist, vendor, client).
- Preserve organization/project security boundaries, RBAC enforcement, audit/traceability, and default-deny posture.
- Keep outputs documentation-only while deferring business logic, integrations, and regulatory exports.

## Deliverables
- docs/specs/27_comptabilite.md with scope, lifecycles, exports, permissions, audit expectations, and future extensions.
- docs/specs/28_contrats.md with contract types, common fields, lifecycle, templates, attachments, permissions, and audit expectations.
- docs/specs/phase1_coherence_audit_compta_contrats.md confirming alignment with glossary, domain, RBAC, audit, and multi-tenancy contracts.
- Index updates (docs/specs/INDEX.md, specs/INDEX.md) referencing the new specs.
- CHANGELOG.md entry and roadmap references documenting this amendment.

## Constraints
- Phase 1 remains documentation-only; no backend, frontend, infrastructure, or integration work is permitted.
- Organization is the security boundary; project is the functional boundary. No cross-organization data access or shared contracts/ledgers.
- No advanced accounting exports (FEC, bank sync, URSSAF/GUSO) or legal automation.
- All identifiers follow docs/specs/13_identifiers_and_time.md and must include organization_id and project_id.
- RBAC must reuse existing roles per docs/specs/08_rbac_model.md with default-deny evaluation.

## Dependencies
- Phase 1 lock charter (docs/roadmap/phase1/step-14.md) for amendment rules.
- Existing finance/accounting context (docs/roadmap/phase1/step-10.md and docs/specs/17_phase1_extended_domains.md).
- Core contracts: glossary, domain model, project/mission model, multi-tenancy and security, RBAC, audit/traceability, and API conventions.

## Acceptance Criteria
- Both specs are published with unique numbering, index registration, and ASCII-only content.
- Lifecycles, permissions, and audit requirements align with existing Phase 1 contracts without introducing cross-organization access.
- Coherence audit confirms no contradictions and records roadmap linkage.
- Roadmap and changelog entries document the amendment, keeping Phase 1 sequencing intact.
