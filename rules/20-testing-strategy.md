# Testing Strategy Standards

> **Purpose:** Standards for test pyramid, contract testing, performance testing,
> chaos engineering, and test data management. Ensures every system has a comprehensive,
> automated testing strategy from day one.

---

## How to Use This File

- **Design Reviews:** Say to an LLM: *"Using these testing standards, create a testing strategy for: [your service]"*
- **Sprint Planning:** Reference test coverage targets and testing pyramid for estimation
- **CI/CD:** Use quality gates to enforce testing standards in pipelines

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [04 — LLD Standards](./04-lld-standards.md) | Testing strategy is mandatory LLD section (§3.9) |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | Tests run as pipeline stages |
| [05 — API Design](./05-api-design.md) | Contract testing for API consumers |
| [15 — Code Review](./15-code-review-guidelines.md) | Test review checklist (§6) |

---

## 1. The Test Pyramid

```
           ┌─────────┐
           │  E2E /  │  ← Few (5-10%)
           │   UI    │     Slow, brittle, expensive
          ┌┴─────────┴┐
          │Integration │  ← Some (20-30%)
          │   / API    │     Test service interactions
         ┌┴───────────┴┐
         │   Contract   │  ← Cross-service (10%)
         │   Tests      │     Verify API contracts
        ┌┴─────────────┴┐
        │   Unit Tests   │  ← Many (60-70%)
        │                │     Fast, isolated, cheap
        └────────────────┘
```

| Layer | What | Speed | Coverage Target | Tools |
|-------|------|:-----:|:---------------:|-------|
| **Unit** | Functions, classes, business logic | < 1s each | 80%+ line coverage | pytest, Jest, JUnit |
| **Integration** | API endpoints, DB operations, external mocks | 1-10s each | Key user flows | pytest + httpx, Supertest |
| **Contract** | API consumer-provider agreements | 1-5s each | All inter-service APIs | Pact, Schemathesis |
| **E2E** | Full user journeys through the live system | 30-120s each | Top 5-10 critical flows | Playwright, Cypress, Selenium |

**Rules:**
- Shift LEFT — catch bugs at the lowest cost layer possible
- If E2E tests > 30% of total → pyramid is inverted (anti-pattern)
- Flaky tests are BUGS — fix or delete, never ignore

---

## 2. Unit Testing Standards

### 2.1 Rules

| Rule | Standard |
|------|---------|
| Coverage target | 80%+ line coverage for business logic |
| Test naming | `test_[method]_[scenario]_[expected_result]` |
| Isolation | No network calls, no database, no filesystem |
| Deterministic | Same result every time — no random data, no time-dependency |
| One assertion per test | Prefer focused tests over multi-assertion tests |
| Test the behavior | Test what it does, not how it does it (avoid testing implementation details) |

### 2.2 What to Unit Test

| ✅ Test | ❌ Don't Test |
|---------|-------------|
| Business logic, calculations | Framework/library internals |
| Validation rules | Getter/setter methods |
| Data transformations | Constants and configuration |
| Edge cases (nulls, empty, boundary) | Third-party API calls (mock these) |
| Error handling paths | Constructors (unless they have logic) |

### 2.3 Arrange-Act-Assert Pattern

```python
def test_order_total_applies_discount_for_premium_users():
    # Arrange
    user = User(tier="premium")
    items = [Item(price=1000, qty=2)]
    
    # Act
    total = calculate_order_total(user, items)
    
    # Assert
    assert total == 1800  # 10% discount applied
```

---

## 3. Integration Testing Standards

### 3.1 What to Integration Test

| Test | How |
|------|-----|
| API endpoint returns correct response | HTTP client → Service → Assert response |
| Database operations work correctly | Service → Real DB (test container) → Assert data |
| Message consumption works | Publish test event → Consumer → Assert side effect |
| External service integration | Service → Mock server (WireMock) → Assert behavior |
| Auth flow works end-to-end | Request with token → Service → Assert access |

### 3.2 Test Containers

Use Docker containers for integration test dependencies:

```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
  test-redis:
    image: redis:7-alpine
  test-localstack:
    image: localstack/localstack
    environment:
      SERVICES: sqs,sns,s3
```

**Rules:**
- Use real databases in containers, NOT in-memory fakes (SQLite ≠ PostgreSQL)
- Each test suite gets a clean database (migrations + seed data)
- Tests MUST clean up after themselves
- Integration tests run in CI on every PR

---

## 4. Contract Testing

### 4.1 When to Contract Test

```
Consumer A ──REST──▶ Provider B
    │                    │
    └── Consumer Contract Test (verifies expected API shape)
                         └── Provider Contract Test (verifies it matches consumers)
```

Use when: Multiple services communicate via APIs or events.

### 4.2 Contract Testing Rules

| Rule | Standard |
|------|---------|
| Contract ownership | Consumer defines expectations, provider verifies |
| Run in CI | Both consumer and provider run contract tests on every PR |
| Breaking changes | Provider CANNOT merge if consumer contracts fail |
| Schema changes | New fields are additive; removal requires consumer coordination |
| Tool | Pact (HTTP), Avro/Protobuf schema registry (events) |

---

## 5. Performance Testing

### 5.1 Test Types

| Type | What | When | Duration |
|------|------|------|:--------:|
| **Load Test** | Expected peak traffic | Before launch, after major changes | 30-60 min |
| **Stress Test** | Beyond expected capacity (find breaking point) | Before launch | 15-30 min |
| **Soak Test** | Sustained load over time (find memory leaks) | Before launch | 4-8 hours |
| **Spike Test** | Sudden traffic surge (flash sale simulation) | Before events | 15-30 min |

### 5.2 Performance Test Targets

| Metric | Target | Fail Threshold |
|--------|--------|:-------------:|
| p50 latency | < 200ms | > 500ms |
| p95 latency | < 500ms | > 2000ms |
| p99 latency | < 1000ms | > 5000ms |
| Error rate | < 0.1% | > 1% |
| Throughput | [defined per service] | < 80% of target |

### 5.3 Tools

| Tool | Best For |
|------|---------|
| **k6** | Developer-friendly, scriptable load testing |
| **Locust** | Python-based, distributed load testing |
| **JMeter** | Enterprise, complex scenarios |
| **Artillery** | Node.js, serverless-friendly |
| **Gatling** | JVM-based, detailed reporting |

---

## 6. Chaos Engineering

### 6.1 Principles

- **Start small:** Inject failures in staging before production
- **Define steady state:** Know what "normal" looks like before breaking things
- **Minimize blast radius:** Start with one service, one failure mode
- **Automate:** Scheduled chaos experiments, not ad-hoc

### 6.2 Failure Scenarios to Test

| Scenario | What to Break | Expected Behavior |
|----------|--------------|------------------|
| Service crash | Kill a service instance | Auto-restart, traffic routed to healthy instances |
| Network failure | Block traffic between services | Circuit breaker activates, fallback used |
| Database failure | Stop DB connections | Graceful degradation, cached data served |
| High latency | Add 5s delay to dependency | Timeout triggers, circuit opens |
| CPU saturation | Stress CPU to 100% | Auto-scaling triggers, no user impact |
| Disk full | Fill disk on a node | Alerts fire, node marked unhealthy |

---

## 7. Test Data Management

### 7.1 Rules

| Rule | Standard |
|------|---------|
| No production data in test environments | Anonymize or use synthetic data |
| Seed data is version-controlled | Migration scripts include test data seeds |
| PII in test data | Use realistic but fake data (Faker libraries) |
| Test data isolation | Each test suite gets its own data context |
| Shared test environments | Use tenant/namespace isolation |

---

## 8. Quality Gates in CI/CD

| Gate | Threshold | Action on Fail |
|------|:---------:|:-------------:|
| Unit test pass rate | 100% | Block merge |
| Unit test coverage | ≥ 80% | Block merge |
| Integration test pass rate | 100% | Block merge |
| Contract test pass rate | 100% | Block merge |
| Security scan (SAST) | No critical/high | Block merge |
| Performance test (pre-production) | Targets met | Block deploy to production |

---

## 9. Testing Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Ice cream cone** (inverted pyramid) | Too many E2E, too few unit tests | Shift tests down to unit/integration |
| **Flaky tests** | Random failures erode trust | Fix root cause, quarantine until fixed |
| **Testing implementation details** | Tests break on refactor, not on bugs | Test behavior and outputs |
| **No test data strategy** | Tests depend on shared mutable data | Isolated test data per suite |
| **Skipping tests for speed** | "We'll add tests later" (never happens) | Tests are required for merge |
| **100% coverage obsession** | Testing getters/setters, diminishing returns | 80% meaningful coverage > 100% meaningless |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
