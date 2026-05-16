# Rule 50: Archpilot Multi-Agent Pipeline (v4.0)

<!-- Archpilot: 50-agent-pipeline.md | Version: 4.0 -->
<!-- Status: MANDATORY | Enforced by: archpilot.py lint + pipeline.py -->

> **Purpose:** This rule governs the full 5-phase agentic pipeline that transforms a
> high-level business requirement into a complete, enterprise-grade architecture artifact set.
> Every phase has mandatory structural constraints that are machine-enforceable.

---

## 1. Pipeline Overview

```
Input.md  →  Phase 0  →  Phase 1  →  Phase 2  →  Phase 3  →  Phase 4
(HLR)       SE Agent    PO Agent    Arch Agent  Arch Agent  Review Agent
            Discovery   Backlog     HLD         LLD(s)      Guardrail Audit
```

| Phase | Agent | Input | Output Artifact | Primary Guardrail |
|-------|-------|-------|-----------------|-------------------|
| 0 | SE Agent (Solutions Engineer) | Input.md | discovery.md | 15 dimensions, no vague adjectives |
| 1 | PO Agent (Product Owner / BA) | discovery.md | requirements.md | 10-20 Epics, 50-150 Stories |
| 2 | Arch Agent (Senior Architect) | discovery.md + requirements.md | Design_HLD.md | 14 sections, C4 diagrams, Rationale + Strategy |
| 3 | Arch Agent (Senior Architect) | Design_HLD.md + requirements.md | Design_LLD_[Service].md × N | 12 sections per LLD, numeric thresholds |
| 4 | Review Agent (Guardrail Auditor) | All artifacts | review_report.md | 12-dimension audit, 0-100 score |

---

## 2. Phase 0: SE Agent — Deep Discovery

**Artifact:** `discovery.md`

### 2.1 Mandatory Dimensions (all 15 required)

| # | Dimension | Key Outputs |
|---|-----------|-------------|
| 1 | Technical Physics | TPS/RPS, Little's Law, latency budget (p50/p95/p99), data volumes |
| 2 | Regulatory & Compliance | Applicable laws, audit trail, certification scope, breach timelines |
| 3 | Security & Threat Surface | STRIDE model, zero-trust posture, auth/authz model |
| 4 | Failure & Resilience | RPO/RTO per tier, CAP theorem choice, graceful degradation states |
| 5 | Cost & FinOps | 3-year TCO, cloud spend envelope, build vs buy decisions |
| 6 | Data Residency & Sovereignty | Geo-fencing, cross-border rules, data classification, jurisdiction |
| 7 | Edge & Hardware Constraints | IoT/device specs, offline operation, OTA strategy |
| 8 | Connectivity & Integration | External system inventory, protocols, legacy adapters |
| 9 | Observability Requirements | Logging standard, RED/USE metrics, tracing, alerting tiers |
| 10 | Lifecycle & Maintainability | API versioning, upgrade paths, deprecation policy |
| 11 | Human Interface & UX | Persona matrix, accessibility (WCAG), i18n/l10n, offline UX |
| 12 | Data Privacy & Ethics | PII inventory, retention limits, consent model, right-to-delete |
| 13 | Third-Party Dependencies | Vendor lock-in risk, exit strategies, SBOM, license compliance |
| 14 | Scaling & Multi-Tenancy | Scaling triggers, tenant isolation model, noisy-neighbor controls |
| 15 | Environmental & Sustainability | SCI score, GreenOps targets, carbon-aware scheduling |

### 2.2 Quality Constraints

- **NO vague adjectives:** fast, scalable, resilient, efficient, flexible, performant are LINT ERRORS.
- **Quantified answers only:** Every field must contain a number, range, or explicit architectural decision.
- **Interrogation List mandatory:** discovery.md MUST end with a table of client questions that block Phase 1.
- **Architectural Trade-offs mandatory:** Two options (high-reliability vs cost-optimised) with explicit cost and TTM.

---

## 3. Phase 1: PO Agent — Requirements Breakdown

**Artifact:** `requirements.md`

### 3.1 Structural Constraints (10:10:50 Rule)

| Metric | Minimum | Maximum | Enforcement |
|--------|--------:|--------:|-------------|
| Epics | 10 | 20 | `archpilot lint --tier 3` |
| User Stories (total) | 50 | 150 | `archpilot lint --tier 3` |
| Stories per Epic | 5 | 10 | Per-epic validation |

### 3.2 Epic Category Requirements

All epics MUST be tagged with one of these categories:

| Category | Scope |
|----------|-------|
| FUNCTIONAL | Core business capabilities |
| DATA & STORAGE | Data models, storage, migration, retention |
| SECURITY & COMPLIANCE | Auth, authz, audit, regulatory |
| INTEGRATION & APIs | External systems, event contracts, API versioning |
| NON-FUNCTIONAL | Performance, availability, scalability, cost |
| DEVOPS & PLATFORM | CI/CD, IaC, secrets, environment management |
| TESTING & QUALITY | Test strategy, coverage, contract tests, chaos |
| MIGRATION & CUTOVER | Data migration, shadow mode, rollback |

### 3.3 Story Quality Constraints

Every User Story MUST have:
- **ID:** `EP-[NN]-S-[NN]` format
- **As a / I want / So that:** all three fields populated
- **Acceptance Criteria:** 3-5 EARS-compliant conditions, all measurable
- **Priority:** MoSCoW (Must / Should / Could / Won't)
- **Story Points:** Fibonacci (1/2/3/5/8/13)
- **Discovery Ref:** `DIM-[NN]` linking to the source dimension

### 3.4 EARS Notation (mandatory for all ACs)

| Pattern | Syntax |
|---------|--------|
| Ubiquitous | `The system SHALL <action>` |
| Event-driven | `WHEN <trigger>, the system SHALL <action>` |
| State-driven | `WHILE <state>, the system SHALL <action>` |
| Unwanted | `IF <precondition>, the system SHALL NOT <action>` |
| Optional | `WHERE <feature> is included, the system SHALL <action>` |

**Forbidden in ACs:** TBD, TODO, "should be fast", "user-friendly", "scalable", or any vague adjective.

---

## 4. Phase 2: Arch Agent — High-Level Design

**Artifact:** `Design_HLD.md`

### 4.1 Mandatory Sections (all 14 required)

| # | Section | Key Content |
|---|---------|-------------|
| 1 | Executive Summary | 3-5 sentences; CTO-readable |
| 2 | Business Context | Drivers, use cases table, stakeholder matrix |
| 3 | System Context Diagram | C4 Level 1, Mermaid `graph TB` |
| 4 | Container Diagram | C4 Level 2, Mermaid `graph TB` + container table |
| 5 | Data Flow | Primary flow + async flow, Mermaid `sequenceDiagram` |
| 6 | Technology Stack | All layers, every choice justified |
| 7 | Integration Architecture | Protocol, auth, SLA, data format per integration |
| 8 | Non-Functional Requirements | All 8 categories, numeric targets |
| 9 | Security Architecture | Zero-trust model, auth/authz, encryption, network |
| 10 | Deployment Architecture | Infra diagram, environments, CI/CD pipeline |
| 11 | Cost Estimate | Per-service monthly (expected + peak), 3-year TCO |
| 12 | Key Architecture Decisions | ADR table with IDs and rationale |
| 13 | Risks & Mitigations | Probability × impact matrix |
| 14 | Roadmap | Phased milestones |

### 4.2 Narrative Mandate (per component)

Every component block in the HLD and LLD MUST include:

```markdown
**Design Rationale:**
[WHY this technology/pattern was chosen over its primary alternative.
This is not optional. A component without a rationale is a placeholder, not a design.]

**Implementation Strategy:**
[HOW the team will build this. Key engineering constraints and first principles.
Not "we will use microservices" — but "the [X] service will be deployed as a stateless
container, horizontally scaled, with its state externalised to [Redis / DB]."]
```

### 4.3 Mermaid Diagram Requirements

- All `graph` and `sequenceDiagram` blocks must be syntactically valid.
- C4 Context diagram: system box + all external actors and systems.
- C4 Container diagram: all deployable units inside the system boundary.
- Data flow: at least 1 happy-path sequence + 1 async/event-driven sequence.
- Infrastructure diagram: AZ layout, load balancer, DB primary/replica topology.

---

## 5. Phase 3: Arch Agent — Low-Level Design(s)

**Artifacts:** `Design_LLD_[ServiceName].md` × N (one per major service from HLD Container Diagram)

### 5.1 Service Identification

The pipeline MUST generate LLDs for the **top 3-5 services** identified in the HLD Container Diagram.
Selection criteria: services with the highest business criticality or most complex internal design.

### 5.2 Mandatory LLD Sections (all 12 required per LLD)

| # | Section | Key Content |
|---|---------|-------------|
| 1 | Scope & Objectives | In-scope/out-of-scope, success criteria table |
| 2 | Assumptions, Constraints & Dependencies | Dependency table with owner and risk |
| 3 | Detailed Component Design | Class/module diagram (Mermaid), SOLID analysis |
| 4 | API Specification | Every endpoint: method, path, request/response schema, error codes |
| 5 | Database Schema | Table definitions, indexes, partitioning, constraints, growth rate |
| 6 | Sequence Diagrams | Happy path + 2 error paths per critical flow |
| 7 | Error Handling & Resilience | Retry policy, circuit-breaker thresholds (numeric), DLQ |
| 8 | Performance Design | Caching layers, query optimization, connection pool sizing |
| 9 | Security Implementation | Auth flow sequence, input validation rules, secrets management |
| 10 | Testing Strategy | Unit/integration/contract/performance hooks + coverage targets |
| 11 | Observability | Log schema (JSON), metric names, trace spans, alert rules |
| 12 | Deployment Notes | Dockerfile hints, env vars, health endpoints, scaling policy |

### 5.3 LLD Numeric Threshold Rule

All thresholds in LLDs MUST be explicit numbers. Forbidden values: TBD, "as appropriate", "configured per environment" without a default.

Examples of compliant thresholds:
- Circuit breaker: opens when error rate > 50% over a 10-second window.
- Cache TTL: 300 seconds for read-heavy entities; 30 seconds for financial data.
- Connection pool: min=5, max=50, acquire-timeout=5s, idle-timeout=300s.
- Retry: max 3 attempts with exponential backoff (1s, 2s, 4s), jitter ±20%.

---

## 6. Phase 4: Review Agent — Guardrail Audit

**Artifact:** `review_report.md`

### 6.1 Audit Dimensions (all 12 checked)

| # | Dimension | Pass Criteria |
|---|-----------|---------------|
| 1 | Discovery Completeness | 15 dimensions present, all quantified |
| 2 | Requirements Quality | EARS notation, measurable ACs, 10:10:50 ratio met |
| 3 | NFR Coverage | 8 categories with numeric targets (no vague adjectives) |
| 4 | Security Guardrails | Zero-trust, STRIDE, OWASP Top 10, auth/authz explicit |
| 5 | Architecture Patterns | Correct pattern for problem, anti-patterns absent, Rationale + Strategy present |
| 6 | Data Architecture | Schema defined, indexes justified, PII handling explicit |
| 7 | Resilience Design | RPO/RTO per tier, circuit-breaker numeric, retry policy, DLQ |
| 8 | Observability | Structured log schema, RED metrics, trace spans, alert thresholds |
| 9 | API Design | REST conventions, versioning, RFC 7807 errors, pagination, rate-limiting |
| 10 | Cost & Sustainability | 3-year TCO estimated, GreenOps/SCI considered |
| 11 | ADR Coverage | Major decisions have ADR IDs, rationale is meaningful |
| 12 | Template Completeness | Zero placeholders, zero TODOs, all mandatory sections present |

### 6.2 Severity & Scoring

| Severity | Definition | Score Impact | Gate |
|----------|------------|:-----------:|------|
| CRITICAL | Blocks design approval | -20 per finding | Must resolve before Phase 1 implementation |
| HIGH | Must resolve before coding | -10 per finding | Must resolve before sprint start |
| MEDIUM | Resolve before go-live | -5 per finding | Must resolve before UAT |
| LOW | Best-practice recommendation | -1 per finding | Resolve in next iteration |

**Scoring:**
- Start at 100.
- Deduct per finding per severity above.
- Floor at 0.

| Score | Status | Delivery Decision |
|------:|--------|-------------------|
| ≥ 80 | PASS | Proceed to implementation |
| 60–79 | CONDITIONAL PASS | Resolve HIGH findings within [X days] before coding |
| < 60 | FAIL | Return to Phase 0/1/2 for rework |

---

## 7. Pipeline-Wide Enforcement Standards

### 7.1 The 10:10:15:50 Mandate

| Metric | Requirement |
|--------|-------------|
| Discovery Dimensions | ≥ 15 |
| Epics | 10 – 20 |
| User Stories | 50 – 150 |
| LLD Services | 3 – 5 |
| Review Audit Score | ≥ 80 to proceed |

### 7.2 Zero-Placeholder Rule

Using `[CONTINUES...]`, `(redacted)`, `TBD`, `TODO`, `FIXME`, `[placeholder]` in ANY artifact
is a **CRITICAL LINT ERROR** that blocks the pipeline at the review phase.

### 7.3 Narrative Mandate

Every design artifact (HLD section, LLD component) MUST include:
- `**Design Rationale:**` — WHY this approach, not WHAT it is.
- `**Implementation Strategy:**` — HOW it will be built, not just that it will be.

A design document without narrative is a template, not a design.

### 7.4 Measurable NFR Mandate

Every NFR acceptance criterion MUST contain a number with a unit.
Forbidden: "fast response", "high availability", "low cost".
Required: "p95 < 200 ms", "99.9% uptime", "< $0.001 per request".

---

## 8. CLI Commands

```bash
# Initialize a project
python archpilot.py init [--dir <path>]

# Run the full agentic pipeline (requires ANTHROPIC_API_KEY)
python archpilot.py run [--dir <path>] [--model <claude-model-id>]

# Re-run guardrail review on existing artifacts
python archpilot.py review [--dir <path>] [--model <claude-model-id>]

# Lint the .specs/ directory
python archpilot.py lint [--dir <path>] [--tier 1|2|3]
```

**Tier definitions for lint:**

| Tier | Use Case | Enforcement Level |
|------|----------|------------------|
| 1 | Starter / prototype | TODOs, placeholders, weak words |
| 2 | Standard / team project | + discovery dimensions, epic count |
| 3 | Enterprise / regulated | + full 10:10:50 ratio, Rationale + Strategy, numeric NFRs |

---

## 9. Artifact Dependency Graph

```
Input.md
    │
    ▼
discovery.md ────────────────────────────────────────────┐
    │                                                     │
    ▼                                                     │
requirements.md ─────────────────────────────────────────┤
    │                                                     │
    ▼                                                     │
Design_HLD.md ───────────────────────────────────────────┤
    │                                                     │
    ├─► Design_LLD_ServiceA.md                           │
    ├─► Design_LLD_ServiceB.md                           │
    └─► Design_LLD_ServiceN.md                           │
                                                         │
    ┌────────────────────────────────────────────────────┘
    ▼
review_report.md  (audits ALL of the above)
```

---

*Archpilot — Pipeline Governance Rule v4.0*
*Created by Gaurav Sharma | Enforced by archpilot.py + tools/pipeline.py*
