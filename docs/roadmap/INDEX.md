# Roadmap Documentation Index

This index routes roadmap documentation and status references governed by agents/docs.md and AGENT.md.

## Status Summary
- docs/STATUS_SUMMARY.md - consolidated roadmap and documentation state.

## Phase Overview
- **Phase 0: Hardening** - Status: Closed on 2025-12-17 (see docs/roadmap/phase0/step-01-harden-bootstrap.md)
- **Phase 1: Foundational documentation** - Status: LOCKED (see docs/roadmap/phase1/step-14.md for immutability and non-regression charter). Steps 00-13 are sealed; any amendment requires a new spec referencing the locked artifact and migration guidance.
- **Phase 2: Technical architecture** - Status: Starting (see docs/roadmap/phase2/INDEX.md for active Step 01-20 deliverables bound to Phase 1 contracts).

## Files
- docs/roadmap/README.md - roadmap diagrams and phase overviews.
- roadmap/phase0/step-00-bootstrap.md - sealed bootstrap log.
- docs/roadmap/phase0/step-01-harden-bootstrap.md - enforcement scope for Phase 0 guardrail validation.
- docs/roadmap/phase0/INDEX.md - Phase 0 step listing maintained under docs/roadmap/.
- docs/roadmap/phase0/diagram.md - Phase 0 visual sequence.
- docs/roadmap/phase1/INDEX.md - Phase 1 step listing.
- docs/roadmap/phase1/step-00.md - Phase 1 Step 00: foundational documentation scope and rules.
- docs/roadmap/phase1/step-01-foundational-domain.md - Phase 1 Step 01: foundational domain baselines (Done).
- docs/roadmap/phase1/step-02.md - Phase 1 Step 02: architecture guardrails, domain contracts, and failure patterns.
- docs/roadmap/phase1/step-03.md - Phase 1 Step 03: data ownership, RBAC, and audit rules.
- docs/roadmap/phase1/step-04.md - Phase 1 Step 04: API and integration conventions.
- docs/roadmap/phase1/step-05.md - Phase 1 Step 05: UX visual language and view specifications.
- docs/roadmap/phase1/step-06.md - Phase 1 Step 06: UI component contracts.
- docs/roadmap/phase1/step-07.md - Phase 1 Step 07: UI page contracts.
- docs/roadmap/phase1/step-08.md - Phase 1 Step 08: Roadmap and execution sheets (Proposed).
- docs/roadmap/phase1/step-09.md - Phase 1 Step 09: Inventory and equipment management (Proposed).
- docs/roadmap/phase1/step-10.md - Phase 1 Step 10: Finance and accounting (Proposed).
- docs/roadmap/phase1/step-11.md - Phase 1 Step 11: cross-domain read models and integration rules (Active).
- docs/roadmap/phase1/step-12.md - Phase 1 Step 12: locations and maps contracts (Proposed).
- docs/roadmap/phase1/step-13-notifications-and-messaging.md - Phase 1 Step 13: notifications and messaging contracts (Proposed).
- docs/roadmap/phase1/step-14.md - Phase 1 Step 14: global lock and non-regression charter (Locked).
- docs/roadmap/phase1/step-15.md - Phase 1 Step 15: UI component contracts reconciliation (Done).
- docs/roadmap/phase1/step-16.md - Phase 1 Step 16: UI page contracts reconciliation (Done).
- docs/roadmap/phase1/step-17.md - Phase 1 Step 17: domain object contracts (Proposed).
- docs/roadmap/phase1/step-18.md - Phase 1 Step 18: planning rules and constraints contract (Proposed).
- docs/roadmap/phase1/step-19.md - Phase 1 Step 19: state machines and lifecycles (Proposed).
- docs/roadmap/phase1/step-20.md - Phase 1 Step 20: permissions and responsibility matrix (Proposed).
- docs/roadmap/phase1/step-21-accounting-and-contracts.md - Phase 1 Step 21: accounting and contracts extension via Step 14 amendment (Proposed).
- docs/roadmap/phase1/step-22-planning-economic-extension.md - Phase 1 Step 22: planning economic extension for derived cost views, contract linkage, and cost centers (Proposed).
- docs/roadmap/phase1/diagram.md - Phase 1 visual sequence.
- docs/specs/18_cross_domain_read_models.md - Phase 1 Step 11: cross-domain read models and projections (Active).
- docs/specs/19_domain_integration_rules.md - Phase 1 Step 11: integration guardrails across domains (Active).
- docs/specs/21_notifications_and_messaging_contracts.md - Phase 1 Step 13: notifications and messaging contracts (Proposed).
- docs/roadmap/next_steps.md - sequencing of upcoming roadmap work.
- docs/roadmap/phase2/INDEX.md - Phase 2 Step 01-20 listings for architecture, data, API, async, security, frontend, deployment, observability, execution governance, testing harness scaffolding, resilience, rate limiting, feature flags, circuit breakers, caching, and consistency/idempotency.
- docs/roadmap/phase2/diagram.md - Phase 2 visual sequence.

## Rules
- Every change must cite a roadmap step before implementation.
- Phase exit is valid only when status lines in roadmap steps are marked Done.
