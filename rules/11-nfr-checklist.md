# Non-Functional Requirements (NFR) Checklist

> **Purpose:** A comprehensive 50+ point checklist for auditing architecture designs against
> non-functional requirements. Feed this to any LLM alongside a design document and ask
> it to audit the design against this checklist.

---

## How to Use This File

- Say to an LLM: *"Audit this design document against the NFR checklist: [paste this file]. Here's the design: [paste design]"*
- The LLM will evaluate each item and report gaps with severity ratings.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [04 — LLD Standards](./04-lld-standards.md) | Use this checklist to audit LLD designs |
| [03 — HLD Standards](./03-hld-standards.md) | Audit HLD NFR summary section |
| [12 — Observability](./12-observability-standards.md) | Detailed standards for Observability checks |
| [07 — Security Architecture](./07-security-architecture.md) | Detailed standards for Security checks |

---

## 1. Performance (15 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| P01 | Latency targets defined for each endpoint (p50, p95, p99) | 🔴 Critical |
| P02 | Throughput targets defined (requests/sec for normal and peak) | 🔴 Critical |
| P03 | Database query performance analyzed (slow query identification) | 🔴 Critical |
| P04 | N+1 query problem identified and mitigated | 🟠 High |
| P05 | Connection pool sizing defined for databases and HTTP clients | 🟠 High |
| P06 | Caching strategy defined (what, where, TTL, invalidation) | 🟠 High |
| P07 | Pagination implemented for all list endpoints | 🟠 High |
| P08 | Payload size limits defined for request/response bodies | 🟡 Medium |
| P09 | CDN configured for static assets and cacheable responses | 🟡 Medium |
| P10 | Async processing used for non-real-time operations | 🟡 Medium |
| P11 | Batch processing strategy for bulk operations | 🟡 Medium |
| P12 | Database indexes defined based on query patterns | 🔴 Critical |
| P13 | Read replicas or CQRS considered for read-heavy workloads | 🟡 Medium |
| P14 | Resource compression enabled (gzip/brotli for responses) | 🟢 Low |
| P15 | Performance testing plan defined (load test, stress test, soak test) | 🟠 High |

---

## 2. Security (12 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| S01 | Authentication mechanism defined (OAuth2, JWT, API Key) | 🔴 Critical |
| S02 | Authorization model defined (RBAC/ABAC with role matrix) | 🔴 Critical |
| S03 | Input validation on ALL user-supplied data | 🔴 Critical |
| S04 | SQL injection prevention (parameterized queries or ORM) | 🔴 Critical |
| S05 | Encryption in transit (TLS 1.2+ for all communication) | 🔴 Critical |
| S06 | Encryption at rest for sensitive data (AES-256, KMS) | 🔴 Critical |
| S07 | Secrets management strategy (not in code, not in env vars) | 🔴 Critical |
| S08 | PII identified, classified, and masking strategy defined | 🟠 High |
| S09 | Rate limiting configured to prevent abuse | 🟠 High |
| S10 | CORS configured restrictively (specific origins) | 🟠 High |
| S11 | Security headers set (HSTS, X-Content-Type, X-Frame-Options) | 🟡 Medium |
| S12 | Dependency vulnerability scanning in CI/CD pipeline | 🟠 High |

---

## 3. Reliability (10 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| R01 | SLA/SLO defined (availability target, e.g., 99.9%) | 🔴 Critical |
| R02 | Circuit breaker pattern for all external dependencies | 🔴 Critical |
| R03 | Retry policy with exponential backoff and jitter | 🟠 High |
| R04 | Timeout explicitly set for every external call | 🔴 Critical |
| R05 | Fallback strategy when dependencies are unavailable | 🟠 High |
| R06 | Health check endpoints for liveness and readiness | 🔴 Critical |
| R07 | Graceful shutdown handling (drain connections, complete in-flight requests) | 🟠 High |
| R08 | Idempotency for mutation operations (retryable writes) | 🟠 High |
| R09 | Dead letter queue (DLQ) for failed async messages | 🟠 High |
| R10 | Chaos engineering or failure injection testing planned | 🟡 Medium |

---

## 4. Scalability (8 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| SC01 | Services are stateless (no in-memory session state) | 🔴 Critical |
| SC02 | Horizontal scaling strategy defined (auto-scaling rules) | 🔴 Critical |
| SC03 | Database partitioning strategy for tables >10M rows | 🟠 High |
| SC04 | Data archival strategy for aging data | 🟡 Medium |
| SC05 | Message queue scaling (partitioning, consumer groups) | 🟠 High |
| SC06 | File/object storage for large payloads (not in DB) | 🟠 High |
| SC07 | Multi-region or multi-AZ deployment considered | 🟡 Medium |
| SC08 | Load tested at 2x and 10x expected peak load | 🟠 High |

---

## 5. Observability (8 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| O01 | Structured logging with JSON format and correlation ID | 🔴 Critical |
| O02 | Key business and technical metrics exposed (Prometheus/StatsD) | 🔴 Critical |
| O03 | Distributed tracing enabled across all services | 🟠 High |
| O04 | Alert rules defined with severity levels and escalation | 🔴 Critical |
| O05 | Dashboard created for service health and SLO tracking | 🟠 High |
| O06 | PII excluded from logs and traces | 🔴 Critical |
| O07 | Log retention policy defined and compliant | 🟡 Medium |
| O08 | Error tracking integrated (Sentry, Datadog, Rollbar) | 🟡 Medium |

---

## 6. Disaster Recovery (6 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| DR01 | RPO (Recovery Point Objective) defined | 🔴 Critical |
| DR02 | RTO (Recovery Time Objective) defined | 🔴 Critical |
| DR03 | Automated backup strategy with verified restoration | 🔴 Critical |
| DR04 | Backup encryption with separate key from production | 🟠 High |
| DR05 | DR runbook documented and tested | 🟠 High |
| DR06 | Cross-region disaster recovery for critical systems | 🟡 Medium |

---

## 7. Maintainability (5 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| M01 | Code follows consistent standards (linting, formatting rules) | 🟡 Medium |
| M02 | API documentation (OpenAPI/Swagger) maintained and current | 🟠 High |
| M03 | Architecture Decision Records (ADRs) for key decisions | 🟠 High |
| M04 | Dependency update strategy (automated PRs, regular review) | 🟡 Medium |
| M05 | Modular design — can replace components without full rewrite | 🟠 High |

---

## 8. Compliance (5 Checks)

| # | Check | Severity |
|---|-------|:--------:|
| C01 | Data classification applied to all stored data | 🟠 High |
| C02 | Data retention policy defined and automated | 🟠 High |
| C03 | Audit trail for all data mutations (who changed what, when) | 🔴 Critical |
| C04 | Data residency requirements met (correct cloud region) | 🔴 Critical |
| C05 | Right-to-deletion (GDPR Art. 17) support implemented | 🟠 High |

---

## Scoring Summary

After auditing, summarize findings:

| Category | Total Checks | ✅ Pass | ❌ Fail | ⚠️ Partial | Score |
|----------|:-----------:|:------:|:------:|:---------:|:-----:|
| Performance | 15 | | | | /15 |
| Security | 12 | | | | /12 |
| Reliability | 10 | | | | /10 |
| Scalability | 8 | | | | /8 |
| Observability | 8 | | | | /8 |
| Disaster Recovery | 6 | | | | /6 |
| Maintainability | 5 | | | | /5 |
| Compliance | 5 | | | | /5 |
| **TOTAL** | **69** | | | | **/69** |

**Rating Scale:**
| Score | Rating | Action |
|-------|--------|--------|
| 60-69 | 🟢 Excellent | Proceed to implementation |
| 50-59 | 🟡 Good | Address medium findings before launch |
| 40-49 | 🟠 Needs Work | Address high/critical findings |
| <40 | 🔴 Not Ready | Major redesign required |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
