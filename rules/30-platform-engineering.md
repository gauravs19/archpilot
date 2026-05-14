# Platform Engineering Standards

> **Purpose:** This rule file defines standards for building Internal Developer Platforms (IDPs)
> — the "golden paths" that accelerate engineering teams by abstracting infrastructure complexity.
> Platform engineering turns cloud primitives into opinionated, self-service capabilities.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Underlying cloud primitives |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | Pipelines that platforms expose |
| [24 — Team Topology](./24-team-topology.md) | Platform team as enabling team |
| [29 — Agentic AI Governance](./29-agentic-ai-governance.md) | AI integration on the platform |

---

## 1. Core Concepts

### 1.1 What is Platform Engineering?

Platform engineering creates a curated product — the Internal Developer Platform (IDP) — that
provides developers with self-service infrastructure, deployment pipelines, observability, and
policy enforcement without requiring deep infrastructure expertise.

**Key principle:** The platform is a product. Developer experience is its KPI.

### 1.2 Golden Paths vs Paved Roads

| Concept | Definition | Rule |
|---------|-----------|------|
| **Golden Path** | The recommended, highest-quality way to do something | Every team SHOULD use golden paths; deviation requires justification |
| **Paved Road** | A supported, well-lit path that may not be the absolute best | Acceptable for teams with specific needs |
| **Off-road** | Custom solution outside platform support | Requires architecture review; team owns full support burden |

**Rule:** Golden paths MUST exist for: service creation, deployment, observability setup, and secret management.

---

## 2. IDP Core Capabilities

Every mature IDP MUST provide these capabilities as self-service:

| Capability | What It Provides | Maturity Level |
|-----------|-----------------|:-------------:|
| **Service Scaffolding** | Template-based new service creation with golden path defaults | L1 (Basic) |
| **CI/CD Pipelines** | Pre-built, opinionated pipelines (lint, test, scan, deploy) | L1 (Basic) |
| **Secret Management** | Self-service secret rotation with vault integration | L1 (Basic) |
| **Observability Stack** | Auto-instrumented logs, metrics, traces per new service | L2 (Standard) |
| **Infrastructure Self-Service** | On-demand databases, queues, caches via catalog | L2 (Standard) |
| **Developer Portal** | Searchable catalog of services, APIs, runbooks, ownership | L2 (Standard) |
| **Policy Enforcement** | Automated compliance gates (security, cost, naming) | L3 (Advanced) |
| **AI Assistance** | LLM-powered development help with platform context | L3 (Advanced) |

---

## 3. Service Scaffolding Standards

### 3.1 Service Template Requirements

Every language/runtime golden path template MUST include:

- [ ] Dockerfile with multi-stage build and non-root user
- [ ] Health check endpoint (`/health`, `/ready`)
- [ ] Structured logging setup (JSON, with correlation ID)
- [ ] OpenTelemetry instrumentation (auto-configured)
- [ ] CI/CD pipeline definition (test, scan, build, push)
- [ ] Secrets injection pattern (no hardcoded values)
- [ ] README with: purpose, local setup, environment variables, runbook link
- [ ] `OWNERS` file for team ownership
- [ ] Default resource limits (CPU/memory requests and limits for Kubernetes)

### 3.2 Service Catalog Entry Requirements

Every service registered in the platform catalog MUST have:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Handles payment processing and refunds
  tags: [payments, financial, critical]
  annotations:
    github.com/project-slug: org/payment-service
    pagerduty.com/integration-key: "xxx"
    grafana/dashboard-url: "https://..."
spec:
  type: service
  lifecycle: production
  owner: team-payments
  system: checkout-platform
  dependsOn:
    - component:fraud-detection-service
    - resource:payments-db
  providesApis:
    - payment-api-v2
```

---

## 4. Developer Portal Standards

### 4.1 Portal Must-Have Features

| Feature | Purpose |
|---------|---------|
| **Service catalog** | Searchable inventory of all services with owner, status, docs |
| **API catalog** | Browsable API contracts with live try-it-out capability |
| **Tech radar** | Org technology landscape (Adopt / Trial / Hold / Retire) |
| **Runbook library** | Searchable per-service operational runbooks |
| **Dependency graph** | Visual service-to-service dependency map |
| **Cost dashboard** | Per-team, per-service cloud cost attribution |
| **Incident history** | Service-specific incident history and post-mortems |
| **Onboarding wizard** | Self-service new service creation through the portal |

### 4.2 Portal Data Quality Rules

- Every service MUST have an owner (no orphaned services)
- API contracts MUST match the deployed version (auto-synced via CI)
- Runbooks MUST be reviewed within 6 months of last incident
- Cost data MUST be refreshed daily
- Dependency graph MUST be auto-generated (no manual updates)

---

## 5. Platform SLOs (Platform as a Product)

The platform team MUST define and publish SLOs for platform services:

| Service | SLO | Measurement |
|---------|-----|------------|
| CI pipeline trigger to start | <30 seconds | p95 |
| Full build + test + deploy cycle | <15 minutes | p95 |
| Secret rotation propagation | <2 minutes | p95 |
| New service scaffold creation | <5 minutes | p95 |
| Portal page load | <2 seconds | p95 |
| Portal search results | <500ms | p95 |

**Rule:** Platform SLO breaches trigger the same incident process as production SLO breaches.

---

## 6. Platform Engineering Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Platform as a gatekeeper | Teams wait weeks for infra; velocity suffers | Self-service first; approval is the exception |
| Snowflake environments | Inconsistent dev/staging/prod; "works on my machine" | IaC-driven, immutable environments from the platform |
| No golden paths | Every team reinvents CI, logging, secrets | Platform team owns opinionated defaults |
| Platform with no SLOs | Platform is best-effort; teams lose trust | Publish and measure platform SLOs |
| No developer feedback loop | Platform solves wrong problems | Quarterly developer satisfaction surveys; NPS tracking |
| Platform team owns all infra | Bottleneck; platform team burned out | Platform provides self-service; product teams own their infra within guardrails |

---

## 7. Platform Engineering Checklist

- [ ] Golden paths exist for service creation, deployment, observability, and secret management
- [ ] Service templates include: Dockerfile, health checks, structured logging, OTel, CI/CD
- [ ] Developer portal has service catalog, API catalog, and tech radar
- [ ] All services have owners in the catalog (no orphans)
- [ ] Platform SLOs published and monitored
- [ ] Cost attribution per team/service available in portal
- [ ] Policy enforcement automated in CI (not manual review)
- [ ] Developer satisfaction measured quarterly

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
