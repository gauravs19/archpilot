# Integration Patterns

> **Purpose:** Standards for designing system integrations — event-driven architecture,
> messaging, API gateways, ETL, webhooks, and inter-service communication.

---

## How to Use This File

- **Claude Projects:** Upload for integration architecture and event-driven design
- **Any LLM:** Say: *"Using these integration patterns, design the integration for: [your systems]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [09 — Microservices Patterns](./09-microservices-patterns.md) | Service communication and saga patterns |
| [06 — Data Architecture](./06-data-architecture.md) | CDC, ETL/ELT data flow patterns |
| [05 — API Design](./05-api-design.md) | REST/API standards for sync integrations |
| [12 — Observability](./12-observability-standards.md) | Tracing across integration boundaries |

---

## 1. Integration Style Selection

```
Need integration? 
├── Real-time, request-response? → Synchronous (REST/gRPC)
├── Real-time, fire-and-forget? → Async Messaging (Queue)
├── Real-time, multiple consumers? → Event Streaming (Pub/Sub)
├── Near-real-time data sync? → Change Data Capture (CDC)
├── Batch data movement? → ETL/ELT Pipeline  
├── External system notification? → Webhooks
└── UI aggregating multiple services? → API Gateway / BFF
```

---

## 2. Event-Driven Architecture

### 2.1 Event Design Standards

**Event Envelope (Standard Schema):**
```json
{
  "eventId": "uuid-v4",
  "eventType": "order.placed",
  "version": "1.0",
  "timestamp": "2026-03-11T09:00:00Z",
  "source": "order-service",
  "correlationId": "uuid-v4",
  "causationId": "uuid-v4",
  "data": { },
  "metadata": {
    "userId": "uuid",
    "tenantId": "uuid"
  }
}
```

### 2.2 Event Naming Convention
```
{domain}.{entity}.{action}
```

| Examples | Meaning |
|----------|---------|
| `order.placed` | An order was created |
| `payment.completed` | Payment was successful |
| `user.profile.updated` | User profile was modified |
| `inventory.stock.depleted` | Stock fell below threshold |

**Rules:**
- Past tense (facts, not commands): `order.placed` ✅, `place.order` ❌
- Lowercase, dot-separated.
- Action verbs: `created`, `updated`, `deleted`, `completed`, `failed`, `expired`, `approved`, `rejected`

### 2.3 Event Schema Versioning
- Schema changes MUST be backward-compatible (additive only).
- New required fields → create a new event version (`order.placed.v2`).
- Consumers MUST handle unknown fields gracefully (ignore, don't fail).
- Schema registry (Confluent, AWS Glue) recommended for Kafka environments.

### 2.4 Delivery Guarantees

| Guarantee | Meaning | Use When | Technology |
|-----------|---------|----------|-----------|
| **At-most-once** | Message may be lost, never duplicated | Metrics, logging (non-critical) | UDP, fire-and-forget |
| **At-least-once** | Message delivered, may be duplicated | Default for all business events | Kafka, SQS, RabbitMQ |
| **Exactly-once** | Message delivered exactly once | Financial transactions | Kafka (idempotent producers + transactional consumers) |

**Default:** At-least-once + idempotent consumers.

### 2.5 Idempotency Rules
Since at-least-once delivery means duplicates are possible:
- Every consumer MUST be idempotent.
- Use `eventId` as a deduplication key.
- Store processed event IDs in a deduplication table (TTL: 7 days).
- Database upserts (INSERT ON CONFLICT) for write operations.

### 2.6 Dead Letter Queue (DLQ)

| Rule | Standard |
|------|----------|
| Every queue/topic MUST have a DLQ | Mandatory |
| Retry policy before DLQ | 3 retries: 1s, 10s, 60s (exponential backoff) |
| DLQ monitoring | Alert when DLQ depth > 0 |
| DLQ processing | Manual review within 24 hours, automated replay tool |
| DLQ retention | 14 days minimum |

---

## 3. Message Broker Selection

| Broker | Best For | Ordering | Persistence | Throughput |
|--------|---------|:--------:|:-----------:|:----------:|
| **Apache Kafka** | Event streaming, high throughput, replay | Per-partition | ✅ Long-term | Very High |
| **RabbitMQ** | Task queues, routing, low latency | Per-queue | ✅ | Medium |
| **AWS SQS** | Simple queuing, serverless | ❌ (FIFO optional) | ✅ | High |
| **AWS SNS+SQS** | Fan-out pub/sub on AWS | Per-FIFO queue | ✅ | High |
| **Azure Service Bus** | Enterprise messaging on Azure | ✅ Sessions | ✅ | Medium-High |
| **Google Pub/Sub** | Serverless messaging on GCP | ❌ | ✅ | High |
| **Redis Streams** | Lightweight streaming, prototyping | Per-stream | ⚠️ Memory | High |

---

## 4. API Gateway Pattern

### 4.1 Responsibilities

```
Client ──▶ [API Gateway] ──▶ Service A
                          ──▶ Service B
                          ──▶ Service C
```

| Responsibility | Implementation |
|---------------|---------------|
| **Routing** | Path-based routing to services |
| **Authentication** | JWT validation, API key check |
| **Rate Limiting** | Per-user, per-IP, per-API key |
| **Request Transform** | Header injection, body transformation |
| **Response Aggregation** | Merge responses from multiple services |
| **Caching** | Cache GET responses by URL + headers |
| **SSL Termination** | TLS at the edge |
| **Logging/Tracing** | Request ID injection, access logging |
| **Circuit Breaking** | Protect against downstream failures |

### 4.2 BFF (Backend for Frontend)

| Client | BFF | Why |
|--------|-----|-----|
| Web App | Web BFF | Aggregates data for desktop UI |
| Mobile App | Mobile BFF | Optimized payloads for bandwidth |
| Partner API | Partner API Gateway | Different auth, rate limits, SLA |

**Rule:** Do NOT build a generic "one gateway for all clients." Different clients have different needs.

---

## 5. Webhook Standards

For outgoing webhooks (notifying external systems):

| Standard | Rule |
|----------|------|
| Format | JSON over HTTPS POST |
| Authentication | HMAC signature in header (`X-Signature-256`) |
| Retry policy | 3 retries: 5s, 30s, 300s — exponential backoff |
| Timeout | 10 seconds per attempt |
| Idempotency | Include `webhookId` for deduplication |
| Versioning | Include `version` field in payload |
| Security | Validate SSL certificates, IP allowlisting optional |
| Monitoring | Track delivery rate, failure rate, latency |

**Webhook Payload:**
```json
{
  "webhookId": "uuid",
  "eventType": "order.completed",
  "version": "1.0",
  "timestamp": "2026-03-11T09:00:00Z",
  "data": { }
}
```

---

## 6. Synchronous Integration Patterns

### 6.1 Service-to-Service Direct Call
```
Service A ──REST──▶ Service B
```
- Acceptable for: simple, low-latency, low-complexity calls.
- MUST have: timeout (5s default), circuit breaker, retry (3x with backoff).
- Maximum chain depth: 3 services.

### 6.2 API Composition Pattern
```
API Composer ──▶ Service A (get user)
             ──▶ Service B (get orders)
             ──▶ Service C (get payments)
             ──▶ Merge and return
```
- Use when: client needs data from multiple services in one call.
- Implement in: API Gateway or BFF.
- Calls SHOULD be parallel where possible.

### 6.3 Saga Orchestrator
- For distributed transactions spanning multiple services.
- See `rules/09-microservices-patterns.md` for saga pattern details.

---

## 7. Data Integration Patterns

### 7.1 ETL vs ELT

| Pattern | Flow | When |
|---------|------|------|
| **ETL** | Extract → Transform → Load | Legacy systems, complex transformations |
| **ELT** | Extract → Load → Transform | Cloud data warehouses (BigQuery, Snowflake, Redshift) |

**Rule:** Prefer ELT for cloud-native analytics — transform where compute is cheap and scalable.

### 7.2 Change Data Capture (CDC)

```
[PostgreSQL] ──Debezium──▶ [Kafka] ──▶ [Elasticsearch / Data Warehouse]
```

- Use for: real-time data sync without modifying application code.
- Technologies: Debezium (open-source), AWS DMS, Azure Change Feed.
- Captures: INSERT, UPDATE, DELETE events from database transaction log.

### 7.3 Batch Data Transfer

| Approach | When | Technology |
|----------|------|-----------|
| File-based (S3/GCS) | Large datasets, partner data exchange | CSV/Parquet + S3 events |
| Database replication | Read replicas for reporting | PostgreSQL streaming replication |
| Scheduled jobs | Periodic aggregation | Apache Airflow, AWS Step Functions |

---

## 8. Integration Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Shared Database** | Tight coupling, schema conflicts | Each service owns its data, integrate via API/events |
| **Point-to-Point Spaghetti** | N services = N² connections | Use event bus or API gateway |
| **Synchronous chain > 3 deep** | Latency multiplication, cascade failures | Break into async events |
| **No idempotency** | Duplicate processing on retry | Deduplication by event ID |
| **No DLQ** | Failed messages silently lost | DLQ + monitoring + replay |
| **Generic mega-event** | One event with 50 fields = tight coupling | Small, domain-specific events |
| **Webhook without retry** | Missed notifications | Retry with exponential backoff |
| **No schema versioning** | Event format changes break consumers | Versioned schemas, backward compatible |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
