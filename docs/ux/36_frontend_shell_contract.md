# Phase 2 Step 10 - Frontend App Shell Contract

## Purpose
Define the wiring expectations for the frontend shell so routing, configuration, and API client scaffolding are consistent with backend bootstrap outputs before domain views are implemented.

## Scope
- Applies to the Vite/React app shell, router initialization, and API client wrapper used during Step 10.
- Includes environment variable loading, base layout shell, and placeholder routes for authenticated vs unauthenticated experiences.
- Excludes feature pages, domain-specific components, and styling refinements beyond layout scaffolding.

## Deliverables
- Router configured with authenticated guard placeholder and routes for `/`, `/login`, and `/health` status page stub.
- API client wrapper that reads base URL from environment with sane defaults for local/CI and attaches request_id/correlation_id headers when provided.
- Layout shell with global providers (query client, error boundary) and loading/error placeholders.
- Environment example updated to document required frontend variables and their precedence.

## Acceptance checks
- `npm run dev` and `npm run build` succeed using committed example environment files without hitting live APIs.
- Health/status stub renders without backend data dependency and surfaces request_id when present in responses.
- Router redirects unauthenticated users away from protected placeholder routes while keeping `/login` public.

## Traceability
- Roadmap: docs/roadmap/phase2/step-10-implementation-bootstrap.md
- Related audits: docs/audits/bootstrap_implementation_plan.md, docs/audits/bootstrap_implementation_report.md
