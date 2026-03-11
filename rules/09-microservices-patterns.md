# Microservices Architecture Patterns

> **Purpose:** This rule file defines when and how to apply microservices patterns.
> It covers decomposition criteria, communication, resilience, data management,
> and anti-patterns. Use as LLM context for consistent microservices design.

---

## How to Use This File

- **Claude Projects:** Upload for microservices decomposition and design
- **Any LLM:** Say: *"Using these microservices patterns, design the architecture for: [your system]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [10 — Integration Patterns](./10-integration-patterns.md) | Inter-service communication patterns |
| [09 — Microservices Patterns](./09-microservices-patterns.md) | Saga references cross-linked here |
| [12 — Observability](./12-observability-standards.md) | Distributed tracing for microservices |
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Container/serverless deployment |

---

## 1. When to Use Microservices (Decision Framework)

### Use Microservices When:
- ✅ Teams need to deploy independently (org scaling > tech scaling)
- ✅ Different components have different scaling requirements
- ✅ Different components have different technology requirements
- ✅ Domain boundaries are well-understood (mature domain model)
- ✅ Organization has DevOps maturity (CI/CD, monitoring, on-call)

### Do NOT Use Microservices When:
- ❌ Team size < 5 developers (overhead exceeds benefit)
- ❌ Domain is not well understood (premature decomposition)
- ❌ Shared database is required for ACID transactions
- ❌ Organization lacks CI/CD and observability infrastructure
- ❌ "Because Netflix does it" (scale-driven decisions for non-scale problems)

**Default Starting Point:** Start with a **Modular Monolith** — well-defined internal modules with clear boundaries. Extract to microservices when a specific module needs independent scaling or deployment.

---

## 2. Service Decomposition

### 2.1 Decomposition Strategies

| Strategy | When to Use | Example |
|----------|------------|---------|
| **By Business Capability** | Clear business domains | Order Service, Payment Service, Inventory Service |
| **By Subdomain (DDD)** | Complex domains with bounded contexts | Core, Supporting, Generic subdomains |
| **By Data Ownership** | Strong data isolation needs | Each service owns its data store |
| **By Team (Conway's Law)** | Organizational alignment | Team A → Service A, Team B → Service B |

### 2.2 Service Sizing Guidelines

| Guideline | Rule |
|-----------|------|
| **Team ownership** | One team owns 2-5 services (not 1 service = 1 developer) |
| **Cognitive load** | A new developer should understand the service in 1-2 days |
| **Deployment frequency** | Each service deploys independently, at least weekly |
| **Data ownership** | Each service has its own data store — NO shared databases |
| **API surface** | 5-15 API endpoints per service (if more, consider splitting) |

### 2.3 Bounded Context Rules
- Each microservice = one bounded context.
- Shared models (e.g., "User") are represented differently in each context:
  - **Order Context:** User = { userId, shippingAddress }
  - **Payment Context:** User = { userId, paymentMethod }
  - **Identity Context:** User = { userId, email, password, roles }
- Communication between contexts uses domain events, not shared models.

---

## 3. Communication Patterns

### 3.1 Synchronous Communication

| Pattern | When | Protocol | Concerns |
|---------|------|----------|----------|
| **REST API** | Simple request-response, CRUD | HTTP/HTTPS | Latency coupling, cascading failures |
| **gRPC** | High-performance, internal services | HTTP/2 + Protobuf | Requires proto management, less tooling |
| **GraphQL** | Frontend aggregation of multiple services | HTTP/HTTPS | Not for service-to-service |

**Rules for Sync Communication:**
- Maximum sync chain depth: **3 services** (A → B → C). Beyond 3, use async.
- ALWAYS set timeouts on every sync call.
- ALWAYS implement circuit breakers on sync dependencies.
- Prefer an API Gateway for external consumers; direct calls for internal.

### 3.2 Asynchronous Communication

| Pattern | When | Technology |
|---------|------|-----------|
| **Event-Driven (Pub/Sub)** | Loose coupling, multiple consumers | Kafka, SNS/SQS, RabbitMQ |
| **Command Queue** | One-to-one task delegation | SQS, RabbitMQ |
| **Event Sourcing** | Full audit trail, temporal queries | Kafka, EventStore |
| **CQRS** | Different read/write models, read-heavy | Separate read DB (Elasticsearch, Redis) |

**Rules for Async Communication:**
- Events are immutable facts ("OrderPlaced"), not commands ("PlaceOrder").
- Event schemas MUST be versioned and backward-compatible.
- Every consumer MUST be idempotent (handle duplicate events gracefully).
- Dead Letter Queue (DLQ) MUST be configured for failed messages.
- Ordering matters? Use partition keys. Ordering doesn't matter? Use competing consumers.

### 3.3 Communication Decision Matrix

```
Need immediate response?
├── YES → Sync (REST/gRPC)
│         └── Will failure cascade? → Add circuit breaker
└── NO  → Async (Events/Queue)
          ├── Multiple consumers? → Pub/Sub (Kafka, SNS)
          └── Single consumer? → Queue (SQS, RabbitMQ)
```

---

## 4. Data Management

### 4.1 Database per Service (Mandatory)
- Each service MUST have its own database.
- No direct database access between services — use APIs or events.
- Database technology can differ per service (polyglot persistence).

### 4.2 Data Consistency Patterns

| Pattern | Consistency | Use When |
|---------|:-----------:|----------|
| **Strong Consistency** | Immediate | Single service, single database |
| **Eventual Consistency** | Delayed | Cross-service operations (default) |
| **Saga Pattern** | Eventual with compensation | Distributed transactions |

### 4.3 Saga Pattern (for Distributed Transactions)

**Choreography (Event-Driven):**
```
Order Service → publishes "OrderCreated"
    → Payment Service → publishes "PaymentCompleted"
        → Inventory Service → publishes "InventoryReserved"
            → Order Service → sets order to "Confirmed"

Compensation (on failure):
    ← Inventory Service → publishes "InventoryReservationFailed"
        ← Payment Service → publishes "PaymentRefunded"
            ← Order Service → sets order to "Failed"
```

**Orchestration (Centralized):**
- A Saga Orchestrator service coordinates the steps.
- Each step is a command; each response triggers the next step.
- Orchestrator handles compensation on failure.

**When to use which:**
| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| Choreography | Loosely coupled, simple | Hard to track, no central view | 3-4 step sagas |
| Orchestration | Clear flow, easier debugging | Single point of control | 5+ step sagas, complex logic |

---

## 5. Resilience Patterns

### 5.1 Mandatory Patterns for Every Service

```
┌─────────────────────────────────────────┐
│              Calling Service            │
│                                         │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │ Timeout  ├──► Circuit  ├──► Retry  │ │
│  │ (strict) │  │ Breaker  │  │ w/    │ │
│  │          │  │          │  │backoff│ │
│  └──────────┘  └──────────┘  └───┬───┘ │
│                                  │      │
│                          ┌───────▼───┐  │
│                          │ Fallback  │  │
│                          │ (cache,   │  │
│                          │  default) │  │
│                          └───────────┘  │
└─────────────────────────────────────────┘
```

### 5.2 Bulkhead Pattern
- Isolate resources per dependency (separate thread pools, connection pools).
- If Payment Service is slow, it doesn't starve Order Service's connections.
- Configure max concurrent requests per downstream service.

### 5.3 Service Mesh Considerations
For 10+ services, consider a service mesh (Istio, Linkerd):
- Automatic mTLS between services.
- Traffic management (canary, A/B, circuit breaking).
- Observability (distributed tracing, metrics).
- Retry and timeout policies without code changes.

---

## 6. Service Discovery & Routing

| Pattern | When | Technology |
|---------|------|-----------|
| **DNS-Based** | Cloud-native, simple | Route53, Cloud DNS, CoreDNS |
| **Client-Side Discovery** | Direct service-to-service | Eureka, Consul |
| **Server-Side Discovery** | Load balancer–mediated | ALB, NGINX, Kubernetes Services |
| **Service Mesh** | Large-scale, complex routing | Istio, Linkerd |

**Kubernetes default:** Kubernetes Services + DNS (built-in service discovery).

---

## 7. API Gateway Pattern

The API Gateway is the SINGLE entry point for external consumers:

**Responsibilities:**
- Request routing to downstream services.
- Authentication and authorization.
- Rate limiting and throttling.
- Request/response transformation.
- SSL termination.
- Caching for GET requests.
- Request aggregation (BFF — Backend for Frontend).

**Technology Options:**
| Gateway | Best For |
|---------|---------|
| AWS API Gateway | Serverless, AWS-native |
| Kong | Open-source, plugin ecosystem |
| NGINX | High performance, simple routing |
| Envoy | Service mesh integration |
| Azure API Management | Azure-native |

---

## 8. Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Distributed Monolith** | Services coupled via shared DB or sync chains | Own your data, use events |
| **Chatty Services** | 50 API calls to render one page | Aggregate via BFF or API Gateway |
| **Nano Services** | 1 endpoint per service | Merge into cohesive bounded contexts |
| **Shared Libraries** | Common lib creates deployment coupling | Duplicate vs couple — choose wisely |
| **Sync Everything** | 5-service sync chain = 5x latency, 5x failure risk | Async by default, sync when necessary |
| **No Service Contract** | API changes break consumers | Contract-first, contract testing |
| **God Service** | One service does everything | Decompose by subdomain |
| **Circular Dependencies** | A calls B, B calls A | Introduce events or merge services |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
