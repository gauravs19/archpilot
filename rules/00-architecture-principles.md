# Architecture Principles — Enterprise Standard

> **Purpose:** These are the foundational rules that govern ALL architecture decisions.
> When used as LLM context, these principles ensure every generated design, document,
> and recommendation is grounded in enterprise-grade thinking.

---

## How to Use This File

- **Claude Projects:** Upload this file as project knowledge
- **ChatGPT:** Paste into Custom GPT instructions or conversation context
- **VS Code / Cursor:** Reference in `.github/copilot-instructions.md` or `.cursorrules`
- **Any LLM:** Prefix your prompt with: *"Follow these architecture principles: [paste this file]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [04 — LLD Standards](./04-lld-standards.md) | Applies these principles at the component level |
| [03 — HLD Standards](./03-hld-standards.md) | Applies these principles at the system level |
| [07 — Security Architecture](./07-security-architecture.md) | Expands Security Principles (§5) |
| [14 — Cost Optimization](./14-cost-optimization.md) | Expands FinOps Principles (§8) |
| [02 — ADR Standards](./02-adr-standards.md) | Implements Decision-Making Framework (§2) |

---

## 1. Design Principles

### 1.1 Separation of Concerns (SoC)
- Every module, service, or component MUST have a single, well-defined responsibility.
- Business logic MUST be separated from infrastructure concerns (databases, messaging, HTTP).
- Presentation, application, domain, and infrastructure layers MUST be independently deployable or replaceable.

### 1.2 Loose Coupling, High Cohesion
- Components SHOULD communicate through well-defined interfaces (APIs, events, contracts), not shared state.
- Internal details of a component MUST NOT leak into its public interface.
- Related functionality SHOULD be grouped together; unrelated functionality MUST be separated.

### 1.3 API-First Design
- All inter-service communication MUST be defined through versioned API contracts BEFORE implementation.
- API contracts SHOULD be the single source of truth — code is generated from contracts, not the other way around.
- Internal APIs follow the same rigor as external APIs.

### 1.4 Configuration Over Code
- Environment-specific values (URLs, credentials, feature flags, thresholds) MUST be externalized into configuration.
- Configuration MUST be environment-aware (dev, staging, production) and NEVER hardcoded.
- Secrets MUST be managed through a secrets manager (AWS Secrets Manager, HashiCorp Vault, Azure Key Vault), NEVER in config files or environment variables in plain text.

### 1.5 Convention Over Configuration
- Adopt framework and language conventions by default. Override only when there is a documented, justified reason.
- Naming conventions (files, classes, APIs, database tables) MUST be consistent across the entire system.
- Directory structures SHOULD follow the established patterns of the chosen framework/language.

### 1.6 Fail Fast, Recover Gracefully
- Systems MUST validate inputs at the boundary (API gateway, service entry points) and reject invalid data immediately.
- Failures MUST be detected quickly through health checks, circuit breakers, and timeouts.
- Recovery mechanisms (retries, fallbacks, graceful degradation) MUST be designed into every external dependency interaction.

### 1.7 Design for Observability
- Every service MUST emit structured logs, metrics, and distributed traces from day one — not retrofitted later.
- Observability is a FIRST-CLASS architectural concern, not an afterthought.
- Each service MUST expose a health check endpoint and readiness probe.

### 1.8 Principle of Least Privilege
- Every component, service, user, and process MUST operate with the minimum permissions required.
- Service-to-service authentication MUST use short-lived tokens or mutual TLS, not shared API keys.
- Database access SHOULD use role-based accounts with query-level restrictions where possible.

---

## 2. Decision-Making Framework

### 2.1 Trade-Off Analysis (Mandatory)
Every significant architecture decision MUST document:
1. **Options Considered** — at least 2-3 alternatives
2. **Evaluation Criteria** — weighted factors (cost, complexity, team skill, scalability, time-to-market)
3. **Decision** — the chosen option with clear rationale
4. **Consequences** — both positive and negative impacts
5. **Reversibility** — how easy is it to change this decision later?

### 2.2 Build vs. Buy vs. Adopt
Use this decision matrix for technology selection:

| Factor | Weight | Evaluate |
|--------|--------|----------|
| Core vs. Peripheral | High | Is this a core differentiator or a commodity capability? |
| Team Expertise | High | Does the team have production experience with this technology? |
| Total Cost of Ownership | High | Include licensing, ops, training, and migration costs over 3 years |
| Community & Support | Medium | Is there active development, documentation, and enterprise support? |
| Lock-in Risk | Medium | How difficult is it to migrate away from this technology? |
| Time to Production | Medium | How quickly can we deliver with this choice? |
| Compliance | High | Does it meet regulatory and security requirements? |

**Rule:** Build only when the capability is a core differentiator AND no mature solution exists.
**Rule:** Default to managed/SaaS services for non-differentiating capabilities.

### 2.3 Reversibility Principle
- **Two-way door decisions** (easily reversible): Move fast, optimize for speed.
- **One-way door decisions** (hard to reverse): Invest in analysis, get stakeholder alignment, document thoroughly.
- When in doubt, choose the option that preserves the most future flexibility.

---

## 3. Scalability Principles

### 3.1 Design for 10x
- Architecture SHOULD handle 10x the current load without fundamental redesign.
- Identify bottlenecks early: single databases, synchronous chains, shared state.
- Horizontal scaling SHOULD be the primary scaling strategy; vertical scaling is a temporary measure.

### 3.2 Statelessness
- Application services MUST be stateless. All state MUST be externalized to databases, caches, or message brokers.
- Session state MUST NOT be stored in-memory on application servers.
- Any instance of a service MUST be replaceable without data loss.

### 3.3 Asynchronous by Default
- Operations that don't require an immediate response SHOULD be processed asynchronously.
- Use message queues or event streams for inter-service communication where real-time response is not required.
- Design for eventual consistency where strong consistency is not a business requirement.

### 3.4 Caching Strategy
- Identify hot data paths and implement caching at the appropriate layer (CDN, API gateway, application, database).
- Every cache MUST have a defined TTL and invalidation strategy.
- Cache-aside pattern is the default; write-through or write-behind MUST be justified.

---

## 4. Reliability Principles

### 4.1 Resilience Patterns (Mandatory for Production)
Every production service MUST implement:

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Circuit Breaker** | Prevent cascade failures when a dependency is down | Open after N failures, half-open to test recovery |
| **Retry with Backoff** | Handle transient failures | Exponential backoff with jitter, max 3 retries |
| **Timeout** | Prevent hanging requests | Every external call MUST have an explicit timeout |
| **Bulkhead** | Isolate failures to prevent system-wide impact | Separate thread pools/connection pools per dependency |
| **Fallback** | Provide degraded service instead of failure | Cached data, default values, or reduced functionality |

### 4.2 Data Durability
- All business-critical data MUST be replicated across at least 2 availability zones.
- Backup strategy MUST define RPO (Recovery Point Objective) and RTO (Recovery Time Objective).
- Backup restoration MUST be tested at least quarterly.

### 4.3 Graceful Degradation
- Systems MUST continue to serve core functionality even when non-critical dependencies fail.
- Feature flags SHOULD be used to disable non-essential features during incidents.
- Load shedding strategy MUST be defined for traffic exceeding capacity.

---

## 5. Security Principles

### 5.1 Zero Trust Architecture
- NEVER trust network location. Authenticate and authorize every request, even internal ones.
- All communication between services MUST be encrypted (TLS 1.2+ minimum, TLS 1.3 preferred).
- Service identity MUST be verified through certificates or tokens, not IP allowlists.

### 5.2 Defense in Depth
- Security controls MUST exist at every layer: network, application, data, identity.
- No single security control should be the only protection against a threat.
- Input validation MUST happen at every trust boundary.

### 5.3 Secure by Default
- All new services MUST start with the most restrictive security configuration.
- Access is denied by default; permissions are explicitly granted.
- Default passwords, keys, and configurations MUST be changed before deployment.

### 5.4 Data Classification
Every data element MUST be classified:

| Classification | Handling | Examples |
|---------------|----------|----------|
| **Public** | No restrictions | Marketing content, public APIs |
| **Internal** | Authenticated access only | Employee directory, internal docs |
| **Confidential** | Role-based access, encrypted at rest | Customer data, financial records |
| **Restricted** | Strict access control, audit logging, encryption | PII, credentials, health records |

---

## 6. Data Architecture Principles

### 6.1 Data Ownership
- Every data entity MUST have a single owning service. Only the owner can write to it.
- Other services access data through the owner's API or through published events.
- No shared databases between services. Each service owns its data store.

### 6.2 Schema Evolution
- Database schemas MUST support backward-compatible evolution (additive changes preferred).
- Breaking schema changes MUST follow a migration strategy with zero-downtime deployment.
- All schema changes MUST be versioned and applied through migration scripts, never manually.

### 6.3 Data Quality
- Data validation MUST happen at the ingestion boundary.
- Data contracts MUST be defined between producers and consumers.
- Data lineage SHOULD be traceable for compliance and debugging.

---

## 7. Operational Principles

### 7.1 Infrastructure as Code (IaC)
- ALL infrastructure MUST be defined in code (Terraform, Pulumi, CloudFormation, CDK).
- No manual changes to production infrastructure. All changes go through the IaC pipeline.
- Infrastructure code MUST be reviewed, tested, and version-controlled like application code.

### 7.2 Deployment Principles
- Every deployment MUST be automated, repeatable, and rollback-capable.
- Blue-green or canary deployments for production. Never big-bang releases.
- Feature flags for separating deployment from feature release.

### 7.3 Incident Response
- Every production system MUST have a runbook with common failure scenarios and resolution steps.
- Post-incident reviews (blameless) MUST happen within 48 hours of every major incident.
- Action items from post-mortems MUST be tracked and prioritized in the backlog.

---

## 8. Cost Principles (FinOps)

### 8.1 Cost-Aware Architecture
- Every architecture decision MUST consider Total Cost of Ownership (3-year projection).
- Cost MUST be a first-class architectural attribute, alongside performance and security.
- Resource tagging MUST be enforced for cost attribution by team, project, and environment.

### 8.2 Right-Sizing
- Start with the smallest viable resource size and scale based on observed metrics.
- Over-provisioning for "just in case" scenarios is an architecture smell — use auto-scaling instead.
- Review and optimize resource utilization monthly.

### 8.3 Managed Over Self-Hosted
- Default to managed services (RDS over self-hosted PostgreSQL, SQS over self-hosted RabbitMQ).
- Self-hosting is justified only when: cost savings exceed 40% at scale, or compliance prevents managed service use.

---

## Quick Reference: Decision Checklist

Before finalizing any architecture decision, verify:

- [ ] Does it follow Separation of Concerns?
- [ ] Is it loosely coupled with well-defined interfaces?
- [ ] Is configuration externalized and environment-aware?
- [ ] Does it fail fast and recover gracefully?
- [ ] Is observability built in (logs, metrics, traces)?
- [ ] Does it follow the Principle of Least Privilege?
- [ ] Has a trade-off analysis been documented?
- [ ] Can it handle 10x load without redesign?
- [ ] Are resilience patterns in place (circuit breaker, retry, timeout)?
- [ ] Is all communication encrypted?
- [ ] Is data ownership clear and shared databases avoided?
- [ ] Is infrastructure defined as code?
- [ ] Has the cost impact been estimated?
- [ ] Is the decision reversible? If not, has it been thoroughly reviewed?

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
