# Archpilot — Windsurf Rules

> **How to use:** Copy this file to your project root as `.windsurfrules`
> Windsurf (Codeium) will use these instructions for all AI-assisted tasks.

You are an expert software engineer working in an enterprise codebase that follows strict
architecture standards enforced by the Archpilot Standards Library.
Apply these rules to ALL code you write, review, or suggest.

## Architecture Rules

### Layer Separation (STRICT)
```
Controllers/Handlers  →  Services/Use Cases  →  Repositories/Ports  →  Database/External
     (HTTP layer)         (Business logic)       (Data access)          (Infrastructure)
```
- Controllers ONLY handle HTTP concerns (parse request, call service, format response).
- Services contain ALL business logic. Services NEVER import HTTP or DB-specific code.
- Repositories handle data access. One repository per aggregate/entity.
- Cross-cutting concerns (logging, auth, validation) use middleware/decorators.

### Naming Conventions
- Files: `snake_case.py` (Python), `kebab-case.ts` (TypeScript)
- Classes: `PascalCase` — `OrderService`, `PaymentRepository`
- Functions/methods: `snake_case` (Python), `camelCase` (TypeScript)
- Constants: `UPPER_SNAKE_CASE` — `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_MS`
- Database tables: `snake_case`, plural — `orders`, `payment_methods`
- API endpoints: `/kebab-case`, plural — `/payment-methods`
- Environment variables: `UPPER_SNAKE_CASE` with app prefix — `APP_DATABASE_URL`

### Error Handling (MANDATORY)
- EVERY external call (HTTP, DB, queue) MUST have try/except with specific error types.
- EVERY external call MUST have an explicit timeout.
- Log errors with context: `{"action": "create_order", "userId": "...", "error": "...", "duration_ms": 145}`
- Return structured errors to clients, NEVER stack traces.
- Use custom exception classes for domain errors: `OrderNotFoundError`, `InsufficientFundsError`.
- Implement RFC 7807 Problem Details for HTTP APIs.

### Database (STRICT)
- NEVER write raw SQL with string concatenation. Use parameterized queries or ORM.
- Every query that touches user input MUST use parameterized binding.
- Every new table MUST have: `id` (UUID), `created_at` (TIMESTAMPTZ), `updated_at` (TIMESTAMPTZ).
- Indexes: add for every foreign key and every column used in WHERE/ORDER BY at scale.
- Migrations are forward-only. Never delete a column without a deprecation window.

### API Design
- REST endpoints use plural nouns: `/users`, `/orders`, `/payments`
- URL paths in kebab-case: `/payment-methods`, `/order-items`
- HTTP methods: GET (read), POST (create), PUT (full replace), PATCH (partial update), DELETE (remove)
- All endpoints return RFC 7807 error format:
```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Validation Error",
  "status": 422,
  "detail": "Field 'email' must be a valid email address",
  "instance": "/orders/123",
  "correlationId": "uuid"
}
```
- Pagination: cursor-based for large collections. Never offset-based beyond page 10.
- Rate limiting: document limits in API spec. Return `Retry-After` on 429.
- Versioning: URL path versioning `/v1/`, `/v2/` for breaking changes.

### Observability (MANDATORY)
Every service MUST emit:
- **Structured logs** (JSON): `{"timestamp", "level", "service", "traceId", "spanId", "message", "context"}`
- **RED metrics**: Request rate, Error rate, Duration (p50/p95/p99)
- **Health endpoints**: `GET /health/live` (liveness) and `GET /health/ready` (readiness)
- **Distributed traces**: Propagate `traceparent` header (W3C Trace Context)

### Security (NON-NEGOTIABLE)
- Input validation at EVERY entry point — never trust client data.
- Sanitize before logging — strip PII, secrets, tokens.
- Dependencies: `pip audit` / `npm audit` in CI. Block HIGH/CRITICAL CVEs.
- Secrets: NEVER hardcode. Use environment variables or secrets manager.
- CORS: explicit allowlist, never `*` in production.

### Testing Standards
- Unit tests: 80% coverage minimum on service/domain layer.
- Integration tests: every repository method tested against a real DB (no mocks for DB).
- Contract tests: for every external API dependency (consumer-driven, Pact).
- Performance tests: p99 latency target validated under expected peak load.

## Cascade / Flow AI Features

When using Cascade for multi-step tasks:
- Break work into spec → implement → test sequence. Do not skip spec.
- After generating code, always run lint + tests before considering the task done.
- Flag any change that touches auth, secrets, migrations, or public APIs for human review.
