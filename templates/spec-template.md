# [Feature Name] — Requirements Specification

<!-- Spec-Kit: requirements.md | SDD Phase 1: SPECIFY -->
<!-- See rule: rules/27-spec-driven-development.md -->

---

## Document Header

```
Feature:         [Feature/Service Name]
Spec ID:         SPEC-[NNN]
Version:         1.0
Status:          DRAFT | IN_REVIEW | APPROVED | AMENDED | SUPERSEDED
Author:          [Name]
Reviewers:       [Names]
Date:            [YYYY-MM-DD]
Related ADRs:    [Links]
Parent Feature:  [Link to parent initiative or epic]
```

## Change Log

| Version | Date | Author | Change Summary | Approved By |
|---------|------|--------|---------------|-------------|
| 1.0 | YYYY-MM-DD | | Initial draft | |

---

## 1. Overview

<!-- 3–5 sentences: business problem, target users, definition of success. -->
<!-- A decision-maker should understand the value from this section alone. -->

**Business Problem:**
[What pain or opportunity does this address?]

**Target Users / Personas:**
[Who uses this feature? Be specific.]

**Definition of Success:**
[How do we know this is done? Link to measurable KPIs.]

---

## 2. User Stories

<!-- Format: As a [type of user], I want [action], so that [benefit]. -->

| ID | User Story | Priority |
|----|-----------|:--------:|
| US-001 | As a [user], I want [action], so that [benefit]. | Must / Should / Could |
| US-002 | | |

---

## 3. Functional Requirements (EARS Notation)

<!-- Every requirement MUST use one of the five EARS patterns:
     - Ubiquitous:       The [system] shall [action].
     - Event-Driven:     When [trigger], the [system] shall [action].
     - State-Driven:     While [state], the [system] shall [action].
     - Unwanted:         If [condition], then the [system] shall [action].
     - Optional:         Where [feature enabled], the [system] shall [action].
     
     Rules:
     - One behavior per statement (no "and" chaining)
     - Name a specific component, not just "the system"
     - Include numeric targets where applicable
     - Mark PII fields explicitly
-->

| ID | EARS Pattern | Requirement | Priority | Source |
|----|:------------:|------------|:--------:|--------|
| FR-001 | Ubiquitous | The [ServiceName] shall [action with specifics]. | Must | US-001 |
| FR-002 | Event-Driven | When [trigger event], the [ServiceName] shall [action]. | Must | US-001 |
| FR-003 | Unwanted | If [error condition], then the [ServiceName] shall [recovery action]. | Must | US-002 |
| FR-004 | State-Driven | While [system state], the [ServiceName] shall [action]. | Should | US-002 |
| FR-005 | Optional | Where [feature flag is enabled], the [ServiceName] shall [action]. | Could | US-003 |

---

## 4. Non-Functional Requirements

<!-- Every NFR MUST have a numeric target — no vague adjectives ("fast", "reliable").  -->

| ID | Category | Requirement | Target | Measurement Method |
|----|----------|------------|:------:|--------------------|
| NFR-001 | Performance | [ServiceName] API response time | p95 < 500ms | Prometheus histogram |
| NFR-002 | Availability | [ServiceName] uptime | 99.9% / month | Uptime monitoring |
| NFR-003 | Throughput | Peak request rate | 1,000 req/sec | Load test |
| NFR-004 | Security | Authentication method | JWT (15-min expiry) | Security audit |
| NFR-005 | Data retention | Logs retained for | 90 days | Log rotation config |
| NFR-006 | Recovery | RTO for [ServiceName] | < 15 minutes | DR drill |
| NFR-007 | Recovery | RPO for [ServiceName] | < 5 minutes | DR drill |
| NFR-008 | Compliance | Data residency | [Region(s)] | Infra audit |

---

## 5. Acceptance Criteria

<!-- Derived directly from EARS requirements above.
     Each criterion MUST be independently testable.
     Format: Given [context], When [action], Then [expected result].
-->

### FR-001 Acceptance Criteria
- [ ] AC-001-1: Given [context], when [action], then [ServiceName] [verifiable outcome].
- [ ] AC-001-2: [Additional criterion for same requirement]

### FR-002 Acceptance Criteria
- [ ] AC-002-1: Given [context], when [trigger], then [ServiceName] [verifiable outcome within timeframe].

### FR-003 Acceptance Criteria
- [ ] AC-003-1: Given [error condition], when [trigger], then [ServiceName] returns HTTP [code] with body matching error schema.
- [ ] AC-003-2: Given [error condition], then [ServiceName] logs the event at WARN level with correlation ID.

---

## 6. Out of Scope

<!-- Explicitly list what this spec does NOT cover. Prevents scope creep. -->

| Item | Reason for Exclusion |
|------|---------------------|
| [Feature/Capability] | [Will be addressed in SPEC-XXX / Out of product scope / Future phase] |
| | |

---

## 7. Assumptions

<!-- What you are taking for granted. If wrong, this spec may be invalidated. -->

| ID | Assumption | Risk if Wrong |
|----|-----------|--------------|
| A-001 | [Assumption statement] | [What breaks if this is false] |
| A-002 | | |

---

## 8. Constraints

<!-- Hard limits that restrict the design space. -->

| ID | Constraint | Source |
|----|-----------|--------|
| C-001 | Must use existing PostgreSQL 14 database | Infrastructure decision |
| C-002 | Budget: =$500/month additional cloud cost | Finance approval |
| C-003 | Must comply with [Regulation] | Legal requirement |

---

## 9. Dependencies

| Dependency | Type | Owner | Risk |
|-----------|------|-------|------|
| [ServiceName] v2 API | External service | [Team] | High |
| [Platform capability] | Platform | [Platform Team] | Medium |

---

## 10. Open Questions

<!-- Blockers requiring human decision before spec can be approved. -->

| # | Question | Impact if Unresolved | Owner | Deadline |
|---|---------|---------------------|-------|---------|
| 1 | [Question] | [Blocks FR-XXX] | [Name] | [Date] |

---

## 11. Requirement Traceability Matrix (RTM)

<!-- Update as design and tasks are created. -->

| Req ID | Summary | Design Component | Task ID | Test ID | Status |
|--------|---------|------------------|---------|---------|:------:|
| FR-001 | | | | | ? |
| FR-002 | | | | | ? |
| NFR-001 | | | | | ? |

**Status legend:** ? Not Started | ?? In Progress | ? Done | ? Blocked

---

*Archpilot — Spec-Driven Development Template*
*See: rules/27-spec-driven-development.md*
