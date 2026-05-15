# Rule 37: The SDD Triage Matrix (Fast-Track)

**Title:** Spec-Driven Development Triage and Fast-Tracking
**Category:** Governance & Process
**Status:** Active

## Context
Spec-Driven Development (SDD) (Rule 27) and Phase 0 Discovery (Rule 36) are heavy processes. Forcing a developer to write a 14-section High-Level Design for a minor bug fix or a simple UI string change causes process fatigue and revolt. Not all features carry the same architectural risk.

## The Rule

Before beginning any engineering task, the architect or tech lead MUST triage the request using the matrix below. 

### Tier 1: The Fast-Track (Low Risk)
- **Criteria:** Changing copy, updating a CSS class, adding a non-indexed column to a DB, fixing a minor null-pointer exception.
- **Blast Radius:** Single component. Zero impact on data integrity, security, or NFRs.
- **Process:** Bypassed. **DO NOT** write a `discovery.md` or `design.md`. Go straight to code/PR.

### Tier 2: The Lightweight Spec (Medium Risk)
- **Criteria:** Adding a standard CRUD endpoint to an existing API, adding a new UI page using existing components, adding a cache to an existing DB query.
- **Blast Radius:** Localized to a single bounded context. Minor impact on TPS or Memory.
- **Process:** 
  - Bypass Phase 0 Discovery.
  - Write a simplified `requirements.md` (no RTM required).
  - Write a lightweight `design.md` (skip sequence diagrams, just define the API/Schema changes).
  - Generate `tasks.md`.

### Tier 3: The Full Archpilot SDD (High Risk)
- **Criteria:** Creating a new microservice, altering distributed transaction logic (Sagas), changing DB engines, integrating a new 3rd-party vendor, processing PII/PCI.
- **Blast Radius:** Cross-system, multi-team dependencies. High risk to security, data integrity, or Cloud FinOps.
- **Process:** 
  - Mandatory Phase 0 `discovery.md` and `assumption-log.md`.
  - Mandatory Phase 1 `requirements.md` (with RTM).
  - Mandatory Phase 2 `design.md` (with Mermaid Archetypes).
  - Mandatory Phase 3 `tasks.md` and `constitution.md`.
  - Must be validated by `archpilot_cli.py lint` in CI/CD.

## Guardrails
- **Default to Tier 3:** If there is a disagreement about the tier, always default to the higher tier.
- **Security Trumps All:** Any change touching Authentication, Authorization, or PII automatically escalates the task to **Tier 3**, regardless of how "small" the code change is.
