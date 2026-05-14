# [Feature Name] — Design Specification

<!-- Spec-Kit: design.md | SDD Phase 2: PLAN -->
<!-- See rule: rules/27-spec-driven-development.md -->
<!-- Input: requirements spec (spec-template.md) -->
<!-- Output: tasks.md (task-list-template.md) -->

---

## Document Header

```
Feature:         [Feature/Service Name]
Design ID:       DESIGN-[NNN]
Spec Ref:        SPEC-[NNN] v[X.Y]
Version:         1.0
Status:          DRAFT | IN_REVIEW | APPROVED
Author:          [Architect/Tech Lead Name]
Reviewers:       [Names]
Date:            [YYYY-MM-DD]
Related ADRs:    [Links]
```

---

## 1. Architecture Overview

### 1.1 Approach Summary

<!-- 3–5 sentences: what architectural approach was chosen and why. -->
<!-- Reference ADRs for significant decisions. -->

**Selected Approach:** [Brief description]
**Key Rationale:** [Why this approach over alternatives — reference ADR-XXX]

### 1.2 Architecture Diagram

```
[Mermaid or ASCII diagram showing components, data flows, and integration points]

Example:
graph LR
    Client --> APIGateway
    APIGateway --> |JWT auth| FeatureService
    FeatureService --> |read/write| Database[(PostgreSQL)]
    FeatureService --> |publish| EventBus[Kafka]
    EventBus --> ConsumerService
```

### 1.3 Key Architecture Decisions

| Decision | Choice | ADR | Rationale Summary |
|---------|--------|:---:|------------------|
| Primary data store | PostgreSQL 14 | ADR-012 | Existing infra; ACID needed |
| Communication style | Async (Kafka) | ADR-015 | Decoupled; load leveling |
| Auth mechanism | JWT + OAuth2 | ADR-005 | Org standard |

---

## 2. Component Design

<!-- For every component: name, responsibility (one sentence), inputs, outputs, dependencies, technology. -->

### 2.1 [ComponentName]

| Attribute | Detail |
|-----------|--------|
| **Responsibility** | [Single sentence — what this component does] |
| **Type** | Service / Module / Library / Lambda / Worker |
| **Technology** | [e.g., Node.js 20, Spring Boot 3.2, Python 3.12] |
| **Inputs** | [What data it receives and from where] |
| **Outputs** | [What data it produces and to where] |
| **Key Dependencies** | [Services, databases, external APIs] |
| **Scales with** | [Request rate / data volume / N/A] |

**Public Interface:**
```
[Key methods / APIs exposed by this component — name, input, output, description]
```

### 2.2 [ComponentName]

<!-- Repeat for each component -->

---

## 3. Data Models

<!-- For every entity: name, description, fields, relationships, constraints. -->

### 3.1 [EntityName]

**Purpose:** [What this entity represents]
**Storage:** [Database name, table/collection name]
**Owner:** [ServiceName]

| Field | Type | Nullable | Default | Constraints | PII | Description |
|-------|------|:-------:|---------|-------------|:---:|-------------|
| id | UUID | No | gen_random_uuid() | PK | No | Unique identifier |
| created_at | TIMESTAMPTZ | No | NOW() | | No | Record creation time |
| updated_at | TIMESTAMPTZ | No | NOW() | | No | Last update time |
| [field] | [type] | Yes/No | | | Yes/No | [Description] |

**Indexes:**
```sql
CREATE INDEX idx_[entity]_[field] ON [table]([field]);  -- [Reason for index]
```

**Relationships:**
- `[EntityName]` has many `[OtherEntity]` (via `[field]`)
- `[EntityName]` belongs to `[OtherEntity]` (via `[foreign_key]`)

### 3.2 Estimated Data Volume

| Metric | Launch | Year 1 | Year 3 |
|--------|:------:|:------:|:------:|
| Rows / events per day | | | |
| Total table size | | | |
| Growth rate | | | |

**Partitioning strategy:** [None / By date / By tenant / By range — triggered when >10M rows]

---

## 4. API / Interface Design

<!-- For every endpoint or event, define the contract. -->
<!-- For REST APIs, prefer OpenAPI snippet. For events, define schema. -->

### 4.1 REST Endpoints

#### `POST /v1/[resource]`

| Field | Detail |
|-------|--------|
| **Purpose** | [What this endpoint does] |
| **Auth** | JWT Bearer token; scope: `[scope:action]` |
| **Rate Limit** | 100 req/min per user |
| **Idempotent** | Yes (via `Idempotency-Key` header) / No |

**Request:**
```json
{
  "field1": "string",
  "field2": 123,
  "optionalField": "string"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "field1": "string",
  "createdAt": "ISO-8601"
}
```

**Error Responses:**
| Status | Code | Condition |
|:------:|------|-----------|
| 400 | `VALIDATION_ERROR` | Missing or invalid fields |
| 401 | `UNAUTHORIZED` | Invalid/expired JWT |
| 409 | `CONFLICT` | Duplicate idempotency key |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

#### `GET /v1/[resource]/{id}`

<!-- Repeat for each endpoint -->

### 4.2 Event Contracts

#### Event: `[domain].[entity].[action]`

| Field | Detail |
|-------|--------|
| **Topic** | `[kafka-topic-name]` |
| **Producer** | [ServiceName] |
| **Consumers** | [ServiceName1], [ServiceName2] |
| **Delivery** | At-least-once |
| **Ordering** | By `[partition key field]` |

**Schema:**
```json
{
  "eventId": "uuid",
  "eventType": "[domain].[entity].[action]",
  "timestamp": "ISO-8601",
  "version": "1.0",
  "payload": {
    "field1": "value",
    "field2": 123
  }
}
```

**Retry policy:** 3 retries, exponential backoff (1s, 2s, 4s) ? DLQ: `[topic-name].dlq`

---

## 5. State Machines

<!-- For any stateful entity, define the state machine. -->

### 5.1 [Entity] State Machine

```
States: PENDING ? PROCESSING ? COMPLETED
                            ? FAILED ? RETRYING ? COMPLETED
                                               ? DEAD_LETTERED
```

| State | Description | Valid Next States | Trigger |
|-------|-------------|:----------------:|---------|
| PENDING | Created, not yet processed | PROCESSING | Picked up by worker |
| PROCESSING | Being processed | COMPLETED, FAILED | Processing result |
| COMPLETED | Successfully processed | — (terminal) | — |
| FAILED | Processing failed; eligible for retry | RETRYING | Retry timer |
| RETRYING | Re-attempting after failure | COMPLETED, DEAD_LETTERED | Processing result |
| DEAD_LETTERED | Max retries exceeded | — (terminal) | Retry exhausted |

**Rules:**
- State transitions MUST be atomic (optimistic locking via `version` field)
- Invalid state transitions MUST throw `InvalidStateTransitionException`

---

## 6. Error Handling Strategy

| Error Category | Handling | Log Level | User Response |
|---------------|---------|:---------:|--------------|
| Validation error | Reject at boundary; return 400 with details | WARN | Structured error body |
| Auth failure | Return 401; do not reveal existence of resource | WARN | Generic auth error |
| Dependency unavailable | Circuit breaker ? fallback; return 503 | ERROR | Retry-After header |
| Database error | Retry 3× with backoff ? return 500 with correlation ID | ERROR | Generic error + correlation ID |
| Unknown exception | Catch-all ? return 500; full stack in logs | ERROR | Generic error + correlation ID |

**Standard error response:**
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "correlationId": "req-uuid",
    "timestamp": "ISO-8601",
    "details": []
  }
}
```

---

## 7. Security Design

| Concern | Design Decision |
|---------|----------------|
| **Authentication** | [JWT / mTLS / API key — with specifics] |
| **Authorization** | [RBAC roles / ABAC policies — with specifics] |
| **Input validation** | [Schema validation library; validation rules] |
| **PII handling** | [Which fields; encryption/pseudonymization method] |
| **Secrets** | [AWS Secrets Manager / Vault — injection method] |
| **Rate limiting** | [Limits per user/IP; enforcement point: gateway vs service] |
| **Audit logging** | [What actions logged; retention period; PII masking in logs] |

**Threat Model (STRIDE summary):**

| Threat | Mitigation |
|--------|-----------|
| Spoofing | JWT validation on every request; short expiry |
| Tampering | Request signing for sensitive mutations |
| Repudiation | Immutable audit log for all state changes |
| Information Disclosure | PII pseudonymized; no PII in logs |
| Denial of Service | Rate limiting + WAF |
| Elevation of Privilege | Scoped OAuth2 tokens; deny-by-default RBAC |

---

## 8. NFR Design

<!-- Map each NFR from spec to a technical design decision. -->

| NFR ID | Target | Technical Solution |
|--------|:------:|--------------------|
| NFR-001 (p95 < 500ms) | Latency | Redis cache for hot reads; async processing for writes |
| NFR-002 (99.9% uptime) | Availability | Multi-AZ deployment; circuit breaker on all dependencies |
| NFR-003 (1,000 req/sec) | Throughput | Horizontal pod autoscaling; connection pooling (max 50) |

---

## 9. Dependency Map

| Dependency | Type | Version | Owner | SLA | Fallback |
|-----------|------|:-------:|-------|:---:|---------|
| [ServiceName] | Internal API | v2 | [Team] | 99.9% | Cached response |
| [Database] | Data store | PostgreSQL 14 | Platform | 99.95% | Read replica |
| [External API] | External | v3 | Vendor | 99.5% | Circuit breaker ? error |

---

## 10. Design Quality Checklist

- [ ] Every FR from requirements.md addressed by a component or interface
- [ ] No constitution.md constraints violated
- [ ] All external dependencies listed with fallback strategies
- [ ] Data models have types, constraints, PII flags, and index strategy
- [ ] Security design addresses all 6 STRIDE threats
- [ ] Each NFR has a corresponding technical solution
- [ ] ADRs created for all significant decisions
- [ ] Estimated data volumes documented with growth projections
- [ ] State machines defined for all stateful entities
- [ ] Error handling covers all failure categories

---

*Archpilot — Spec-Driven Development Template*
*See: rules/27-spec-driven-development.md*
