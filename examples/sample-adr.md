# ADR-001: Use PostgreSQL for Multi-Tenant User Profile Storage

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Date** | 2026-03-11 |
| **Deciders** | Architecture Team, Platform Lead |
| **Supersedes** | N/A |

---

## Context

Our SaaS platform needs a primary database for user profile storage. The system currently
has 200 tenants with a growth target of 2,000 tenants within 18 months. Each tenant has
10-500 users, meaning we need to handle approximately 50,000-1,000,000 user profiles.

**Key requirements:**
- Complex queries across user profiles (search, filter, sort by multiple attributes)
- Multi-tenant data isolation (tenant A must never see tenant B's data)
- ACID transactions for profile updates and role assignments
- Full-text search on user names, emails, and custom fields
- Regulatory compliance (GDPR Article 17 — right to deletion per tenant)

**Team context:**
- Backend team has 5 years of strong SQL/relational database experience
- Limited experience with NoSQL databases
- Currently using PostgreSQL 14 for the existing authentication service
- Budget: $2,000/month for database infrastructure

**Forces:**
- Need for complex queries favors relational databases
- Multi-tenant isolation favors row-level security or schema-per-tenant
- Team expertise heavily skewed toward SQL
- Cost constraints favor open-source or AWS-managed options

---

## Decision

**We will use PostgreSQL (AWS RDS) with row-level security for multi-tenant user
profile storage.**

PostgreSQL is the strongest fit across all evaluation criteria. It excels at complex
relational queries, provides native row-level security for tenant isolation, and
leverages the team's deep SQL expertise. The existing PostgreSQL infrastructure for
authentication can share operational knowledge, runbooks, and monitoring.

---

## Alternatives Considered

| Criterion (Weight) | PostgreSQL RDS (Chosen) | DynamoDB | MongoDB Atlas |
|-------------------|:-----------------------:|:--------:|:-------------:|
| Complex Queries (25%) | 10/10 — native SQL, joins, CTEs | 4/10 — limited queries | 7/10 — aggregation pipeline |
| Team Expertise (20%) | 10/10 — 5 years experience | 3/10 — learning curve | 5/10 — some familiarity |
| Multi-Tenant Isolation (15%) | 9/10 — row-level security | 7/10 — partition key | 6/10 — requires careful design |
| Cost @ Scale (15%) | 7/10 — $400-800/mo on RDS | 6/10 — unpredictable at query volume | 5/10 — Atlas pricing |
| Full-Text Search (10%) | 7/10 — pg_trgm + GIN indexes | 2/10 — not supported | 8/10 — Atlas Search |
| ACID Transactions (10%) | 10/10 — native | 6/10 — limited to single-item | 8/10 — multi-document txn |
| GDPR Compliance (5%) | 9/10 — easy tenant deletion | 7/10 — partition delete | 7/10 — collection delete |
| **Weighted Score** | **8.8/10** | **4.7/10** | **6.3/10** |

### PostgreSQL RDS (Chosen)
Best overall fit. Native relational capabilities handle our complex query requirements
without workarounds. Row-level security provides tenant isolation at the database level.
Team productivity is highest since everyone knows PostgreSQL. Operationally consistent
with our existing auth database.

### DynamoDB
Excellent for key-value access patterns at massive scale, but our workload is
query-heavy with complex filters, joins, and sorts. Would require extensive
denormalization and maintaining secondary indexes for every query pattern. Team would
need significant training. Scored lowest due to query limitations and team expertise gap.

### MongoDB Atlas
Reasonable choice with the aggregation pipeline handling moderate query complexity.
Atlas Search would provide better full-text search than PostgreSQL. However, multi-tenant
isolation requires application-level enforcement (no native row-level security), and the
team has less experience with document modeling. Higher operational cost at our scale.

---

## Consequences

### Positive
- Team can start immediately — no learning curve, instant productivity
- Complex queries (search, filter, sort, paginate) work natively with SQL
- Row-level security enforces tenant isolation at the database level (defense in depth)
- Consistent technology stack with existing auth service — shared operational knowledge
- Strong ecosystem: pgAdmin, pg_dump, logical replication, extensions
- GDPR compliance straightforward — DELETE WHERE tenant_id = X

### Negative
- Horizontal scaling is harder than DynamoDB — requires read replicas or Citus for sharding
- At extreme scale (>10M profiles), may need partitioning strategy
- Full-text search is adequate but not as feature-rich as Elasticsearch or Atlas Search
- Single primary write node — write throughput limited by instance size

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|:----------:|:------:|-----------|
| Write throughput bottleneck at >5,000 tenants | Medium | Medium | Add read replicas for queries, connection pooling (PgBouncer), upgrade instance class |
| Full-text search performance at scale | Medium | Low | Add Elasticsearch for search-only if pg_trgm is insufficient; defer until proven necessary |
| Schema migration complexity as data model evolves | Low | Medium | Use Flyway for versioned migrations, backward-compatible changes only, test with production-sized data |

---

## Compliance & Standards

- **GDPR Article 17:** Supported via `DELETE FROM profiles WHERE tenant_id = ?` + cascading deletes
- **Data Encryption:** RDS encryption at rest (AES-256 via KMS), TLS 1.3 in transit
- **Audit Trail:** Row-level audit via `created_at`, `updated_at`, `created_by` columns
- **Backup:** Automated RDS snapshots with 30-day retention, cross-region for DR

---

## References

- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [AWS RDS PostgreSQL Pricing](https://aws.amazon.com/rds/postgresql/pricing/)
- [Multi-Tenant Patterns in PostgreSQL](https://www.citusdata.com/blog/2018/06/28/scaling-real-time-saas-analytics/)
- [DynamoDB Single-Table Design](https://www.alexdebrie.com/posts/dynamodb-single-table/)
- [MongoDB Multi-Tenancy Patterns](https://www.mongodb.com/docs/manual/tutorial/model-data-for-multi-tenancy/)

---

*Generated using Archpilot ADR Standards v1.0*
