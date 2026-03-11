# Code Review Guidelines (Architecture-Aware)

> **Purpose:** Code review standards that go beyond syntax and style — focusing on
> architecture smells, design patterns, performance, security, and maintainability.

---

## How to Use This File

- **Code Reviews:** Use as a review checklist for pull requests
- **Any LLM:** Say: *"Using these review guidelines, review this code: [paste code]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [05 — API Design](./05-api-design.md) | API-specific review standards |
| [07 — Security Architecture](./07-security-architecture.md) | Security review depth |
| [12 — Observability](./12-observability-standards.md) | Logging and tracing review |
| [04 — LLD Standards](./04-lld-standards.md) | Design-level review standards |

---

## 1. Review Priorities

Review in this order of importance:

| Priority | Focus | Question to Ask |
|:--------:|-------|----------------|
| 🔴 **P0** | **Correctness** | Does it do what it's supposed to? |
| 🔴 **P1** | **Security** | Can this be exploited? Is data protected? |
| 🟠 **P2** | **Architecture** | Does it follow our patterns? Will it scale? |
| 🟡 **P3** | **Performance** | Are there obvious performance issues? |
| 🟢 **P4** | **Maintainability** | Can someone else understand and modify this? |
| 🔵 **P5** | **Style** | Does it follow coding conventions? (Automate this!) |

**Rule:** Style issues (P5) SHOULD be caught by linters/formatters, not humans. Reviewers focus on P0-P4.

---

## 2. Architecture Review Checks

### 2.1 Separation of Concerns
- [ ] Business logic is NOT in controllers/handlers (should be in service/domain layer)
- [ ] Database queries are NOT in API handlers (use repository pattern)
- [ ] Infrastructure concerns (HTTP, DB, messaging) are isolated from domain logic
- [ ] No god classes/modules doing too many things

### 2.2 API Design
- [ ] New endpoints follow REST conventions (from `rules/05-api-design.md`)
- [ ] Error responses use standard error format with error codes
- [ ] Input validation at the API boundary (not deep in business logic)
- [ ] Pagination on list endpoints
- [ ] No breaking changes to existing API contracts

### 2.3 Data Access
- [ ] No N+1 query patterns (eager loading where needed)
- [ ] Parameterized queries (no string concatenation for SQL)
- [ ] Appropriate indexes for new query patterns
- [ ] Database migrations are backward-compatible
- [ ] No raw SQL in application code without justification

### 2.4 Dependency Management
- [ ] No new heavyweight dependencies for simple tasks
- [ ] Dependencies are pinned to specific versions
- [ ] No known vulnerabilities in new dependencies
- [ ] Circular dependencies between modules/services are avoided

### 2.5 Configuration
- [ ] No hardcoded values (URLs, credentials, thresholds)
- [ ] Configuration is environment-aware
- [ ] Feature flags for new features (not hardcoded booleans)
- [ ] Secrets are NOT in code, configs, or environment variable files

---

## 3. Security Review Checks

- [ ] No credentials, tokens, or API keys in code
- [ ] User input is validated AND sanitized
- [ ] SQL queries use parameterized statements
- [ ] Authentication is checked on new endpoints
- [ ] Authorization is checked (correct role/permission for the action)
- [ ] Sensitive data is not logged (PII, tokens, passwords)
- [ ] File uploads are validated (type, size, content)
- [ ] External URLs are validated (SSRF prevention)
- [ ] CORS settings are restrictive (not `*`)
- [ ] Rate limiting is applied to public-facing endpoints

---

## 4. Performance Review Checks

- [ ] No database queries inside loops (N+1 problem)
- [ ] Large result sets are paginated (not loading all into memory)
- [ ] Expensive operations are cached where appropriate
- [ ] Async processing for non-critical, slow operations
- [ ] Connection pools are used for DB/HTTP clients (not per-request connections)
- [ ] No unbounded collections (arrays/lists that can grow without limit)
- [ ] Timeouts set for all external calls
- [ ] Response payloads are reasonably sized (no unnecessary data)

---

## 5. Error Handling Review

- [ ] All external calls have error handling (try/catch, circuit breaker)
- [ ] Errors are logged with sufficient context for debugging
- [ ] Error responses don't leak internal details (stack traces, DB errors)
- [ ] Retryable operations have retry logic with backoff
- [ ] Non-retryable failures fail fast with clear error messages
- [ ] Null/empty cases are handled (no NullPointerException equivalents)

---

## 6. Testing Review

- [ ] New code has corresponding unit tests
- [ ] Edge cases are tested (empty input, boundary values, nulls)
- [ ] Integration tests for new API endpoints or DB operations
- [ ] Tests are deterministic (no flaky tests, no time-dependent assertions)
- [ ] Test names clearly describe what they're testing
- [ ] Mocks are appropriate (not mocking what you own, mock what you don't)

---

## 7. Observability Review

- [ ] Key operations have structured log statements
- [ ] Correlation ID is propagated (not starting a new one)
- [ ] New metrics are emitted for important operations
- [ ] Error paths have ERROR-level logging with context
- [ ] No sensitive data in logs or traces
- [ ] Health check endpoint updated if new dependencies are added

---

## 8. PR Description Standards

Every PR MUST include:

```markdown
## What
<!-- What does this PR do? 1-2 sentences -->

## Why
<!-- Why is this change needed? Link to ticket/issue -->

## How
<!-- Brief description of the approach -->

## Testing
<!-- How was this tested? What test cases were added? -->

## Rollback
<!-- How to rollback if this causes issues in production -->

## Checklist
- [ ] Unit tests added/updated
- [ ] No secrets in code
- [ ] API changes are backward-compatible
- [ ] Database migration is reversible
- [ ] Logging added for key operations
```

---

## 9. Common Review Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Nitpicking style** | Wastes time on formatting | Use linters/formatters (automate P5) |
| **Rubber-stamping** | "Looks good" without reading | Minimum 1 substantive comment per PR |
| **Gatekeeping** | PR blocked for days, no feedback | Respond within 4 business hours |
| **Scope creep in review** | Requesting unrelated improvements | Separate "must fix" from "nice to have" |
| **No context** | PR with no description | Reject PRs without description |
| **Reviewing only the diff** | Miss broader architectural impact | Check file context, not just changed lines |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
