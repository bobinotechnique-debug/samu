# UX Journeys - Phase 2 Step UX-02

Authoritative, named user journeys describing observable navigation and review flows across Planning, Mission, Notifications, and Acceptance surfaces. Declarative only; no UI layouts, APIs, or business logic.

## Journey List
- Mission Readiness Review
- Assignment Acceptance Path
- Change Notice Acknowledgment

## Mission Readiness Review
- Name: Mission Readiness Review
- Trigger: A project member sees a mission flagged for readiness confirmation in Planning.
- Entry Surface: Planning
- Flow Steps:
  1. Planning surface displays the mission with a readiness indicator and project context.
  2. User opens the mission from Planning to the Mission surface while maintaining project context.
  3. Mission surface presents status, schedule, and assignment summaries without edit controls.
  4. User follows the provided navigation to Notifications to view related readiness notices.
  5. Notifications surface highlights the mission readiness item and shows its current attention state.
  6. User opens the readiness notice, which presents the associated acceptance prompt.
  7. Acceptance surface shows the prompt with mission identifiers and available acknowledgment choices.
- Exit Surface: Acceptance
- Visibility Guarantees:
  - Organization, project, and mission identifiers remain visible across all steps.
  - Readiness indicator and notice status remain consistent between Planning, Mission, and Notifications.
  - Acceptance prompt mirrors the mission context without adding new states.
- Non-Goals:
  - No definition of readiness criteria, backend triggers, or state transitions.
  - No modification of mission data or notification delivery mechanics.

## Assignment Acceptance Path
- Name: Assignment Acceptance Path
- Trigger: A collaborator is assigned to a mission and needs to acknowledge the assignment.
- Entry Surface: Planning
- Flow Steps:
  1. Planning surface shows the mission with an assignment update indicator tied to the collaborator.
  2. User navigates into the Mission surface from Planning to review assignment details.
  3. Mission surface lists the collaborator assignment and highlights pending acknowledgment.
  4. User proceeds to Notifications via the provided navigation cue for assignment notices.
  5. Notifications surface presents the assignment notice with an action-required marker.
  6. User selects the notice, revealing the acceptance prompt for the assignment.
  7. Acceptance surface displays assignment acknowledgment options with mission context.
- Exit Surface: Acceptance
- Visibility Guarantees:
  - Assignment visibility aligns across Planning, Mission, and Notifications without conflicting statuses.
  - Acceptance prompt shows the same collaborator and mission identifiers as prior surfaces.
  - Notice action-required markers remain visible until the acceptance step is completed.
- Non-Goals:
  - No rules for assignment approval logic, reassignment, or escalation handling.
  - No specification of notification delivery channels or timing.

## Change Notice Acknowledgment
- Name: Change Notice Acknowledgment
- Trigger: A mission change notice is issued that requires acknowledgment.
- Entry Surface: Planning
- Flow Steps:
  1. Planning surface surfaces the mission with a change notice badge in the mission list.
  2. User opens the mission from Planning to the Mission surface to review the change summary.
  3. Mission surface presents the updated mission details and links to the related notice.
  4. User navigates to Notifications to view the mission change notice.
  5. Notifications surface lists the change notice with visibility of its required action.
  6. User opens the notice and is directed to the acceptance prompt.
  7. Acceptance surface displays acknowledgment choices referencing the documented change.
- Exit Surface: Acceptance
- Visibility Guarantees:
  - Change notice badges and statuses remain aligned between Planning and Notifications.
  - Mission identifiers and change summary references are consistent across Mission and Acceptance.
  - Required-action markers persist until the acceptance prompt is addressed.
- Non-Goals:
  - No specification of change detection logic, diffing rules, or audit storage.
  - No alterations to mission lifecycle states or notification suppression behavior.

## Validation Checklist
- Scope respected: YES
- Out-of-scope avoided: YES
- ASCII only: YES
- Phase alignment verified: YES
- Indexes updated: YES
