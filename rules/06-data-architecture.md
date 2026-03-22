# Data Architecture Standards

> **Purpose:** This rule file defines standards for data modeling, storage selection,
> governance, and data flow design. Ensures every data-related architecture decision
> follows enterprise best practices for integrity, performance, and compliance.

---

## How to Use This File

- **Claude Projects:** Upload as project knowledge for data modeling and storage decisions
- **Design Reviews:** Reference when reviewing database schemas and data flows
- **Any LLM:** Say: *"Using these data architecture standards, design the data model for: [your service]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [04 — LLD Standards](./04-lld-standards.md) | DB design is a mandatory LLD section (§3.4.5) |
| [07 — Security Architecture](./07-security-architecture.md) | Encryption, PII handling, data classification |
| [10 — Integration Patterns](./10-integration-patterns.md) | CDC, ETL/ELT, event-driven data flows |
| [14 — Cost Optimization](./14-cost-optimization.md) | Storage tier selection for cost efficiency |

---

## 1. Data Modeling Principles

### 1.1 Entity Design Rules
- Every entity MUST have a primary key (UUID preferred over auto-increment for distributed systems).
- Every entity MUST include audit columns: `created_at`, `updated_at`, `created_by`, `updated_by`.
- Soft delete (`deleted_at` timestamp) is preferred over hard delete for business-critical data.
- Column names use `snake_case`. Table names use `snake_case`, plural (`users`, `order_items`).
- NEVER use reserved SQL keywords as column/table names.

### 1.2 Normalization vs Denormalization

| Context | Approach | When |
|---------|----------|------|
| **OLTP (Transactional)** | Normalize to 3NF | Default for write-heavy workloads |
| **OLAP (Analytical)** | Denormalize (star/snowflake schema) | Reporting, dashboards |
| **Read-Heavy APIs** | Strategic denormalization | When joins cause p95 > targets |
| **Event Stores** | Append-only, immutable | Event-sourced systems |

**Rule:** Start normalized. Denormalize only when measured performance requires it. Document the trade-off in an ADR.

### 1.3 Data Types

| Use Case | ✅ Do | ❌ Don't |
|----------|-------|---------|
| IDs | UUID (gen_random_uuid()) | Auto-increment integers (enumerable) |
| Money | Integer (minor units: cents/paisa) + currency code | Float/double (precision loss) |
| Timestamps | TIMESTAMPTZ (timezone-aware) | TIMESTAMP (ambiguous timezone) |
| Status/Enum | VARCHAR with CHECK constraint | Integer codes (1,2,3 = unreadable) |
| JSON data | JSONB (PostgreSQL) with validation | Untyped TEXT storing JSON |
| Booleans | BOOLEAN | VARCHAR ('yes','no','true') |
| Short text | VARCHAR(n) with appropriate n | VARCHAR(255) for everything |
| Long text | TEXT | VARCHAR(10000) |

---

## 2. Storage Selection Framework

### 2.1 Decision Matrix

| Requirement | PostgreSQL | MySQL | DynamoDB | MongoDB | Redis | Elasticsearch |
|------------|:----------:|:-----:|:--------:|:-------:|:-----:|:-------------:|
| Complex queries (joins) | ✅ | ✅ | ❌ | ⚠️ | ❌ | ⚠️ |
| ACID transactions | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ |
| Horizontal scaling | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| Key-value access | ⚠️ | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| Full-text search | ⚠️ | ⚠️ | ❌ | ⚠️ | ❌ | ✅ |
| Time-series data | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ✅ |
| Caching | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Document storage | ✅(JSONB) | ❌ | ✅ | ✅ | ❌ | ✅ |
| Managed service cost | Medium | Low | Low-Medium | Medium | Low | High |

### 2.2 Default Recommendations

| Use Case | Default Choice | Alternative |
|----------|---------------|-------------|
| General OLTP | PostgreSQL | MySQL |
| Session/Cache | Redis | Memcached |
| Full-Text Search | Elasticsearch | PostgreSQL FTS |
| Document Store | MongoDB or PostgreSQL JSONB | DynamoDB |
| Key-Value (massive scale) | DynamoDB | Redis Cluster |
| Analytics/OLAP | BigQuery, Redshift, ClickHouse | PostgreSQL (small scale) |
| Time Series | TimescaleDB, InfluxDB | Prometheus (metrics only) |
| Graph Data | Neo4j, Neptune | PostgreSQL (simple graphs) |
| File/Object Storage | S3, GCS, Azure Blob | MinIO (self-hosted) |

---

## 3. Data Governance

### 3.1 Data Classification

| Level | Label | Examples | Handling |
|:-----:|-------|---------|----------|
| 1 | **Public** | Marketing content, public docs | No restrictions |
| 2 | **Internal** | Employee directory, internal reports | Authenticated access |
| 3 | **Confidential** | Customer data, financial records | Encrypted, role-based access |
| 4 | **Restricted** | PII, credentials, health records | Encrypted, audit logged, masked in non-prod |

### 3.2 Data Ownership Rules
- Every table/collection MUST have a designated **owning service**.
- Only the owning service can write to its tables. Other services access via API or events.
- NO shared databases between services.
- Data ownership is documented in a data catalog.

### 3.3 Data Retention Policy

| Data Category | Retention Period | After Expiry |
|--------------|:----------------:|-------------|
| Transaction records | 7 years | Archive to cold storage |
| User activity logs | 90 days | Delete |
| Audit logs | 3 years | Archive |
| Session data | 24 hours | Delete |
| PII (if consent withdrawn) | 30 days | Hard delete + confirmation |
| Backups | 30 days | Auto-expire |

### 3.4 PII Data Handling

| Practice | Implementation |
|----------|---------------|
| **Identification** | All PII columns tagged in schema definitions |
| **Minimization** | Collect only what is strictly necessary |
| **Encryption** | Column-level encryption for sensitive fields |
| **Masking** | Mask in logs, non-prod environments, and support tools |
| **Access Control** | Row-level security, column-level permissions |
| **Right to Deletion** | Automated GDPR Article 17 compliance process |
| **Pseudonymization** | Replace identifiers in analytics/reporting |
| **Data Lineage** | Track where PII flows across systems |

---

## 4. Data Flow Patterns

### 4.1 Synchronous Data Exchange
```
Service A ──REST/gRPC──▶ Service B
```
- Use for: real-time queries, single-record lookups, authentication checks.
- MUST have: timeout, circuit breaker, retry with backoff.

### 4.2 Event-Driven Data Flow
```
Service A ──publish──▶ [Event Bus] ──subscribe──▶ Service B, C, D
```
- Use for: state changes that multiple consumers need, loose coupling.
- Events are facts (immutable), not commands.

### 4.3 Change Data Capture (CDC)
```
Database ──CDC──▶ [Kafka/Debezium] ──▶ Data Warehouse / Search Index
```
- Use for: syncing data to analytics, search indexes, or read replicas without application changes.

### 4.4 ETL / ELT
```
Sources ──Extract──▶ [Staging] ──Transform──▶ [Data Warehouse] ──Load──▶ [BI Tools]
```
- Use for: batch analytics, reporting, data aggregation.
- ELT preferred over ETL for modern cloud data warehouses (transform where compute is cheap).

### 4.5 CQRS (Command Query Responsibility Segregation)
```
Write Path: API ──▶ Command Service ──▶ Write DB (PostgreSQL)
                                          │
                                    [Domain Event]
                                          │
Read Path:  API ──▶ Query Service ──▶ Read DB (Elasticsearch / Redis)
```
- Use for: read-heavy workloads where read and write models differ significantly.
- Write DB is the source of truth. Read DB is eventually consistent.

---

## 5. Database Migration Standards

### 5.1 Migration Rules
- ALL schema changes through versioned migration scripts (Flyway, Alembic, Liquibase). NEVER manual DDL.
- Migrations MUST be backward-compatible with the previous application version (zero-downtime deployment).
- Migration naming: `V{version}__{description}.sql` (e.g., `V0023__add_user_preferences_table.sql`).
- Every migration MUST have a tested rollback script.

### 5.2 Safe Migration Patterns

| Operation | Safe Approach | Unsafe Approach |
|-----------|--------------|-----------------|
| Add column | Add as nullable, backfill, then add NOT NULL | Add NOT NULL column (locks table) |
| Remove column | Stop reading → deploy → remove column in next release | Drop column directly |
| Rename column | Add new column → copy data → update code → drop old | ALTER RENAME (breaks running code) |
| Add index | CREATE INDEX CONCURRENTLY | CREATE INDEX (locks table) |
| Change data type | Add new column with new type → migrate → drop old | ALTER COLUMN TYPE (may fail) |

### 5.3 Data Migration Checklist
- [ ] Migration is idempotent (can run twice without error)
- [ ] Backward compatible with current running application version
- [ ] Rollback script tested in staging
- [ ] Large table migrations chunked (not single transaction)
- [ ] Indexes created CONCURRENTLY
- [ ] Migration tested with production-sized data (timing verified)
- [ ] PII implications assessed (new PII fields? retention? masking?)

---

## 6. Indexing Strategy

### 6.1 When to Add an Index
- Every foreign key column → index (always).
- Columns in WHERE clauses → index (if selectivity > 10%).
- Columns in ORDER BY → index (for sorted queries).
- Columns in JOIN conditions → index (always).
- DO NOT index columns that are rarely queried.
- DO NOT index columns with very low cardinality (e.g., boolean with 50/50 split).

### 6.2 Index Types

| Type | When | Example |
|------|------|---------|
| B-tree | Default, equality and range queries | `WHERE status = 'active'` |
| Hash | Exact equality only | `WHERE id = 'uuid'` |
| GIN | Array/JSONB containment queries | `WHERE tags @> '{backend}'` |
| GiST | Geospatial, full-text search | `WHERE location <-> point` |
| Partial | Filtered subset of rows | `WHERE status = 'active'` (only index active rows) |
| Composite | Multi-column queries | `WHERE tenant_id = ? AND created_at > ?` |

### 6.3 Index Monitoring
- Track index usage: drop unused indexes (they slow down writes).
- Track slow queries (>100ms) and add indexes based on EXPLAIN ANALYZE.
- Review index strategy with each major feature release.

---

## 7. Concurrency Control

### 7.1 Pattern Selection

| Pattern | When | Postgres Mechanism |
|---------|------|--------------------|
| **Optimistic locking** | Read-heavy, conflicts rare, short transactions | `version` column + conditional UPDATE |
| **Pessimistic locking** | Write-heavy, conflicts frequent, critical correctness | `SELECT FOR UPDATE` |
| **Atomic update** | Single-table write with a guard condition | UPDATE with WHERE guard + RETURNING |
| **Advisory lock** | Coordination across tables or external APIs | `pg_try_advisory_xact_lock()` |

### 7.2 Optimistic Locking

Add a `version` integer column. Read it with the row. On update, assert the version hasn't changed.

```sql
-- Schema
ALTER TABLE orders ADD COLUMN version INTEGER NOT NULL DEFAULT 0;

-- Read
SELECT id, status, total, version FROM orders WHERE id = $1;

-- Update — will update 0 rows if another transaction won the race
UPDATE orders
SET status = $1, version = version + 1
WHERE id = $2 AND version = $3
RETURNING id;

-- If RETURNING returns no row: conflict — retry or surface to user
```

Use when: inventory updates, account settings, document editing. Not suitable for financial balances (use atomic update instead).

### 7.3 Atomic Update (Financial Operations)

Never read-then-write for balance-sensitive operations. Push the guard condition into the UPDATE:

```sql
-- ❌ read-then-write — two concurrent transactions both see balance = 100
SELECT balance FROM wallets WHERE user_id = $1;
UPDATE wallets SET balance = balance - $2 WHERE user_id = $1;

-- ✅ atomic — the WHERE clause is the concurrency guard
UPDATE wallets
SET balance = balance - $2
WHERE user_id = $1 AND balance >= $2
RETURNING balance;
-- No row returned = insufficient balance (another request got there first)
```

### 7.4 Pessimistic Locking

Use when a transaction spans multiple steps and correctness requires exclusive access:

```sql
BEGIN;
SELECT * FROM seats WHERE id = $1 FOR UPDATE;
-- Other transactions trying to SELECT FOR UPDATE on this row will block here
UPDATE seats SET status = 'reserved', user_id = $2 WHERE id = $1;
COMMIT;
```

**Warning:** `SELECT FOR UPDATE` holds a row lock for the transaction duration. Keep transactions short. Never hold a lock across a network call (e.g., don't lock a row, call a payment API, then commit — the payment API timeout becomes a lock timeout).

### 7.5 Distributed Coordination (Advisory Locks)

When coordinating across tables or with external systems, Postgres advisory locks prevent double-processing without a separate Redis dependency:

```sql
-- Returns true if lock acquired, false if another transaction holds it
SELECT pg_try_advisory_xact_lock(hashtext('invoice:' || invoice_id::text));
-- Lock auto-released at transaction end — no explicit unlock needed
```

Use when: processing the same webhook from two sources, preventing duplicate job execution, coordinating cross-table operations that can't be expressed as a single UPDATE.

### 7.6 Concurrency Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Read balance → check → update | Race window between read and write | Atomic UPDATE with WHERE guard |
| `SELECT FOR UPDATE` across API call | Lock held during external call timeout | Move external call outside the transaction |
| Optimistic locking on financial data | Version conflict loses money, not just a retry | Use atomic update instead |
| Application-level mutex (in-memory) | Breaks under horizontal scaling | Database-level locking |
| No locking on idempotency key insert | Two concurrent requests both insert | UNIQUE constraint + INSERT ON CONFLICT |

---

## 8. Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `VARCHAR(255)` for everything | Hides intent, wastes storage | Use appropriate types and sizes specific to each field |
| No indexes on foreign keys | Slow joins, full table scans | Always index FK columns |
| Shared database between services | Tight coupling, deployment bottleneck | Each service owns its data store |
| Auto-increment IDs exposed externally | Enumerable, leaks business info | Use UUIDs for public-facing identifiers |
| FLOAT for money | Precision loss causes real financial errors | Use integer minor units (cents) + currency code |
| No data retention policy | Storage costs grow unbounded, compliance risk | Define retention per data type, automate cleanup |
| Manual DDL in production | Unreproducible, no rollback, drift | All changes via versioned migration scripts |
| Storing PII without classification | Privacy violations, compliance failure | Tag every PII column, apply masking + encryption |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
