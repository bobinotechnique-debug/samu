# Domain Model Overview

## Purpose
Capture the high-level entities and relationships for the project-centric planning SaaS.

## Scope
- Organization, project, mission, assignment, collaborator, and execution site relationships.
- Tenancy boundaries and ownership expectations in documentation form.

## Assumptions
- Organization remains the strict security boundary as defined in AGENT.md.
- No code or schema changes occur during Phase 1; only documentation is maintained.

## Exclusions
- Detailed API contract payloads or database schemas.
- Scheduling algorithms or optimization logic.

## Related Specifications
- Data ownership invariants are expanded in docs/specs/07_data_ownership.md.
- RBAC scoping aligned to domain entities is defined in docs/specs/08_rbac_model.md.
- Audit and traceability expectations per entity appear in docs/specs/09_audit_and_traceability.md.
- API conventions, identifier formats, and versioning rules governing domain exposure are defined in docs/specs/10_api_conventions.md, docs/specs/12_api_versioning.md, and docs/specs/13_identifiers_and_time.md.
