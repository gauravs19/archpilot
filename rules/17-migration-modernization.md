# Migration & Modernization Playbook

> **Purpose:** Standards for legacy system assessment, migration strategies, and modernization
> patterns. Covers Strangler Fig, dual-write, data migration, and coexistence patterns —
> essential for brownfield projects that make up 80%+ of real-world architecture work.

---

## How to Use This File

- **Assessment:** Say to an LLM: *"Using this migration playbook, assess this legacy system and propose a modernization strategy: [describe system]"*
- **Planning:** Use the decision trees to choose the right migration pattern
- **Execution:** Reference the phase-by-phase migration guidance

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [09 — Microservices Patterns](./09-microservices-patterns.md) | Decomposition targets for migration |
| [06 — Data Architecture](./06-data-architecture.md) | Data migration patterns and standards |
| [02 — ADR Standards](./02-adr-standards.md) | Document migration decisions as ADRs |
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Cloud-native target architecture |

---

## 1. Legacy System Assessment

### 1.1 Assessment Framework

Score each dimension 1-5:

| Dimension | Score 1 (Critical) | Score 5 (Healthy) |
|-----------|-------------------|-------------------|
| **Business Value** | Feature unused, no revenue impact | Core revenue driver |
| **Technical Health** | Unmaintainable, no tests, outdated stack | Clean code, tested, modern stack |
| **Operational Risk** | Frequent outages, no monitoring | Stable, well-monitored |
| **Team Knowledge** | Original developers gone, no docs | Team understands codebase well |
| **Cost of Ownership** | Expensive licenses, specialized infra | Low cost, commodity infra |
| **Security Posture** | Unpatched, known vulnerabilities | Current, compliant |
| **Integration Complexity** | Tightly coupled to 10+ systems | Loose coupling, clear APIs |

### 1.2 Assessment Decision Matrix

```
Score 28-35 → RETAIN: System is healthy, low priority for change
Score 21-27 → REFACTOR: Improve incrementally (code quality, tests, monitoring)
Score 14-20 → RE-PLATFORM: Move to modern infra (cloud, containers) without rewrite
Score 7-13  → REBUILD: Full rewrite with modern architecture
```

### 1.3 The 6 R's of Migration (AWS Framework)

| Strategy | What | When | Risk | Effort |
|----------|------|------|:----:|:------:|
| **Retain** | Keep as-is | System works fine, low business value | None | None |
| **Retire** | Decommission | No longer needed, replaced | Low | Low |
| **Rehost** (Lift & Shift) | Move to cloud as-is | Quick migration, cost savings | Low | Low |
| **Re-platform** | Minor changes for cloud | Managed DB, containers, no rewrite | Medium | Medium |
| **Refactor** | Re-architect for cloud-native | Performance, scalability needs | High | High |
| **Replace** | Buy SaaS/COTS | Commodity capability (HR, CRM, email) | Medium | Medium |

---

## 2. Migration Patterns

### 2.1 Strangler Fig Pattern

```
Phase 1: Route ALL traffic through proxy
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Client   │────▶│  Proxy   │────▶│Legacy System │
└──────────┘     └──────────┘     └──────────────┘

Phase 2: New service handles SOME routes
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Client   │────▶│  Proxy   │──┬─▶│Legacy System │ (remaining routes)
└──────────┘     └──────────┘  │  └──────────────┘
                               │  ┌──────────────┐
                               └─▶│ New Service   │ (migrated routes)
                                  └──────────────┘

Phase 3: All traffic to new system, legacy decommissioned
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Client   │────▶│  Proxy   │────▶│ New Service   │
└──────────┘     └──────────┘     └──────────────┘
```

**Rules:**
- Start with the lowest-risk, best-understood module
- Keep the proxy/router as a simple pass-through — no business logic
- Each migrated module MUST be independently testable and deployable
- Rollback route MUST exist for every migration step (switch traffic back)
- Measure: feature parity + performance parity before cutting over

### 2.2 Anti-Corruption Layer (ACL)

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│ New Service   │────▶│ Anti-Corruption  │────▶│Legacy System │
│(clean domain) │     │ Layer (Adapter)  │     │ (messy API)  │
└──────────────┘     └─────────────────┘     └──────────────┘
```

- Translates between new domain model and legacy data model
- Isolates the new system from legacy quirks
- ACL is temporary — removed when legacy is fully replaced
- ACL handles: data format translation, protocol translation, error mapping

### 2.3 Branch by Abstraction

```
Step 1: Create abstraction layer over existing implementation
Step 2: Build new implementation behind the same abstraction
Step 3: Feature flag to switch between old and new
Step 4: Verify new implementation, remove old
```

Use for: replacing internal components (DB layer, service client, algorithm) without stopping feature development.

### 2.4 Parallel Run / Shadow Mode

```
All traffic ──▶ Legacy System (produces REAL result)
           └──▶ New System (produces SHADOW result, compare but don't use)
```

- Both systems process the same inputs
- Compare outputs for correctness (log discrepancies)
- When discrepancy rate drops to < 0.1%, switch to new system
- Use for: critical systems where correctness is paramount (payments, billing)

---

## 3. Data Migration Patterns

### 3.1 Migration Strategies

| Strategy | How | Risk | Use When |
|----------|-----|:----:|----------|
| **Big Bang** | Migrate all data at once, switch over | High | Small datasets, tolerance for downtime |
| **Trickle Migration** | Migrate in batches over time | Medium | Large datasets, need to stay live |
| **Dual-Write** | Write to both old and new simultaneously | Medium | Zero-downtime migration |
| **CDC-Based** | Capture changes from source DB, replay to target | Low | Real-time sync, minimal app changes |

### 3.2 Dual-Write Pattern (Detail)

```
Phase 1: Write to OLD (primary), async replicate to NEW
Phase 2: Write to BOTH (dual-write), read from OLD
Phase 3: Write to BOTH, read from NEW (validation)
Phase 4: Write to NEW (primary), stop writing to OLD
```

**Dual-Write Rules:**
- NEVER trust dual-write to be perfectly consistent — design for reconciliation
- Run a reconciliation job that compares OLD and NEW periodically
- Handle failures: if write to NEW fails, log + retry, don't fail the operation
- Set a hard deadline for Phase 4 cutover — dual-write is expensive to maintain

### 3.3 Data Migration Checklist

- [ ] Source data profiled (row counts, data quality issues, edge cases)
- [ ] Target schema designed and validated
- [ ] Mapping document: source field → target field (with transformations)
- [ ] PII identified and handled (encryption, masking in non-prod)
- [ ] Migration script idempotent (can run twice without corruption)
- [ ] Rollback plan: can we restore the old data if migration fails?
- [ ] Performance tested with production-volume data
- [ ] Reconciliation report: counts and checksums match
- [ ] Incremental/delta migration tested (for trickle approach)
- [ ] Downtime window communicated (if big-bang)

---

## 4. Migration Planning Template

### 4.1 Migration Phases

| Phase | Activities | Duration | Gate |
|-------|-----------|:--------:|------|
| **Phase 0: Discovery** | System assessment, dependency mapping, data profiling | 2-4 weeks | Assessment report approved |
| **Phase 1: Foundation** | Set up target infra, CI/CD, monitoring, ACL/proxy | 3-6 weeks | Target environment ready |
| **Phase 2: Pilot Module** | Migrate 1 low-risk module, validate end-to-end | 4-6 weeks | Pilot passes UAT |
| **Phase 3: Incremental Migration** | Migrate remaining modules in priority order | 8-16 weeks | Each module passes UAT |
| **Phase 4: Data Migration** | Migrate/sync data, reconciliation, cutover | 2-4 weeks | Data reconciliation passes |
| **Phase 5: Decommission** | Redirect all traffic, decommission legacy | 2-4 weeks | Legacy shut down |
| **Phase 6: Hypercare** | Monitor, fix issues, performance tuning | 2-4 weeks | SLA met for 30 days |

### 4.2 Risk Assessment for Migrations

| # | Risk | Probability | Impact | Mitigation |
|---|------|:-----------:|:------:|-----------|
| 1 | Undocumented legacy behavior | High | High | Shadow mode / parallel run for critical paths |
| 2 | Data quality issues in source | High | Medium | Data profiling + cleansing before migration |
| 3 | Performance regression | Medium | High | Load test new system with production traffic patterns |
| 4 | Integration with unchanged systems break | Medium | High | Contract tests for all integration points |
| 5 | Extended dual-write period | Medium | Medium | Hard deadline for cutover, reconciliation automation |
| 6 | Team lacks knowledge of legacy system | High | Medium | Reverse engineering sessions, pair with legacy team |

---

## 5. Modernization Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Full rewrite from scratch** | Takes years, costs millions, often fails | Strangler Fig — migrate incrementally |
| **Lift-and-shift only** | Cloud costs exceed on-prem, no benefit | Re-platform at minimum, refactor high-value components |
| **Migrating everything at once** | Massive risk, no rollback | Prioritize by business value, migrate in phases |
| **No rollback plan** | Stuck if migration fails | Every phase must have a documented rollback path |
| **Ignoring data migration** | "We'll figure out the data later" | Data migration is 40% of total effort — plan upfront |
| **Not testing with real data** | Works in test, fails in production | Test with production-volume, production-quality data |
| **Keeping legacy "just in case"** | Perpetual dual-maintenance | Set a firm decommission date and enforce it |
| **No success metrics** | Can't prove migration was worth it | Define KPIs: latency, error rate, cost, dev velocity |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
