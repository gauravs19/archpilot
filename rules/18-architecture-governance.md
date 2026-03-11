# Architecture Governance

> **Purpose:** Standards for Architecture Review Boards (ARB), technology radar management,
> standards enforcement, and exception handling. Essential for GCCs, enterprises, and
> organizations with 50+ engineers needing consistent architecture decisions.

---

## How to Use This File

- **GCC/Enterprise:** Use to set up or improve your architecture governance process
- **ARB Setup:** Say to an LLM: *"Using this governance framework, design an ARB process for a [size] engineering organization"*
- **Tech Radar:** Use the template to maintain your organization's approved technology list

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [00 — Architecture Principles](./00-architecture-principles.md) | Principles that governance enforces |
| [02 — ADR Standards](./02-adr-standards.md) | ADRs are the primary governance artifact |
| [15 — Code Review](./15-code-review-guidelines.md) | Code-level governance |
| [21 — Tech Debt Mgmt](./21-tech-debt-management.md) | Governance tracks debt |

---

## 1. Architecture Review Board (ARB)

### 1.1 Purpose
The ARB exists to ensure architecture decisions are:
- **Consistent** — across teams, services, and projects
- **Informed** — based on data, not opinions or trends
- **Documented** — via ADRs for institutional memory
- **Aligned** — with business strategy and technology roadmap

### 1.2 ARB Composition

| Role | Responsibility | Voting? |
|------|--------------|:------:|
| **Chief Architect** (Chair) | Facilitates, resolves tie-breaks | ✅ |
| **Domain Architects** (2-3) | Evaluate within their domain expertise | ✅ |
| **Security Architect** | Evaluates security implications | ✅ |
| **Engineering Manager** | Evaluates team capacity and skill fit | ⚠️ Advisory |
| **Product Manager** | Provides business context and priority | ⚠️ Advisory |
| **Presenting Team** | Presents the proposal, answers questions | ❌ |

### 1.3 ARB Meeting Cadence

| Org Size | Frequency | Duration | Format |
|----------|:---------:|:--------:|--------|
| < 50 engineers | Monthly | 60 min | Informal reviews as needed |
| 50-200 engineers | Bi-weekly | 90 min | Formal ARB with agenda |
| 200+ engineers | Weekly | 60 min | Formal ARB with submission process |

### 1.4 What Requires ARB Review

| Decision | ARB Required? |
|----------|:------------:|
| New technology introduction (language, framework, database) | ✅ Always |
| New service/microservice creation | ✅ Always |
| Architecture pattern change (monolith → microservices) | ✅ Always |
| Cloud provider or region change | ✅ Always |
| Cross-team API contract changes | ✅ Always |
| Major refactoring affecting 3+ services | ✅ Always |
| New third-party SaaS adoption | ⚠️ If cost > $5K/year |
| Library/framework version upgrade | ❌ Team decision |
| Internal refactoring within one service | ❌ Team decision |
| Bug fixes and feature implementation | ❌ Team decision |

### 1.5 ARB Submission Template

```markdown
## ARB Request: [Title]

**Submitted by:** [Team/Person]
**Date:** [YYYY-MM-DD]
**Category:** [New Technology | New Service | Pattern Change | Integration]

### Problem Statement
What problem are we solving? Why now?

### Proposed Solution
High-level approach (attach HLD or ADR)

### Alternatives Considered
At least 2 alternatives with trade-off analysis

### Impact Assessment
- Services affected: [list]
- Teams affected: [list]
- Data impact: [new data stores, migrations]
- Security impact: [auth, encryption, compliance]
- Cost impact: [monthly/annual estimate]

### Request
[ ] Approval to proceed
[ ] Feedback before proceeding
[ ] Exception to existing standard (specify which)
```

### 1.6 ARB Outcomes

| Outcome | Meaning | Next Step |
|---------|---------|-----------|
| **Approved** | Proceed as proposed | Create ADR, begin implementation |
| **Approved with Conditions** | Proceed after addressing feedback | Address conditions, re-confirm with chair |
| **Deferred** | Needs more information or analysis | Resubmit with additional data |
| **Rejected** | Does not align with standards or strategy | Document rationale, suggest alternative |

---

## 2. Technology Radar

### 2.1 Ring Definitions

| Ring | Meaning | Action |
|------|---------|--------|
| **Adopt** | Proven in production, recommended for new projects | Use by default, no ARB needed |
| **Trial** | Promising, being evaluated in 1-2 projects | Can use with ARB awareness |
| **Assess** | Interesting, worth exploring via PoC | PoC only, not for production |
| **Hold** | Do not use for new projects, plan exit if current | Migration plan required |

### 2.2 Technology Radar Template

| Category | Technology | Ring | Notes |
|----------|-----------|:----:|-------|
| **Languages** | Python 3.12 | Adopt | Primary backend language |
| | TypeScript 5 | Adopt | Frontend and Node.js services |
| | Go 1.22 | Trial | Performance-critical services |
| | Rust | Assess | Exploring for core infra |
| **Frameworks** | FastAPI | Adopt | Python APIs |
| | Next.js 14 | Adopt | React SSR/SSG |
| | Spring Boot 3 | Hold | Legacy Java services only |
| **Databases** | PostgreSQL 16 | Adopt | Default OLTP |
| | Redis 7 | Adopt | Caching, sessions |
| | MongoDB 7 | Trial | Document-heavy use cases |
| | Oracle | Hold | Migrate away, cost reduction |
| **Cloud** | AWS | Adopt | Primary cloud |
| | Azure | Trial | Specific GCC requirements |
| | GCP | Assess | ML/BigQuery exploration |
| **Messaging** | SQS/SNS | Adopt | Default async |
| | Kafka | Trial | High-throughput streaming |
| **Observability** | Datadog | Adopt | APM + logs + metrics |
| | Prometheus + Grafana | Trial | Cost-conscious alternative |
| **IaC** | Terraform | Adopt | Multi-cloud provisioning |

### 2.3 Radar Review Cadence
- **Full review:** Quarterly (all categories)
- **Emergency change:** Any time via ARB (e.g., security vulnerability in a tool)
- **New entries:** Can be proposed by any engineer, reviewed by ARB

---

## 3. Standards Enforcement

### 3.1 Enforcement Mechanisms

| Level | Mechanism | Enforcement |
|-------|-----------|-------------|
| **Automated** | CI/CD checks (linting, security scan, schema validation) | Block merge |
| **Code Review** | Reviewer enforces code-level standards | Block merge |
| **Design Review** | Architect reviews HLD/LLD against standards | Block implementation |
| **ARB Review** | Board reviews architecture decisions | Block deployment |
| **Audit** | Quarterly compliance audit against standards | Findings tracked in backlog |

### 3.2 Exception Process

When a team needs to deviate from a standard:

1. **Submit Exception Request** to ARB with:
   - Which standard is being violated and why
   - Business justification (why the standard doesn't fit)
   - Risk assessment (what could go wrong)
   - Exit plan (how to return to compliance, with timeline)
2. **ARB evaluates** and either approves (with conditions) or rejects
3. **Approved exceptions** are time-boxed (max 12 months) and tracked
4. **Review:** All exceptions reviewed every quarter

### 3.3 Compliance Scorecard

Track per-team compliance (monthly):

| Team | ADRs | Code Review | Security Scan | Test Coverage | API Standards | Score |
|------|:----:|:-----------:|:------------:|:-------------:|:------------:|:-----:|
| Orders | ✅ | ✅ | ✅ | 85% ✅ | ✅ | 5/5 |
| Payments | ✅ | ✅ | ✅ | 72% ⚠️ | ✅ | 4/5 |
| Legacy | ❌ | ⚠️ | ❌ | 45% ❌ | N/A | 1/5 |

---

## 4. Architecture Governance Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Ivory tower architecture** | Architects design without building | Architects MUST code or pair-program regularly |
| **ARB as bottleneck** | Teams wait weeks for approval | SLA: ARB response within 5 business days |
| **Standards without automation** | Rules exist but nobody follows them | Automate enforcement in CI/CD |
| **No exception process** | Teams either break rules or are blocked | Formal exception process with time-boxing |
| **Governance without value** | Process for process' sake | Every governance activity must help teams ship better |
| **Outdated tech radar** | "Approved" list from 3 years ago | Quarterly radar reviews are mandatory |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
