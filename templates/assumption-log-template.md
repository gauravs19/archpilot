# [Project Name] - Architectural Assumption Log

<!-- Archpilot: assumption-log.md | Phase 0/1 Tracker -->
<!-- Governed by: rules/36-discovery-ambiguity.md & rules/01-solution-design.md -->

> **Purpose:** To systematically track, validate, and mitigate architectural assumptions. An invalidated assumption late in the project lifecycle causes catastrophic design failure.

---

## Assumption Registry

| ID | Category | The Assumption | Risk if False | Mitigation / Validation Plan | Status | Owner |
|----|----------|----------------|---------------|------------------------------|:------:|-------|
| A-001 | `Traffic` | Peak concurrent users will not exceed 50,000 in Year 1. | System will buckle under memory exhaustion; requires completely different DB topology. | Load test current beta users to establish baseline. Get PM sign-off. | `OPEN` | Arch |
| A-002 | `Integration`| The legacy Mainframe API supports 100 requests per second. | We will DDoS the mainframe, causing company-wide outages. | Request rate-limit documentation from Mainframe team. | `VALIDATED` | Tech Lead |
| A-003 | `Data` | Customer PII does not need to be physically stored in the EU. | Massive GDPR fines and legal block on launch. | Consult with internal Legal & Compliance team. | `INVALIDATED`| Arch |
| A-004 | `Client` | The client has an internal DevOps team to manage K8s. | Client cannot run our software; we must switch to managed PaaS. | Explicitly ask client CTO during next sync. | `OPEN` | Presales |

---

## Status Legend
- `OPEN`: The assumption has been stated but not verified. Proceed with caution.
- `VALIDATED`: Evidence confirms the assumption is true. Safe to design around.
- `INVALIDATED`: The assumption is false. Immediate architectural pivot required.

## Category Tags
- `Traffic / Scale`
- `Integration / API`
- `Data / Storage`
- `Security / Compliance`
- `Client / Organization`
- `Budget / FinOps`

---
*Archpilot - Assumption Log Template*
