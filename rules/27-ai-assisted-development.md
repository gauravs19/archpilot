# AI-Assisted Development Standards

> **Purpose:** Architecture and code review standards for teams using AI coding tools
> (Cursor, GitHub Copilot, Claude, Windsurf). Covers the failure modes specific to
> AI-generated code and the review patterns needed to catch them before production.

---

## How to Use This File

- **Code Review:** *"Using these standards, review this AI-generated code for production readiness: [paste code]"*
- **Pre-Launch Audit:** *"Apply the AI-assisted development checklist to my codebase at [path] and flag any issues"*
- **Team Standards:** Add to your `.cursorrules` or Cursor project instructions to prime AI tools to avoid these patterns

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [15 — Code Review Guidelines](./15-code-review-guidelines.md) | §10 adds AI-specific review checks |
| [07 — Security Architecture](./07-security-architecture.md) | Depth on OWASP, STRIDE, zero-trust |
| [06 — Data Architecture](./06-data-architecture.md) | Data integrity, migration standards |
| [12 — Observability Standards](./12-observability-standards.md) | Structured logging, correlation IDs |
| [26 — AI/ML Architecture](./26-ai-ml-architecture.md) | Building AI *systems* (RAG, MLOps, agents) — distinct from this file |

> **Scope distinction:** `26-ai-ml-architecture.md` covers designing AI/ML systems.
> This file covers auditing code *generated* by AI development tools.

---

## The Core Mental Model

AI coding tools generate syntactically correct, semantically naive code. They:

- **Optimize for the happy path.** Error handling, edge cases, and failure modes are consistently underweighted.
- **Have no operational context.** They don't know your load profile, your tenant isolation requirements, or your DB constraints.
- **Are data-blind.** They know your schema but not your data volume, your hotspot queries, or which columns have NULLs in 40% of rows.
- **Generate modules in isolation.** Each function or module is coherent in isolation. Integration contracts between modules are implicit and frequently incompatible.
- **Draw from training data, not production telemetry.** Package suggestions, pattern choices, and configuration defaults reflect training-time popularity, not current CVE status or production fitness.

This doesn't make AI tools dangerous — it makes them **junior collaborators**. You ship with a senior review.

---

## Part A — Security Failure Modes

### A.1 Prototype Pollution

AI commonly uses `lodash.merge`, `Object.assign`, or recursive merge utilities with user-controlled input without understanding prototype pollution risk.

**Tell:** Deep merge of user-supplied objects into application config or state.

```javascript
// ❌ AI-generated — prototype pollution via __proto__
_.merge(config, userSettings);

// ✅ Use a safe merge that ignores prototype keys
const safeSettings = JSON.parse(JSON.stringify(userSettings)); // strips prototype chain
_.merge(config, safeSettings);

// Or validate explicitly
if ('__proto__' in userSettings || 'constructor' in userSettings) {
  throw new Error('Invalid settings');
}
```

### A.2 JWT Algorithm Confusion

AI generates `jwt.verify(token, secret)` without specifying the `algorithms` option, allowing an attacker to switch the token to `alg: none` or RS256 with a public key as the HMAC secret.

**Tell:** Any `jwt.verify()` call without an explicit `algorithms` array.

```javascript
// ❌ AI-generated — no algorithm constraint
const payload = jwt.verify(token, process.env.JWT_SECRET);

// ✅ Explicit algorithm list
const payload = jwt.verify(token, process.env.JWT_SECRET, {
  algorithms: ['HS256']
});
```

### A.3 SSRF via User-Controlled URLs

AI generates HTTP fetch calls using user-supplied URLs without validation, enabling Server-Side Request Forgery — attackers can target internal services, cloud metadata endpoints (169.254.169.254), or loop back to the application itself.

**Tell:** `fetch(url)`, `axios.get(url)`, or `http.request(url)` where `url` is user-supplied.

```javascript
// ❌ AI-generated — no SSRF protection
const response = await fetch(req.body.webhookUrl);

// ✅ Validate against allowlist of permitted domains/schemes
const allowedHosts = ['api.example.com', 'hooks.partner.com'];
const parsed = new URL(req.body.webhookUrl);
if (!allowedHosts.includes(parsed.hostname)) {
  throw new AppError('URL not permitted', 400);
}
const response = await fetch(req.body.webhookUrl);
```

### A.4 Non-Null Assertion as Env Var Tell

TypeScript `!` non-null assertions on `process.env` lookups are the AI equivalent of "I know this exists but didn't bother to check." They silence TypeScript and let the application start with missing config — failing silently at runtime.

**Tell:** `process.env.SOME_VAR!` anywhere in the codebase.

```typescript
// ❌ AI-generated — silences TypeScript, blows up at runtime
const client = new Stripe(process.env.STRIPE_SECRET_KEY!);

// ✅ Validate at startup, fail fast with a clear message
function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Required environment variable ${name} is not set`);
  return value;
}

const client = new Stripe(requireEnv('STRIPE_SECRET_KEY'));
```

**Pattern:** Run env validation as the first thing in `main()` / app startup. Never inline `!` assertions for env vars.

### A.5 Dependency Selection Risk

AI selects packages based on training data popularity, not current CVE status. A package that was dominant in training data may have known vulnerabilities in the version AI suggests.

**Mandatory gates:**
```bash
npm audit --audit-level=high    # fail CI on high/critical
npx npm-check-updates           # surface packages with available security patches
npx depcheck                    # remove packages AI added but aren't actually used
```

---

## Part B — Data Integrity Failure Modes

### B.1 Missing WHERE Clauses

AI generates UPDATE and DELETE statements in the happy path (update this record) but forgets to scope them when the user's instruction was slightly ambiguous. A missing WHERE clause is a table-wipe waiting for a bug.

**Tell:** Any `UPDATE` or `DELETE` without a mandatory row-scoping WHERE clause.

```sql
-- ❌ AI-generated — updates every row
UPDATE subscriptions SET status = 'cancelled';

-- ✅ Scope to specific record
UPDATE subscriptions SET status = 'cancelled' WHERE id = $1 AND user_id = $2;
```

**Code review rule:** Every `UPDATE` and `DELETE` must have a WHERE clause. No exceptions without documented justification.

### B.2 Race Conditions in Increment Patterns

AI generates read-modify-write patterns for counters, balances, and inventory. Under concurrent load these produce lost updates — two requests read the same value and both write it back incremented by one, when the true result should be incremented by two.

**Tell:** Pattern: `const x = record.value; ... update({ value: x + 1 })`.

```javascript
// ❌ AI-generated — read-modify-write, race condition
const user = await db.users.findById(userId);
await db.users.update({ credits: user.credits - amount });

// ✅ Atomic update at the database level
await db.users.update({
  credits: db.raw('credits - ?', [amount])
}, {
  where: { id: userId, credits: db.gte(amount) } // guard against going negative
});
```

### B.3 Multi-Tenant Query Isolation

AI generates queries by resource ID without understanding multi-tenancy. Without explicit `orgId`/`tenantId` scoping, a user from Org A can access Org B's data by guessing resource IDs.

**Tell:** Any query that fetches by `id` alone without a tenant discriminator.

```javascript
// ❌ AI-generated — IDOR vulnerability, no tenant scope
const document = await db.documents.findById(req.params.id);

// ✅ Always scope to the authenticated tenant
const document = await db.documents.findOne({
  where: { id: req.params.id, orgId: req.user.orgId }
});
if (!document) throw new NotFoundError();
```

**Architecture rule:** Every query on a multi-tenant table must include the tenant discriminator. Add Row-Level Security (RLS) at the database layer as defense-in-depth.

### B.4 Missing Database-Level Constraints

AI adds validation in application code but omits the matching DB constraints. Application-layer validation can be bypassed (direct DB writes, migrations, batch scripts). The database is the last line of defense.

**Rule:** For every application-layer validation, ask: "what enforces this at the DB layer?"
- Uniqueness: `UNIQUE` constraint, not just `findOne` then `create`
- Non-null: `NOT NULL` constraint
- Range/domain: `CHECK` constraint
- Referential integrity: `FOREIGN KEY`

---

## Part C — Error Handling Failure Modes

### C.1 Swallowed Catch Blocks

AI generates try/catch blocks that log the error and continue execution as if nothing happened. The operation failed, but the caller gets a success response.

**Tell:** `catch` block that only calls `console.error()` (or `logger.error()`) with no re-throw, no error response, and no state rollback.

```javascript
// ❌ AI-generated — swallowed error, silent failure
async function chargeCustomer(id, amount) {
  try {
    await stripe.charges.create({ amount, customer: id });
  } catch (err) {
    console.error('Charge failed:', err);
    // function returns undefined — caller assumes success
  }
}

// ✅ Fail loudly, preserve cause chain
async function chargeCustomer(id, amount) {
  try {
    await stripe.charges.create({ amount, customer: id });
  } catch (err) {
    throw new PaymentError(`Charge failed for customer ${id}`, { cause: err });
  }
}
```

### C.2 Error Serialization Stripping the Cause Chain

`JSON.stringify(new Error('...'))` returns `{}` in Node.js — the message and stack are non-enumerable properties. AI frequently logs `JSON.stringify(err)` losing all diagnostic context.

**Tell:** `JSON.stringify(error)` or `logger.error({ error })` where `error` is an Error object.

```javascript
// ❌ AI-generated — logs empty object
logger.error({ error: err }, 'Payment failed');

// ✅ Serialize explicitly
logger.error({
  error: {
    message: err.message,
    code: err.code,
    stack: err.stack,
    cause: err.cause?.message,
  }
}, 'Payment failed');
```

### C.3 Missing Correlation ID Propagation

AI generates logging statements but doesn't thread a request-scoped correlation ID through the call chain. In production, logs from a single failed request are unlinked — impossible to reconstruct the event sequence.

**Tell:** Log statements with no `requestId` or `correlationId` field, or a new UUID generated at the log call site.

```javascript
// ❌ AI-generated — no correlation context
logger.error({ userId }, 'Payment failed');

// ✅ Use AsyncLocalStorage to propagate correlation ID without passing it everywhere
import { AsyncLocalStorage } from 'async_hooks';
export const requestContext = new AsyncLocalStorage<{ requestId: string }>();

// In middleware:
app.use((req, res, next) => {
  const requestId = req.headers['x-request-id'] ?? crypto.randomUUID();
  requestContext.run({ requestId }, next);
});

// In any log call:
const ctx = requestContext.getStore();
logger.error({ requestId: ctx?.requestId, userId }, 'Payment failed');
```

---

## Part D — Scalability Failure Modes

### D.1 Connection Pool Misconfiguration for Serverless

AI generates database connection config for always-on servers. In serverless or container-per-request environments (Vercel, Lambda, Cloud Run), each instance creates its own connection pool — exhausting database connections under load.

**Tell:** Standard `DATABASE_URL` or `pg.Pool({ max: 10 })` config in a serverless deployment context.

```javascript
// ❌ AI-generated — creates pool per instance, breaks at scale
const pool = new Pool({ connectionString: process.env.DATABASE_URL, max: 10 });

// ✅ For serverless: limit to 1 connection per instance + use PgBouncer externally
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 1,
});

// Architecture rule: use PgBouncer or Neon/Supabase connection pooler in front
// of Postgres in any serverless or horizontally-scaled deployment
```

### D.2 Cache Stampede

AI adds caching without the single-flight pattern. When a cached value expires under high concurrency, all concurrent requests miss the cache simultaneously and all hit the database — the "thundering herd."

**Tell:** `const cached = await cache.get(key); if (!cached) { const result = db.query(...); await cache.set(key, result); return result; }` with no lock or deduplication.

```javascript
// ❌ AI-generated — stampede under load
async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  const user = await db.users.findById(id); // all requests hit this simultaneously
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 300);
  return user;
}

// ✅ Single-flight: deduplicate concurrent requests for the same key
const inflight = new Map<string, Promise<User>>();

async function getUser(id: string) {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  if (!inflight.has(id)) {
    const p = db.users.findById(id)
      .then(user => {
        redis.set(`user:${id}`, JSON.stringify(user), 'EX', 300);
        inflight.delete(id);
        return user;
      });
    inflight.set(id, p);
  }
  return inflight.get(id)!;
}
```

### D.3 CPU-Bound Work in Async Paths

AI conflates "async" with "non-blocking." `async/await` only yields for I/O — CPU-bound work (parsing, encryption, large JSON serialization, RegEx on user input) blocks the Node.js event loop regardless of the async wrapper.

**Tell:** Heavy computation inside an async function with no worker thread offload.

```javascript
// ❌ AI-generated — blocks event loop
app.post('/import', async (req, res) => {
  const rows = parseCSV(req.body); // CPU-bound, blocks all other requests
  const results = rows.map(transformRow);
  res.json({ count: results.length });
});

// ✅ Offload to worker thread or queue
import { Worker } from 'worker_threads';

app.post('/import', async (req, res) => {
  const jobId = await queue.add('csv-import', { data: req.body });
  res.json({ jobId }); // respond immediately, process async
});
```

### D.4 Query Timeouts Absent

AI is schema-aware but data-blind. A query that's fast on a seeded dev database with 100 rows may full-scan a 10M row production table. Without statement timeouts, a runaway query holds a connection open indefinitely.

**Tell:** No `statement_timeout` in DB config, no timeout option on individual query calls.

```javascript
// ✅ Set statement_timeout at connection level (Postgres)
await pool.query("SET statement_timeout = '5000'"); // 5s max

// ✅ Or per-query for critical paths
await pool.query({
  text: 'SELECT * FROM events WHERE user_id = $1',
  values: [userId],
  // driver-level timeout (separate from statement_timeout)
});

// ✅ In knex/Sequelize: configure globally
const knex = Knex({
  client: 'pg',
  connection: { ... },
  pool: { acquireTimeoutMillis: 5000 }
});
```

---

## Part E — Ops Readiness Failure Modes

### E.1 Destructive Migrations

AI generates `NOT NULL` column additions without defaults. In Postgres, this locks the table while backfilling. On a large table this can mean minutes of downtime. Worse, AI sometimes generates `NOT NULL` with no default and no backfill at all — which fails immediately on any table with existing rows.

**Tell:** Migration with `ADD COLUMN ... NOT NULL` and no `DEFAULT` clause on a non-empty table.

```sql
-- ❌ AI-generated — locks table, fails if rows exist
ALTER TABLE users ADD COLUMN tier VARCHAR(20) NOT NULL;

-- ✅ Expand-backfill-contract pattern
-- Step 1: Add nullable
ALTER TABLE users ADD COLUMN tier VARCHAR(20);
-- Step 2: Backfill existing rows (can run online)
UPDATE users SET tier = 'free' WHERE tier IS NULL;
-- Step 3: Add NOT NULL constraint after backfill
ALTER TABLE users ALTER COLUMN tier SET NOT NULL;
```

**Rule:** Every destructive migration (NOT NULL additions, column drops, type changes, index drops) requires a rollback script in the same PR.

### E.2 No Graceful Shutdown

AI generates Express/Fastify apps that don't handle `SIGTERM`. When Kubernetes or a PaaS terminates a container, in-flight requests are dropped — users get connection resets mid-transaction.

**Tell:** No `process.on('SIGTERM', ...)` handler.

```javascript
// ✅ Graceful shutdown
const server = app.listen(PORT, () => console.log(`Listening on ${PORT}`));

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('HTTP server closed');
    pool.end(); // close DB connections
    process.exit(0);
  });

  // Force exit if connections don't drain within 30s
  setTimeout(() => process.exit(1), 30_000);
});
```

### E.3 Missing Startup Env Validation

AI inlines `process.env.X` calls throughout the codebase. Missing env vars surface as runtime errors deep in request paths — not at startup where they're easy to diagnose and fix.

**Pattern:** Validate all required env vars at startup, fail fast with a clear error listing what's missing.

```javascript
// ✅ Centralized env validation at startup
const REQUIRED_ENV = [
  'DATABASE_URL',
  'STRIPE_SECRET_KEY',
  'JWT_SECRET',
  'REDIS_URL',
];

const missing = REQUIRED_ENV.filter(key => !process.env[key]);
if (missing.length > 0) {
  console.error('Missing required environment variables:', missing.join(', '));
  process.exit(1);
}
```

---

## Part F — Composition Failure Modes

### F.1 Works in Isolation, Fails in Composition

AI generates modules that are internally coherent but carry implicit contracts that conflict when composed. This is the most common AI-specific production failure mode that doesn't appear in unit tests.

**Example:** Module A generates UUIDs as strings. Module B expects UUID objects. Module A returns null for missing records. Module B expects an empty array. Both work perfectly in their own tests — the integration fails.

**Pattern:** Validate contracts at integration boundaries with explicit schemas.

```typescript
// ❌ AI-generated — implicit contract, breaks at integration
// user-service.ts: returns null if not found
async function getUser(id: string): Promise<User | null> { ... }

// payment-service.ts: assumes user always exists
async function charge(userId: string) {
  const user = await userService.getUser(userId);
  return stripe.charge(user.stripeId, amount); // TypeError: Cannot read property 'stripeId' of null
}

// ✅ Explicit contracts at integration boundaries
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string().uuid(),
  stripeId: z.string().startsWith('cus_'),
  email: z.string().email(),
});

async function charge(userId: string) {
  const rawUser = await userService.getUser(userId);
  if (!rawUser) throw new NotFoundError(`User ${userId} not found`);
  const user = UserSchema.parse(rawUser); // validates shape, throws if malformed
  return stripe.charge(user.stripeId, amount);
}
```

**Review rule:** Any module boundary where AI-generated code calls other AI-generated code is a composition risk point. Explicit runtime schema validation (Zod, Joi, class-validator) at these boundaries is the mitigation.

### F.2 Incompatible Error Handling Contracts

AI generates inconsistent error handling across modules — some throw, some return `null`, some return `{ error, data }` tuples. The inconsistency isn't visible until composition.

**Tell:** Mixed patterns across the same codebase: some functions throw on not-found, others return null.

**Rule:** Establish a single error contract per layer and enforce it. Either throw custom errors and catch at the boundary, or return Result types — not both.

---

## AI-Assisted Development — Code Review Checklist

Use this as a final gate before merging AI-generated code to main.

### Security
- [ ] No `!` non-null assertions on `process.env` lookups
- [ ] `jwt.verify()` specifies `algorithms` option explicitly
- [ ] Deep merge utilities not used with user-supplied objects without sanitization
- [ ] External URLs from user input validated against an allowlist
- [ ] `npm audit --audit-level=high` returns clean
- [ ] No hardcoded credentials, tokens, or API keys

### Data Integrity
- [ ] Every `UPDATE`/`DELETE` has a WHERE clause with at minimum the primary key
- [ ] Concurrent counter/balance operations use atomic DB updates, not read-modify-write
- [ ] Multi-tenant queries include `orgId`/`tenantId` scope, not just resource ID
- [ ] Database-level constraints exist for all application-layer validations

### Error Handling
- [ ] No catch blocks that only log and continue (swallowed errors)
- [ ] Error objects serialized with `.message`, `.stack`, `.cause` — not `JSON.stringify(err)`
- [ ] Correlation ID propagated through async call chains (not generated per log call)

### Scalability
- [ ] DB connection pool sized for deployment target (serverless: `max: 1` + pooler)
- [ ] Cache patterns include stampede protection for high-concurrency paths
- [ ] CPU-bound operations not blocking the event loop — offloaded to workers/queues
- [ ] Statement timeouts configured at DB or query level

### Ops Readiness
- [ ] `NOT NULL` migrations use expand-backfill-contract pattern with rollback script
- [ ] SIGTERM handler implemented with in-flight request drain
- [ ] All required env vars validated at startup with `process.exit(1)` on missing

### Composition
- [ ] Integration boundaries between AI-generated modules have explicit schema validation
- [ ] Error contract is consistent across module boundaries (throw vs return null vs Result)

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
