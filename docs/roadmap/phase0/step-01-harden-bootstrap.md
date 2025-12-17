# Phase 0 - Step 01: Harden Bootstrap

## Goal
Enforce Phase 0 guardrails so bootstrap scaffolding is validated deterministically in local and CI runs.

## Deliverables
- PowerShell validate entrypoint that orchestrates all guards in a deterministic order.
- Updated guard scripts with strict templates for ASCII, agents, docs, and roadmap coverage.
- CI workflow that runs validate on pull requests and main pushes.
- Roadmap, changelog, and operations docs updated to reflect enforceable Phase 0.

## Acceptance Criteria
- `PS1/validate.ps1` executes guards in order and stops on the first failure while emitting pass or fail summaries.
- Guard scripts provide actionable errors for ASCII violations, agent precedence, documentation coverage, and roadmap linkage.
- docs/ops/agent_errors.md follows the required template and is enforced by validation.
- validate runs in CI for pull_request and main push events and fails the workflow on guard failures.

## Tests
- Local: `pwsh -File PS1/validate.ps1` from the repository root.
- CI: GitHub Actions validate workflow runs `PS1/validate.ps1` on Windows with pwsh.

## Risks
- Guards may need tightening in later phases; extension points should remain clear for future strictness.
- Non-ASCII content or missing indexes will block merges until corrected.
