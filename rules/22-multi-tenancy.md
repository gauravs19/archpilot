# Multi-Tenancy Architecture Patterns

> **Purpose:** Standards for designing multi-tenant systems — covering isolation models,
> data partitioning, tenant-aware security, noisy neighbor prevention, and onboarding.
> Essential for SaaS platforms, GCCs building shared services, and B2B products.

---

## How to Use This File

- **SaaS Design:** Say to an LLM: *"Using these multi-tenancy patterns, design a tenant isolation strategy for: [your SaaS product]"*
- **Architecture Review:** Use the isolation model decision tree to evaluate existing designs

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [06 — Data Architecture](./06-data-architecture.md) | Database partitioning for tenant data |
| [07 — Security Architecture](./07-security-architecture.md) | Tenant-level auth, ABAC, row-level security |
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Infrastructure isolation per tenant |
| [14 — Cost Optimization](./14-cost-optimization.md) | Per-tenant cost attribution |

---

## 1. Tenant Isolation Models

### 1.1 Isolation Spectrum

```
Full Isolation ◄──────────────────────────► Full Sharing
                                                         
 Separate        Separate DBs,    Shared DB,      Shared DB,
 Infrastructure  Shared App       Separate        Shared
 (Silo)          (Bridge)         Schema (Pool)   Schema (Pool)
                                                         
 $$$$$           $$$$             $$               $
 Max Security    Good Balance     Cost Efficient   Most Efficient
 Max Compliance  Good Compliance  Standard         Standard
```

### 1.2 Model Selection

| Model | How | Pros | Cons | Use When |
|-------|-----|------|------|----------|
| **Silo** (separate infra per tenant) | Dedicated VPC, DB, compute per tenant | Max isolation, compliance-friendly | Expensive, hard to manage at scale | Healthcare (HIPAA), government, finance |
| **Bridge** (shared app, separate DB) | Shared compute, separate DB per tenant | Good isolation, manageable cost | DB management overhead grows with tenants | B2B SaaS with < 100 tenants |
| **Pool** (shared DB, schema-per-tenant) | Shared DB, each tenant has own schema | Good isolation, moderate cost | Schema migrations across all tenants | B2B SaaS with 100-1000 tenants |
| **Pool** (shared DB, shared schema) | Shared everything, `tenant_id` column | Cheapest, simplest | Risk of data leakage, noisy neighbor | B2C SaaS, 1000+ tenants |

### 1.3 Decision Tree

```
Does the customer require physical data isolation?
├── YES (compliance/regulatory) → Silo Model
│
└── NO → How many tenants?
    ├── < 50 (enterprise B2B) → Bridge Model (separate DBs)
    ├── 50-1000 (mid-market B2B) → Pool (separate schema)
    └── 1000+ (SMB/B2C) → Pool (shared schema + tenant_id)
```

---

## 2. Data Partitioning

### 2.1 Shared Schema Pattern (Most Common)

Every table includes a `tenant_id` column:

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,       -- ← EVERY table has this
    customer_id UUID NOT NULL,
    total_amount BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE INDEX idx_orders_tenant ON orders(tenant_id);
CREATE INDEX idx_orders_tenant_status ON orders(tenant_id, status);
```

**Rules:**
- `tenant_id` is **mandatory** on every table (no exceptions)
- Every query MUST include `tenant_id` in the WHERE clause
- Row-Level Security (RLS) in PostgreSQL as defense-in-depth:

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.current_tenant')::UUID);
```

### 2.2 Separate Schema Pattern

```
database: saas_platform
├── schema: tenant_abc123
│   ├── orders
│   ├── customers
│   └── products
├── schema: tenant_def456
│   ├── orders
│   ├── customers
│   └── products
└── schema: shared
    ├── tenants
    ├── plans
    └── billing
```

### 2.3 Data Isolation Checklist

- [ ] Every table has `tenant_id` (shared schema) or is in tenant-specific schema
- [ ] Row-Level Security (RLS) enabled as defense-in-depth
- [ ] Application enforces `tenant_id` at the ORM/repository layer
- [ ] Queries are tested to ensure no cross-tenant data leakage
- [ ] Backups can be restored per-tenant (not just whole-database)
- [ ] Data export/deletion can be done per-tenant (GDPR)
- [ ] Search indexes (Elasticsearch) are filtered by tenant

---

## 3. Application Architecture

### 3.1 Tenant Context Flow

```
Request ──▶ [API Gateway] ──▶ [Auth Middleware] ──▶ [Tenant Resolver] ──▶ [Service]
                                    │                      │
                                    ▼                      ▼
                              Validate JWT           Extract tenant_id
                              Check permissions      Set in request context
                                                     Set in DB session
```

### 3.2 Tenant Resolution Strategies

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| **Subdomain** | `acme.app.com` | Clean, standard | DNS/SSL management |
| **Path prefix** | `app.com/acme/api/` | Simple routing | URL pollution |
| **Header** | `X-Tenant-Id: acme` | Flexible, API-friendly | Easy to tamper |
| **JWT claim** | `{ "tenant_id": "acme" }` | Secure, no extra lookup | Token size |

**Recommended:** JWT claim (secure) + subdomain (user-facing).

### 3.3 Middleware Pattern

```python
# Every request MUST set tenant context
@app.middleware("http")
async def tenant_middleware(request, call_next):
    tenant_id = extract_tenant_from_jwt(request)
    if not tenant_id:
        return JSONResponse(status_code=403, content={"error": "Invalid tenant"})
    
    # Set tenant in request state
    request.state.tenant_id = tenant_id
    
    # Set tenant in DB session (for RLS)
    db.execute(f"SET app.current_tenant = '{tenant_id}'")
    
    response = await call_next(request)
    return response
```

---

## 4. Noisy Neighbor Prevention

### 4.1 Resource Isolation

| Resource | Strategy |
|----------|---------|
| **API rate limiting** | Per-tenant limits (not just per-IP) |
| **Database connections** | Connection pool per tenant OR tenant-aware pool limits |
| **CPU/Memory** | Resource quotas per tenant (K8s resource limits) |
| **Storage** | Per-tenant storage quotas with alerts |
| **Background jobs** | Tenant-aware queue priorities; don't let one tenant monopolize workers |

### 4.2 Rate Limiting per Tenant

| Plan | API Limit | Storage | Compute Priority |
|------|:---------:|:-------:|:----------------:|
| Free | 100 req/min | 1 GB | Low |
| Starter | 500 req/min | 10 GB | Normal |
| Business | 2,000 req/min | 100 GB | High |
| Enterprise | 10,000 req/min | Unlimited | Dedicated |

### 4.3 Monitoring

- Dashboard per tenant: request count, error rate, latency, storage usage
- Alert when any single tenant consumes > 30% of shared resources
- Automated throttling when limits exceeded (graceful degradation, not hard block)

---

## 5. Tenant Lifecycle

### 5.1 Onboarding (Provisioning)

| Step | Action | Automation |
|:----:|--------|:----------:|
| 1 | Create tenant record in `tenants` table | Automated |
| 2 | Create tenant-specific schema or namespace (if applicable) | Automated |
| 3 | Run initial data seed (default settings, roles) | Automated |
| 4 | Provision DNS record (if subdomain model) | Automated |
| 5 | Create admin user for tenant | Automated |
| 6 | Send welcome email with setup instructions | Automated |

**Rule:** Tenant onboarding MUST be fully automated. Target: < 30 seconds.

### 5.2 Offboarding (Deprovisioning)

| Step | Action | Timeline |
|:----:|--------|:--------:|
| 1 | Disable tenant access (soft delete) | Immediate |
| 2 | Export tenant data (provide to customer) | Within 24 hours |
| 3 | Delete tenant data from active systems | Within 30 days |
| 4 | Delete tenant data from backups | Within 90 days |
| 5 | Release tenant-specific resources | After data deletion |

---

## 6. Multi-Tenancy Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Missing `tenant_id` on a table** | Cross-tenant data leak | Automated schema validation in CI |
| **Tenant resolution in business logic** | Scattered, inconsistent | Centralize in middleware |
| **No rate limiting per tenant** | One tenant can DoS others | Tenant-aware rate limiting |
| **Global DB queries without tenant filter** | Full table scans, data leaks | ORM-level tenant filter enforced |
| **Same credentials for all tenants** | Security breach affects everyone | Per-tenant encryption keys |
| **No tenant-level monitoring** | Can't identify noisy neighbors | Per-tenant metrics and dashboards |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
