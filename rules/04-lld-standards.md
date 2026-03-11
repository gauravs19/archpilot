# Low-Level Design (LLD) Standards

> **Purpose:** This rule file defines the standards, structure, and level of detail required
> when creating a Low-Level Design document. When used as LLM context, it ensures every
> generated LLD is production-grade, implementation-ready, and enterprise-compliant.

---

## How to Use This File

- Feed this to any LLM alongside `templates/lld-template.md`
- Say: *"Using these LLD standards, create an LLD for [your system/feature]"*
- The LLM will produce a comprehensive, structured LLD following these rules.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [00 — Architecture Principles](./00-architecture-principles.md) | Foundational principles applied at component level |
| [03 — HLD Standards](./03-hld-standards.md) | Parent HLD that this LLD implements |
| [05 — API Design](./05-api-design.md) | Detailed API standards for §3.4.4 |
| [06 — Data Architecture](./06-data-architecture.md) | Database modeling standards for §3.4.5 |
| [12 — Observability](./12-observability-standards.md) | Observability details for §3.8 |
| [templates/lld-template.md](../templates/lld-template.md) | Ready-to-fill LLD template |

---

## 1. When to Write an LLD

| Situation | LLD Required? |
|-----------|:------------:|
| New service or microservice | ✅ Always |
| Major feature with 3+ components | ✅ Always |
| Database schema changes (new tables/entities) | ✅ Always |
| API contract changes (new endpoints, breaking changes) | ✅ Always |
| Infrastructure changes (new clusters, networking) | ⚠️ If complex |
| Bug fix or minor enhancement | ❌ No |
| Config change | ❌ No |

**Rule:** If the change touches more than one service, it MUST have an LLD.
**Rule:** If the change introduces a new data store, it MUST have an LLD.

---

## 2. LLD vs HLD — The Distinction

| Aspect | HLD | LLD |
|--------|-----|-----|
| **Audience** | Stakeholders, Architects, PMs | Developers, Tech Leads, Reviewers |
| **Abstraction** | Logical components, data flows | Classes, methods, schemas, API specs |
| **Diagrams** | C4 Context + Container | Sequence, Class, ER, State Machine |
| **Detail Level** | "We will use a message queue" | "RabbitMQ with fanout exchange, 3 queues, DLQ with 3 retry policy" |
| **Scope** | System-wide | Single service or feature |
| **Outcome** | Architecture approval | Implementation blueprint |

---

## 3. Mandatory LLD Sections

Every LLD MUST contain these sections. Each section below defines what MUST be included.

### 3.1 Document Header
```
Title:           [Feature/Service Name] — Low-Level Design
Version:         [1.0, 1.1, etc.]
Author:          [Name]
Reviewers:       [Names]
Status:          [Draft | In Review | Approved | Superseded]
Date:            [YYYY-MM-DD]
Related ADRs:    [Link to relevant ADRs]
Related HLD:     [Link to parent HLD if exists]
```

### 3.2 Scope & Objectives
- WHAT this LLD covers — specific feature, service, or component.
- WHAT it does NOT cover — explicit exclusions to prevent scope creep.
- Business context — WHY this is being built (link to requirements or user stories).
- Success criteria — measurable outcomes that define "done."

### 3.3 Assumptions & Constraints
- **Assumptions:** What you are taking for granted (e.g., "Authentication is handled by the API Gateway").
- **Constraints:** What limits your design (e.g., "Must use existing PostgreSQL 14 database," "Budget: $500/month").
- **Dependencies:** What external systems or teams this design depends on.

### 3.4 Detailed Design

#### 3.4.1 Component Architecture
- List every component/module being created or modified.
- For each component, define:
  - **Responsibility** — single sentence describing what it does
  - **Inputs** — what data it receives and from where
  - **Outputs** — what data it produces and to where
  - **Dependencies** — what it calls or relies on
  - **Technology** — specific library, framework, or service used

#### 3.4.2 Class / Module Design
- Class diagrams or module structure showing:
  - Class/module names with clear naming convention
  - Key methods with signatures (name, parameters, return type)
  - Properties/fields with types
  - Relationships (inheritance, composition, dependency injection)
  - Design patterns used (Repository, Factory, Strategy, Observer, etc.)

**Rules for class design:**
- Follow SOLID principles — flag any violation with justification.
- Prefer composition over inheritance.
- All public methods MUST have documented input/output contracts.
- Side effects MUST be explicitly documented.

#### 3.4.3 Sequence Diagrams
MUST include sequence diagrams for:
- **Happy path** — the primary success flow.
- **Key error paths** — at least the top 3 most likely failure scenarios.
- **Edge cases** — boundary conditions, concurrent access, empty states.

Sequence diagrams MUST show:
- Actor/caller
- All services/components involved
- Request/response payloads (summarized)
- Database operations
- Async operations (queues, events)
- Timeout and retry behavior

#### 3.4.4 API Specification
For every new or modified API endpoint:

| Field | Required |
|-------|:------:|
| HTTP Method + Path | ✅ |
| Description | ✅ |
| Request Headers | ✅ |
| Path Parameters | ✅ |
| Query Parameters | ✅ |
| Request Body (with JSON schema) | ✅ |
| Response Body — success (with JSON schema) | ✅ |
| Response Body — error (with error codes) | ✅ |
| Status Codes (200, 201, 400, 401, 403, 404, 409, 422, 500) | ✅ |
| Rate Limiting | ✅ |
| Authentication/Authorization | ✅ |
| Pagination (if list endpoint) | ✅ |
| Idempotency (if mutation endpoint) | ⚠️ If applicable |
| Versioning strategy | ✅ |

**API Naming Rules:**
- Use nouns for resources: `/users`, `/orders`, `/payments`
- Use kebab-case for multi-word paths: `/payment-methods`
- Use plural nouns for collections: `/users` not `/user`
- Nest resources logically: `/users/{id}/orders`
- Actions use verbs only when CRUD doesn't fit: `/orders/{id}/cancel`

#### 3.4.5 Database Design
For every new or modified data store:

**Schema Definition:**
- Table/collection names with naming convention
- All columns/fields with:
  - Name, data type, size/precision
  - Nullable (YES/NO)
  - Default value
  - Constraints (PK, FK, UNIQUE, CHECK)
  - Index (if applicable — type: B-tree, GIN, etc.)
- Relationships between tables (1:1, 1:N, M:N with join tables)

**Data Rules:**
- Estimated row count at launch and at 1-year, 3-year projections
- Partitioning strategy (if table exceeds 10M rows)
- Archival/retention policy
- Soft delete vs hard delete strategy
- Audit columns: `created_at`, `updated_at`, `created_by`, `updated_by`
- PII columns MUST be identified and flagged

**Migration Strategy:**
- Migration script approach (Flyway, Alembic, Liquibase, raw SQL)
- Backward compatibility — can the old code work with the new schema during rollout?
- Rollback plan — can the migration be reversed without data loss?

#### 3.4.6 Event / Message Design
For event-driven components:

| Field | Required |
|-------|:------:|
| Event name / topic | ✅ |
| Producer service | ✅ |
| Consumer service(s) | ✅ |
| Event schema (JSON) | ✅ |
| Delivery guarantee (at-least-once, exactly-once) | ✅ |
| Ordering guarantee | ✅ |
| Retry policy | ✅ |
| Dead letter queue (DLQ) strategy | ✅ |
| Idempotency handling | ✅ |
| Schema versioning approach | ✅ |

### 3.5 Error Handling Strategy
Define for the entire service:

| Error Category | Strategy |
|---------------|----------|
| **Validation errors** (bad input) | Return 400/422 with structured error body; log at WARN |
| **Authentication failures** | Return 401; log at WARN with source IP |
| **Authorization failures** | Return 403; log at WARN with user ID and attempted action |
| **Not found** | Return 404; do NOT leak information about existence |
| **Conflict / race condition** | Return 409; include current state in response |
| **Downstream service failure** | Circuit breaker → fallback → return 503 with Retry-After header |
| **Database failure** | Retry with backoff (max 3) → return 500 with correlation ID |
| **Unhandled exception** | Catch-all handler → return 500 with generic message; log full stack at ERROR |
| **Timeout** | Return 504; log with timing details at ERROR |

**Error Response Contract:**
```json
{
  "error": {
    "code": "PAYMENT_INSUFFICIENT_FUNDS",
    "message": "The payment could not be processed due to insufficient funds.",
    "details": [
      {
        "field": "amount",
        "issue": "Exceeds available balance"
      }
    ],
    "correlationId": "req-abc123-def456",
    "timestamp": "2026-03-11T09:30:00Z",
    "documentation": "https://docs.api.example.com/errors/PAYMENT_INSUFFICIENT_FUNDS"
  }
}
```

### 3.6 Security Considerations
MUST address for every LLD:

- [ ] **Authentication:** How is the caller authenticated? (JWT, OAuth2, mTLS, API key)
- [ ] **Authorization:** What RBAC/ABAC rules apply? Which roles can access which endpoints?
- [ ] **Input Validation:** What validation rules apply? (type, length, range, format, allowlist)
- [ ] **SQL Injection:** Are parameterized queries used? Are ORMs configured safely?
- [ ] **XSS/CSRF:** Are outputs encoded? Are CSRF tokens used for state-changing operations?
- [ ] **Sensitive Data:** Is PII encrypted at rest? Is data masked in logs?
- [ ] **Secrets Management:** How are API keys, DB credentials, tokens managed?
- [ ] **Rate Limiting:** What limits apply per user, per IP, per API key?
- [ ] **Audit Trail:** What operations are logged for compliance? What is the retention period?

### 3.7 Performance Considerations

- **Latency targets:** p50, p95, p99 latency for each endpoint
- **Throughput targets:** Expected requests per second (normal, peak)
- **Database query performance:**
  - Expected query execution time
  - Indexes required
  - N+1 query prevention strategy
  - Connection pool sizing
- **Caching:**
  - What is cached?
  - Cache key structure
  - TTL
  - Invalidation strategy
- **Payload sizes:** Maximum request/response body sizes
- **Pagination:** Strategy for large result sets (cursor-based preferred over offset)

### 3.8 Observability Plan

| Type | What to Capture |
|------|----------------|
| **Structured Logs** | Request ID, user ID, action, duration, outcome, error details |
| **Metrics** | Request count, latency histogram, error rate, queue depth, DB pool usage |
| **Traces** | Distributed trace IDs propagated across all service calls |
| **Alerts** | Error rate > 5% for 5 min, p99 latency > 2s, queue depth > 1000, DB connection exhaustion |
| **Dashboards** | Service health, SLO burn rate, dependency status, business metrics |

**Logging Rules:**
- Use structured JSON logging (not plain text).
- Include correlation/request ID in every log entry.
- NEVER log PII, passwords, tokens, or full credit card numbers.
- Log levels: DEBUG (local only), INFO (request lifecycle), WARN (recoverable issues), ERROR (failures requiring attention).

### 3.9 Testing Strategy

| Test Type | Scope | Coverage Target |
|-----------|-------|:---------------:|
| **Unit Tests** | Individual functions/methods, business logic | 80%+ |
| **Integration Tests** | API endpoints, database operations, external service mocks | Key flows |
| **Contract Tests** | API contract validation between consumer and provider | All inter-service APIs |
| **Performance Tests** | Latency and throughput under load | Before production launch |
| **Security Tests** | OWASP Top 10, authentication bypass, injection | Before production launch |

### 3.10 Deployment & Rollout

- **Deployment strategy:** Blue-green, canary, rolling update (specify which and why)
- **Feature flags:** List any feature flags used during rollout
- **Rollback procedure:** Step-by-step rollback plan if deployment fails
- **Monitoring during rollout:** What metrics to watch in the first 30 minutes
- **Database migration timing:** Run before deploy, during deploy, or after deploy?

### 3.11 Open Questions & Risks

| # | Question / Risk | Impact | Owner | Decision Deadline |
|---|----------------|--------|-------|-------------------|
| 1 | | | | |
| 2 | | | | |

---

## 4. Quality Checklist — LLD Review

Before approving an LLD, verify:

### Completeness
- [ ] All mandatory sections are present
- [ ] Sequence diagrams cover happy path AND error paths
- [ ] API contracts include all status codes and error responses
- [ ] Database schema includes indexes, constraints, and migration plan
- [ ] Security considerations are addressed (not just "TBD")

### Correctness
- [ ] Class design follows SOLID principles
- [ ] No shared mutable state between services
- [ ] Idempotency is handled for all mutation operations
- [ ] Error handling covers all failure modes (not just happy path)
- [ ] Data types and sizes are appropriate (not just `VARCHAR(255)` everywhere)

### Clarity
- [ ] A developer can implement this without asking the architect clarifying questions
- [ ] Diagrams are readable and use standard notation
- [ ] Naming is consistent throughout the document
- [ ] Acronyms and terms are defined or linked to glossary

### Non-Functional
- [ ] Latency and throughput targets are defined
- [ ] Caching strategy is documented where applicable
- [ ] Observability (logs, metrics, traces, alerts) is planned
- [ ] Testing strategy covers unit, integration, contract, and performance

---

## 5. Common LLD Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | What to Do Instead |
|-------------|---------------|-------------------|
| "We'll handle errors later" | Error handling IS the design | Define error strategy upfront |
| VARCHAR(255) for everything | Wastes storage, hides intent | Use appropriate types and sizes |
| No indexes defined | Performance issues in production | Define indexes based on query patterns |
| "Security: TBD" | Security is not optional | Address auth, authz, encryption in LLD |
| No sequence diagrams | Implementation ambiguity | At minimum: happy path + top 3 errors |
| Shared database between services | Tight coupling, blocking deployments | Each service owns its data store |
| Synchronous chain of 5+ services | Latency multiplication, fragile | Use async messaging for long chains |
| No pagination on list endpoints | Memory issues, slow responses | Cursor-based pagination by default |
| Logging "everything" | Log noise, compliance risk | Structured logging with clear levels |
| No rollback plan | Stuck in broken state | Define rollback for every deployment |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
