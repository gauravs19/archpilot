# Data Contract Standards

> **Purpose:** This rule file defines standards for data contracts between producers and
> consumers of data — the formal, version-controlled agreements that prevent schema drift,
> silent breaking changes, and the "garbage in, garbage out" failures in data pipelines
> and event-driven systems.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [06 — Data Architecture](./06-data-architecture.md) | Data modeling and storage standards |
| [10 — Integration Patterns](./10-integration-patterns.md) | Event-driven and CDC patterns |
| [05 — API Design](./05-api-design.md) | API as a form of data contract |
| [31 — API Governance](./31-api-governance.md) | Lifecycle governance for API contracts |

---

## 1. What is a Data Contract?

A data contract is a formal, version-controlled specification that defines:
- **Schema:** The structure, types, and constraints of data
- **Semantics:** The business meaning of each field
- **Quality:** Expectations about completeness, freshness, and accuracy
- **SLA:** When data will be available and how reliable it is
- **Ownership:** Who produces it, who consumes it, who is responsible

> "A data contract is the API for your data." — Data Mesh principle

---

## 2. When to Write a Data Contract

| Situation | Contract Required? |
|-----------|:-----------------:|
| New Kafka topic / event stream | ? Always |
| New database table consumed by another team | ? Always |
| New data pipeline output | ? Always |
| New REST/GraphQL API | ? Always (see rule 05) |
| Modifying an existing schema with consumers | ? Always |
| Internal database table (single-service owned) | ? LLD schema is sufficient |
| Temporary data (dev/test only) | ? No |

---

## 3. Data Contract Structure

Every data contract MUST include these sections:

### 3.1 Metadata

```yaml
contract:
  id: "DC-payments-transaction-events-v2"
  version: "2.1.0"
  status: "ACTIVE"  # DRAFT | ACTIVE | DEPRECATED | RETIRED
  created: "2026-01-15"
  last_updated: "2026-04-01"
  owner_team: "team-payments"
  owner_email: "payments-eng@company.com"
  consumers:
    - team: "team-analytics"
      contact: "analytics-eng@company.com"
    - team: "team-fraud"
      contact: "fraud-eng@company.com"
  transport: "kafka"  # kafka | rest-api | s3 | database | grpc
  topic_or_path: "payments.transaction.events"
  schema_registry: "https://schema-registry.internal/subjects/payments-transaction-events"
```

### 3.2 Schema Definition

```yaml
schema:
  format: "avro"  # avro | json-schema | protobuf | parquet
  compatibility: "BACKWARD"  # BACKWARD | FORWARD | FULL | NONE
  fields:
    - name: "transaction_id"
      type: "string"
      format: "uuid"
      nullable: false
      pii: false
      description: "Unique transaction identifier (UUID v4)"
      example: "550e8400-e29b-41d4-a716-446655440000"

    - name: "amount"
      type: "decimal"
      precision: 18
      scale: 4
      nullable: false
      pii: false
      description: "Transaction amount in the currency specified by currency_code"
      validation:
        minimum: 0.0001
        maximum: 1000000.0000

    - name: "customer_email"
      type: "string"
      nullable: true
      pii: true
      pii_handling: "pseudonymized"
      description: "Customer email — pseudonymized with SHA-256 before publishing"
```

### 3.3 Data Quality Expectations

```yaml
quality:
  completeness:
    - field: "transaction_id"
      expected_null_rate: 0.0
    - field: "amount"
      expected_null_rate: 0.0
  freshness:
    max_delay_seconds: 30  # Max seconds from event occurrence to availability
    measurement: "event_time to publish_time"
  validity:
    - field: "currency_code"
      rule: "ISO 4217 3-letter code"
      expected_pass_rate: 1.0
  volume:
    expected_daily_events: 500000
    alert_if_below: 400000  # Alert if volume drops >20%
    alert_if_above: 750000  # Alert if volume spikes >50%
```

### 3.4 SLA

```yaml
sla:
  availability: "99.9%"
  measurement_window: "30-day rolling"
  max_latency_p95_seconds: 30
  support_response_sla: "2 business hours"
  incident_notification: "payments-oncall@company.com"
  scheduled_maintenance_window: "Sundays 02:00-04:00 UTC"
```

### 3.5 Changelog

```yaml
changelog:
  - version: "2.1.0"
    date: "2026-04-01"
    type: "MINOR"
    change: "Added optional 'merchant_category_code' field"
    migration: "Consumers can safely ignore new field"

  - version: "2.0.0"
    date: "2026-01-15"
    type: "MAJOR"
    change: "Replaced 'customer_name' (PII) with 'customer_id' (pseudonymized)"
    migration: "Consumers must update schema. customer_name no longer published."
    notice_period_months: 12
```

---

## 4. Schema Compatibility Rules

### 4.1 Compatibility Matrix

| Change | BACKWARD Compatible? | FORWARD Compatible? | Safe to Deploy? |
|--------|:-------------------:|:------------------:|:---------------:|
| Add optional field | ? Yes | ? Yes | ? Yes |
| Add required field with default | ? Yes | ? Yes | ? Yes |
| Add required field without default | ? No | ? Yes | ?? Major version |
| Remove optional field | ? Yes | ? No | ?? Major version + notice |
| Remove required field | ? Yes | ? No | ?? Major version + notice |
| Change field type (widening, e.g., int?long) | ? Yes | ? No | ?? Check consumers |
| Change field type (narrowing, e.g., long?int) | ? No | ? No | ?? Never without major |
| Rename field | ? No | ? No | ?? Use add+deprecate pattern |
| Change field semantics (same name, new meaning) | ? No | ? No | ?? Never |

### 4.2 Safe Field Rename Pattern

NEVER rename a field directly. Use this migration pattern:
1. Add new field with correct name (MINOR version)
2. Publish both old and new field for transition period
3. Notify consumers; give 6+ months
4. Remove old field (MAJOR version)

---

## 5. Data Contract Governance

### 5.1 Contract Registry

All data contracts MUST be registered in a central registry (e.g., Confluent Schema Registry, AWS Glue Data Catalog, or internal GitOps-based registry):
- Contracts are version-controlled in Git
- Schema registry enforces compatibility rules on every publish
- Breaking changes require: new major version + consumer impact assessment + notice period

### 5.2 Consumer Impact Assessment

Before publishing a breaking change:

| Step | Action |
|------|--------|
| 1 | List all registered consumers from contract metadata |
| 2 | Notify each consumer team with: change description, impact, migration guide |
| 3 | Get written acknowledgement from each consumer team |
| 4 | Set migration deadline (minimum: 6 months for minor, 12 months for major breaking) |
| 5 | Monitor consumer migration progress |
| 6 | Only retire old version after 100% consumers migrated OR deadline passed |

### 5.3 Contract Drift Detection

Automated monitoring MUST detect and alert on:
- Schema published to registry that differs from the approved contract
- Data quality metrics falling below thresholds defined in contract
- Volume anomalies (above/below alert thresholds)
- Freshness SLA breaches
- Consumer error rate spike (may indicate undeclared breaking change)

---

## 6. Data Contract Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Implicit contracts (no documentation) | Consumers break silently on changes | Formal contract required before first consumer |
| Schema drift (code diverges from contract) | Contract becomes fiction | Schema registry enforces contract at publish time |
| Renaming fields in place | Breaks all consumers | Use add+deprecate+remove pattern over multiple versions |
| No consumer registry | Can't assess change impact | Consumers MUST register against contract |
| "Just update your code" | Surprise breaking changes | Minimum 6-month notice for any breaking change |
| PII in raw events | Compliance violation | Pseudonymize/encrypt PII before publishing |
| No quality expectations | Silent data rot | Define completeness, freshness, validity targets |

---

## 7. Data Contract Checklist

- [ ] Contract metadata complete (ID, version, owner, consumers, transport)
- [ ] Schema definition with types, nullability, PII flags, descriptions, examples
- [ ] Quality expectations defined (completeness, freshness, validity, volume)
- [ ] SLA defined (availability, latency, support response)
- [ ] Registered in schema registry with compatibility mode set
- [ ] All PII fields flagged and handling method specified
- [ ] Changelog maintained with version history
- [ ] Consumers registered against the contract
- [ ] Drift detection monitoring active
- [ ] Breaking change process followed for any non-backward-compatible change

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
