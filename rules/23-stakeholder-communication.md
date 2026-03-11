# Stakeholder Communication Guide

> **Purpose:** Standards for how architects communicate with different stakeholders —
> CTOs, product managers, developers, clients, and business executives. Covers
> presentation techniques, decision framing, and language adaptation per audience.

---

## How to Use This File

- **Before a meeting:** Say to an LLM: *"Using this communication guide, help me prepare a [architecture review / proposal / status update] for [audience]"*
- **Writing docs:** Use the audience adaptation rules to tailor your language

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [01 — Solution Design](./01-solution-design.md) | SDD is a stakeholder communication artifact |
| [18 — Architecture Governance](./18-architecture-governance.md) | ARB presentation standards |
| [16 — Estimation Framework](./16-estimation-framework.md) | Communicating estimates to stakeholders |

---

## 1. Know Your Audience

### 1.1 Stakeholder Map

| Stakeholder | They Care About | They DON'T Care About | Speak In |
|------------|----------------|----------------------|----------|
| **CTO / VP Engineering** | Tech strategy, risk, timeline, team impact | Implementation details, code | Business outcomes + tech trade-offs |
| **Product Manager** | Features, timeline, user impact, cost | Database schemas, infrastructure | User stories, timelines, dependencies |
| **Developers** | How to build it, patterns, APIs, trade-offs | Business strategy, budget | Technical depth, code examples |
| **Business Executive (CEO/CFO)** | Revenue impact, cost, timeline, risk | Technology choices | Money, time, competitive advantage |
| **Client (External)** | Solution fits their needs, cost, timeline, trust | Your internal processes | Confidence, capability, references |
| **Security/Compliance** | Risks, gaps, audit readiness | Feature velocity | Threats, controls, compliance status |
| **Operations/SRE** | Operability, monitoring, runbooks, on-call impact | Feature details | SLOs, alert rules, deployment impact |

### 1.2 The 3-Layer Communication Model

Every architecture communication should work at 3 levels:

```
Layer 1: EXECUTIVE SUMMARY (30 seconds)
├── What are we doing?
├── Why does it matter?
└── What do we need?

Layer 2: KEY DETAILS (5 minutes)
├── Approach / options considered
├── Trade-offs and recommendation
├── Timeline and cost
└── Risks

Layer 3: DEEP DIVE (30 minutes, if asked)
├── Architecture diagrams
├── Technical analysis
├── Data model
└── NFR details
```

**Rule:** Always start at Layer 1. Only go deeper if the audience asks.

---

## 2. Communication Frameworks

### 2.1 Architecture Decision Presentation (STAR-T)

| Step | What | Example |
|------|------|---------|
| **S**ituation | Current state, context | "Our monolith serves 50K users but deploys take 4 hours" |
| **T**rade-offs | Options with pros/cons | "Option A: Extract services (16 weeks). Option B: Optimize monolith (4 weeks)" |
| **A**nalysis | Data-driven recommendation | "At current growth, monolith hits scaling limits in 6 months" |
| **R**ecommendation | Clear recommendation with rationale | "Recommend Option A — invest 16 weeks now, avoid 3-month rewrite later" |
| **T**imeline | Phased delivery plan | "Phase 1 (4 weeks): User service. Phase 2 (6 weeks): Catalog" |

### 2.2 Risk Communication (Traffic Light)

| Color | Meaning | Audience Action |
|:-----:|---------|----------------|
| 🟢 Green | On track, no concerns | Acknowledge |
| 🟡 Yellow | Potential issue, mitigation in progress | Be aware, may need decision |
| 🔴 Red | Blocked or high-risk, needs intervention | Decision required NOW |

**Rule:** Never surprise stakeholders with a 🔴. If it was 🟢 last week and 🔴 this week, you missed the 🟡 signal.

### 2.3 Technical to Business Translation

| Technical Concept | Business Translation |
|------------------|---------------------|
| "We need to add caching" | "We can make the app 5x faster for $50/month" |
| "We should split the monolith" | "Each team can ship features independently, releasing weekly instead of monthly" |
| "We have technical debt" | "Past shortcuts are slowing us down — every new feature takes 30% longer" |
| "We need database migration" | "We can cut licensing costs from $200K to $20K/year" |
| "Microservices architecture" | "Each part of the system can scale, update, and recover independently" |
| "99.99% availability" | "Less than 1 hour of downtime per year" |
| "Distributed tracing" | "When a customer reports an issue, we can pinpoint the exact failure in seconds" |

---

## 3. Meeting Types & Preparation

### 3.1 Architecture Review (ARB)

| Aspect | Standard |
|--------|---------|
| Duration | 60 min |
| Preparation | ARB submission template completed, distributed 2 days before |
| Visual aids | Architecture diagram (C4), trade-off matrix, risk table |
| Outcome | Decision: Approved / Conditions / Deferred / Rejected |

### 3.2 Design Review (with Dev Team)

| Aspect | Standard |
|--------|---------|
| Duration | 45 min |
| Preparation | LLD draft shared 1 day before |
| Focus | API design, data model, error handling, performance, security |
| Outcome | Feedback incorporated, LLD updated |

### 3.3 Status Update (Steering Committee)

| Aspect | Standard |
|--------|---------|
| Duration | 30 min |
| Format | Traffic light report: scope, timeline, budget, risks |
| Focus | Decisions needed, blockers, achievements |
| Outcome | Decisions made, blockers unblocked |

### 3.4 Technical Proposal (Client)

| Aspect | Standard |
|--------|---------|
| Duration | 60 min |
| Format | Presentation: problem → approach → team → timeline → cost |
| Focus | Confidence, capability, understanding of their problem |
| Outcome | Client shortlists or requests follow-up |

---

## 4. Written Communication Standards

### 4.1 Email/Slack Rules

| Audience | Format | Length |
|----------|--------|:------:|
| CTO / Executive | Bullet points, bottom-line first | < 5 lines |
| PM | Summary + impact + timeline | < 10 lines |
| Dev Team | Detail allowed, code snippets OK | As needed |
| Client (external) | Professional, structured, proofread | < 1 page |

### 4.2 Document Structure

Every architecture document follows the **Pyramid Principle:**

```
Conclusion first
├── Supporting argument 1
│   └── Evidence / data
├── Supporting argument 2
│   └── Evidence / data
└── Supporting argument 3
    └── Evidence / data
```

**Rule:** Lead with the recommendation. Never bury the conclusion at the end.

---

## 5. Influence Without Authority

Architects often don't have direct authority over teams. Influence through:

| Technique | How | Example |
|-----------|-----|---------|
| **Data > Opinions** | Show metrics, benchmarks, costs | "P95 latency is 3s; standard is < 500ms" |
| **Options, not mandates** | Present 2-3 options with trade-offs | "Option A costs less, Option B scales better" |
| **Show, don't tell** | PoC, prototype, working code | Build a 2-day spike to prove the approach |
| **Align with goals** | Connect your recommendation to team/business goals | "This helps us hit the Q3 launch date" |
| **Build relationships** | 1:1 coffee chats with tech leads | Understand their constraints before proposing |
| **Document decisions** | ADRs create institutional credibility | "As we decided in ADR-015..." |

---

## 6. Communication Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **"Let me explain the architecture"** (unprompted 60-min lecture) | Audience glazes over, loses trust | Ask what they need, start at Layer 1 |
| **Jargon with business audience** | "We need CQRS with event sourcing" — they hear nothing | Translate to business impact |
| **No recommendation** | "Here are 5 options" without a clear recommendation | Always recommend. Say "I recommend X because..." |
| **Surprise escalation** | "We're 6 weeks behind" (first time hearing it) | Incremental updates, never hide bad news |
| **Architecture astronaut** | Over-engineering for future that may never come | Design for today, plan for tomorrow |
| **Email novels** | 2-page Slack messages nobody reads | Bottom-line first, details in attachment |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
