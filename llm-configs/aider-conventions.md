# Archpilot — Aider Conventions

> **How to use:** Copy relevant sections into `.aider.conf.yml` or reference this file
> with `--read llm-configs/aider-conventions.md` in your aider session.

---

## Recommended Aider Setup

```yaml
# .aider.conf.yml — place at project root
model: claude-sonnet-4-6        # or claude-opus-4-8 for complex design tasks
edit-format: udiff               # cleanest for large refactors
auto-commits: false              # always review before committing
dirty-commits: false
read:
  - llm-configs/aider-conventions.md
  - rules/00-architecture-principles.md
  - rules/27-spec-driven-development.md
```

---

## Coding Conventions (Aider will apply these to every edit)

### Python
```python
# File structure: always in this order
# 1. Module docstring
# 2. Imports (stdlib → third-party → local)
# 3. Constants
# 4. Classes / functions
# 5. if __name__ == "__main__"

# Type hints: mandatory on all public functions
def process_order(order_id: str, user_id: str) -> dict:
    ...

# Errors: raise specific exceptions with context
raise OrderNotFoundError(f"Order {order_id} not found for user {user_id}")

# Logging: structured, with context
logger.info("order.processed", extra={
    "order_id": order_id,
    "user_id": user_id,
    "duration_ms": elapsed
})
```

### TypeScript / JavaScript
```typescript
// Strict mode always enabled
// Return types mandatory on all exported functions
export async function createOrder(dto: CreateOrderDto): Promise<OrderResponse> { ... }

// No `any` — use `unknown` and narrow, or define a type
// Error handling: always typed
try {
  ...
} catch (error: unknown) {
  if (error instanceof AppError) { ... }
  throw error;
}
```

---

## Architecture Workflow with Aider

Follow this sequence for every feature — do NOT skip steps:

### Step 1: Update the spec first
```bash
aider .specs/requirements.md
# Prompt: "Add a user story for [feature] following EARS notation with measurable ACs"
```

### Step 2: Update or create LLD
```bash
aider .specs/Design_LLD_[Service].md
# Prompt: "Add API endpoint spec and sequence diagram for [feature] to the [Service] LLD"
```

### Step 3: Implement
```bash
aider src/services/order.service.ts src/repositories/order.repository.ts
# Prompt: "Implement the createOrder method per the LLD spec"
```

### Step 4: Write tests
```bash
aider tests/unit/order.service.test.ts tests/integration/order.repository.test.ts
# Prompt: "Write unit + integration tests for createOrder with the acceptance criteria from the LLD"
```

### Step 5: Lint and validate
```bash
python archpilot.py lint --tier 2
```

---

## What Aider Should Never Do

- Do NOT add placeholder comments like `# TODO: implement later`
- Do NOT leave `pass` or `NotImplementedError` in production paths
- Do NOT skip error handling on external calls
- Do NOT hardcode secrets, URLs, or environment-specific values
- Do NOT create a new abstraction for fewer than 3 usages
- Do NOT generate code without first checking the relevant LLD exists

---

## Useful Aider Commands for Archpilot Projects

```bash
# Start a design session (read-only context from rules)
aider --read rules/03-hld-standards.md --read rules/05-api-design.md

# Implement from LLD
aider --read .specs/Design_LLD_PaymentService.md \
      src/services/payment.service.ts \
      src/repositories/payment.repository.ts

# Review a file against architecture principles
aider --read rules/00-architecture-principles.md \
      --message "Review this file for architecture violations" \
      src/services/order.service.ts

# Generate tests for a service
aider --read .specs/Design_LLD_OrderService.md \
      --message "Generate integration tests for OrderService per the LLD acceptance criteria" \
      tests/integration/order.service.test.ts
```
