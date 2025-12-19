# UX Surface Contracts - Phase 2 Step UX-01

Authoritative UX surface contracts aligned to Phase 1 page and component agreements. ASCII only. Declarative descriptions; no implementation detail, business logic, or API behavior.

## Planning

### Purpose
- Provide a consolidated planning view of missions within a project scope, preserving organization and project boundaries.

### User Intent
- Scan mission schedules and assignment load at a glance.
- Identify scheduling conflicts, gaps, or overlaps.
- Access mission details without altering mission state.

### Screen Structure (textual layout)
- Header: project name, timeframe selectors, view toggle (timeline/board) using approved controls.
- Primary area: mission list segmented by time or status lanes (matches Phase 1 planning page layout).
- Side panel: filters (status, collaborators, timeframe) and legend using existing filter and badge components.
- Footer/status bar: selection summary and audit context (read-only).

### UX States (visible states only)
- Loading: placeholder skeletons for header controls and mission containers.
- Empty: no missions matching filters; show empty-state message with CTA to navigate to mission creation entry point (no inline creation).
- Populated: missions rendered with read-only summaries per component contracts.
- Filtered: subset view with active filter indicators.
- Error banner: non-blocking display when data cannot be retrieved; allows retry.

### Allowed Interactions
- Switch between timeline and board representations using existing toggle control.
- Apply/remove filters; clear all filters.
- Expand a mission summary to view details in a side drawer or modal defined in page contracts.
- Navigate to mission creation flow via provided link/button (no inline editing).
- Refresh/retry data when error banner is visible.

### Forbidden UX Patterns
- Inline mission creation or edits within the planning surface.
- Drag-and-drop that mutates mission scheduling or assignments.
- Cross-project navigation shortcuts that bypass project context.
- Displaying backend error codes or technical traces to users.

## Mission

### Purpose
- Present mission-specific details, assignments, schedule, and status in a project-scoped view.

### User Intent
- Review mission scope, timeline, and assigned collaborators.
- Verify readiness states and dependencies as defined by existing contracts.
- Access related documents and linked planning context.

### Screen Structure (textual layout)
- Header: mission title, status badge, project and organization identifiers.
- Tabs/sections: Overview, Schedule, Assignments, Activity log (read-only), adhering to Phase 1 page structure.
- Sidebar: key metadata (owner, priority, tags) and quick links to planning surface.
- Footer: audit stamp (created/updated by) with no editing affordances.

### UX States (visible states only)
- Loading: skeletons for header and tab containers.
- Empty assignments: mission exists but no collaborators; placeholder text with navigation to collaborator selection flow (outside this surface).
- Populated: mission details, schedule, and assignments visible per existing component contracts.
- Read-only locked: mission state locked by governance; all interactive controls disabled with tooltip messaging.
- Error banner: retrieval issues; offers retry without exposing raw errors.

### Allowed Interactions
- Switch between tabs/sections without altering mission state.
- Open collaborator profiles from assignment list in read-only mode.
- Trigger navigation to allowed edit flows (e.g., open existing mission edit page) via clearly labeled buttons; no inline edits.
- Retry data fetch when error banner shown.

### Forbidden UX Patterns
- Inline editing of mission attributes on this surface.
- State transitions (e.g., start/complete) without following approved workflows.
- Removing assignments directly from read-only lists.
- Exposing backend identifiers or audit event IDs.

## Collaborator

### Purpose
- Provide a collaborator-centric view of assignments, availability, and profile context within a single organization.

### User Intent
- See upcoming and active mission assignments for the collaborator.
- Understand availability windows and workload distribution.
- Access profile details without modifying identity or permissions.

### Screen Structure (textual layout)
- Header: collaborator name, role badges, organization marker.
- Availability strip: calendar or heatmap component as defined in component contracts (read-only rendering).
- Assignment list: grouped by status/timeframe with mission links.
- Sidebar: contact and skills tags sourced from existing profile fields.

### UX States (visible states only)
- Loading: skeleton rows for assignments and availability strip.
- No assignments: empty-state message with guidance to add via planning/mission flows (not inline here).
- Populated: assignments and availability rendered per contract.
- Limited visibility: restricted fields masked with "restricted" indicator when RBAC hides details.
- Error banner: retrieval failure with retry affordance.

### Allowed Interactions
- Navigate to mission surfaces from assignment entries (read-only context preservation).
- Filter assignments by timeframe or status using approved controls.
- Expand assignment cards for additional detail (no edits).
- Retry loading when errors occur.

### Forbidden UX Patterns
- Editing collaborator profiles or permissions from this surface.
- Reassigning or removing assignments inline.
- Cross-organization navigation.
- Displaying calculated workload percentages beyond existing metrics.

## Notifications and Acceptance

### Purpose
- Present user-facing notifications and acceptance prompts related to missions, collaborations, and governance actions.

### User Intent
- Review pending notifications with clear source context.
- Acknowledge or accept mission-related actions when required.
- Dismiss non-critical alerts without altering underlying records.

### Screen Structure (textual layout)
- Header: notification center title, filter tabs (All, Unread, Action Required).
- Feed list: notification items with status indicators and timestamps, adhering to notification component contracts.
- Action pane: contextual area for acceptance prompts when an item is selected.
- Footer: audit note on notification policy and delivery time references.

### UX States (visible states only)
- Loading: skeleton placeholders for list items and action pane.
- Empty: no notifications in current filter; show empty-state copy.
- Unread items: highlighted per visual language; badge count in header.
- Action required: items that need acknowledgment/acceptance show primary action control.
- Read/dismissed: visually de-emphasized items remain visible for traceability.
- Error banner: retrieval or action failure shown non-invasively with retry.

### Allowed Interactions
- Mark notification as read/unread using existing toggle affordance.
- Dismiss non-blocking notifications.
- Accept/acknowledge actionable items using provided primary/secondary buttons; actions must follow predefined flows without inline edits.
- Filter and sort notifications by status or recency.
- Retry failed loads or actions when error banner displayed.

### Forbidden UX Patterns
- Hard-deleting notifications from the feed.
- Editing mission or collaborator data directly from a notification item.
- Auto-accepting actions without explicit user input.
- Displaying transport/channel metadata not surfaced in Phase 1 contracts.

## Validation Checklist
- Scope respected: YES
- Out-of-scope avoided: YES
- ASCII only: YES
- Phase alignment verified: YES
- Indexes updated: YES
