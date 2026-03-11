# Estimation Framework

> **Purpose:** Standards for software effort estimation — covering T-shirt sizing,
> story points, Function Point Analysis, bottom-up estimation, and proposal costing.
> Ensures consistent, defensible estimates across presales, planning, and delivery.

---

## How to Use This File

- **Presales:** Say to an LLM: *"Using this estimation framework, estimate the effort for: [project description]"*
- **Sprint Planning:** Use story point guidelines for consistent sizing across teams
- **Proposals:** Reference the bottom-up estimation model for SOW/RFP responses

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [01 — Solution Design](./01-solution-design.md) | Cost estimate section (§3.8) of SDD |
| [14 — Cost Optimization](./14-cost-optimization.md) | Infrastructure cost estimation |
| [04 — LLD Standards](./04-lld-standards.md) | Component-level sizing input |
| [Presales Persona](../llm-configs/personas/presales-solutioner.md) | Uses this for proposal estimation |

---

## 1. Estimation Methods — When to Use What

| Method | Accuracy | When to Use | Audience |
|--------|:--------:|------------|----------|
| **T-Shirt Sizing** | ±50% | Early presales, roadmap planning, portfolio prioritization | PM, Business |
| **Story Points (Relative)** | ±30% | Sprint planning, feature comparison | Dev team |
| **Bottom-Up (Task Decomposition)** | ±15% | SOW/proposal, fixed-price projects | Delivery lead, Client |
| **Function Point Analysis (FPA)** | ±20% | Large programs, benchmarking, vendor comparison | Enterprise PMO |
| **Analogous (Historical)** | ±25% | Repeat projects, similar domain | Architect, PM |
| **Three-Point (PERT)** | ±15% | Risk-aware planning, critical path | PM, Architect |

**Rule:** NEVER give a single-point estimate. Always provide a **range** (optimistic → realistic → pessimistic).

---

## 2. T-Shirt Sizing

### 2.1 Size Definitions

| Size | Effort Range | Complexity | Team | Duration |
|:----:|:----------:|-----------|:----:|:--------:|
| **XS** | 1-3 person-days | Config change, minor feature | 1 dev | < 1 week |
| **S** | 4-10 person-days | Single component, well-defined | 1-2 devs | 1-2 weeks |
| **M** | 11-30 person-days | Multi-component, some unknowns | 2-3 devs | 2-6 weeks |
| **L** | 31-90 person-days | Cross-service, integration work | 3-5 devs | 6-12 weeks |
| **XL** | 91-200 person-days | New system, platform-level change | 5-8 devs | 3-6 months |
| **XXL** | 200+ person-days | Multi-system program | 8+ devs | 6+ months (decompose!) |

**Rule:** If an estimate lands on XXL, decompose it into smaller items before proceeding.

### 2.2 Quick Sizing Guide

```
Feature Description → Ask:
├── How many services/components touched?
│   ├── 1 → S or M
│   ├── 2-3 → M or L
│   └── 4+ → L or XL
├── New database tables/schemas?
│   └── YES → Add one size up
├── External integration (3rd party API)?
│   └── YES → Add one size up
├── Security/compliance implications?
│   └── YES → Add one size up
└── Is the requirement well-defined?
    └── NO → Add one size up (uncertainty buffer)
```

---

## 3. Story Points (Fibonacci Scale)

### 3.1 Reference Scale

| Points | Reference Example | Complexity | Risk |
|:------:|------------------|-----------|:----:|
| **1** | Update a UI label, fix a typo | Trivial, no unknowns | None |
| **2** | Add a field to an existing API + DB | Simple, well-known pattern | Low |
| **3** | New CRUD endpoint with validation | Moderate, one component | Low |
| **5** | Feature with business logic + 2 components | Moderate, some decisions | Medium |
| **8** | Cross-service feature with new event flow | Complex, integration work | Medium |
| **13** | New service with DB, API, events, tests | High complexity, multiple unknowns | High |
| **21** | System redesign, data migration involved | Very high, needs decomposition | High |

**Rules:**
- If it's > 13, DECOMPOSE into smaller stories before estimating.
- Points measure COMPLEXITY + UNCERTAINTY, not time.
- Calibrate with the team — "What is our 3-pointer?" as the anchor.
- Re-estimate after spike/PoC if uncertainty was the driver.

### 3.2 Velocity-Based Planning

```
Team Velocity (avg last 3 sprints): V points/sprint
Total Backlog: T points
Estimated Sprints: T / V (add 20% buffer)
```

---

## 4. Bottom-Up Estimation (Task Decomposition)

### 4.1 Work Breakdown Structure (WBS)

| Phase | Activities | % of Total |
|-------|-----------|:----------:|
| **Requirements & Design** | Requirements analysis, HLD, LLD, ADR, design review | 15-20% |
| **Development** | Implementation, unit tests, code review | 35-40% |
| **Integration & Testing** | Integration testing, API testing, E2E testing | 15-20% |
| **DevOps & Infrastructure** | CI/CD, IaC, environments, monitoring | 10-15% |
| **UAT & Bug Fixing** | User acceptance testing, defect resolution | 10-15% |
| **Documentation & KT** | Technical docs, user guides, knowledge transfer | 5% |
| **Project Management** | Scrum ceremonies, status reporting, stakeholder mgmt | 8-10% |

### 4.2 Bottom-Up Template

| # | Component | Tasks | Effort (Days) | Assumptions |
|---|-----------|-------|:-------------:|-------------|
| 1 | User Service | API: 5 endpoints, DB: 3 tables, Auth integration | 18 | OAuth2 via Cognito |
| 2 | Order Service | API: 8 endpoints, DB: 5 tables, Payment integration | 28 | Razorpay webhooks |
| 3 | Notification Service | SQS consumer, Email/SMS/Push templates | 12 | SES + SNS setup |
| | **Dev Subtotal** | | **58** | |
| | + Design (20%) | | 12 | |
| | + Testing (20%) | | 12 | |
| | + DevOps (10%) | | 6 | |
| | + UAT + Bugfix (15%) | | 9 | |
| | + PM + Buffer (10%) | | 6 | |
| | **TOTAL** | | **103 person-days** | |

### 4.3 Complexity Multipliers

| Factor | Multiplier | When |
|--------|:---------:|------|
| New technology (team learning) | 1.3x | First time using a framework/service |
| Legacy integration | 1.4x | Integrating with undocumented/old system |
| Compliance requirements (PCI, HIPAA) | 1.2x | Regulatory audit preparation |
| Multi-tenancy | 1.3x | Tenant isolation, data partitioning |
| High availability (99.99%+) | 1.3x | Multi-region, complex failover |
| Distributed team (multi-timezone) | 1.15x | Communication overhead |
| Unclear requirements | 1.3x | Requirements still evolving |
| Performance-critical (sub-100ms) | 1.25x | Optimization and load testing overhead |

---

## 5. Function Point Analysis (FPA)

### 5.1 Counting Rules

| Component Type | Description | Low | Average | High |
|---------------|-----------|:---:|:-------:|:----:|
| **External Input (EI)** | Data entry, file upload, API POST | 3 FP | 4 FP | 6 FP |
| **External Output (EO)** | Reports, exports, API responses | 4 FP | 5 FP | 7 FP |
| **External Inquiry (EQ)** | Search, lookup, GET endpoints | 3 FP | 4 FP | 6 FP |
| **Internal Logical File (ILF)** | Database tables/entities maintained | 7 FP | 10 FP | 15 FP |
| **External Interface File (EIF)** | External system data referenced | 5 FP | 7 FP | 10 FP |

### 5.2 FP to Effort Conversion

| Language/Stack | Hours per FP | Notes |
|---------------|:----------:|-------|
| Python / Node.js | 6-8 hrs | Modern frameworks |
| Java / .NET | 8-12 hrs | Enterprise stacks |
| Low-Code / No-Code | 2-4 hrs | Platform-dependent |
| Legacy (COBOL, mainframe) | 15-20 hrs | Complex environments |

### 5.3 Quick FP Estimation

```
Total FP = Σ(EI + EO + EQ + ILF + EIF)
Adjusted FP = Total FP × (0.65 + 0.01 × Σ(14 adjustment factors))
Effort (hours) = Adjusted FP × Hours-per-FP
Effort (person-months) = Effort / 160
```

---

## 6. Three-Point Estimation (PERT)

For risk-aware estimating:

```
Expected = (Optimistic + 4 × Most Likely + Pessimistic) / 6
Standard Deviation = (Pessimistic - Optimistic) / 6
```

| Task | Optimistic | Most Likely | Pessimistic | Expected | StdDev |
|------|:---------:|:----------:|:----------:|:--------:|:------:|
| User Auth module | 8 days | 12 days | 20 days | 12.7 days | 2 days |
| Payment Integration | 10 days | 15 days | 30 days | 16.7 days | 3.3 days |
| Data Migration | 5 days | 10 days | 25 days | 11.7 days | 3.3 days |

**Rule:** For fixed-price proposals, use the **P75 estimate** (Expected + 1 StdDev) as the commitment.

---

## 7. Estimation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Single-point estimate** | Creates false precision | Always give a range (best/likely/worst) |
| **Anchor bias** | "The client said 3 months" → estimate backwards | Estimate independently, THEN compare |
| **Developer-only estimation** | Misses testing, DevOps, PM overhead | Include ALL roles in estimation |
| **No buffer for unknowns** | 100% utilization assumed | Add 15-25% contingency buffer |
| **Estimating before design** | Missing architecture complexity | At minimum, do T-shirt sizing at design level |
| **Copy-paste from last project** | Different context, different team | Use analogous estimation with adjustment factors |
| **Forgetting non-functional work** | No time for security, perf, observability | NFRs add 15-30% to functional estimates |
| **Ignoring environment setup** | CI/CD, IaC, monitoring setup = real work | Budget 10-15% for DevOps/infra |

---

## 8. Estimation Checklist

Before submitting an estimate, verify:

- [ ] Estimation method is appropriate for the stage (T-shirt for presales, WBS for SOW)
- [ ] Range provided, not a single number
- [ ] All phases included (design, dev, test, DevOps, UAT, PM, KT)
- [ ] Complexity multipliers applied (legacy, compliance, new tech)
- [ ] Contingency buffer included (15-25%)
- [ ] Assumptions documented explicitly
- [ ] Dependencies on other teams/vendors identified
- [ ] Non-functional requirements effort included
- [ ] Team ramp-up time factored in (if new team)
- [ ] Signed off by a senior architect or tech lead

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
