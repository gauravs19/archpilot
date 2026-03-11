# Archpilot — VS Code / GitHub Copilot Instructions

> **How to use:** Copy this file to your project as `.github/copilot-instructions.md`
> GitHub Copilot will use these instructions as context for all code suggestions and chat.

---

## Architecture Standards

You are working in a codebase that follows strict enterprise architecture standards.
Apply these principles to ALL code suggestions, completions, and explanations.

### Design Principles
1. **Separation of Concerns** — Business logic MUST be in service/domain layer, NOT in controllers or handlers.
2. **Repository Pattern** — Database access through repository classes. No raw queries in services.
3. **Dependency Injection** — Components receive dependencies through constructors, not global imports.
4. **Interface-First** — Define interfaces/protocols before implementations.
5. **Single Responsibility** — Each class/module has exactly one reason to change.

### API Standards
- REST endpoints use plural nouns: `/users`, `/orders`, `/payments`
- URL paths in kebab-case: `/payment-methods`, `/order-items`
- HTTP methods: GET (read), POST (create), PUT (full replace), PATCH (partial update), DELETE (remove)
- All endpoints return consistent error format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "correlationId": "uuid"
  }
}
```
- Pagination uses cursor-based approach (not offset)
- All request bodies are validated at the API boundary
- Status codes: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Validation Error), 429 (Rate Limited), 500 (Server Error)

### Database Standards
- Use parameterized queries — NEVER string concatenation for SQL
- All tables have: `id` (UUID PK), `created_at`, `updated_at`, `created_by`
- Use TIMESTAMPTZ for timestamps (timezone-aware)
- Soft delete with `deleted_at` column for business data
- Add indexes on: foreign keys, WHERE clause columns, ORDER BY columns
- Column names in snake_case

### Error Handling
- Every external call has: timeout, retry with backoff, circuit breaker
- Catch specific exceptions, not generic Exception
- Log errors with: correlation ID, context, duration, outcome
- Return appropriate HTTP status codes (not 200 for everything)
- Never expose stack traces or internal paths to clients

### Security
- Validate and sanitize ALL user input
- Use parameterized queries (SQL injection prevention)
- Never log passwords, tokens, PII, or credit card numbers
- Check authorization at the endpoint level
- Secrets come from environment/secrets manager, never hardcoded
- Use short-lived tokens (JWT with 15-30 min expiry)

### Observability
- Use structured logging (JSON format)
- Include correlation ID in every log entry
- Log at appropriate levels: INFO (normal ops), WARN (recovered issues), ERROR (failures)
- Emit metrics for: request count, latency, error rate, queue depth
- Propagate trace context across service calls

### Testing
- Write unit tests for business logic (80%+ coverage)
- Write integration tests for API endpoints
- Test edge cases: empty input, boundary values, null, duplicate
- Tests are independent and deterministic (no shared state)
- Use descriptive test names that explain the scenario

### Code Style
- Functions/methods do one thing. If it needs "and" in the name, split it.
- Maximum function length: 30 lines (excluding comments/docstrings)
- Return early for error conditions (guard clauses)
- Prefer explicit over implicit. No magic numbers — use named constants.
- Every public function/method has a docstring explaining purpose, parameters, and return value.

### When Generating New Code
- Always include error handling (not just the happy path)
- Always include input validation
- Always include logging for key operations
- Always add type hints (Python) or type annotations (TypeScript)
- Always include a TODO comment for anything that needs future work
- Prefer async/await for I/O-bound operations
