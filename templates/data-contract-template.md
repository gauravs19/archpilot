# [Dataset/Event Name] — Data Contract

<!-- See rule: rules/32-data-contracts.md -->

---

## Contract Metadata

```yaml
contract:
  id: "DC-[domain]-[entity]-[type]-v[N]"
  version: "1.0.0"
  status: "DRAFT"  # DRAFT | ACTIVE | DEPRECATED | RETIRED
  created: "YYYY-MM-DD"
  last_updated: "YYYY-MM-DD"
  owner_team: "[team-name]"
  owner_email: "[team-email@company.com]"
  transport: "kafka"  # kafka | rest-api | s3 | database | grpc | webhook
  topic_or_path: "[kafka-topic | api-path | s3-bucket/prefix | db.table]"
  schema_format: "json-schema"  # avro | json-schema | protobuf | parquet
  compatibility_mode: "BACKWARD"  # BACKWARD | FORWARD | FULL | NONE
  schema_registry_url: "[https://schema-registry.internal/subjects/...]"
  consumers:
    - team: "[consumer-team-name]"
      contact: "[email@company.com]"
      registered_date: "YYYY-MM-DD"
```

---

## 1. Overview

**Dataset / Event:** [Name]
**Business Purpose:** [What business event or process does this data represent?]
**Producer Service:** [ServiceName]
**Data Classification:** Public | Internal | Confidential | Restricted

---

## 2. Schema Definition

<!-- Define every field: name, type, nullable, PII, description, example, validation. -->

### 2.1 Top-Level Structure

```json
{
  "eventId": "string (uuid)",
  "eventType": "string",
  "timestamp": "string (ISO-8601)",
  "version": "string",
  "schemaVersion": "string",
  "payload": { ... }
}
```

### 2.2 Field Definitions

| Field Path | Type | Nullable | PII | Description | Example | Validation |
|-----------|------|:-------:|:---:|------------|---------|-----------|
| `eventId` | string (uuid) | No | No | Unique event identifier | `550e8400-...` | UUID v4 format |
| `eventType` | string | No | No | Event type discriminator | `payments.tx.created` | Enum (see §2.3) |
| `timestamp` | string | No | No | Event occurrence time (UTC) | `2026-05-14T10:00:00Z` | ISO-8601 |
| `version` | string | No | No | Schema version | `1.0` | Semver |
| `payload.transactionId` | string (uuid) | No | No | Business transaction ID | `abc-123-...` | UUID v4 |
| `payload.amount` | number | No | No | Transaction amount | `99.99` | >0, =1,000,000 |
| `payload.currency` | string | No | No | ISO 4217 currency code | `USD` | 3-letter enum |
| `payload.customerId` | string | No | Yes | Customer identifier (pseudonymized) | `cust_sha256_abc` | SHA-256 hash |
| `payload.email` | string | Yes | Yes | Customer email — MUST NOT be published raw | N/A | Pseudonymize before publish |

### 2.3 Enumerated Values

| Field | Allowed Values |
|-------|--------------|
| `eventType` | `payments.transaction.created`, `payments.transaction.updated`, `payments.transaction.failed` |
| `payload.currency` | ISO 4217 codes: `USD`, `EUR`, `GBP`, `INR`, ... |
| `payload.status` | `PENDING`, `PROCESSING`, `COMPLETED`, `FAILED`, `REFUNDED` |

### 2.4 Full Example Payload

```json
{
  "eventId": "550e8400-e29b-41d4-a716-446655440000",
  "eventType": "payments.transaction.created",
  "timestamp": "2026-05-14T10:00:00Z",
  "version": "1.0",
  "schemaVersion": "1.0.0",
  "payload": {
    "transactionId": "txn-abc123-def456",
    "amount": 149.99,
    "currency": "USD",
    "customerId": "cust_sha256_3f2a1b",
    "status": "PENDING",
    "merchantId": "merchant-xyz-789",
    "createdAt": "2026-05-14T10:00:00Z"
  }
}
```

---

## 3. Data Quality Expectations

```yaml
quality:
  completeness:
    - field: "eventId"
      max_null_rate: 0.0
    - field: "payload.transactionId"
      max_null_rate: 0.0
    - field: "payload.amount"
      max_null_rate: 0.0

  freshness:
    max_delay_seconds: 30
    measurement: "event timestamp to kafka publish time"
    slo: "p95 < 30s"

  validity:
    - field: "payload.currency"
      rule: "Must be valid ISO 4217 code"
      expected_pass_rate: 1.0
    - field: "payload.amount"
      rule: "Must be positive number"
      expected_pass_rate: 1.0

  volume:
    expected_daily_events: 500000
    alert_threshold_low: 400000   # Alert if <80% of expected
    alert_threshold_high: 750000  # Alert if >150% of expected
```

---

## 4. SLA

```yaml
sla:
  availability: "99.9%"
  measurement_window: "30-day rolling"
  max_publish_latency_p95_seconds: 30
  support_response_sla: "2 business hours"
  incident_contact: "[oncall-channel or email]"
  scheduled_maintenance:
    window: "Sundays 02:00–04:00 UTC"
    advance_notice_hours: 48
```

---

## 5. PII Handling

| Field | PII Type | Handling Method | Compliance |
|-------|---------|----------------|-----------|
| `payload.customerId` | Customer identity | SHA-256 pseudonymization | GDPR Art. 4(5) |
| `payload.email` | Contact data | MUST NOT be published | GDPR, CCPA |

**Pseudonymization key rotation:** [Monthly / Quarterly / On breach]
**Right to erasure:** [How is erasure implemented — event replay, tombstone, or reference deletion?]

---

## 6. Compatibility & Migration

### Current Version: 1.0.0
**Compatibility mode:** BACKWARD (new consumers can read old messages)

### Planned Changes (Roadmap)

| Target Version | Planned Change | Type | Target Date |
|:-------------:|---------------|:----:|:-----------:|
| 1.1.0 | Add optional `payload.merchantCategory` field | MINOR | [YYYY-MM-DD] |
| 2.0.0 | Replace `payload.customerId` with `payload.customerRef` (format change) | MAJOR | [YYYY-MM-DD] |

### Consumer Migration Policy
- **MINOR changes:** No migration needed; consumers can ignore new optional fields
- **MAJOR breaking changes:** 12-month notice minimum; migration guide provided; both versions active during transition

---

## 7. Changelog

| Version | Date | Type | Change | Migration Required |
|---------|------|:----:|--------|:-----------------:|
| 1.0.0 | YYYY-MM-DD | INITIAL | Initial contract definition | No |

---

## 8. Consumer Registration

<!-- Every team consuming this data MUST register here. -->

| Consumer Team | Use Case | SLA Dependency | Registered | Contact |
|--------------|---------|:-------------:|:---------:|---------|
| team-analytics | Revenue reporting | No (best-effort) | YYYY-MM-DD | analytics@company.com |
| team-fraud | Real-time fraud detection | Yes | YYYY-MM-DD | fraud@company.com |

---

## 9. Data Contract Quality Checklist

- [ ] All fields have: type, nullable, PII flag, description, example, validation
- [ ] No PII fields are published raw (pseudonymized or excluded)
- [ ] Quality expectations defined: completeness, freshness, validity, volume
- [ ] SLA documented with availability, latency, and support contact
- [ ] Compatibility mode set in schema registry
- [ ] Consumer registration complete
- [ ] Changelog maintained from version 1.0.0
- [ ] Breaking change notice period documented

---

*Archpilot — Data Contract Template*
*See: rules/32-data-contracts.md*
