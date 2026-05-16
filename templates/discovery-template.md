# [Project Name] — Phase 0 Discovery & Ambiguity Report

<!-- Archpilot: discovery.md | Phase 0: DISCOVERY -->
<!-- Governed by: rules/36-discovery-ambiguity.md | rules/50-agent-pipeline.md v4.0 -->
<!-- MANDATORY: All 15 dimensions must be populated. No placeholders. No TBD. -->

---

## Document Header

```
Project:          [Project / Initiative Name]
Discovery ID:     DISC-[NNN]
Version:          1.0
Status:           DRAFT | IN_REVIEW | APPROVED
Author:           [Name — SE Agent or Human Architect]
Date:             [YYYY-MM-DD]
Input Source:     .specs/Input.md
```

---

## Executive Intent

*Before discussing "how", we must define "why". Why is the business funding this?*

- **Primary Business Driver:**  [Revenue growth / Cost reduction / Compliance / Competitive parity / Risk mitigation]
- **Target Market & Persona:**  [Who pays? Who uses? What is their primary pain?]
- **Definition of Business Success:** [Quantified outcome, e.g., "onboard 10,000 users in Q3 without adding support headcount"]
- **Definition of Technical Success:** [e.g., "p95 API latency < 200 ms at 5,000 concurrent users"]
- **Stakeholder Hierarchy:**

| Role | Name / Team | Authority | Interest |
|------|-------------|-----------|----------|
| Executive Sponsor | | Decision | Budget & ROI |
| Product Owner | | Input | Scope & Priority |
| Engineering Lead | | Decision | Feasibility & Delivery |
| Security / Compliance | | Veto | Risk & Regulatory |
| Operations | | Input | Reliability & Runbooks |

---

## Prompt Deconstruction

**The Vague Request:**
> *[Paste the raw, ambiguous client request here]*

**Technical Translation (what this actually means to engineer):**

| Client Phrase | Engineering Reality | Key Decision Unlocked |
|---------------|--------------------|-----------------------|
| "real-time" | sub-X ms latency, push vs pull, SSE vs WebSocket | Transport protocol |
| "global" | multi-region, CDN, data residency constraints | Deployment topology |
| "scalable" | RPS targets, auto-scaling triggers, sharding strategy | Data partitioning model |
| [add more] | | |

---

## Dimension 1: Technical Physics

*Throughput, latency, concurrency, and the engineering math behind them.*

### 1.1 Traffic Model

| Metric | Nominal | Peak | Basis |
|--------|--------:|-----:|-------|
| Requests per second (RPS) | | | |
| Concurrent users | | | |
| Read / Write ratio | %R / %W | | |
| Burst factor (peak / nominal) | | | |
| Seasonality pattern | | | |

### 1.2 Little's Law Calculation

```
L  = λ × W
L  = [concurrent users]
λ  = [arrival rate RPS]
W  = [avg response time ms] = L / λ = [result ms]

Throughput headroom required: [X]× above nominal for auto-scaling trigger.
```

### 1.3 Latency Budget

| Tier | Target (p50) | Target (p95) | Target (p99) | SLA Breach Action |
|------|-------------:|-------------:|-------------:|-------------------|
| API Gateway | ms | ms | ms | |
| Core Service | ms | ms | ms | |
| Database Read | ms | ms | ms | |
| Database Write | ms | ms | ms | |
| External Dependency | ms | ms | ms | |

### 1.4 Data Volume

| Dataset | Current Size | 12-Month Growth | 3-Year Projection | Archival Strategy |
|---------|------------:|----------------:|------------------:|-------------------|
| | | | | |

---

## Dimension 2: Regulatory & Compliance

*Which laws, standards, and certifications apply?*

| Regulation | Applicable | Key Obligation | Enforcement Deadline |
|------------|:----------:|----------------|----------------------|
| GDPR | Yes / No | | |
| HIPAA | Yes / No | | |
| PCI-DSS Level | Yes / No | | |
| SOX | Yes / No | | |
| CCPA / CPRA | Yes / No | | |
| ISO 27001 | Yes / No | | |
| Regional laws | [list] | | |

**Audit Trail Requirements:**
- Log retention period: [X years]
- Immutability requirement: [Yes/No — WORM storage?]
- Who can access audit logs: [roles]
- Breach notification window: [X hours]

---

## Dimension 3: Security & Threat Surface

*STRIDE threat model applied to each major component.*

### 3.1 Authentication & Authorization Model

| Mechanism | Standard | Token Lifetime | Refresh Strategy |
|-----------|----------|---------------:|------------------|
| User Auth | OIDC / OAuth2 / SAML | | |
| Service-to-Service | mTLS / JWT / API Key | | |
| Admin Auth | MFA required | | |
| Authorization Model | RBAC / ABAC / ReBAC | | |

### 3.2 STRIDE Threat Model

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Privilege Escalation |
|-----------|----------|-----------|-------------|-----------------|-----|----------------------|
| API Gateway | | | | | | |
| Core Service | | | | | | |
| Database | | | | | | |
| Message Queue | | | | | | |
| [other] | | | | | | |

### 3.3 Abuse & Malicious Actor Vectors

| Attack Vector | Likelihood | Impact | Defense Mechanism |
|---------------|:----------:|:------:|-------------------|
| API key theft | | | |
| SQL/NoSQL injection | | | |
| Bot / scraper abuse | | | |
| Insider threat | | | |
| Supply-chain compromise | | | |

---

## Dimension 4: Failure & Resilience

*CAP theorem choices, RPO/RTO targets, and graceful degradation states.*

### 4.1 Availability Targets

| Service Tier | SLA | Allowed Downtime / Month | Architecture Implication |
|--------------|----:|-------------------------:|--------------------------|
| Critical path | % | | |
| Supporting services | % | | |
| Batch / background | % | | |

### 4.2 Recovery Objectives

| Scenario | RPO (max data loss) | RTO (max downtime) | Strategy |
|----------|--------------------:|-------------------:|----------|
| Single AZ failure | | | |
| Regional failure | | | |
| Catastrophic data loss | | | |
| Ransomware / corruption | | | |

### 4.3 CAP Theorem Decision

| Data Domain | Consistency Choice | Reason |
|-------------|-------------------|--------|
| Financial transactions | Strong (CP) | |
| User profile reads | Eventual (AP) | |
| [other domain] | | |

### 4.4 Graceful Degradation States

| Dependency Down | Degraded Behavior | User Impact | Recovery Trigger |
|-----------------|-------------------|-------------|------------------|
| Primary DB | Read from replica | Stale reads ≤ Xs | Replica health check |
| External API | Serve cached response | | Cache TTL expiry |
| Auth service | Allow cached tokens for X min | | Service restore |

---

## Dimension 5: Cost & FinOps

*TCO model, margin profile, and FinOps strategy.*

### 5.1 Cloud Spend Envelope

| Phase | Monthly Target | Monthly Hard Cap | FinOps Review Cadence |
|-------|---------------:|----------------:|----------------------|
| MVP | $ | $ | |
| Growth | $ | $ | |
| Scale | $ | $ | |

### 5.2 Build vs Buy Analysis

| Capability | Build | Buy / SaaS | Decision | Rationale |
|------------|:-----:|:----------:|----------|-----------|
| Auth | | | | |
| Search | | | | |
| Notifications | | | | |
| [other] | | | | |

### 5.3 Compute Strategy

| Workload Type | Strategy | Justification |
|---------------|----------|---------------|
| Always-on API | Reserved instances (X%) + On-demand | |
| Batch jobs | Spot instances | |
| Burst compute | On-demand / serverless | |

### 5.4 3-Year TCO Estimate

| Year | Infra | Licensing | Personnel | Total |
|------|------:|----------:|----------:|------:|
| Y1 | $ | $ | $ | $ |
| Y2 | $ | $ | $ | $ |
| Y3 | $ | $ | $ | $ |

---

## Dimension 6: Data Residency & Sovereignty

*Geo-fencing, cross-border transfer rules, and data classification.*

| Data Class | Residency Constraint | Allowed Regions | Cross-Border Transfer | Encryption at Rest |
|------------|---------------------|-----------------|----------------------|--------------------|
| PII — EU residents | EU only (GDPR Art 44) | eu-west-1, eu-central-1 | SCC required | AES-256 + KMS |
| PII — US residents | | | | |
| Financial records | | | | |
| Anonymized analytics | | | | |

**Data Sovereignty Map:**
```
[Region / Country] → [Applicable Laws] → [Storage Constraint] → [Transfer Mechanism]
```

---

## Dimension 7: Edge & Hardware Constraints

*IoT, device limits, offline operation, and connectivity quality.*

| Device / Node Type | OS / Firmware | CPU / RAM | Storage | Connectivity | Offline Requirement |
|-------------------|--------------|----------:|--------:|--------------|---------------------|
| | | | | | |

**Edge Compute Strategy:**
- Edge inference required: Yes / No
- Sync protocol: [MQTT / gRPC / REST / custom]
- Conflict resolution for offline-first: [last-write-wins / CRDT / manual]
- OTA update mechanism: [mechanism + rollback strategy]

---

## Dimension 8: Connectivity & Integration

*External system inventory, protocols, and legacy adapters.*

| System | Owner | Protocol | Auth | Data Format | SLA | Failure Behaviour |
|--------|-------|----------|------|------------|----:|-------------------|
| | | REST/gRPC/Events | JWT/mTLS | JSON/Avro | ms | Circuit-break |

**Legacy System Constraints:**
- Systems with no modern API: [list + adapter strategy]
- Batch-only integrations: [system + frequency + file format]
- Protocol translation needed: [e.g., SOAP → REST via adapter layer]

**Event Bus / Messaging:**
- Broker technology: [Kafka / RabbitMQ / SNS+SQS / Azure Service Bus]
- Exactly-once delivery required: Yes / No (justification)
- Event schema registry: [Confluent / AWS Glue / custom]

---

## Dimension 9: Observability Requirements

*Logging standards, metric dimensions, tracing strategy.*

### 9.1 Logging

| Field | Standard | Example |
|-------|----------|---------|
| Format | Structured JSON | `{"ts":"...","level":"...","service":"...","trace_id":"...","msg":"..."}` |
| Log levels used | DEBUG / INFO / WARN / ERROR / FATAL | |
| PII scrubbing | Required fields | email, phone, SSN masked |
| Retention | Hot / Warm / Cold | 7d / 30d / 1 year |
| Sink | [CloudWatch / ELK / Loki / Datadog] | |

### 9.2 Metrics (RED + USE)

| Metric | Dimension Labels | Alert Threshold | Page Threshold |
|--------|-----------------|----------------:|---------------:|
| Request Rate (R) | service, endpoint, method | | |
| Error Rate (E) | service, endpoint, status_code | >1% | >5% |
| Duration (D) p95 | service, endpoint | >200ms | >500ms |
| CPU Utilization (U) | host, service | >70% | >90% |
| Saturation (S) | queue depth, pool usage | | |

### 9.3 Distributed Tracing

- Tracing standard: [OpenTelemetry / Jaeger / AWS X-Ray / Datadog APM]
- Sampling strategy: [100% errors + 10% success / adaptive]
- Span naming convention: `service.operation` e.g. `payment.charge`
- Trace propagation headers: [W3C TraceContext / B3]

### 9.4 Alerting Tiers

| Tier | Condition | Channel | On-Call Response |
|------|-----------|---------|-----------------|
| P1 — Critical | SLA breach, data loss risk | PagerDuty + Slack | 5 min |
| P2 — High | Error rate >1%, p95 >200ms | Slack | 30 min |
| P3 — Medium | Resource saturation >70% | Email | Business hours |

---

## Dimension 10: Lifecycle & Maintainability

*Versioning strategy, upgrade paths, deprecation policy.*

| Concern | Decision | Rationale |
|---------|----------|-----------|
| API versioning scheme | URI path (v1/v2) / Header / Content-Type | |
| Backward compat window | X months after new version GA | |
| Deprecation notice period | X weeks min | |
| DB migration strategy | [Flyway / Liquibase / custom] | |
| Dependency update policy | [Renovate / Dependabot + manual approval] | |
| Support EOL timeline | | |

**Long-running Migration Risk:**
- Tables with >10M rows: [list — online vs offline migration strategy]
- Blue-green vs rolling deploy: [decision + rationale]
- Feature flag strategy: [tool + scope]

---

## Dimension 11: Human Interface & UX

*User personas, device matrix, accessibility, offline, and i18n.*

### 11.1 Persona Matrix

| Persona | Technical Level | Primary Device | Connectivity | Key Goal |
|---------|:--------------:|----------------|-------------|---------|
| | | | | |

### 11.2 Accessibility Requirements

| Standard | Level | Key Requirements |
|----------|-------|-----------------|
| WCAG | 2.1 AA / 2.2 AA / AAA | Screen reader, keyboard nav, contrast ratio |
| Section 508 | Yes / No | |

### 11.3 Internationalization

| Locale | Language | Date Format | Currency | RTL | Priority |
|--------|----------|-------------|----------|:---:|:--------:|
| en-US | English | MM/DD/YYYY | USD | No | P1 |
| [other] | | | | | |

### 11.4 Offline & Progressive Enhancement

- Offline-first requirement: Yes / No
- Service Worker scope: [pages / features that work offline]
- Data sync conflict strategy: [when reconnected]

---

## Dimension 12: Data Privacy & Ethics

*PII inventory, anonymization strategy, retention, and consent.*

### 12.1 PII Inventory

| Data Element | Classification | Storage Location | Retention | Anonymization Method |
|--------------|---------------|-----------------|----------:|----------------------|
| Email address | PII | Users DB | 3 years | Hashed after X months |
| IP address | PII | Logs | 90 days | Truncated to /24 |
| Payment card | PCI | Tokenised (never stored) | N/A | Tokenization |
| [other] | | | | |

### 12.2 Consent & Rights Management

| Right | Mechanism | SLA for Fulfillment |
|-------|-----------|-------------------:|
| Right to Access | Self-service portal export | 30 days |
| Right to Erasure | Soft-delete + anonymize job | 30 days |
| Right to Portability | JSON export endpoint | 30 days |
| Consent withdrawal | Toggle in account settings | Immediate |

### 12.3 Algorithmic Ethics

- Automated decisions affecting users: [Yes/No — describe]
- Bias audit requirement: [Yes/No — standard/frequency]
- Human review override: [Yes/No — trigger conditions]

---

## Dimension 13: Third-Party Dependencies

*Vendor inventory, lock-in risk, and exit strategies.*

| Vendor / SaaS | Function | Lock-in Risk | Exit Strategy | License | Annual Cost |
|---------------|----------|:------------:|---------------|---------|------------:|
| | | H/M/L | | | $ |

**Open-Source License Compliance:**

| Library | License | Obligation | Compliant |
|---------|---------|------------|:---------:|
| | MIT/Apache/GPL | | Yes/No |

**Supply-Chain Security Posture:**
- SBOM generation: [Yes/No — tool]
- Dependency scanning: [Dependabot / Snyk / Trivy]
- Container image signing: [Sigstore / Notary]

---

## Dimension 14: Scaling & Multi-Tenancy

*Horizontal/vertical scaling model, tenant isolation, noisy-neighbor controls.*

### 14.1 Scaling Model

| Service | Scaling Axis | Scale-Out Trigger | Scale-In Trigger | Max Instances |
|---------|-------------|------------------:|----------------:|:-------------:|
| API tier | Horizontal | CPU >60% / RPS >X | CPU <30% | |
| Worker tier | Horizontal | Queue depth >X | Queue <Y | |
| DB | Vertical + Read replicas | | | |

### 14.2 Multi-Tenancy Model

| Dimension | Decision | Rationale |
|-----------|----------|-----------|
| Isolation model | Silo / Bridge / Pool | |
| Data partitioning | Schema-per-tenant / Row-level (tenant_id) | |
| Compute isolation | Shared / Dedicated pods | |
| Noisy-neighbor control | Rate limiting per tenant (X RPS cap) | |
| Tenant onboarding | Automated / Manual approval | |

### 14.3 Elasticity SLAs

- Scale-out latency target: < X minutes from trigger to healthy
- Scale-in cooldown: X minutes (avoid thrashing)
- Minimum warm instances: X (cold-start avoidance)

---

## Dimension 15: Environmental & Sustainability

*SCI score, carbon-aware scheduling, GreenOps.*

### 15.1 Software Carbon Intensity (SCI)

```
SCI = (E × I) + M  per functional unit

E  = Energy consumed by software (kWh)
I  = Location-based carbon intensity (gCO2/kWh)
M  = Embodied carbon of hardware
Functional unit: [per 1,000 API requests / per user session / per data-GB processed]

Baseline estimate: [X gCO2eq / functional unit]
Target reduction:  [X% over 3 years]
```

### 15.2 Carbon-Aware Design Opportunities

| Opportunity | Implementation | Estimated Saving |
|-------------|---------------|-----------------|
| ARM instances (Graviton/Ampere) | Replace x86 for stateless services | ~20% energy |
| Spot/preemptible for batch | Shift workloads to low-carbon time windows | ~30% carbon |
| Region selection | Prefer regions with renewable energy (>80% RE) | ~40% carbon |
| Auto-scale to zero | Idle service shutdown after X min | |
| Data transfer optimization | Compress + cache to reduce egress | |

### 15.3 GreenOps Targets

| Metric | Baseline | 12-Month Target | 36-Month Target |
|--------|:--------:|:---------------:|:---------------:|
| SCI score | | | |
| Cloud carbon footprint (gCO2e) | | | |
| Renewable energy % | | | |

---

## Critical Edge Cases & Failure Modes

*Scenarios that will break naive implementations.*

| ID | Edge Case Scenario | Potential Impact | Required Defense |
|----|--------------------|-----------------|------------------|
| EC-01 | [Network partition between services] | [e.g., split-brain inconsistency] | [Quorum writes / leader election] |
| EC-02 | [External API rate limit exceeded] | [Service halt] | [Circuit breaker + DLQ + retry] |
| EC-03 | [DB failover during write transaction] | [Data loss] | [Idempotent writes + WAL replay] |
| EC-04 | [Burst 10× traffic spike] | [Cascading timeouts] | [Auto-scale + backpressure + shed load] |
| EC-05 | [PII breach via misconfigured bucket] | [Regulatory fine + brand damage] | [S3 Block Public Access + MACIe scan] |

---

## Architectural Trade-offs

*Present two options — business must choose before Phase 1 begins.*

### Option A: [High-Reliability / Higher-Cost]

| Attribute | Detail |
|-----------|--------|
| Architecture | [e.g., Active-Active multi-region, event-sourced, strong consistency] |
| Pros | Max resilience, zero data loss, full audit trail |
| Cons | Higher engineering complexity, longer TTM |
| Infra Cost (monthly) | $$$ |
| Time to Market | Slow (X months) |
| Best for | [mission-critical, regulated, high-transaction-value] |

### Option B: [Cost-Optimised / Faster-TTM]

| Attribute | Detail |
|-----------|--------|
| Architecture | [e.g., Single-region Active-Passive, CRUD, eventual consistency] |
| Pros | Fast TTM, simple debugging, low infra cost |
| Cons | 5-min RPO risk, harder to scale globally later |
| Infra Cost (monthly) | $ |
| Time to Market | Fast (Y months) |
| Best for | [MVP, low-regulation, cost-sensitive] |

---

## Interrogation List

*The exact questions the client MUST answer to unblock `requirements.md`.*

| # | Question | Impact if Unresolved | Priority | Due |
|---|----------|---------------------|:--------:|-----|
| 1 | Are you willing to pay [3×] infra costs for 99.99% uptime, or is 99.9% acceptable? | Active-Active vs Active-Passive topology | HIGH | |
| 2 | What is the maximum tolerable data loss (RPO) in a catastrophic failure? | DB replication and backup strategy | HIGH | |
| 3 | Which data residency jurisdictions must we comply with? | Storage region and cross-border transfer rules | HIGH | |
| 4 | Is there an existing identity provider (IdP) to integrate with? | Auth architecture | MEDIUM | |
| 5 | What is the expected tenant/customer count in Year 1 and Year 3? | Isolation model and scaling strategy | MEDIUM | |
| 6 | [Add domain-specific question] | | | |

---

*Archpilot — Discovery Template v4.0 | Governed by rules/50-agent-pipeline.md*
*Generated by Phase 0: SE Agent | Created by Gaurav Sharma*
