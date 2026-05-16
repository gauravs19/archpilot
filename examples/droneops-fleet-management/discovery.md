# DroneOps SaaS — Phase 0 Discovery & Ambiguity Report

<!-- Archpilot: discovery.md | Phase 0: DISCOVERY -->
<!-- Governed by: rules/36-discovery-ambiguity.md | rules/50-agent-pipeline.md v4.0 -->

---

## Document Header

```
Project:          DroneOps Fleet Management SaaS
Discovery ID:     DISC-001
Version:          1.0
Status:           APPROVED
Author:           SE Agent (Phase 0)
Date:             2026-05-15
Input Source:     .specs/Input.md
```

---

## Executive Intent

- **Primary Business Driver:** Market capture in commercial drone operations ($14B TAM by 2030). Monetize via per-seat SaaS subscriptions ($48K/year enterprise ACV) and compliance-reporting premium add-ons.
- **Target Market & Persona:** Operations managers at logistics (last-mile delivery), agriculture (precision crop monitoring), and infrastructure inspection (power lines, pipelines) enterprises. Pain: fragmented tooling — operators use spreadsheets, vendor mobile apps, and manual logs across 10-500 drones.
- **Definition of Business Success:** 50 paying enterprise customers within 12 months; 500 by end of Year 2; churn < 5% annually; NPS > 50.
- **Definition of Technical Success:** Telemetry ingestion at p95 < 500 ms end-to-end (drone to dashboard) at 25,000 concurrent telemetry streams; mission planning API p95 < 200 ms; system availability >= 99.9% monthly.
- **Stakeholder Hierarchy:**

| Role | Name / Team | Authority | Interest |
|------|-------------|-----------|----------|
| Executive Sponsor | CEO / CTO | Budget & direction | Revenue growth, market position |
| Product Owner | Head of Product | Scope & priority | Feature completeness, TTM |
| Engineering Lead | VP Engineering | Feasibility | Architecture quality, team velocity |
| Security / Compliance | CISO + Legal | Veto | FAA/EASA compliance, data security |
| SRE Team | Operations | Input | Reliability, on-call load |
| Enterprise Customer | Ops Manager | Input | Usability, real-time accuracy |

---

## Prompt Deconstruction

**The Vague Request:**
> "Real-time visibility into drone fleet with mission planning and regulatory compliance"

**Technical Translation:**

| Client Phrase | Engineering Reality | Key Decision Unlocked |
|---------------|--------------------|-----------------------|
| "real-time visibility" | Sub-500ms telemetry pipeline: MQTT to Kafka to WebSocket push to React dashboard | Stateful WebSocket infra; horizontal scaling for 25K streams |
| "mission planning" | Geospatial engine: KML/GeoJSON waypoint validation, airspace class lookup, geofence polygon intersection | PostGIS database, FAA LAANC API integration |
| "regulatory compliance" | Automated log generation in FAA DroneZone XML + EASA U-Space ASTERIX format | Dual-format report engine, jurisdiction detection by GPS coords |
| "multi-tenant" | Row-level tenant isolation in PostgreSQL + per-tenant Kafka topics + per-tenant rate limits | DB partitioning model, noisy-neighbor controls |
| "500 drones per tenant" | 500 drones x 1 msg/sec x 500 tenants = 250,000 msg/sec peak ingest | Kafka partitioning, consumer sizing, storage IOPS |

---

## Dimension 1: Technical Physics

### 1.1 Traffic Model

| Metric | Nominal | Peak | Basis |
|--------|--------:|-----:|-------|
| Telemetry messages/sec | 5,000 | 25,000 | 50 tenants x avg 100 drones x 1 msg/sec; peak = 500 tenants x 500 drones |
| Concurrent WebSocket connections | 500 | 2,500 | 1 ops manager per 10 active drones |
| Mission planning API (RPS) | 50 | 500 | Batch uploads during shift start |
| Video stream sessions (concurrent) | 50 | 300 | 1 stream per active incident |
| Read/Write ratio (telemetry DB) | 90% R / 10% W | | Dashboard queries dominate |
| Burst factor | 5x nominal | | Shift start window 07:00-09:00 |

### 1.2 Little's Law Calculation

```
L  = lambda x W
L  = 5,000 messages in-flight concurrently
lambda = 5,000 msg/sec (nominal)
W  = 1 second end-to-end budget

Latency budget allocation:
  MQTT broker ingestion:        50 ms
  Kafka produce + consume:     150 ms
  Telemetry processing:         50 ms
  WebSocket fan-out:           150 ms
  Network (cellular to cloud): 100 ms
  TOTAL:                       500 ms  (p95 target)

Peak (25,000 msg/sec): Kafka must scale to 50 partitions minimum.
Auto-scale trigger: Kafka consumer lag > 10,000 messages.
```

### 1.3 Latency Budget

| Tier | Target p50 | Target p95 | Target p99 | SLA Breach Action |
|------|----------:|----------:|----------:|-------------------|
| Telemetry ingest (MQTT broker) | 20 ms | 50 ms | 100 ms | Alert P2; scale broker |
| Kafka end-to-end | 50 ms | 150 ms | 300 ms | Alert P2; add partitions |
| Dashboard WebSocket push | 100 ms | 300 ms | 500 ms | Alert P1 if >500ms |
| Mission planning API | 80 ms | 200 ms | 400 ms | Alert P2 |
| Video stream startup | 500 ms | 2,000 ms | 5,000 ms | Alert P3 |
| Compliance report generation | 2s | 10s | 30s | Async; no SLA breach |

### 1.4 Data Volume

| Dataset | 12-Month Growth | 3-Year Projection | Archival Strategy |
|---------|----------------:|------------------:|-------------------|
| Telemetry time-series (raw) | 2 TB/month | 72 TB | Hot 30d -> Warm 90d -> Cold S3 Glacier |
| Flight logs (structured) | 50 GB/month | 1.8 TB | Hot 90d -> Cold 7 years (FAA) |
| Video recordings | 500 GB/month | 18 TB | Hot 7d -> Cold 30d -> Delete (GDPR) |
| Compliance reports | 2 GB/month | 72 GB | 7 years (regulatory) |

---

## Dimension 2: Regulatory & Compliance

| Regulation | Applicable | Key Obligation | Enforcement Deadline |
|------------|:----------:|----------------|----------------------|
| FAA Part 107 (USA) | Yes | Log retention 3 years; LAANC airspace auth; Remote ID | Day 1 launch |
| EASA U-Space (EU) | Yes | USSP registration; ASTERIX flight data format; geo-awareness | EU expansion Month 9 |
| DGCA NPNT (India) | Yes | No-Permission-No-Takeoff digital token; pre-approval | India Month 15 |
| GDPR (EU users) | Yes | Video + PII data residency in EU; right-to-delete; 72-hr breach notification | EU expansion Month 9 |
| CCPA (California) | Yes | Opt-out of data sale; privacy notice; consumer rights portal | Day 1 launch |
| SOC 2 Type II | Yes | Yearly audit; availability, confidentiality, security principles | Month 12 |
| ISO 27001 | Planned | Information security management certification | Month 18 |

**Audit Trail:**
- Flight log retention: 3 years (FAA) / 7 years (EU commercial aviation)
- Immutability: S3 Object Lock (Compliance mode) for all flight and compliance logs
- Breach notification: 72 hours to supervisory authority (GDPR Art. 33)

---

## Dimension 3: Security & Threat Surface

### 3.1 Authentication & Authorization

| Mechanism | Standard | Token Lifetime | Refresh Strategy |
|-----------|----------|---------------:|------------------|
| User Auth | OAuth 2.0 + OIDC (Auth0) | Access token: 15 min | Refresh token: 7 days, rotated on use |
| Drone-to-Cloud | Mutual TLS (X.509 cert per drone) | Cert: 1 year | Auto-rotate via ACME |
| Service-to-Service | JWT signed RS256 | 5 min | Service account rotation every 90 days |
| Admin Auth | MFA mandatory (TOTP + hardware key) | Session: 4 hours | Re-auth on privilege escalation |
| Authorization Model | RBAC at tenant level (Fleet Admin / Operator / Viewer) + ABAC for drone ownership | | |

### 3.2 STRIDE Threat Model

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Privilege Escalation |
|-----------|----------|-----------|-------------|-----------------|-----|----------------------|
| MQTT Broker | mTLS cert per drone; reject unknown certs | HMAC-SHA256 signed payloads | Kafka offset = immutable audit | TLS 1.3 in transit | 100 msg/sec rate limit per client | Drone cannot publish to another tenant's topic |
| Mission Planning API | JWT Bearer + tenant claim | Geofence polygon signature verification | Logged with user ID + timestamp | AES-256 at rest | 500 RPS per tenant; circuit breaker | Fleet Admin only can approve missions |
| PostgreSQL | IAM role auth; no direct internet access | Row-level security (tenant_id) | pgaudit logging | Encrypted at rest; no PII in app logs | Connection pool limits | App role -- no DBA access from app layer |
| Video Streams | Signed URL (15-min expiry) | SRTP for live streams | Session ID logged | HLS AES-128 encryption | Concurrent stream cap per tenant | Viewer sees only own tenant's streams |

### 3.3 Abuse Vectors

| Attack Vector | Likelihood | Impact | Defense |
|---------------|:----------:|:------:|---------|
| GPS spoofing (fake drone position) | HIGH | HIGH | Cross-validate GPS with barometric alt + acceleration delta; alert on position jump > 50m in 1s |
| MQTT topic hijacking (drone impersonation) | MEDIUM | HIGH | Per-drone X.509 cert; topic ACL = cert CN must match topic prefix |
| Tenant data leakage (broken RLS) | MEDIUM | CRITICAL | Row-level security at DB layer; per-tenant Kafka topic ACLs; canary sentinel records in integration tests |
| Compliance report forgery | LOW | CRITICAL | Reports signed with platform private key; hash stored in WORM S3; immutable ledger entry |

---

## Dimension 4: Failure & Resilience

### 4.1 Availability Targets

| Service Tier | SLA | Downtime/Month | Architecture |
|--------------|----:|---------------:|--------------|
| Telemetry ingest pipeline | 99.9% | 43.8 min | Active-Active multi-AZ Kafka; MQTT broker cluster |
| Mission planning API | 99.9% | 43.8 min | Multi-AZ EKS; ALB health-check routing |
| Dashboard (read) | 99.5% | 3.65 hrs | CDN-cached static assets; read replica fallback |
| Compliance reporting | 99.0% | 7.3 hrs | Async job queue; retry on failure |
| Video streaming | 98.0% | 14.4 hrs | Best-effort; no contractual SLA |

### 4.2 Recovery Objectives

| Scenario | RPO | RTO | Strategy |
|----------|----:|----:|----------|
| Single AZ failure | 0 (no data loss) | < 2 min | Multi-AZ ALB auto-routing |
| Regional failure | 1 min (Kafka replication lag) | < 15 min | Active-Passive DR in us-west-2; Route53 failover |
| Database primary failure | 30 sec (replica lag) | < 1 min | RDS Multi-AZ automatic failover |
| Kafka broker failure | 0 (replication factor 3) | < 30 sec | Kafka auto-leader election |

### 4.3 CAP Theorem Decisions

| Data Domain | Consistency | Reason |
|-------------|-------------|--------|
| Telemetry (live position) | AP (Eventual) | Stale position 2s ago is fine; availability is safety-critical |
| Mission plan (waypoints) | CP (Strong) | Drone must fly the approved mission -- no stale reads allowed |
| Compliance flight logs | CP (Strong) | Regulatory audit requires exact data |
| Dashboard analytics | AP (Eventual) | 5-min stale analytics is acceptable |

### 4.4 Graceful Degradation States

| Dependency Down | Degraded Behavior | User Impact | Recovery Trigger |
|-----------------|-------------------|-------------|------------------|
| Primary telemetry DB | Serve from Redis cache (last 60s) | Positions stale <= 60s | DB health check restored |
| Kafka cluster | MQTT broker buffers to disk (max 1 GB/broker) | Telemetry delayed up to 5 min | Kafka cluster restored |
| FAA LAANC API | Queue mission; manual approval workflow | No autonomous takeoff; operator alerted | LAANC health check restored |
| Auth0 (IdP) | Cache last-valid JWT for 15 min | No new logins for 15 min | Auth0 restored |

---

## Dimension 5: Cost & FinOps

### 5.1 Cloud Spend Envelope

| Phase | Monthly Target | Monthly Hard Cap | FinOps Review |
|-------|---------------:|----------------:|---------------|
| MVP (Month 1-6) | $12,000 | $18,000 | Monthly |
| Launch (Month 7-12) | $35,000 | $50,000 | Bi-weekly |
| Growth (Year 2) | $85,000 | $120,000 | Weekly |

### 5.2 Build vs Buy

| Capability | Decision | Rationale |
|------------|----------|-----------|
| Auth / IdP | Buy (Auth0, $0.023/MAU) | 6-month dev save; SOC 2 pre-certified |
| Telemetry time-series DB | Buy (Amazon Timestream) | Managed, serverless, $0.50/GB |
| MQTT Broker | Buy (AWS IoT Core, $1/million msgs) | Scales to 1M connections; managed |
| Video streaming | Buy (AWS Kinesis Video Streams) | Complex to self-host |
| Airspace data | Buy (Airspace Link API, $500/month) | FAA LAANC integration pre-built |
| Mission planning engine | Build | Core IP; no viable off-the-shelf option |
| Compliance report engine | Build | Custom FAA/EASA format logic |
| Dashboard (React) | Build | Tenant-branded UI differentiation |

### 5.3 3-Year TCO

| Year | Infra (AWS) | SaaS/Licensing | Personnel | Total |
|------|------------:|---------------:|----------:|------:|
| Y1 | $294,000 | $96,000 | $1,800,000 | $2,190,000 |
| Y2 | $720,000 | $144,000 | $2,400,000 | $3,264,000 |
| Y3 | $1,440,000 | $192,000 | $3,000,000 | $4,632,000 |
| **3-Year Total** | **$2,454,000** | **$432,000** | **$7,200,000** | **$10,086,000** |

Break-even: 210 enterprise customers at $48K/year ACV = $10.08M ARR covers 3-year TCO.

---

## Dimension 6: Data Residency & Sovereignty

| Data Class | Residency Constraint | Allowed Regions | Cross-Border Transfer | Encryption at Rest |
|------------|---------------------|-----------------|----------------------|--------------------|
| EU user PII (GDPR) | EU only | eu-west-1 (Ireland) | SCCs required for US support access | AES-256 + KMS CMK |
| EU flight logs (EASA) | EU only | eu-west-1 | Not permitted | AES-256 + KMS CMK |
| US flight logs (FAA) | USA only | us-east-1, us-west-2 | Not permitted | AES-256 + KMS CMK |
| India NPNT tokens | India only | ap-south-1 (Mumbai) | Not permitted | AES-256 + KMS CMK |
| Video recordings | Same region as tenant | Per-tenant region | Not permitted without consent | AES-256 |
| Anonymized analytics | Any region | us-east-1 (primary) | Permitted | AES-256 |

**Implementation:** Multi-region AWS; tenant-to-region mapping in Control Plane DB. Tenant selects home region at onboarding.

---

## Dimension 7: Edge & Hardware Constraints

| Device Type | OS / Firmware | Connectivity | Offline Requirement |
|-------------|--------------|--------------|---------------------|
| DJI Matrice 300 RTK | DJI SDK v5 (ARM) | 4G LTE + 900MHz RC | 90-sec telemetry buffer on signal loss |
| Parrot ANAFI USA | GroundSDK (ARM) | WiFi + 4G | 60-sec buffer |
| Autel EVO II (Year 2) | Autel SDK (ARM) | 4G LTE | 60-sec buffer |
| Ground Control Station | Ubuntu 20.04 (x86) | Ethernet/WiFi | Full offline mission planning |

**Edge Strategy:**
- Onboard autonomy (obstacle avoidance, emergency landing): drone firmware -- not platform scope
- Telemetry buffering: SDK-level circular buffer; flush to MQTT on connectivity restore
- Sync protocol: MQTT over TLS 1.3; QoS Level 1 (at-least-once delivery)
- Conflict resolution: Server-side deduplication by (drone_id, timestamp_ms); last-write-wins on same timestamp

---

## Dimension 8: Connectivity & Integration

| System | Protocol | Auth | SLA | Failure Behaviour |
|--------|----------|------|----:|-------------------|
| DJI Mobile SDK v5 | SDK + MQTT bridge | App-level API key | 99.5% | Buffer 90s; retry; alert if gap > 90s |
| Parrot GroundSDK | SDK + MQTT bridge | API key | 99.0% | Buffer 60s; retry |
| FAA LAANC (Airspace Link) | REST | OAuth 2.0 Client Credentials | 99.0% | Queue mission; manual approval fallback |
| EASA U-Space USSP | REST + ASTERIX | mTLS | 99.5% | Queue; alert compliance team |
| Aviation Weather API | REST | API Key | 95.0% | Serve cached forecast (6-hr stale OK) |
| Auth0 (IdP) | OIDC | Client credentials | 99.9% | Cache last-valid JWT; block new logins max 15 min |

**Event Bus:** Apache Kafka on Amazon MSK. Topics: `telemetry.raw.<tenant_id>`, `mission.events.<tenant_id>`, `incidents.<tenant_id>`. Schema registry: AWS Glue (Avro). Exactly-once delivery: required for mission state transitions only (Kafka transactions).

---

## Dimension 9: Observability Requirements

### 9.1 Logging Standard

All services emit structured JSON:
```json
{"ts":"2026-05-15T07:00:00Z","level":"INFO","service":"telemetry-processor",
 "trace_id":"abc123","tenant_id":"t_xyz","drone_id":"d_001","msg":"Telemetry processed"}
```
PII scrubbing: drone GPS coordinates hashed in analytics logs. Retention: CloudWatch 30d hot; S3 1-year archive.

### 9.2 Key Metrics (RED + USE)

| Metric | Alert Threshold | Page Threshold |
|--------|----------------:|---------------:|
| `telemetry.pipeline.latency_p95` | > 400 ms | > 800 ms |
| `kafka.consumer.lag` | > 10,000 msgs | > 50,000 msgs |
| `mission.api.error_rate` | > 1% | > 5% |
| `incident.detection.latency_p95` | > 5s | > 15s |
| `db.connection_pool.saturation` | > 70% | > 90% |

### 9.3 Tracing & Alerting

- Standard: OpenTelemetry -> AWS X-Ray; W3C TraceContext headers
- Sampling: 100% errors + 5% success (head-based)
- P1 (5-min response): Telemetry pipeline >800ms; Kafka lag >50K; data breach detected
- P2 (30-min response): Error rate >1%; p95 >400ms; drone signal loss
- P3 (business hours): Resource saturation >70%

---

## Dimension 10: Lifecycle & Maintainability

| Concern | Decision | Rationale |
|---------|----------|-----------|
| API versioning | URI path (/v1/, /v2/) | Explicit; cache-friendly; industry standard |
| Backward compat window | 12 months after new version GA | Enterprise customers need migration runway |
| Deprecation notice | 6 months minimum written notice | SOC 2 change management requirement |
| DB migrations | Flyway (schema versioning in Git) | CI-enforced; reversible; auditable |
| Dependency updates | Renovate Bot (weekly automated PRs) + manual approval | Balance freshness with stability |
| Blue-green deploy | Yes -- ALB weighted routing 10% canary to 100% over 30 min | Zero-downtime; rollback in <5 min |
| Feature flags | LaunchDarkly (per-tenant flag targeting) | Gradual rollout; kill switch per tenant |

**Migration risk:** Telemetry table exceeds 10M rows within 3 months. All migrations must be online (pg_repack; no table locks). Zero-downtime migrations only.

---

## Dimension 11: Human Interface & UX

### 11.1 Persona Matrix

| Persona | Device | Connectivity | Key Goal |
|---------|--------|-------------|---------|
| Fleet Operations Manager | Desktop + 27" monitor | Ethernet (ops center) | Full fleet situational awareness; map-centric view |
| Field Drone Operator | iPad + iPhone | 4G LTE (field) | Mission execution; real-time alerts |
| Compliance Officer | Desktop | Ethernet | Generate regulatory reports in 1 click |
| Tenant System Admin | Desktop | Ethernet | User management; API key management |

### 11.2 Accessibility & i18n

- WCAG 2.1 AA: Screen reader for alerts; keyboard navigation for map; 4.5:1 contrast; color-blind-safe palette
- Locales at launch: en-US, en-GB; Phase 2: de-DE, fr-FR, ja-JP

### 11.3 Offline UX

- GCS offline mode: Full mission planning and geofence editing offline; sync on reconnect
- Service Worker: Caches map tiles (24h); mission planner; last-known fleet state
- Conflict resolution: Server-authoritative; offline missions validated against live airspace data on sync

---

## Dimension 12: Data Privacy & Ethics

### 12.1 PII Inventory

| Data Element | Classification | Retention | Anonymization |
|--------------|---------------|----------:|---------------|
| Pilot email / name | PII | Account lifetime + 30 days | Hashed in analytics after 90 days |
| Drone GPS position (live) | Commercially sensitive | 90 days hot; 3 years cold | Aggregated to 1 km grid for analytics |
| Video footage | Sensitive (may capture persons) | 7 days default; configurable | Deleted on schedule; no platform-level analysis |
| Flight logs | Regulatory | 3-7 years | Never -- regulatory requirement |
| IP address | PII | Logs 90 days | Truncated to /24 in analytics |

### 12.2 Consent & Rights

| Right | Mechanism | SLA |
|-------|-----------|----:|
| Right to Access | Self-service export (JSON/CSV) | 30 days |
| Right to Erasure | Account deletion; cascades to PII (except regulatory flight logs) | 30 days |
| Right to Portability | Export missions, logs, telemetry in open format | 30 days |
| Consent withdrawal | Toggle in account settings | Immediate |

**Conflict:** GDPR erasure vs FAA 3-year retention for flight logs. Resolution: flight logs flagged as regulatory-retained; excluded from erasure; disclosed in privacy policy and ToS. Legal review required.

---

## Dimension 13: Third-Party Dependencies

| Vendor | Function | Lock-in Risk | Exit Strategy | Annual Cost |
|--------|----------|:------------:|---------------|------------:|
| AWS | Primary cloud | HIGH | Multi-cloud IaC (Terraform); 12-month migration | $294K Y1 |
| Auth0 | Identity Provider | MEDIUM | Migrate to Keycloak (self-hosted); 3-month effort | $36K/yr |
| DJI SDK | Drone telemetry (primary) | HIGH | Drone Adapter Layer abstraction; 6-month swap | $0 (free SDK) |
| Airspace Link | FAA LAANC integration | MEDIUM | Direct FAA API; 6-month effort | $6K/yr |
| LaunchDarkly | Feature flags | LOW | Migrate to Unleash (OSS); 1-month effort | $12K/yr |
| Amazon MSK | Managed Kafka | HIGH | Self-managed Kafka on EKS; 3-month migration | $36K/yr |

**SBOM:** Syft in CI pipeline per release. Dependency scanning: Dependabot + Trivy. Container signing: Cosign (Sigstore).

---

## Dimension 14: Scaling & Multi-Tenancy

### 14.1 Scaling Model

| Service | Scaling Axis | Scale-Out Trigger | Max Instances |
|---------|-------------|------------------:|:-------------:|
| Kafka (MSK) | Add brokers + partitions | Consumer lag > 10K msgs | 15 brokers |
| Telemetry Processor | Horizontal (EKS HPA) | CPU > 60% or Kafka lag > 5K | 50 pods |
| Mission Planning API | Horizontal (EKS HPA) | CPU > 60% or RPS > 300 | 20 pods |
| Dashboard BFF | Horizontal (EKS HPA) | WebSocket connections > 400/pod | 30 pods |
| PostgreSQL (RDS) | Vertical + Read Replicas | CPU > 70% | 1 primary + 3 replicas |

### 14.2 Multi-Tenancy Model

| Dimension | Decision | Rationale |
|-----------|----------|-----------|
| Isolation model | Pool (shared infra) + Row-level security | <$50/tenant/month at 500 tenants; RLS enforced at DB layer |
| Data partitioning | tenant_id FK on all tables; PostgreSQL row security policies | Prevents cross-tenant leakage at DB layer |
| Kafka isolation | Per-tenant topic prefix: `telemetry.raw.<tenant_id>` | Prevents topic pollution |
| Noisy-neighbor control | Per-tenant rate limits: MQTT 1,000 msg/sec; API 500 RPS | |
| Tenant onboarding | Automated (Terraform workspace per tenant) | |

### 14.3 Elasticity SLAs

- Scale-out: New pods healthy within 90 seconds of HPA trigger
- Scale-in cooldown: 5 minutes (prevent thrashing during burst windows)
- Minimum warm instances: 3 per critical service (Telemetry Processor, Mission API, Dashboard BFF)

---

## Dimension 15: Environmental & Sustainability

### 15.1 SCI Score

```
SCI = (E x I) + M  per 1,000 telemetry messages processed

E  = 0.002 kWh per 1,000 messages
I  = 415 gCO2/kWh (us-east-1 grid average 2026)
M  = 0.5 gCO2 (amortized hardware embodied carbon)

SCI baseline = (0.002 x 415) + 0.5 = 1.33 gCO2eq per 1,000 messages
At 5,000 msg/sec: ~210 tCO2e/year

Target: Reduce to 147 tCO2e/year by Year 2 (30% reduction via ARM + region selection).
```

### 15.2 GreenOps Targets

| Initiative | Implementation | Saving |
|------------|---------------|--------|
| Graviton3 (ARM) instances | Replace x86 for Telemetry Processor + Mission API | ~25% energy |
| Spot instances for batch | Compliance reports + archival jobs | ~40% cost; ~35% carbon |
| eu-west-1 for EU tenants | Ireland: 96% renewable energy | ~55% carbon for EU workloads |
| Auto-scale to zero (non-prod) | Spin down dev/staging after 20 min idle | ~15% overall |

| Metric | Baseline | 12-Month Target | 36-Month Target |
|--------|:--------:|:---------------:|:---------------:|
| SCI score (gCO2e/1K msgs) | 1.33 | 1.10 | 0.93 |
| Graviton instance % | 0% | 60% | 90% |

---

## Critical Edge Cases & Failure Modes

| ID | Edge Case | Potential Impact | Required Defense |
|----|-----------|-----------------|--------------------|
| EC-01 | GPS spoofed telemetry (attacker sends false position) | Drone appears wrong location; compliance log falsified | Cross-validate GPS with barometric alt + accelerometer delta; alert on position jump > 50m in 1s |
| EC-02 | Tenant A queries Tenant B's telemetry (broken RLS) | Critical data breach; regulatory violation | Row-level security + canary sentinel records in integration tests per release |
| EC-03 | 500 drones launch simultaneously (fleet shift start) | Kafka consumer lag spike; dashboard unresponsive | Pre-warm 10 extra consumer pods 5 min before shift; Kafka lag alert at 10K |
| EC-04 | Drone enters geofence mid-mission (wind drift) | Regulatory violation | Geofence check on drone (SDK) + server-side; breach detected <1s; alert <3s |
| EC-05 | LAANC API down during mission planning | Fleet grounded | Queue missions; manual approval fallback; degraded mode badge on UI |
| EC-06 | Video stream saturates telemetry pipeline network | Position data delayed | Separate network path; QoS: telemetry > video |
| EC-07 | GDPR erasure request conflicts with FAA 3-year flight log retention | Legal contradiction | Regulatory-retained flag on flight logs; excluded from erasure; disclosed in ToS |

---

## Architectural Trade-offs

### Option A: Active-Active Multi-Region (High-Reliability)

| Attribute | Detail |
|-----------|--------|
| Architecture | Kafka multi-region replication; active-active us-east-1 + eu-west-1; 0 RPO |
| Pros | Zero data loss; sub-100ms failover; EASA data residency native |
| Cons | 2.5x infra cost; complex operations; 4-month additional engineering |
| Infra Cost (monthly) | ~$87,000 |
| Time to Market | 18 months |

### Option B: Single-Region + Passive DR (Recommended for MVP)

| Attribute | Detail |
|-----------|--------|
| Architecture | us-east-1 primary; us-west-2 passive DR (1-min RPO); eu-west-1 for EU tenants |
| Pros | 40% lower cost; 12-month TTM; simpler operations; extensible to Option A |
| Cons | 1-min RPO on regional failure; 15-min RTO for DR failover |
| Infra Cost (monthly) | ~$35,000 |
| Time to Market | 12 months |

**Recommendation:** Option B for launch. Architect for Option A migration in Year 2.

---

## Interrogation List

| # | Question | Impact if Unresolved | Priority |
|---|----------|---------------------|:--------:|
| 1 | Is 1-minute RPO on regional failure acceptable, or is near-zero RPO required from Day 1? | $52K/month infra difference; Option A vs B decision | HIGH |
| 2 | Do enterprise customers require dedicated compute pods (single-tenant), or is pool + RLS sufficient? | 3x cost difference | HIGH |
| 3 | Which EU regulations apply at launch -- EASA U-Space only, or also national laws (German LuftVO)? | Report formats and data residency strictness | HIGH |
| 4 | Is live video streaming required at MVP, or can it be deferred to Month 9? | Video saves 3 months TTM if deferred | MEDIUM |
| 5 | Compliance reporting -- premium add-on or included in base subscription? | Build priority at MVP vs later | MEDIUM |
| 6 | Customers bring their own drones, or does platform include hardware procurement? | Device management feature scope | LOW |
