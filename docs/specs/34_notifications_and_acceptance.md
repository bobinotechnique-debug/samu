# Phase 2 Spec 34 - Notifications and Acceptance

## 1. Purpose
- Define the notification model and acceptance flow for assignment engagement without embedding business rules in the frontend.
- Provide delivery guarantees, payload contracts, and forbidden patterns to keep engagement auditable and idempotent.

## 2. Notification Model
- A notification is an intent + delivery artifact: it informs but is not itself a legal act.
- Mandatory channel: in-app inbox/center scoped by org_id and project_id.
- Optional future channels: email, SMS, push; they mirror in-app payload but cannot be authoritative for actions.
- Delivery semantics: at-least-once for async deliveries; clients render idempotently using notification_id and type.

## 3. Notification Types
- ASSIGNMENT_PROPOSED: assignment ready for acceptance; includes proposal expiration metadata.
- ASSIGNMENT_UPDATED: proposal changed (dates, role, rate) while remaining PROPOSED.
- ASSIGNMENT_CANCELED: assignment canceled or declined, with reason codes.
- CONTRACT_EXPECTED_WARNING: acceptance recorded but contract missing after grace window.
- CONTRACT_READY: contract generated and ready for signature/acknowledgement (no e-sign in scope).

## 4. Payload Contract (minimum fields)
- id
- org_id
- project_id
- recipient_id (collaborator or manager)
- type (enum above)
- entity_ref: { mission_id, assignment_id }
- created_at (UTC ISO 8601)
- read_at (nullable)
- metadata (object) including message template variables, proposal_expires_at, reason_code, and correlation_id/trace_id.

## 5. Read and Ack Semantics
- In-app notifications default to unread; marking read sets read_at and writes audit event notification.read.
- Re-deliveries reuse the same notification_id when retrying a failed async channel; clients must treat duplicates as idempotent using id + type.
- Notifications never execute transitions; they surface pending actions (accept/decline) or missing artifacts (contract, documents).

## 6. Acceptance Flow
- Collaborator action ACCEPTED is the authoritative legal acknowledgement for an assignment; must be captured with actor_id, occurred_at, and optional comment.
- Optional manager confirmation (CONFIRMED) occurs after acceptance and enforces document/budget checks per docs/specs/33_assignment_engagement_states.md.
- Frontend collects intent and calls backend API; frontend must not enforce business rules locally.
- Decline uses CANCELED with reason=declined_by_collaborator; notification ASSIGNMENT_CANCELED emitted.

## 7. Delivery Guarantees and Operational Rules
- Async delivery retries with exponential backoff and max_attempts configurable per channel; failures emit audit events notification.delivery_failed with attempt count and error code.
- At-least-once delivery means duplicates are possible; UI must rely on notification_id and correlation_id to avoid duplicate banners or toasts.
- Outbox/publisher must include trace_id; downstream channels propagate trace_id for observability.

## 8. Forbidden Patterns
- Notification must not trigger contract generation without acceptance; contracts enqueue only after AssignmentAccepted event (see docs/specs/35_contract_generation_pipeline.md).
- Frontend must not write business rules or alter state directly; all transitions occur server-side with audit.
- No silent read receipts; read_at updates require explicit user action or deliberate auto-mark with audit annotation.

## 9. Alignment and Dependencies
- Aligns with docs/specs/21_notifications_and_messaging_contracts.md for channel behaviors and docs/specs/25_consistency_and_idempotency.md for idempotent delivery.
- Respects ownership and RBAC: notification queries filtered by org_id/project_id and recipient membership.

## 10. Roadmap Linkage
- Phase 2 Step 21 (docs/roadmap/phase2/step-21-engagement-states.md) scopes these notification and acceptance rules.
