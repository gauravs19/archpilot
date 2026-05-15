# [Project Name] - Phase 0 Discovery & Ambiguity Report

<!-- Archpilot: discovery.md | Phase 0: DISCOVERY -->
<!-- Governed by: rules/36-discovery-ambiguity.md -->

---

## 1. Executive Intent (The "Why")
*Before discussing "how", we must define "why". Why is the business funding this?*

- **Primary Business Driver:** [e.g., Increase revenue, reduce operational cost, regulatory compliance, competitive parity.]
- **Target Market/Persona:** [Who pays for this? Who uses this?]
- **Definition of Success (Business):** [e.g., "Must onboard 10,000 new users in Q3 without adding support headcount."]

---

## 2. Prompt Deconstruction
*Bridging the gap between the client's vague request and engineering reality.*

**The Vague Request:**
> *[Paste the raw, ambiguous client request here]*

**Technical Translation:**
- [e.g., Client asks: "Real-time global dashboard."]
- [Translation: "Requires sub-500ms latency globally, multi-region read replicas, and WebSocket/SSE streaming infrastructure."]

---

## 3. The 5-Vector Discovery Sieve
*Systematically forcing out missing constraints.*

### 3.1 Scale Vector
- **Expected Throughput:** [e.g., 10k TPS during peak, 1k TPS nominal]
- **Read/Write Ratio:** [e.g., 95% reads, 5% writes]
- **Seasonality/Bursts:** [e.g., 10x spikes on Black Friday]

### 3.2 Failure Vector (Resilience)
- **Worst-Case Tolerance:** [e.g., What happens if the primary DB goes down? Data loss vs Downtime?]
- **Graceful Degradation:** [e.g., Can the UI function in 'offline mode' if the recommendation engine is down?]

### 3.3 Security & Malicious Actor Vector
- **Data Classification:** [e.g., PII, PCI-DSS, HIPAA, or public data?]
- **Abuse Vectors:** [e.g., How could a bot network exploit the APIs for financial gain?]

### 3.4 State & Time Vector
- **Consistency Needs:** [e.g., Is Read-After-Write consistency mandatory, or is Eventual Consistency acceptable?]
- **Data Freshness:** [e.g., How stale can a dashboard metric be? 1 second? 5 minutes?]

### 3.5 Cost Vector
- **Margin Profile:** [e.g., Is the business highly sensitive to infrastructure costs per transaction?]

---

## 4. Critical Edge Cases & Failure Modes
*Scenarios that will break naive implementations.*

| ID | Edge Case Scenario | Potential Impact | Required Defense |
|----|--------------------|------------------|------------------|
| EC-01 | [e.g., Network Partition between regions] | [e.g., Split-brain data corruption] | [e.g., Quorum-based writes] |
| EC-02 | [e.g., External API rate limits exceeded] | [e.g., Complete service halt] | [e.g., Circuit breakers + DLQ] |

---

## 5. Architectural Trade-offs
*We cannot finalize the design until the business prioritizes what matters most. Choose one option.*

### Option A: [e.g., High-Reliability, Event-Sourced]
- **Architecture Overview:** [Brief description]
- **Pros:** Maximum resilience, complete audit log, zero data loss.
- **Cons:** High engineering complexity, higher operational overhead.
- **Estimated Infra Cost:** High ($$$)
- **Time to Market (TTM):** Slow (4-6 months)

### Option B: [e.g., Cost-Optimized, CRUD-based]
- **Architecture Overview:** [Brief description]
- **Pros:** Fast time-to-market, simple debugging, low infrastructure cost.
- **Cons:** 5-minute RPO risk during regional outages, harder to scale globally later.
- **Estimated Infra Cost:** Low ($)
- **Time to Market (TTM):** Fast (1-2 months)

---

## 6. The Interrogation List
*The exact questions the client MUST answer to unblock `requirements.md`.*

| # | Question to Business / Client | Impact if Unresolved | Priority |
|---|-------------------------------|----------------------|----------|
| 1 | [e.g., Are you willing to pay 3x infra costs to guarantee 99.99% uptime, or is 99.9% acceptable?] | Dictates active-active vs active-passive architecture. | HIGH |
| 2 | [e.g., What is the maximum tolerable data loss (RPO) in a catastrophic failure?] | Determines database replication strategy. | HIGH |
| 3 | [Question...] | [Impact...] | MEDIUM |

---
*Archpilot - Discovery Template*
