# Decision 002 - Notification and Acceptance

Status: SEALED
Date: 2025-12-24

## Acceptance state machine (authoritative)
- Draft: intent recorded, not sent to collaborator.
- Pending Acceptance: notification dispatched and awaiting collaborator response.
- Accepted: collaborator confirms; reservation holds and planning proceeds.
- Refused: collaborator declines; reservation released and risk alert raised.
- Expired: no response before the deadline; reservation released and escalation triggered.
- Withdrawn: issuer cancels before acceptance; reservation released.
- Restart requires creating a new acceptance instance; states do not rewind.

## Notification states and relation to acceptance
- Prepared -> Dispatched -> Delivered -> Acknowledged/Failed/Escalated.
- Acceptance transitions to Pending Acceptance only once a notification is Dispatched.
- Failed or Escalated notifications keep acceptance in Pending Acceptance but record retries; Delivered without Acknowledged keeps acceptance pending until collaborator action or expiry.

## Triggers
- Creating or updating an assignment that requires collaborator acceptance prepares a notification.
- Linking a signed contract to an assignment with acceptance required dispatches a notification if none is active.
- Deadline proximity for Pending Acceptance triggers reminders; expiry triggers escalation.
- Explicit refusal or acceptance generates confirmations to stakeholders.

## Effects of acceptance outcomes
- Accepted: locks availability reservation for the assignment, locks the acceptance artifact, and records the contract reference if present; planning remains authoritative for schedule and scope.
- Refused: releases availability reservation, marks the acceptance artifact immutable, and raises a blocking risk signal until the planner adjusts staffing.
- Expired: releases availability reservation, marks the acceptance artifact immutable, and raises a warning risk signal.
- Withdrawn: releases availability reservation and records the withdrawal reason; no changes to planning beyond risk annotations.

## Auditability
- Log every transition with timestamps, actor, channel, payload snapshot (assignment id, contract id if any, recipient, deadline, template key), and outcome.
- Preserve notification dispatch traces (prepared payload, delivery attempts, acknowledgements) for replay.
- Maintain idempotent event identifiers so retries cannot create duplicate acceptance states.

## Forbidden transitions
- Accepted -> Pending Acceptance.
- Refused -> Pending Acceptance or Refused -> Accepted without creating a new acceptance instance.
- Expired -> Pending Acceptance without a new acceptance instance.
- Direct Draft -> Accepted/Refused/Expired without passing through Pending Acceptance.
- Pending Acceptance -> Withdrawn after collaborator acknowledgement; withdrawal must precede acceptance or refusal.

## Decision Status
SEALED - blocking for async/event model and contracts
