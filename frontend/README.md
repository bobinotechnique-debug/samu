# Frontend

React + Vite skeleton aligned with Phase 2 Step 10. The shell wires routing, providers, API client bootstrap, and placeholder UI without business logic.

## Structure
- `src/app` - application shell, route definitions, and providers.
- `src/pages/Placeholder` - placeholder page for routing targets.
- `src/shared/api` - environment loader and simple HTTP client wrapper.
- `src/shared/components/ErrorBoundary.tsx` - basic error boundary wiring.
- `src/test/setupTests.ts` - Jest DOM matcher registration for Vitest.

## Local usage
1. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL`.
2. Install dependencies: `npm install`.
3. Run tests: `npm run test`.
4. Start dev server: `npm run dev -- --host --port 4173`.
