# Audit and Traceability Rules

## Purpose
Define mandatory audit and traceability requirements to ensure accountability, reproducibility, and security across the platform.

## Scope
- Applies to all domain operations affecting organizations, projects, missions, assignments, planning artifacts, and role bindings.
- Governs audit event coverage, required audit record fields, retention, and access rules during Phase 1 documentation.

## Assumptions
- Organization remains the security boundary and project remains the functional boundary for all audit context.
- Default-deny authorization and strict data ownership rules from docs/specs/07_data_ownership.md and docs/specs/08_rbac_model.md are in force.
- Phase 1 records expectations only; implementation will follow later roadmap steps.

## Exclusions
- Implementation of logging pipelines, storage backends, or SIEM integrations.
- Real-time alerting or monitoring configurations.

## Mandatory Audit Events
- Mission lifecycle: create, update, delete, publish, and status transitions MUST be audited with before/after summaries.
- Assignment lifecycle: create, update, delete, reassignment, and status changes MUST be audited.
- Planning artifacts: creation, updates, publication, and approvals MUST be audited when introduced.
- Role and permission changes: grants, revocations, and role escalations MUST be audited.
- Project and organization configuration changes: creation, updates, archival, and ownership transfers MUST be audited.
- Authentication and authorization failures SHOULD be logged with correlation ids without leaking secrets.

## Required Fields per Audit Record
- who: authenticated actor identifier (user_id) or system service id; MUST NOT be null.
- when: timestamp in UTC with timezone offset.
- org_id: MUST be present for every record.
- project_id: MUST be present for project, mission, planning, or assignment events.
- entity_type: canonical name (organization, project, mission, assignment, planning_artifact, role_binding, collaborator).
- entity_id: identifier of the impacted entity.
- action: verb describing the event (create, update, delete, publish, assign, revoke, etc.).
- diff_summary: concise description of changes; MUST avoid sensitive data but be specific enough for review.
- request_id / correlation_id: identifier linking all logs for a single request or workflow; MUST be generated server-side.
- source_ip and user_agent SHOULD be captured for interactive sessions where available.

## Retention and Access Rules
- Audit records MUST be immutable after write; corrections require append-only compensating entries referencing the original record id.
- Retention MUST meet organization policy with a minimum default of 400 days unless overridden by compliance requirements.
- Access to audit logs MUST be limited to org_owner, org_admin, and designated compliance roles; project_manager MAY access project-scoped audit records when allowed by policy.
- Export of audit data across organizations MUST follow explicit governance and MUST NOT mix records from different organizations in a single export without org_id partitioning.

## Correlation and Traceability
- Every request that mutates data MUST include or generate a correlation_id and propagate it through downstream services and audit entries.
- Audit pipelines MUST preserve ordering per entity where possible and include correlation_id to reconstruct sequences.
- Audit lookups MUST support filtering by org_id, project_id, entity_type, entity_id, action, and correlation_id to enable investigations.

## Related Specifications
- Error envelope requirements for audit-friendly responses are defined in docs/specs/11_api_error_model.md.
- Identifier and timestamp formats required for audit fields are defined in docs/specs/13_identifiers_and_time.md.
- Versioning rules that govern audit field stability are defined in docs/specs/12_api_versioning.md.
- UX presentation of audit context in mission flows and planning surfaces is guided by docs/specs/14_visual_language.md and docs/ux/INDEX.md.
