# Tests

Sample cross-cutting tests to validate backend and frontend baselines from the repository root.

- Backend tests use pytest to exercise FastAPI health probes and can run from `pytest tests/backend`.
- Frontend tests use Vitest and Testing Library to render the placeholder shell from `npm run test -- --dir ../tests/frontend` inside the `frontend` directory.
