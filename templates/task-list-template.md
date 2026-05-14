# [Feature Name] — Implementation Task List

<!-- Spec-Kit: tasks.md | SDD Phase 3: TASK -->
<!-- See rule: rules/27-spec-driven-development.md -->
<!-- Input: design-spec-template.md -->
<!-- Output: Implementation (Phase 4) -->

---

## Header

```
Feature:         [Feature/Service Name]
Task List ID:    TASKS-[NNN]
Design Ref:      DESIGN-[NNN] v[X.Y]
Spec Ref:        SPEC-[NNN] v[X.Y]
Version:         1.0
Status:          DRAFT | APPROVED | IN_PROGRESS | DONE
Author:          [Tech Lead Name]
Date:            [YYYY-MM-DD]
```

---

## Task Overview

| Metric | Value |
|--------|-------|
| Total tasks | [N] |
| Estimated effort | [N] hours |
| Target sprint | [Sprint N] |
| Assigned team | [Team name] |

---

## Dependency Graph

```
T-01 ? T-02 ? T-04 ? T-07
  ?         ? T-05 ? T-08
T-03          T-06
```

---

## Tasks

---

### Task T-01: [Setup / Foundation Task]

**Status:** ? Not Started
**Effort:** [1–4 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** None (starting point)
**Blocks:** T-02, T-03

#### Description
[One paragraph: what needs to be done, why it is needed, and what approach to take. Reference specific sections of design.md.]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Create | `src/[module]/[file].ts` | [What this file does] |
| Modify | `src/config/[file].ts` | [What changes] |
| Create | `test/unit/[file].test.ts` | Unit tests for above |

#### Acceptance Criteria
- [ ] **AC-T01-1** (FR-001): [Specific, verifiable criterion derived from EARS requirement]
- [ ] **AC-T01-2** (FR-001): [Another specific, independently testable criterion]
- [ ] **AC-T01-3** (NFR-001): [Performance criterion — e.g., "Returns within 100ms in unit test with mock"]
- [ ] **AC-T01-4** (General): All new code passes linting and type-check without errors

#### Test Requirements
- **Unit test file:** `test/unit/[file].test.ts`
  - Test: [happy path description]
  - Test: [error path description]
  - Test: [edge case description]
- **Coverage:** =80% line coverage on new code

#### Constitution Checks
- [ ] No hardcoded config values (must use environment variables)
- [ ] No shared mutable state
- [ ] Follows naming convention: [specific convention from constitution]
- [ ] Structured JSON logging with correlation ID

#### Notes / Clarifications
> [Any implementation notes, design decisions specific to this task, or questions for the team]

---

### Task T-02: [Data Layer Task]

**Status:** ? Not Started
**Effort:** [2–4 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-01
**Blocks:** T-04, T-05

#### Description
[Implementation description referencing design.md §3 Data Models]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Create | `src/repositories/[entity].repository.ts` | Data access layer |
| Create | `migrations/[timestamp]_create_[table].sql` | Database migration |
| Create | `test/unit/repositories/[entity].repository.test.ts` | Repository unit tests |

#### Acceptance Criteria
- [ ] **AC-T02-1** (FR-002): Migration creates table with schema matching design.md §3.1
- [ ] **AC-T02-2** (FR-002): All columns have correct types, nullability, and constraints
- [ ] **AC-T02-3** (FR-002): Indexes defined in design are created by migration
- [ ] **AC-T02-4** (NFR-001): Repository queries execute in <50ms on test dataset of 10,000 rows
- [ ] **AC-T02-5** (General): Migration is backward compatible (old code + new schema works)

#### Test Requirements
- **Unit test file:** `test/unit/repositories/[entity].repository.test.ts`
  - Test: create — happy path
  - Test: create — duplicate key violation
  - Test: findById — found
  - Test: findById — not found (returns null, not throws)
  - Test: update — optimistic lock conflict
- **Migration test:** Verify up and down migrations both succeed

#### Constitution Checks
- [ ] Parameterized queries only (no string concatenation)
- [ ] PII fields use column-level encryption per constitution
- [ ] Audit columns (created_at, updated_at, created_by) present

---

### Task T-03: [Service Layer Task]

**Status:** ? Not Started
**Effort:** [2–4 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-01
**Blocks:** T-04

#### Description
[Implementation description referencing design.md §2 Component Design]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Create | `src/services/[feature].service.ts` | Business logic layer |
| Create | `test/unit/services/[feature].service.test.ts` | Service unit tests |

#### Acceptance Criteria
- [ ] **AC-T03-1** (FR-001): Service validates all input fields per design §6 Error Handling
- [ ] **AC-T03-2** (FR-002): Service calls repository with correct parameters on happy path
- [ ] **AC-T03-3** (FR-003): If repository throws DatabaseException, service retries 3× with backoff
- [ ] **AC-T03-4** (FR-004): Service publishes [EventName] event after successful operation
- [ ] **AC-T03-5** (General): No business logic in repository; no data access in service caller

#### Test Requirements
- **Unit test file:** `test/unit/services/[feature].service.test.ts`
  - All repository calls mocked
  - Test: happy path (verify event published)
  - Test: validation error (verify 400-equivalent thrown)
  - Test: repository failure (verify retry behavior)
  - Test: retry exhausted (verify 503-equivalent thrown with correlation ID)

---

### Task T-04: [API Layer Task]

**Status:** ? Not Started
**Effort:** [2–3 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-02, T-03
**Blocks:** T-06

#### Description
[Implementation of REST endpoints per design.md §4 API Design]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Create | `src/controllers/[feature].controller.ts` | Request/response handling |
| Modify | `src/routes/index.ts` | Register new routes |
| Create | `openapi/[feature]-spec.yaml` | OpenAPI 3.1 contract |
| Create | `test/integration/[feature].api.test.ts` | Integration tests |

#### Acceptance Criteria
- [ ] **AC-T04-1** (FR-001): `POST /v1/[resource]` returns 201 with body matching design schema
- [ ] **AC-T04-2** (FR-001): `GET /v1/[resource]/{id}` returns 200 or 404 per design
- [ ] **AC-T04-3** (FR-003): Invalid request body returns 400 with structured error body (no stack trace)
- [ ] **AC-T04-4** (NFR-001): Integration test p95 response time <500ms with in-memory mock DB
- [ ] **AC-T04-5** (General): OpenAPI spec validates with Spectral lint (zero errors)

#### Test Requirements
- **Integration test:** Real HTTP calls with mocked repository
- **Contract test:** Responses validated against OpenAPI spec schemas

---

### Task T-05: [Event / Async Task]

**Status:** ? Not Started
**Effort:** [2–4 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-02
**Blocks:** T-07

#### Description
[Event producer/consumer implementation per design.md §4.2 Event Contracts]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Create | `src/events/producers/[event].producer.ts` | Kafka producer |
| Create | `src/events/consumers/[event].consumer.ts` | Kafka consumer |
| Create | `test/unit/events/[event].producer.test.ts` | Producer tests |

#### Acceptance Criteria
- [ ] **AC-T05-1** (FR-004): Events published match schema defined in design.md §4.2
- [ ] **AC-T05-2** (FR-005): Consumer is idempotent (processing same event twice = same result)
- [ ] **AC-T05-3** (FR-006): Failed messages routed to DLQ after 3 retries
- [ ] **AC-T05-4** (General): Schema validated against schema registry on publish

---

### Task T-06: [Security & Auth Task]

**Status:** ? Not Started
**Effort:** [1–2 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-04
**Blocks:** T-07

#### Description
[Security controls per design.md §7 Security Design]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Modify | `src/middleware/auth.middleware.ts` | Add new scopes for this feature |
| Modify | `src/middleware/ratelimit.middleware.ts` | Apply rate limits per design |
| Create | `test/security/[feature].security.test.ts` | Security-focused tests |

#### Acceptance Criteria
- [ ] **AC-T06-1** (NFR-004): Unauthenticated requests return 401 (not 403 or 404)
- [ ] **AC-T06-2** (NFR-004): Requests with insufficient scope return 403
- [ ] **AC-T06-3** (NFR-003): Requests beyond rate limit return 429 with Retry-After header
- [ ] **AC-T06-4** (General): PII fields not present in any log output (verified by log scan in test)

---

### Task T-07: [Observability Task]

**Status:** ? Not Started
**Effort:** [1–2 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-03, T-05, T-06
**Blocks:** T-08 (final integration)

#### Description
[Observability instrumentation per design.md §8 NFR Design]

#### Files to Create / Modify
| Action | File Path | Purpose |
|--------|-----------|---------|
| Modify | `src/services/[feature].service.ts` | Add structured logging |
| Create | `src/metrics/[feature].metrics.ts` | Prometheus metrics |
| Modify | `infra/dashboards/[service]-dashboard.json` | Update Grafana dashboard |

#### Acceptance Criteria
- [ ] **AC-T07-1** (NFR-002): Every request log entry includes: requestId, userId, action, duration, outcome
- [ ] **AC-T07-2** (NFR-002): Prometheus metrics exposed: request_count, latency_histogram, error_rate
- [ ] **AC-T07-3** (NFR-002): Distributed trace ID propagated in all outbound calls
- [ ] **AC-T07-4** (General): No PII in any log line (verified by log format review)

---

### Task T-08: [Final Integration & Smoke Test]

**Status:** ? Not Started
**Effort:** [1–2 hours]
**Assignee:** [Name / Unassigned]
**Depends on:** T-07 (all previous tasks)
**Blocks:** Nothing (last task)

#### Description
End-to-end validation of the complete feature in staging environment.

#### Acceptance Criteria
- [ ] **AC-T08-1**: End-to-end happy path works in staging (from API call to event consumed)
- [ ] **AC-T08-2**: RTM 100% complete — every FR and NFR has a passing test
- [ ] **AC-T08-3**: Performance test shows p95 < target under 80% of peak load
- [ ] **AC-T08-4**: No Critical or High findings in security scan
- [ ] **AC-T08-5**: Grafana dashboard shows healthy metrics in staging

---

## Task Summary

| ID | Title | Status | Effort | Assignee | Blocks |
|----|-------|:------:|:------:|----------|--------|
| T-01 | Setup / Foundation | ? | 2h | | T-02, T-03 |
| T-02 | Data Layer | ? | 3h | | T-04, T-05 |
| T-03 | Service Layer | ? | 3h | | T-04 |
| T-04 | API Layer | ? | 2h | | T-06 |
| T-05 | Events / Async | ? | 3h | | T-07 |
| T-06 | Security & Auth | ? | 2h | | T-07 |
| T-07 | Observability | ? | 2h | | T-08 |
| T-08 | Integration Smoke | ? | 2h | | — |

**Total Estimated Effort:** [N] hours

**Status legend:** ? Not Started | ?? In Progress | ? Done | ? Blocked

---

*Archpilot — Spec-Driven Development Template*
*See: rules/27-spec-driven-development.md*
