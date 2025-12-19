# Roadmap Overview

The roadmap traces sealed Phase 0 guardrails, locked Phase 1 documentation, and the additive Phase 2 architecture rollout. Each phase diagram below mirrors the authoritative step files and is also stored in its respective directory for reuse.

## Table of Contents
- [Phase 0](#phase-0)
- [Phase 1](#phase-1)
- [Phase 2](#phase-2)

## Phase 0

```mermaid
graph TD
  P0("Phase 0: Hardening (Closed)")
  P0 --> S00("Step 00: Bootstrap (Done)")
  P0 --> S01("Step 01: Harden Bootstrap (Done)")
```

See also: [docs/roadmap/phase0/diagram.md](phase0/diagram.md).

## Phase 1

```mermaid
graph TD
  subgraph Done
    S100["Step 00: Initiation (Done)"]
    S101["Step 01: Foundational domain (Done)"]
    S102["Step 02: Architecture guardrails (Done)"]
    S103["Step 03: Ownership, RBAC, audit (Done)"]
    S105["Step 05: UX visual language (Done)"]
    S106["Step 06: UI component contracts (Done)"]
    S107["Step 07: UI page contracts (Done)"]
    S115["Step 15: UI component contracts (Done)"]
    S116["Step 16: Page contracts (Done)"]
  end

  subgraph Active
    S104["Step 04: API and integration (In progress)"]
    S111["Step 11: Cross-domain read models (Active)"]
  end

  subgraph Proposed
    S108["Step 08: Roadmap and execution sheets (Proposed)"]
    S109["Step 09: Inventory and equipment (Proposed)"]
    S110["Step 10: Finance and accounting (Proposed)"]
    S112["Step 12: Locations and maps (Proposed)"]
    S113["Step 13: Notifications and messaging (Proposed)"]
    S117["Step 17: Domain object contracts (Proposed)"]
    S118["Step 18: Planning rules (Proposed)"]
    S119["Step 19: State machines (Proposed)"]
    S120["Step 20: Permissions matrix (Proposed)"]
  end

  subgraph Locked
    S114["Step 14: Lock charter (Locked)"]
  end

  S100 --> S101 --> S102 --> S103 --> S104
  S104 --> S105 --> S106 --> S107 --> S114
  S114 --> S115 --> S116 --> S117
  S116 --> S118 --> S119 --> S120
  S107 -.-> S108
  S107 -.-> S109
  S107 -.-> S110
  S111 --> S114
  S104 --> S111
```

See also: [docs/roadmap/phase1/diagram.md](phase1/diagram.md).

## Phase 2

```mermaid
graph TD
  P2("Phase 2: Architecture and Delivery")
  P2 --> S201["Step 01: High level architecture (Starting)"]
  P2 --> S202["Step 02: Low level architecture (Starting)"]
  P2 --> S203["Step 03: Persistence model (Starting)"]
  P2 --> S204["Step 04: API architecture (Starting)"]
  P2 --> S205["Step 05: Async and jobs (Starting)"]
  P2 --> S206["Step 06: Security and trust (Starting)"]
  P2 --> S207["Step 07: Frontend architecture (Starting)"]
  P2 --> S208["Step 08: Deployment and environments (Starting)"]
  P2 --> S209["Step 09: Observability and operations (Starting)"]
  P2 --> S210["Step 10: Implementation bootstrap (Starting)"]
  P2 --> S211["Step 11: First vertical slice (In progress)"]
  P2 --> S212["Step 12: Execution governance (Starting)"]
  P2 --> S213["Step 13: Testing strategy and harness (In progress)"]
```

See also: [docs/roadmap/phase2/diagram.md](phase2/diagram.md).
