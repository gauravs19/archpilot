# Migration Plan: Monolith to Microservices

## E-Commerce Monolith Modernization

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Gaurav Sharma |
| **Date** | 2026-03-11 |
| **Status** | Approved |
| **Migration Strategy** | Strangler Fig (incremental extraction) |

---

## 1. Current State Assessment

### 1.1 The Legacy System

| Attribute | Detail |
|-----------|--------|
| **Application** | ShopEasy — B2C e-commerce platform |
| **Architecture** | Monolithic Java Spring Boot application |
| **Database** | Single Oracle 19c database (500+ tables) |
| **Age** | 7 years in production |
| **Codebase** | ~300K lines of Java, ~150K lines of JSP |
| **Team** | 25 developers working on the same codebase |
| **Deployment** | Monthly releases, 4-hour maintenance windows |
| **Uptime** | 99.5% (frequent deployment-related incidents) |

### 1.2 Assessment Scores

| Dimension | Score | Notes |
|-----------|:-----:|-------|
| Business Value | 5 (Critical) | $50M annual revenue flows through this |
| Technical Health | 2 (Poor) | No tests, spaghetti code, Spring 4 |
| Operational Risk | 2 (Poor) | Monthly incidents, 4-hour deploy windows |
| Team Knowledge | 3 (Moderate) | Original team left, partial docs |
| Cost of Ownership | 2 (Poor) | Oracle license: $200K/year |
| Security Posture | 2 (Poor) | Unpatched dependencies, no WAF |
| Integration Complexity | 2 (Poor) | 500-table shared DB, 12 batch jobs |

**Assessment Score: 18/35 → REBUILD (with Strangler Fig approach)**

### 1.3 Pain Points Driving Migration

1. **Deployment fear** — every release risks breaking unrelated features
2. **Team bottleneck** — 25 developers in one repo, constant merge conflicts
3. **Oracle cost** — $200K/year in licensing alone
4. **Scaling impossible** — can't scale catalog search without scaling payments
5. **Technology stagnation** — Spring 4, Java 8, jQuery — can't hire modern talent

---

## 2. Target Architecture

### 2.1 Target State

```
┌──────────────────────────────────────────────────┐
│                   CloudFront CDN                  │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────▼───────────────────────────┐
│              API Gateway (Kong)                   │
│     Rate limiting, Auth, Routing                  │
└──┬──────┬──────┬──────┬──────┬──────┬───────────┘
   │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│Cata-││Cart ││Order││Pay- ││User ││Noti-│
│log  ││Svc  ││Svc  ││ment ││Svc  ││fy   │
│Svc  ││     ││     ││Svc  ││     ││Svc  │
└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘
   ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│PG   ││Redis││PG   ││PG   ││PG   ││SQS  │
│Cata ││Cart ││Ordr ││Pay  ││User ││Queue│
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
```

| Service | Technology | Database | Rationale |
|---------|-----------|----------|-----------|
| Catalog | Python/FastAPI | PostgreSQL + Elasticsearch | Search performance, team skill |
| Cart | Python/FastAPI | Redis | Low latency, ephemeral data |
| Order | Python/FastAPI | PostgreSQL | Complex queries, ACID needed |
| Payment | Python/FastAPI | PostgreSQL | Transaction integrity, audit |
| User | Python/FastAPI | PostgreSQL | Auth via Cognito + user profile |
| Notification | Python/FastAPI | SQS consumer | Event-driven, decoupled |

---

## 3. Migration Phases

### Phase 0: Foundation (Weeks 1-6)

**Goal:** Set up infrastructure and the routing proxy (no business logic changes)

| # | Task | Duration | Owner |
|---|------|:--------:|-------|
| 1 | Set up AWS VPC, subnets, security groups via Terraform | 1 week | DevOps |
| 2 | Deploy API Gateway (Kong) as proxy in front of monolith | 1 week | DevOps |
| 3 | All traffic flows: Client → Kong → Monolith (zero behavior change) | 1 week | DevOps |
| 4 | Set up CI/CD pipeline (GitHub Actions) | 1 week | DevOps |
| 5 | Set up monitoring (Datadog) for monolith + new infra | 1 week | DevOps |
| 6 | Set up ECS Fargate cluster for new services | 1 week | DevOps |

**Gate:** All traffic flowing through Kong with zero errors for 1 week.

### Phase 1: Extract User Service (Weeks 7-12)

**Goal:** First extraction — low-risk, well-understood, proves the pattern

| # | Task | Duration |
|---|------|:--------:|
| 1 | Design User Service API (OpenAPI spec) | 3 days |
| 2 | Build User Service (CRUD + auth integration with Cognito) | 2 weeks |
| 3 | Data migration: Oracle `users` table → PostgreSQL | 1 week |
| 4 | Anti-Corruption Layer: User Service adapts to legacy format | 3 days |
| 5 | Kong routing: `/api/users/*` → User Service | 1 day |
| 6 | Shadow mode: compare legacy vs new responses for 1 week | 1 week |
| 7 | Cut over: Kong routes user traffic to new service | 1 day |
| 8 | Decommission user code from monolith | 3 days |

**Gate:** User Service handles 100% of user traffic with < 0.1% error rate for 2 weeks.

### Phase 2: Extract Catalog Service (Weeks 13-20)

**Goal:** Highest-value extraction — enables independent scaling of search

| # | Task | Duration |
|---|------|:--------:|
| 1 | Design Catalog API | 3 days |
| 2 | Build Catalog Service with Elasticsearch for search | 3 weeks |
| 3 | Data migration: Oracle → PostgreSQL (products, categories, inventory) | 2 weeks |
| 4 | Dual-read: Catalog Service reads from PostgreSQL, fallback to Oracle | 1 week |
| 5 | Kong routing: product/search endpoints → Catalog Service | 1 day |
| 6 | Shadow mode for 2 weeks | 2 weeks |
| 7 | Cut over and decommission catalog code from monolith | 3 days |

**Gate:** Catalog search p95 < 200ms (vs 2s in monolith); full feature parity.

### Phase 3: Extract Order + Payment Services (Weeks 21-32)

**Goal:** Most critical extraction — requires saga pattern

| # | Task | Duration |
|---|------|:--------:|
| 1 | Design Order and Payment APIs | 1 week |
| 2 | Build Order Service with SQS-based event publishing | 3 weeks |
| 3 | Build Payment Service with Razorpay integration | 3 weeks |
| 4 | Implement saga: Order → Payment → Notification | 2 weeks |
| 5 | Data migration: order + payment tables → separate PostgreSQL DBs | 2 weeks |
| 6 | Parallel run for payment flows (critical) | 2 weeks |
| 7 | Cut over with canary (5% → 25% → 50% → 100%) | 1 week |

**Gate:** Zero payment discrepancies in parallel run; reconciliation matches.

### Phase 4: Extract Cart + Notification (Weeks 33-38)

| # | Task | Duration |
|---|------|:--------:|
| 1 | Build Cart Service (Redis-backed) | 2 weeks |
| 2 | Build Notification Service (SQS consumer) | 2 weeks |
| 3 | Route and cut over | 2 weeks |

### Phase 5: Decommission Monolith (Weeks 39-42)

| # | Task | Duration |
|---|------|:--------:|
| 1 | Remove all business logic from monolith (only static pages remain) | 1 week |
| 2 | Migrate frontend to Next.js | 2 weeks |
| 3 | Decommission Oracle database | 1 week |
| 4 | Decommission monolith servers | 1 day |

---

## 4. Risk Register

| # | Risk | Probability | Impact | Mitigation |
|---|------|:-----------:|:------:|-----------|
| 1 | Undocumented business logic in monolith | High | High | Shadow mode for every extraction, legacy developer pairing |
| 2 | Oracle → PostgreSQL data type incompatibilities | Medium | Medium | Data profiling + type mapping document before migration |
| 3 | Performance regression in new services | Medium | High | Load testing with production traffic patterns before cutover |
| 4 | Distributed transaction failures (order+payment) | Medium | High | Saga pattern with compensating transactions |
| 5 | Team learning curve (Java → Python) | Medium | Medium | 2-week training bootcamp before Phase 1 |

---

## 5. Success Metrics

| Metric | Before (Monolith) | Target (After) |
|--------|:-----------------:|:--------------:|
| Deployment frequency | Monthly (1/month) | Daily (per service) |
| Deployment duration | 4 hours (maintenance window) | < 5 minutes (zero downtime) |
| Mean time to recovery | 2 hours | < 15 minutes |
| Search latency (p95) | 2,000ms | < 200ms |
| Oracle license cost | $200K/year | $0 |
| Infrastructure cost | $15K/month | $8K/month (PostgreSQL + AWS) |
| Developer onboarding time | 4 weeks | 1 week (per service) |
| Production incidents/month | 3-4 | < 1 |

---

## 6. Timeline Summary

```
Wk 1-6    ████████████ Phase 0: Foundation + Proxy
Wk 7-12   ████████████ Phase 1: User Service
Wk 13-20  ████████████████ Phase 2: Catalog Service
Wk 21-32  ████████████████████████ Phase 3: Order + Payment
Wk 33-38  ████████████ Phase 4: Cart + Notifications
Wk 39-42  ████████ Phase 5: Decommission Monolith
           ────────────────────────────────────────
           Total: ~10 months
```

---

*Generated using Archpilot Migration & Modernization Standards v1.0*
