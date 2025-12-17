# Frontend Agent Contract

## Scope
- Web UI implementation using React, Vite, and TailwindCSS.
- Client-side state, routing, and API integration surfaces.
- UX alignment for project and mission planning flows.

## Non-Goals
- Backend API or database changes.
- Infrastructure automation or CI configuration beyond frontend needs.
- Product specification ownership outside frontend UX feedback.

## Stop Conditions
- Stop if roadmap coverage is unclear or missing for requested work.
- Halt when frontend CI or guard scripts are failing.
- Pause when changes would alter backend contracts without backend agent approval.

## File Ownership Boundaries
- Owns frontend/ and frontend-focused assets under ux/.
- Collaborates on api/ specifications for client-server contracts.
- Does not modify backend/, ops/, or devops tooling without coordination.

## Required Outputs (Docs + Tests Policy)
- Update UX documentation and frontend readmes for changes impacting flows.
- Provide frontend automated tests or stories aligned with new UI behavior.
- Ensure changelog and roadmap mappings are recorded for frontend deliveries.
