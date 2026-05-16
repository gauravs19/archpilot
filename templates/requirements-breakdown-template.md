# [Project Name] — Requirements Breakdown

<!-- Archpilot: requirements.md | Phase 1: PO AGENT -->
<!-- Governed by: rules/27-spec-driven-development.md | rules/50-agent-pipeline.md v4.0 -->
<!-- CONSTRAINT: 10-20 Epics | 50-150 User Stories | All ACs measurable | EARS notation -->

---

## Document Header

```
Project:     [Project Name]
Version:     1.0
Status:      DRAFT | IN_REVIEW | APPROVED
Author:      [Name — PO Agent or Human BA]
Date:        [YYYY-MM-DD]
Discovery:   discovery.md v[X]
```

## Change Log

| Version | Date | Author | Summary | Approved By |
|---------|------|--------|---------|-------------|
| 1.0 | | | Initial generation from discovery.md | |

---

## Requirements Statistics

| Metric | Count | Rule 50 Constraint |
|--------|------:|-------------------|
| Total Epics | 0 | 10 – 20 |
| Total User Stories | 0 | 50 – 150 |
| Stories per Epic (avg) | 0 | 5 – 10 |
| Must-priority stories | 0 | |
| Security-tagged stories | 0 | |
| NFR-tagged stories | 0 | |

---

## Epic Categories

| Category | Epic IDs | Story Count |
|----------|----------|:-----------:|
| FUNCTIONAL | EP-01 – EP-XX | |
| DATA & STORAGE | EP-XX – EP-XX | |
| SECURITY & COMPLIANCE | EP-XX – EP-XX | |
| INTEGRATION & APIs | EP-XX – EP-XX | |
| NON-FUNCTIONAL | EP-XX – EP-XX | |
| DEVOPS & PLATFORM | EP-XX – EP-XX | |
| TESTING & QUALITY | EP-XX – EP-XX | |
| MIGRATION & CUTOVER | EP-XX – EP-XX | |

---

<!--
═══════════════════════════════════════════════════════════
  SECTION A: FUNCTIONAL EPICS
  Core business capabilities — what the system must DO.
═══════════════════════════════════════════════════════════
-->

## EP-01: [Epic Title — Functional Domain 1]

> **Category:** FUNCTIONAL
> **Business Value:** [One sentence: what business outcome does this epic deliver?]
> **Discovery Ref:** [DIM-01, DIM-08] — link to discovery dimensions that drive this epic
> **Definition of Done:**
> - All stories accepted and tested in Staging.
> - NFR targets verified under load test.
> - Security review passed.
> - Runbook written for all new services.

### EP-01-S-01: [Story Title]

| Field | Value |
|-------|-------|
| **As a** | [persona] |
| **I want** | [specific action or capability] |
| **So that** | [measurable business outcome] |
| **Priority** | Must / Should / Could / Won't |
| **Story Points** | 1 / 2 / 3 / 5 / 8 / 13 |
| **NFR Tags** | [Performance] [Security] [Availability] [Cost] [Compliance] |
| **Discovery Ref** | DIM-[XX] |

**Acceptance Criteria (EARS notation):**
1. WHEN [trigger event], the system SHALL [specific measurable behaviour].
2. WHEN [error condition], the system SHALL return [specific error code] within [X ms].
3. The system SHALL [ubiquitous requirement — always true].
4. IF [precondition], the system SHALL NOT [unwanted behaviour].
5. WHERE [optional feature] is enabled, the system SHALL [additional behaviour].

**Edge Cases:**
- [Edge case 1 — what happens at boundary conditions]
- [Edge case 2 — what happens when dependency is unavailable]

---

### EP-01-S-02: [Story Title]

| Field | Value |
|-------|-------|
| **As a** | |
| **I want** | |
| **So that** | |
| **Priority** | |
| **Story Points** | |
| **NFR Tags** | |
| **Discovery Ref** | |

**Acceptance Criteria (EARS notation):**
1.
2.
3.

---

<!-- Repeat EP-01-S-NN pattern for all stories in this epic -->

---

## EP-02: [Epic Title — Functional Domain 2]

> **Category:** FUNCTIONAL
> **Business Value:**
> **Discovery Ref:**
> **Definition of Done:** [Same structure as EP-01 — customize per epic]

### EP-02-S-01: [Story Title]

| Field | Value |
|-------|-------|
| **As a** | |
| **I want** | |
| **So that** | |
| **Priority** | |
| **Story Points** | |
| **NFR Tags** | |
| **Discovery Ref** | |

**Acceptance Criteria (EARS notation):**
1.
2.
3.

---

<!--
═══════════════════════════════════════════════════════════
  SECTION B: DATA & STORAGE EPICS
  How data is created, stored, accessed, and governed.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [Data & Storage Epic Title]

> **Category:** DATA & STORAGE
> **Business Value:**
> **Discovery Ref:** [DIM-06 Data Residency, DIM-12 Data Privacy]
> **Definition of Done:**
> - Schema migrations tested in lower environments.
> - PII fields identified and masked in non-prod.
> - Data retention job deployed and verified.
> - Query performance validated at 10× expected data volume.

### EP-XX-S-01: [Story Title]

| Field | Value |
|-------|-------|
| **As a** | |
| **I want** | |
| **So that** | |
| **Priority** | |
| **Story Points** | |
| **NFR Tags** | [Data Integrity] [Performance] [Compliance] |
| **Discovery Ref** | |

**Acceptance Criteria (EARS notation):**
1. The system SHALL store [entity] with the following schema: [fields listed].
2. WHEN a record is created, the system SHALL generate a UUID primary key within 1 ms.
3. The system SHALL NOT store [PII field] in plaintext — it must be [encrypted/hashed/tokenised].
4. WHEN a query runs against the [table] with a filter on [column], p95 response SHALL be < [X ms] at [Y] rows.
5. WHEN the retention period of [X years] expires, the system SHALL anonymise [fields] within 24 hours.

---

<!--
═══════════════════════════════════════════════════════════
  SECTION C: SECURITY & COMPLIANCE EPICS
  Authentication, authorisation, audit, and regulatory.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [Security & Compliance Epic Title]

> **Category:** SECURITY & COMPLIANCE
> **Business Value:**
> **Discovery Ref:** [DIM-02 Regulatory, DIM-03 Security]
> **Definition of Done:**
> - Pen test passed with no Critical/High findings unresolved.
> - OWASP Top 10 checklist completed.
> - Compliance audit evidence package generated.
> - All secrets rotated and managed via secrets manager.

### EP-XX-S-01: Authentication & Session Management

| Field | Value |
|-------|-------|
| **As a** | registered user |
| **I want** | to authenticate using [OIDC / OAuth2 / MFA] |
| **So that** | only authorised identities access protected resources |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Security] [Compliance] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria (EARS notation):**
1. WHEN a user submits valid credentials, the system SHALL issue a JWT with expiry ≤ [15 min] within [500 ms].
2. WHEN a JWT expires, the system SHALL return HTTP 401 and the client SHALL use the refresh token.
3. WHEN [X] consecutive failed login attempts occur within [Y min], the system SHALL lock the account and notify via email.
4. The system SHALL NOT store passwords in plaintext — bcrypt (cost factor ≥ 12) is mandatory.
5. WHEN admin MFA is disabled, the system SHALL NOT permit access to administrative endpoints.

---

<!--
═══════════════════════════════════════════════════════════
  SECTION D: INTEGRATION & APIs EPICS
  External system contracts, event publishing, API design.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [Integration Epic Title]

> **Category:** INTEGRATION & APIs
> **Business Value:**
> **Discovery Ref:** [DIM-08 Connectivity & Integration]
> **Definition of Done:**
> - Contract tests passing against all external system mocks.
> - API versioning strategy enforced (v1 route live, v2 route deployed).
> - Rate limiting verified under load test.
> - OpenAPI spec published to developer portal.

### EP-XX-S-01: [Integration Story Title]

| Field | Value |
|-------|-------|
| **As a** | [consuming system / external partner] |
| **I want** | [access to specific API / event stream] |
| **So that** | [integration purpose] |
| **Priority** | |
| **Story Points** | |
| **NFR Tags** | [Integration] [Reliability] [Security] |
| **Discovery Ref** | DIM-08 |

**Acceptance Criteria (EARS notation):**
1. The system SHALL expose a [REST/gRPC] endpoint at [/v1/resource] following OpenAPI 3.1 specification.
2. WHEN the external system returns HTTP 5XX, the system SHALL retry with exponential backoff: [1s, 2s, 4s] max [3 attempts].
3. WHEN retry limit is exceeded, the system SHALL publish the failed event to the DLQ and emit a metric `integration.dlq.depth`.
4. The system SHALL enforce a rate limit of [X RPS] per API key, returning HTTP 429 with `Retry-After` header.
5. WHEN a breaking change is introduced, the system SHALL maintain the previous API version for ≥ [90 days].

---

<!--
═══════════════════════════════════════════════════════════
  SECTION E: NON-FUNCTIONAL EPICS
  Performance, availability, scalability, and cost NFRs.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [NFR Epic Title]

> **Category:** NON-FUNCTIONAL
> **Business Value:** System meets contractual SLAs and user experience targets.
> **Discovery Ref:** [DIM-01 Technical Physics, DIM-04 Resilience]
> **Definition of Done:**
> - Load test passing at 2× expected peak RPS.
> - SLA targets met for 30 consecutive days in production.
> - Auto-scaling verified: scale-out within [X min] of trigger.
> - Chaos engineering game day passed (inject: pod kill, DB failover, network partition).

### EP-XX-S-01: Performance Targets

| Field | Value |
|-------|-------|
| **As a** | product stakeholder |
| **I want** | the system to meet defined performance SLAs |
| **So that** | users have a consistent, acceptable experience |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Availability] |
| **Discovery Ref** | DIM-01, DIM-04 |

**Acceptance Criteria (EARS notation):**
1. The system SHALL serve [primary API endpoint] at p50 < [X ms], p95 < [Y ms], p99 < [Z ms] under [N RPS] nominal load.
2. WHEN traffic spikes to [2×] nominal, the system SHALL auto-scale within [X min] and maintain p95 < [Y ms].
3. The system SHALL maintain ≥ [99.9%] availability measured monthly, excluding scheduled maintenance windows.
4. WHEN a single AZ fails, the system SHALL recover and resume serving traffic within [5 min].
5. The system SHALL NOT exceed [$ X] cloud spend per [1,000] requests at nominal scale.

---

<!--
═══════════════════════════════════════════════════════════
  SECTION F: DEVOPS & PLATFORM EPICS
  CI/CD, IaC, containerisation, environment management.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [DevOps & Platform Epic Title]

> **Category:** DEVOPS & PLATFORM
> **Business Value:**
> **Discovery Ref:** [DIM-10 Lifecycle, DIM-09 Observability]
> **Definition of Done:**
> - Pipeline deploys to Production without manual steps.
> - IaC applied in all environments (dev / staging / prod).
> - All secrets sourced from secrets manager (no hardcoded values).
> - Rollback verified: deploy and rollback cycle < [15 min].

### EP-XX-S-01: CI/CD Pipeline

| Field | Value |
|-------|-------|
| **As a** | developer |
| **I want** | automated CI/CD from commit to production |
| **So that** | delivery cycle is < [X hours] with quality gates enforced |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [DevOps] [Quality] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria (EARS notation):**
1. WHEN code is pushed to `main`, the pipeline SHALL run: lint → unit tests → build → integration tests → SAST → deploy-staging.
2. WHEN any pipeline stage fails, the system SHALL block the merge and notify the author via [Slack / email].
3. WHEN all quality gates pass, the system SHALL deploy to Production via [blue-green / rolling] strategy with zero downtime.
4. The pipeline SHALL complete lint → staging-deploy within [15 min] (p95 measured over 30 days).
5. WHEN a production deploy fails health checks, the system SHALL automatically rollback to the previous version within [5 min].

---

<!--
═══════════════════════════════════════════════════════════
  SECTION G: TESTING & QUALITY EPICS
  Test strategy, coverage targets, and quality gates.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [Testing & Quality Epic Title]

> **Category:** TESTING & QUALITY
> **Business Value:**
> **Discovery Ref:** [DIM-10 Lifecycle]
> **Definition of Done:**
> - Coverage targets met and enforced in CI.
> - Contract tests running in CI against provider stubs.
> - Performance test suite baseline committed and running weekly.
> - Chaos game day playbook executed once per quarter.

### EP-XX-S-01: Test Coverage Standards

| Field | Value |
|-------|-------|
| **As a** | engineering lead |
| **I want** | enforced test coverage thresholds |
| **So that** | regressions are caught before they reach production |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Quality] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria (EARS notation):**
1. The system SHALL enforce minimum unit test coverage of [80%] branch coverage, failing the CI pipeline if below threshold.
2. The system SHALL have integration tests for all [external API / DB / queue] integrations.
3. WHEN a new API endpoint is added, the system SHALL require a corresponding contract test before merge is permitted.
4. The system SHALL run a performance baseline test weekly, alerting if p95 degrades by >[10%] from the prior week.
5. WHERE chaos engineering is enabled, the system SHALL pass a quarterly game day: pod kill, AZ loss, DB failover.

---

<!--
═══════════════════════════════════════════════════════════
  SECTION H: MIGRATION & CUTOVER EPICS
  Data migration, shadow mode, traffic cut, rollback.
═══════════════════════════════════════════════════════════
-->

## EP-XX: [Migration & Cutover Epic Title]

> **Category:** MIGRATION & CUTOVER
> **Business Value:**
> **Discovery Ref:** [DIM-10 Lifecycle, DIM-04 Resilience]
> **Definition of Done:**
> - Data migration dry-run completed with zero data loss verified.
> - Rollback plan tested and documented.
> - Cutover runbook approved by operations.
> - Shadow mode verified for ≥ [X days] before full cutover.

### EP-XX-S-01: Data Migration

| Field | Value |
|-------|-------|
| **As a** | operations engineer |
| **I want** | data migrated from [legacy system] to [new system] with zero loss |
| **So that** | the new system can serve live traffic without data gaps |
| **Priority** | Must |
| **Story Points** | 13 |
| **NFR Tags** | [Data Integrity] [Reliability] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria (EARS notation):**
1. WHEN migration is run against production data, the system SHALL verify row counts match within 100% before cutover gate.
2. WHEN a migration batch fails, the system SHALL log the failure, stop the migration, and notify on-call within [5 min].
3. The system SHALL complete migration of [N million] records within [X hours] at [Y records/sec] throughput.
4. WHEN rollback is triggered, the system SHALL restore service from legacy within [RTO: X min].
5. The system SHALL run in shadow mode for ≥ [X days], comparing outputs of old and new systems, before full cutover.

---

## Requirements Traceability Matrix (RTM)

| Story ID | Business Goal | Discovery Dim | HLD Component | LLD Service | Test Coverage |
|----------|---------------|:-------------:|---------------|-------------|:-------------:|
| EP-01-S-01 | | DIM-[X] | | | Unit + Integration |
| EP-01-S-02 | | | | | |

---

## Glossary

| Term | Definition |
|------|-----------|
| EARS | Easy Approach to Requirements Syntax — IEEE standard for unambiguous requirements |
| MoSCoW | Must / Should / Could / Won't — priority classification |
| NFR | Non-Functional Requirement — quality attributes (performance, security, etc.) |
| AC | Acceptance Criterion — measurable condition that defines "done" |
| DIM-XX | Discovery Dimension reference from discovery.md |

---

*Archpilot — Requirements Breakdown Template v4.0*
*Governed by rules/27-spec-driven-development.md | rules/50-agent-pipeline.md*
*Created by Gaurav Sharma*
