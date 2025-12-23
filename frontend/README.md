# Frontend

React + Vite skeleton aligned with Phase 2 Step 10. The shell wires routing, providers, API client bootstrap, and placeholder UI without business logic.

## Structure
- `src/app` - application shell, route definitions, and providers.
- `src/pages/*` - placeholder pages for planning, missions, collaborators, settings, and not found routing.
- `src/shared/api` - environment loader and HTTP client wrapper with versioned path support.
- `src/shared/components/ErrorBoundary.tsx` - basic error boundary wiring.
- `src/test/setupTests.ts` - Jest DOM matcher registration for Vitest.

## Local usage
1. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL` (defaults to `http://localhost:8000`).
2. Install dependencies: `npm install`.
3. Run tests: `npm run test`.
4. Start dev server: `npm run dev -- --host --port 4173`.
