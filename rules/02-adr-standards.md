# ADR Standards — Architecture Decision Records

> **Purpose:** This rule file defines when, how, and in what format Architecture Decision
> Records should be created. When used as LLM context, it ensures every generated ADR
> follows enterprise best practices with proper trade-off analysis.

---

## How to Use This File

- Feed this to any LLM alongside `templates/adr-template.md`
- Say: *"Using these ADR standards, create an ADR for: [your decision]"*
- The LLM will produce a structured, complete ADR following these rules.

---

## 1. What is an ADR?

An Architecture Decision Record (ADR) is a **short document** that captures a single
architecture decision, its context, the options considered, and the consequences.

ADRs are:
- **Immutable records** — once accepted, they are not edited (they are superseded by new ADRs)
- **Version controlled** — stored in the repository alongside the code they govern
- **Sequentially numbered** — ADR-001, ADR-002, etc.

---

## 2. When to Write an ADR

### MUST Write an ADR
- Choosing a database technology (PostgreSQL vs DynamoDB vs MongoDB)
- Choosing a messaging system (Kafka vs RabbitMQ vs SQS)
- Choosing an architectural pattern (monolith vs microservices vs modular monolith)
- Choosing an authentication strategy (JWT vs session vs OAuth2 flow)
- Choosing a cloud provider or region
- Choosing a deployment strategy (K8s vs serverless vs VMs)
- Introducing a new framework or library that affects multiple teams
- Changing a data model that impacts multiple services
- Any decision that is costly to reverse

### SHOULD Write an ADR
- Choosing between two approaches within a single service (if non-trivial)
- Adopting a specific design pattern for a domain problem
- Selecting a third-party service or SaaS tool
- Deciding on a caching strategy

### Do NOT Write an ADR
- Variable naming conventions (code style guide is better)
- Minor library version choices
- Bug fixes or feature implementation details
- Decisions that are trivially reversible

---

## 3. ADR Lifecycle

```
Proposed → Accepted → [Active]
                        │
                  ┌─────┴─────┐
                  ▼           ▼
             Deprecated   Superseded
                          (by ADR-XXX)
```

| Status | Meaning |
|--------|---------|
| **Proposed** | Under review, not yet approved |
| **Accepted** | Approved by architecture review, currently active |
| **Deprecated** | No longer relevant (technology retired, feature removed) |
| **Superseded** | Replaced by a newer ADR (must link to the new one) |

**Rules:**
- Never delete an ADR. Mark it as deprecated or superseded.
- When an ADR is superseded, update the old ADR's status AND link to the new one.
- The new ADR SHOULD reference the old ADR it supersedes.

---

## 4. ADR Structure (Mandatory Sections)

### 4.1 Title
- Format: `ADR-{number}: {concise decision statement}`
- The title MUST be a statement, not a question.
- Good: `ADR-003: Use PostgreSQL for User Profile Storage`
- Bad: `ADR-003: Database Selection` (too vague)
- Bad: `ADR-003: Should We Use PostgreSQL?` (question, not decision)

### 4.2 Status
One of: `Proposed | Accepted | Deprecated | Superseded by ADR-XXX`

### 4.3 Date
ISO 8601 format: `YYYY-MM-DD`

### 4.4 Context
**What this section MUST include:**
- The business or technical problem driving this decision
- Current state — what exists today
- Constraints — budget, timeline, team skills, compliance
- Forces — what tensions exist (speed vs quality, cost vs capability, etc.)

**Rules:**
- Write as objective facts, not opinions.
- Include quantitative data where possible (traffic volume, team size, budget).
- Reference the business requirement or user story that created this need.

### 4.5 Decision
**What we chose and WHY.**
- State the decision clearly in 1-2 sentences.
- Then explain the reasoning — connect it back to the context and constraints.
- Reference the evaluation criteria that led to this choice.

### 4.6 Alternatives Considered
MUST include at least 2 alternatives (including the chosen option).

For each alternative, document:

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Criteria 1 (weighted) | Score | Score | Score |
| Criteria 2 (weighted) | Score | Score | Score |
| **Total** | | | |

**Evaluation criteria SHOULD include:**
- Technical fit (does it solve the problem?)
- Team expertise (do we know this technology?)
- Total cost of ownership (licensing, ops, training)
- Scalability (does it handle our growth plan?)
- Community & ecosystem (support, documentation, longevity)
- Operational complexity (how hard to run in production?)
- Lock-in risk (how hard to migrate away?)

**Rules:**
- Never present a single option. If there's truly only one option, document why alternatives were rejected.
- Be honest about the trade-offs of the chosen option. Every choice has downsides.
- Include "Do Nothing" as an option when applicable.

### 4.7 Consequences

**Positive consequences** — what we gain:
- List specific benefits from this decision.

**Negative consequences** — what we accept:
- List specific trade-offs or downsides.
- These are NOT risks; they are known, accepted costs.

**Risks** — what could go wrong:
- List risks with likelihood and impact.
- Include mitigation strategies for each risk.

### 4.8 Compliance & Standards (Optional but Recommended)
- Does this decision affect regulatory compliance (GDPR, SOC2, PCI-DSS)?
- Does it align with organization architecture principles?
- Does it follow industry standards?

### 4.9 References
- Links to RFCs, blog posts, benchmarks, vendor documentation, or related ADRs.

---

## 5. File Naming & Storage

### Naming Convention
```
docs/adr/NNN-short-description.md
```

Examples:
```
docs/adr/001-use-postgresql-for-user-profiles.md
docs/adr/002-adopt-event-driven-architecture.md
docs/adr/003-choose-github-actions-for-cicd.md
```

**Rules:**
- Sequential numbering, zero-padded to 3 digits.
- Lowercase, kebab-case.
- Description matches the decision statement.

### Storage Location
- ADRs MUST live in the repository they govern: `docs/adr/`
- Organization-wide ADRs (cross-cutting) go in a dedicated architecture repository.

---

## 6. Quality Checklist

Before approving an ADR, verify:

- [ ] Title is a clear decision statement (not a question or vague topic)
- [ ] Context includes the problem, constraints, and forces
- [ ] At least 2 alternatives are evaluated with criteria
- [ ] Trade-off analysis uses weighted scoring (not just "gut feel")
- [ ] Consequences include BOTH positive and negative impacts
- [ ] Risks have mitigation strategies
- [ ] The decision is traceable to a business need
- [ ] Status is correctly set
- [ ] References are included for external sources

---

## 7. Common ADR Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "We chose X because it's popular" | No analysis, bandwagon fallacy | Evaluate against YOUR constraints |
| Only one option presented | Bias confirmation, no real decision | Always show 2+ alternatives |
| All pros, no cons | Dishonest, hides future problems | Every option has trade-offs — document them |
| 500-word context, 1-line decision | Effort in wrong place | Decision + reasoning MUST be the strongest section |
| "Decided in meeting" with no ADR | Lost institutional knowledge | If it's worth deciding, it's worth recording |
| Never updating status | Stale decisions cause confusion | Review quarterly, mark deprecated/superseded |
| Too many ADRs for trivial choices | ADR fatigue, noise | Only architect-level decisions need ADRs |

---

## 8. Example Decision Topics

For reference, here are common enterprise architecture decisions that SHOULD have ADRs:

**Data Layer:**
- Primary database technology, Read replicas vs CQRS, Caching strategy, Data partitioning approach

**Communication:**
- Sync vs async communication, Message broker choice, API protocol (REST vs GraphQL vs gRPC)

**Infrastructure:**
- Cloud provider, Container orchestration, CDN choice, DNS strategy, Multi-region approach

**Security:**
- Authentication provider, Token strategy, Encryption approach, API gateway selection

**Architecture Style:**
- Monolith vs microservices, Event sourcing vs CRUD, Serverless vs containerized

**DevOps:**
- CI/CD platform, GitFlow vs trunk-based, Deployment strategy, IaC tooling

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
