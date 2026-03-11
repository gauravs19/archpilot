# Technical Debt Management

> **Purpose:** Framework for identifying, scoring, prioritizing, and paying down
> technical debt. Ensures architecture teams track debt systematically instead of
> letting it accumulate until forced rewrites.

---

## How to Use This File

- **Debt Assessment:** Say to an LLM: *"Using this tech debt framework, analyze the technical debt in: [system description or codebase]"*
- **Sprint Planning:** Use the prioritization matrix to decide which debt to pay down each sprint
- **Stakeholder Communication:** Use the business impact scoring to justify debt paydown

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [18 — Architecture Governance](./18-architecture-governance.md) | ARB tracks systemic debt |
| [15 — Code Review](./15-code-review-guidelines.md) | Code reviews flag new debt |
| [17 — Migration & Modernization](./17-migration-modernization.md) | Large-scale debt remediation |
| [14 — Cost Optimization](./14-cost-optimization.md) | Debt has cost implications |

---

## 1. What is Technical Debt?

### 1.1 Types of Technical Debt

| Type | Description | Example | Common Source |
|------|-----------|---------|--------------|
| **Deliberate / Strategic** | Conscious shortcut for speed | "Ship without caching, add later" | PM pressure, MVP |
| **Accidental / Unintentional** | Didn't know better at the time | N+1 queries, VARCHAR(255) everywhere | Inexperience |
| **Bit Rot** | System degraded over time | Outdated dependencies, unmaintained code | Neglect |
| **Environmental** | External changes made system suboptimal | Library deprecated, cloud service sunset | Technology evolution |
| **Architecture Debt** | System-level structural issues | Shared database, monolith that should be split | Growth without redesign |

### 1.2 Debt vs Defect

| | Technical Debt | Defect (Bug) |
|-|:-----------:|:----------:|
| System works? | ✅ Yes (for now) | ❌ No |
| User-visible? | Usually no | Usually yes |
| Urgency | Can be deferred | Must fix |
| Impact | Slows future work | Breaks current work |

---

## 2. Technical Debt Registry

### 2.1 Registry Template

| ID | Title | Type | Service | Severity | Business Impact | Effort | Paydown Priority |
|:--:|-------|:----:|---------|:--------:|:---------------:|:------:|:----------------:|
| TD-001 | Shared database between Order and Payment services | Architecture | Order, Payment | High | Deployment coupling, can't scale independently | L (30 days) | 🔴 P1 |
| TD-002 | No database indexes on frequently queried columns | Accidental | Catalog | Medium | Slow search, p95 > 2s | S (3 days) | 🔴 P1 |
| TD-003 | jQuery in admin dashboard | Bit Rot | Admin UI | Low | Hard to hire, hard to maintain | M (15 days) | 🟡 P3 |
| TD-004 | Python 3.9 (EOL Dec 2025) | Environmental | All | High | Security risk, no patches | M (10 days) | 🟠 P2 |
| TD-005 | Hardcoded configuration values | Accidental | Notification | Medium | Can't change without deploy | S (2 days) | 🟠 P2 |

### 2.2 Registry Rules

- Every tech debt item MUST be documented in the registry (not just "we know about it")
- New debt discovered during code review → add to registry immediately
- Sprint planning reviews top 5 debt items every sprint
- Registry is visible to the entire team (not a hidden architect spreadsheet)

---

## 3. Debt Scoring Framework

### 3.1 Severity Score (1-5)

| Score | Severity | Definition |
|:-----:|:--------:|-----------|
| 5 | **Critical** | Blocking production reliability or security |
| 4 | **High** | Significantly slowing development velocity |
| 3 | **Medium** | Causes recurring issues or workarounds |
| 2 | **Low** | Minor inconvenience, code smell |
| 1 | **Minimal** | Cosmetic, nice-to-fix |

### 3.2 Impact Score (1-5)

| Score | Impact | Definition |
|:-----:|:------:|-----------|
| 5 | **Critical** | Affects all users, risks outage, compliance violation |
| 4 | **High** | Affects major features, slows team significantly |
| 3 | **Medium** | Affects specific features, moderate friction |
| 2 | **Low** | Affects edge cases, minor friction |
| 1 | **Minimal** | No user impact, developer inconvenience only |

### 3.3 Effort Score (1-5)

| Score | Effort | Duration |
|:-----:|:------:|----------|
| 1 | **XS** | < 1 day (quick fix during sprint) |
| 2 | **S** | 1-3 days |
| 3 | **M** | 1-2 weeks |
| 4 | **L** | 2-6 weeks |
| 5 | **XL** | > 6 weeks (needs dedicated initiative) |

### 3.4 Priority Calculation

```
Priority Score = (Severity × 2) + (Impact × 2) - Effort
```

| Priority Score | Priority | Action |
|:--------------:|:--------:|--------|
| 15-20 | 🔴 **P1 — Immediate** | Fix this sprint or next sprint |
| 10-14 | 🟠 **P2 — Soon** | Plan for next quarter |
| 5-9 | 🟡 **P3 — Backlog** | Track, fix opportunistically |
| < 5 | 🟢 **P4 — Accept** | Documented, accepted, revisit in 6 months |

---

## 4. Debt Paydown Strategies

### 4.1 Budget Allocation

| Strategy | Approach | Best For |
|----------|---------|----------|
| **20% Rule** | 20% of sprint capacity reserved for debt paydown | Product companies, ongoing dev |
| **Debt Sprint** | Dedicated sprint every 4-6 sprints for debt only | Teams with heavy debt backlog |
| **Boy Scout Rule** | Leave code better than you found it (fix small debt in every PR) | Accidental and bit rot debt |
| **Dedicated Initiative** | Multi-sprint project to address architecture debt | Architecture-level debt (shared DB split) |
| **New Feature Tax** | New features MUST address related debt before shipping | Preventing new debt accumulation |

### 4.2 When to Pay Down Debt

```
Should we fix this debt NOW?
├── Is it causing production incidents? → YES → Fix immediately (P1)
├── Is it blocking a planned feature? → YES → Fix before the feature
├── Is it a security vulnerability? → YES → Fix this sprint
├── Will it get worse if we wait? → YES → Plan for next sprint
├── Is it isolated and low-risk? → YES → Boy Scout Rule (fix opportunistically)
└── Is it cosmetic/preference? → YES → Document and accept (P4)
```

---

## 5. Preventing New Debt

### 5.1 Guardrails

| Prevention | How |
|-----------|-----|
| **Definition of Done includes quality** | Unit tests, no known debt added, docs updated |
| **Architecture review for new services** | ARB approval prevents architecture debt |
| **Automated quality checks** | CI/CD: coverage, linting, security scan |
| **Debt-aware estimation** | Estimates include time to do it right, not just "make it work" |
| **Tech radar** | Prevents adopting technologies that create future debt |
| **Code review standards** | Reviewers flag debt creation (architecture smells) |

### 5.2 Acceptable Debt Documentation

When debt is created deliberately:

```markdown
## Deliberate Debt: [Title]
**Created:** [Date]
**Author:** [Name]
**Reason:** [Why we're taking this shortcut]
**Impact:** [What will be harder later]
**Payback Plan:** [When and how we'll fix it]
**Deadline:** [Must be resolved by this date]
**Tracking:** [TD-XXX in debt registry]
```

---

## 6. Debt Metrics & Reporting

### 6.1 Key Metrics

| Metric | Target | Alert |
|--------|--------|-------|
| Total open debt items | Trending down | Increasing for 3+ months |
| P1/P2 debt items | < 5 at any time | > 10 items |
| Average age of P1 debt | < 2 sprints | > 4 sprints |
| Debt created vs resolved per sprint | Resolved ≥ Created | Created > 2x Resolved |
| % of sprint capacity on debt | ~20% | < 5% for 3+ sprints |

### 6.2 Reporting to Stakeholders

| Audience | What They Care About | Format |
|----------|--------------------|---------| 
| **Developers** | What to fix, effort estimates | Debt registry in backlog |
| **Engineering Manager** | Team velocity impact, sprint allocation | Monthly debt report |
| **CTO/VP** | Business risk, cost of delay, trend lines | Quarterly executive summary |
| **Product Manager** | Feature velocity impact, timeline risk | Sprint planning debt discussion |

---

## 7. Tech Debt Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **"We'll fix it later"** | Later never comes | Document with deadline, add to registry |
| **Invisible debt** | Not tracked, not prioritized | Registry is mandatory for all known debt |
| **All or nothing** | "We need 3 months to fix tech debt" | Incremental — 20% per sprint |
| **Gold plating** | "Let's rewrite everything properly" | Fix highest-priority debt first |
| **Blaming the previous team** | Debt is the system's problem, not a person's | Focus on impact and fix, not blame |
| **Zero debt tolerance** | Over-engineering, shipping too slowly | Strategic debt is OK — with a payback plan |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
