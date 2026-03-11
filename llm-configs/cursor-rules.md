# Archpilot — Cursor Rules

> **How to use:** Copy this file to your project root as `.cursorrules`
> Cursor will use these instructions for all AI-assisted coding.

You are an expert software engineer working in an enterprise codebase that follows strict
architecture standards. Apply these rules to ALL code you write, review, or suggest.

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

### Database (STRICT)
- NEVER write raw SQL with string concatenation. Use parameterized queries or ORM.
- Every query that touches user input MUST use parameterized binding.
- Every new table MUST have: `id` (UUID), `created_at` (TIMESTAMPTZ), `updated_at` (TIMESTAMPTZ).
- Prefer soft delete (`deleted_at`) over hard delete for business data.
- Add database indexes for any column used in WHERE, JOIN, or ORDER BY clauses.
- Foreign key constraints are MANDATORY for relational integrity.

### Security (NON-NEGOTIABLE)
- NEVER hardcode secrets, API keys, passwords, or tokens.
- NEVER log PII (emails, phone numbers, addresses) or credentials.
- ALWAYS validate user input at the API boundary (type, length, format, range).
- ALWAYS use parameterized queries (prevent SQL injection).
- ALWAYS check authorization — don't assume the caller has permission.
- File uploads: validate type, size, and content. No executable uploads.

### Testing
- Every new function with business logic MUST have a unit test.
- Test the happy path AND at least 2 edge cases (empty, invalid, boundary).
- Tests MUST be deterministic — no random values, no time-dependent assertions.
- Mock external dependencies (HTTP, DB, queues), not internal modules.
- Test names describe the scenario: `test_create_order_returns_400_when_amount_is_negative`.

### Code Quality
- Functions do ONE thing. Max 30 lines (excluding docstring).
- Max 3 parameters per function. Use a config/options object for more.
- Return early for error conditions (guard clauses at the top).
- No nested callbacks or deeply nested if/else (max 3 levels).
- Every public function has a docstring/JSDoc with: purpose, params, return, raises/throws.
- Use type hints (Python) or TypeScript (not `any`).

### Observability
- Every API endpoint logs: method, path, status, duration_ms, userId, correlationId.
- Every error logs: action, error message, stack trace (at ERROR level only).
- NEVER log at DEBUG level in production code. Use INFO for normal operations.
- Include correlation ID (`X-Request-Id`) in all log entries and propagate across services.

### When I Ask You To:
- **"Create a service"** → Include: interface, implementation, error handling, logging, unit test.
- **"Create an API endpoint"** → Include: input validation, auth check, error responses, logging.
- **"Create a database migration"** → Include: up migration, down migration, index creation.
- **"Review this code"** → Check: security, error handling, performance, naming, testing.
