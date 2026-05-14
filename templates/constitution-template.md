# [Project Name] — Architecture Constitution

<!-- This is the project-level "law". It applies to every task, every AI session,
     every code review, and every agent action. It is the highest-priority context
     document in the Spec-Kit hierarchy.
     
     See rule: rules/27-spec-driven-development.md §2.4
     See rule: rules/29-agentic-ai-governance.md §3.1 -->

---

## Document Header

```
Project:         [Project/Product Name]
Constitution ID: CONST-[NNN]
Version:         1.0
Status:          DRAFT | APPROVED | AMENDED
Owner:           [Architect/Tech Lead Name]
Approved By:     [Names]
Date:            [YYYY-MM-DD]
Review Cadence:  [Quarterly / Monthly]
Next Review:     [YYYY-MM-DD]
```

> ?? **This document is immutable during a sprint.** Changes require architect approval.
> All AI agents and developers MUST treat these rules as non-negotiable constraints.

---

## 1. Technology Stack

<!-- Lock the approved technology choices. Unapproved technologies require arch review. -->

### 1.1 Languages & Runtimes

| Language | Version | Approved Use |
|---------|:-------:|-------------|
| TypeScript | 5.x | All backend services, frontend |
| Python | 3.12+ | Data pipelines, ML scripts only |
| SQL | PostgreSQL dialect | Database queries |

### 1.2 Core Frameworks & Libraries

| Category | Technology | Version | Notes |
|----------|-----------|:-------:|-------|
| Backend framework | [e.g., Express / NestJS / FastAPI] | [x.x] | All new services |
| ORM / Data access | [e.g., Prisma / TypeORM] | [x.x] | No raw SQL except migrations |
| Testing | [e.g., Jest / Pytest] | [x.x] | All unit and integration tests |
| Logging | [e.g., Winston / Pino] | [x.x] | JSON structured format only |
| HTTP client | [e.g., Axios / httpx] | [x.x] | No fetch() in Node backend |
| Schema validation | [e.g., Zod / Pydantic] | [x.x] | Validate at every boundary |
| Auth | [e.g., jsonwebtoken] | [x.x] | No auth library replacements |

### 1.3 Infrastructure & Cloud

| Category | Technology | Notes |
|----------|-----------|-------|
| Cloud provider | AWS | No multi-cloud without ADR |
| Compute | ECS Fargate (containers) | No EC2 self-management |
| Database | RDS PostgreSQL 14 | No self-hosted databases |
| Cache | ElastiCache Redis | No in-memory application cache |
| Queue / Events | Amazon SQS + MSK (Kafka) | No RabbitMQ or NATS |
| Secret management | AWS Secrets Manager | No .env files in prod |
| Container registry | ECR | No Docker Hub in production |

---

## 2. Architecture Constraints

<!-- These are design boundaries that cannot be violated without an approved ADR. -->

### 2.1 Service Boundaries

- [ ] Each service MUST own its database. No shared databases between services.
- [ ] Services MUST communicate via APIs or events — no shared libraries that cross service boundaries
- [ ] No synchronous call chains longer than 3 hops — use async for longer chains
- [ ] A new service requires: LLD document + ADR for service boundary decision

### 2.2 Data Constraints

- [ ] PII fields MUST be identified, documented, and encrypted at rest
- [ ] No PII in logs — ever. Use pseudonymized IDs in log entries.
- [ ] Database schemas MUST be changed via migration files only (no manual ALTER TABLE in production)
- [ ] All migration scripts MUST be backward-compatible (old code + new schema must work)

### 2.3 Deployment Constraints

- [ ] All deployments MUST go through CI/CD — no manual deploys
- [ ] Production deployments MUST use blue-green or canary strategy
- [ ] Feature flags MUST be used for any user-facing change larger than a bug fix
- [ ] Infrastructure MUST be defined as code (Terraform) — no manual console changes

---

## 3. Security Non-Negotiables

> ?? **Zero-tolerance rules. Violation blocks merge automatically.**

- [ ] **No hardcoded secrets** — API keys, passwords, tokens, connection strings MUST use Secrets Manager
- [ ] **No SQL concatenation** — all DB queries MUST use parameterized queries or ORM
- [ ] **JWT validation on every request** — no unprotected endpoints except explicitly designed public routes
- [ ] **No admin endpoints without MFA** — all ops/admin APIs require additional auth factor
- [ ] **No PII in logs** — automated scanner enforced in CI
- [ ] **TLS everywhere** — all internal service-to-service calls MUST use TLS 1.2+
- [ ] **Least privilege IAM** — service roles MUST have only the permissions they need; wildcard resource IAM is forbidden
- [ ] **OWASP Top 10 addressed** — SAST scan must pass before merge

---

## 4. Coding Standards

### 4.1 Naming Conventions

| Artifact | Convention | Example |
|---------|-----------|---------|
| TypeScript files | kebab-case | `payment-service.ts` |
| TypeScript classes | PascalCase | `PaymentService` |
| TypeScript functions/variables | camelCase | `processPayment()` |
| TypeScript interfaces | PascalCase + `I` prefix | `IPaymentRepository` |
| Database tables | snake_case, plural | `payment_transactions` |
| Database columns | snake_case | `created_at`, `user_id` |
| REST endpoints | kebab-case, plural nouns | `/payment-methods` |
| Kafka topics | `[domain].[entity].[action]` | `payments.transaction.created` |
| Environment variables | SCREAMING_SNAKE_CASE | `DATABASE_URL` |
| Feature flags | `[team]-[feature]-[state]` | `payments-refunds-enabled` |

### 4.2 Code Structure (All Services)

```
src/
+-- controllers/       # HTTP request/response only. No business logic.
+-- services/          # Business logic only. No HTTP or DB code.
+-- repositories/      # Data access only. No business logic.
+-- events/
¦   +-- producers/     # Event publishing
¦   +-- consumers/     # Event consuming
+-- middleware/        # Cross-cutting: auth, logging, rate-limit
+-- models/            # Types, interfaces, DTOs
+-- config/            # Configuration loading (no hardcoded values)
+-- utils/             # Pure utility functions (no side effects)

test/
+-- unit/              # Mirror of src/ structure. All dependencies mocked.
+-- integration/       # Real HTTP calls, mocked external services
+-- security/          # Auth bypass tests, input validation, injection tests
```

### 4.3 Code Quality Rules

- [ ] No function >40 lines (extract to smaller functions)
- [ ] No file >200 lines (split into modules)
- [ ] No nested callbacks >2 levels deep (use async/await)
- [ ] All public methods MUST have JSDoc / docstring with: purpose, params, return, throws
- [ ] `any` type is FORBIDDEN in TypeScript (use `unknown` and narrow)
- [ ] `console.log` is FORBIDDEN (use structured logger)
- [ ] `TODO` comments MUST include: ticket number and date — `// TODO(TICKET-123, 2026-06-01): description`

---

## 5. Prohibited Patterns

> ?? **These will fail automated code review.**

| Pattern | Why | Alternative |
|---------|-----|-------------|
| `process.env.SECRET_KEY` directly in code | Secrets leak | Use config service that loads from Secrets Manager |
| `SELECT *` queries | Performance and tight coupling | Always select explicit columns |
| Returning raw DB errors to client | Information disclosure | Map to domain errors |
| `catch (e) { }` empty catch | Silent failures | Log error; rethrow or handle explicitly |
| `new Date()` in domain logic | Non-deterministic; hard to test | Inject clock as dependency |
| Circular dependencies between modules | Tight coupling | Restructure using dependency inversion |
| Direct DB calls in controllers | Layering violation | Always go through repository layer |
| Synchronous file I/O | Blocking the event loop | Use async fs methods |
| Global state / singletons without DI | Untestable; side effects | Use dependency injection container |

---

## 6. AI Agent Boundaries

<!-- Rules for what AI agents may and may not do autonomously. -->

| Action | Agent May Do? | Required Approval |
|--------|:------------:|------------------|
| Write new feature code | ? Autonomously | None (within task scope) |
| Write unit tests | ? Autonomously | None |
| Create new files within task scope | ? Autonomously | None |
| Modify migration files | ?? Draft only | Human DBA review required |
| Modify `constitution.md` | ?? Never | — |
| Modify `.env` or secrets config | ?? Never | — |
| Commit to `main` or `release` | ?? Never | — |
| Call production APIs | ?? Never | — |
| Provision cloud resources | ?? Never | — |
| Delete files | ?? With confirmation | Human must confirm |
| Modify CI/CD pipeline | ?? Draft only | Platform team review |

**Agent context loading rule:** Each agent session loads ONLY:
1. This constitution (always)
2. The specific task from tasks.md
3. The files that task modifies
4. Relevant sections of design.md

Do NOT load the entire codebase into an agent context.

---

## 7. Definition of Done

Every user story / task is "Done" when:

- [ ] All acceptance criteria in the task pass
- [ ] Unit test coverage =80% on new code
- [ ] Integration tests pass for affected flows
- [ ] Linting and type-check pass with zero errors
- [ ] Security scan passes (no Critical or High findings)
- [ ] No PII in logs (automated scanner pass)
- [ ] OpenAPI spec updated if endpoints changed
- [ ] RTM updated — spec requirement mapped to passing test
- [ ] PR reviewed by at least one human (cannot be auto-merged by agent)
- [ ] Monitoring/alerting verified in staging

---

## 8. Change Log

| Version | Date | Author | Change | Approved By |
|---------|------|--------|--------|-------------|
| 1.0 | YYYY-MM-DD | | Initial constitution | |

---

*Archpilot — Spec-Driven Development Constitution Template*
*See: rules/27-spec-driven-development.md, rules/29-agentic-ai-governance.md*
