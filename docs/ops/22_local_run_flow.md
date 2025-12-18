# Local Run Flow - Phase 2 Step 11 Vertical Slice

Status: In Progress

## Purpose

Document the minimal commands to stand up the auth + org context vertical slice locally with migrations, seed data, and frontend access.

## Prerequisites

- Docker + Docker Compose
- Python 3.11+ and Node 20+ for direct script execution
- Environment variables: SAMU_DATABASE_URL, SAMU_DEV_TOKEN (optional override for seed), VITE_API_BASE_URL

## Steps

1) Run migrations

- `powershell ./PS1/migrate.ps1`
- `docker compose run --rm api alembic upgrade head`

2) Seed dev data

- `powershell ./PS1/seed.ps1` (creates dev@samu.local, two orgs, memberships, and a token)
- `docker compose run --rm --profile seed seed` (alternate compose-driven seed)

3) Start services

- `docker compose up api frontend db cache`
- API auto-runs `alembic upgrade head` on startup; frontend served on port 4173 by default.

4) Call the slice

- Use the seeded token as a bearer credential; set `X-Org-ID` to switch between seeded orgs.
- Endpoints exercised by the frontend: `/api/v1/orgs/me`, `/api/v1/orgs`, `/api/v1/orgs/{org_id}/memberships`.

5) Tests

- Backend: `pip install -e ./backend[dev] && pytest` (uses in-memory sqlite)
- Frontend: `npm install && npm run test`
