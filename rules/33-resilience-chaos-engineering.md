# Resilience & Chaos Engineering Standards

> **Purpose:** This rule file defines standards for systematically testing and improving
> system resilience through chaos engineering. It transforms resilience from an aspirational
> property into a measurable, continuously verified system attribute.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [04 — LLD Standards](./04-lld-standards.md) | Resilience patterns at component level |
| [00 — Architecture Principles](./00-architecture-principles.md) | Resilience principles (§4) |
| [12 — Observability](./12-observability-standards.md) | Observability required to measure chaos experiments |
| [19 — Incident Management](./19-incident-management.md) | Chaos findings feed the incident playbook |
| [20 — Testing Strategy](./20-testing-strategy.md) | Chaos as advanced testing layer |

---

## 1. What is Chaos Engineering?

Chaos engineering is the discipline of experimenting on a system to build confidence in its
ability to withstand turbulent conditions in production.

> "Chaos engineering is not about breaking things on purpose. It is about revealing
> the hidden assumptions your system makes about the world." — Chaos Engineering Principle

### 1.1 Chaos Engineering vs Testing

| Aspect | Traditional Testing | Chaos Engineering |
|--------|--------------------|--------------------|
| Scope | Known failure modes | Unknown and emergent failures |
| Environment | Dev/staging (usually) | Production (safely) or staging mirror |
| Trigger | Explicit test case | Injected fault/condition |
| Goal | Verify correctness | Reveal weakness |
| Frequency | Per-deployment | Continuous (scheduled) |

---

## 2. The Chaos Engineering Loop

```
1. DEFINE steady state ? 2. HYPOTHESIZE ? 3. INJECT fault ? 4. OBSERVE ? 5. IMPROVE
        ?                                                                        ¦
        +---------------------- Repeat on schedule ------------------------------+
```

### 2.1 Step 1: Define Steady State

Steady state = the normal, healthy behavior of the system (measurable).

Define steady state using:
- **Business metrics:** Order completion rate >99.5%, checkout success rate >99%
- **Technical metrics:** p99 latency <1s, error rate <0.1%, queue depth <500

**Rule:** If you cannot define steady state, you cannot do chaos engineering. Observability MUST come first.

### 2.2 Step 2: Hypothesize

For each experiment, state: *"We believe that when [fault is injected], [system component] will [expected behavior], and steady state will be maintained."*

Example: *"We believe that when the payment-gateway returns 503 for 30 seconds, the checkout service will activate its circuit breaker, serve cached pricing, and order completion rate will remain above 95%."*

### 2.3 Step 3: Inject Fault

Apply the fault in a controlled manner (see §4 for fault types). Always:
- Start with the smallest blast radius possible
- Have a kill switch ready (immediate fault removal)
- Have a rollback plan if steady state is violated

### 2.4 Step 4: Observe

During and after fault injection:
- Monitor steady-state metrics continuously
- Record: time to detect, time to recover, blast radius (actual vs expected)
- Capture any unexpected behaviors or cascading failures

### 2.5 Step 5: Improve

- If hypothesis confirmed ? document confidence; schedule next harder experiment
- If hypothesis rejected ? create improvement ticket; fix before running again
- Always: update runbooks, alerts, and architecture docs with findings

---

## 3. Blast Radius Control

| Level | Scope | Who Approves | Environment |
|-------|-------|:------------:|-------------|
| **Level 1** | Single instance / replica | Team lead | Staging |
| **Level 2** | Single service | Architect | Staging |
| **Level 3** | Service + its direct dependencies | Architect + SRE | Staging or production (off-peak) |
| **Level 4** | Availability zone | CTO + SRE lead | Production (with customer comms) |
| **Level 5** | Multi-region / full system | Executive + CTO | Production (scheduled GameDay) |

**Rule:** NEVER jump levels. Start at Level 1 and graduate with each successful experiment.
**Rule:** Production experiments above Level 2 require advance customer communication.

---

## 4. Fault Injection Types

### 4.1 Infrastructure Faults

| Fault | Tool | Target |
|-------|------|--------|
| Kill a process/pod | Chaos Monkey, k6, kubectl | Application process |
| Terminate a VM/instance | AWS FIS, Chaos Monkey | EC2/EKS node |
| Network latency injection | Toxiproxy, tc netem, Istio | Service-to-service calls |
| Packet loss | tc netem, Toxiproxy | Network interface |
| Disk I/O throttling | cgroups, AWS FIS | Disk throughput |
| Memory pressure | stress-ng | Container/VM |
| CPU saturation | stress-ng | Container/VM |
| DNS failure | Blockade, custom DNS | Name resolution |

### 4.2 Application Faults

| Fault | Injection Method |
|-------|----------------|
| Slow response (latency) | Sleep injection in code, Toxiproxy |
| HTTP 5xx errors | Mock server, feature flag, Toxiproxy |
| Dependency timeout | Reduced timeout config, Toxiproxy |
| Exception/panic | Fault injection middleware |
| Queue consumer failure | Kill consumer, pause consumer group |
| Database connection exhaustion | Fill connection pool |
| Cache unavailability | Stop/block Redis/Memcached |
| Message schema corruption | Publish invalid schema to queue |

### 4.3 Data Faults

| Fault | Purpose |
|-------|---------|
| Read-only database | Test failover to replica |
| Stale cache | Verify cache-miss handling |
| Corrupt event payload | Verify schema validation and DLQ routing |
| Partial data (missing required fields) | Verify validation at boundaries |

---

## 5. GameDay Standards

A GameDay is a structured, time-boxed chaos experiment run as a team exercise.

### 5.1 GameDay Preparation Checklist

**4 weeks before:**
- [ ] Scope defined: which systems, which faults, blast radius Level N
- [ ] Steady-state metrics identified and dashboards ready
- [ ] Hypothesis documented for each planned experiment
- [ ] Rollback procedures documented and tested
- [ ] Customer communication drafted (if production)

**1 week before:**
- [ ] Stakeholder sign-off obtained
- [ ] On-call team briefed; incident response process reviewed
- [ ] Kill switches tested (can we stop the fault immediately?)
- [ ] Staging environment validated (mirrors production behavior)

**Day of:**
- [ ] All participants in war room (physical or virtual)
- [ ] Dashboards visible on shared screen
- [ ] Communication channel open (Slack/Teams bridge)
- [ ] Time-box agreed: max 4 hours

### 5.2 GameDay Output Artifacts

Every GameDay MUST produce:

1. **Experiment Report:** Hypothesis, fault injected, observations, outcome (pass/fail)
2. **Weakness Registry:** All weaknesses found, severity, ticket created
3. **Runbook Updates:** New failure scenarios added to service runbooks
4. **Architecture Review Items:** Systemic weaknesses requiring design changes
5. **Next GameDay Scope:** Harder experiments based on this session's findings

---

## 6. Chaos Engineering Maturity Levels

| Level | Capability |
|-------|-----------|
| **0 — Ad Hoc** | No formal chaos practice; resilience tested only by real incidents |
| **1 — Staged** | Manual fault injection in staging; no production |
| **2 — Scheduled** | Regular chaos experiments in staging; basic automation |
| **3 — Production-Ready** | Automated chaos in production (low blast radius); GameDays quarterly |
| **4 — Continuous** | Automated chaos runs continuously in production; findings auto-create tickets |
| **5 — Chaos as Culture** | All teams run chaos experiments; resilience is a delivery gate |

**Target:** All production systems MUST reach Level 3 within 12 months of go-live.

---

## 7. Resilience Patterns Verification Checklist

Use chaos engineering to verify these patterns work as designed:

| Pattern | Chaos Test | Expected Behavior |
|---------|-----------|------------------|
| **Circuit Breaker** | Inject 100% failure on dependency | Circuit opens after N failures; fallback activates |
| **Retry with Backoff** | Inject intermittent 503s | Retries with increasing delay; succeeds on recovery |
| **Bulkhead** | Saturate thread pool for one dependency | Other dependencies unaffected |
| **Timeout** | Inject 60-second delay | Request fails at configured timeout; not after 60s |
| **Graceful Degradation** | Kill non-critical service | Core features continue; degraded features show graceful error |
| **Health Check** | Kill application process | Load balancer detects unhealthy within 10s; stops routing |
| **DLQ** | Inject malformed messages | Messages routed to DLQ; consumer continues processing valid messages |
| **Multi-AZ Failover** | Terminate all instances in one AZ | Traffic shifts to healthy AZ within RPO |

---

## 8. Chaos Engineering Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Chaos without observability | Can't measure steady state or impact | Observability first; chaos second |
| Production chaos without staging proof | Uncontrolled blast radius | Start in staging; graduate to production |
| No rollback plan | Stuck in broken state | Kill switch and rollback required before experiment starts |
| Running chaos during peak hours | Unnecessary customer impact | Off-peak windows for Level 3+; never during launches |
| "We already know what will break" | Confirmation bias; missed surprises | Hypothesis-driven; test assumptions, not certainties |
| No improvement tickets | Chaos finds weaknesses; nothing changes | Every weakness must have a tracked ticket with priority |
| One-time GameDay (never repeated) | Fixes get regressed over time | Scheduled repeating experiments; resilience is continuous |

---

## 9. Chaos Engineering Checklist

- [ ] Steady-state metrics defined for all production services
- [ ] Observability in place (logs, metrics, traces) before any experiment
- [ ] Fault injection tools available (Toxiproxy, k6, AWS FIS, or equivalent)
- [ ] Blast radius levels defined; approval gates per level
- [ ] Kill switches tested before every experiment
- [ ] Hypothesis documented for each experiment
- [ ] GameDay conducted quarterly (minimum)
- [ ] All resilience patterns (circuit breaker, retry, timeout, bulkhead) verified by chaos test
- [ ] Weakness registry maintained and tracked in backlog
- [ ] Runbooks updated after every GameDay

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
