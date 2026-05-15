# [Project Name] - Discovery & Ambiguity Report

<!-- Archpilot: discovery.md | Phase 0: DISCOVERY -->
<!-- Governed by: rules/36-discovery-ambiguity.md -->

---

## 1. The Deconstructed Prompt
**Client Request:**
> *[Paste the vague/ambiguous request here]*

**What This Actually Means Technically:**
- [Translate the business ask into technical realities. e.g., "This requires a globally distributed database with active-active replication."]

---

## 2. Implicit Assumptions
*These are the technical assumptions the architect is making. If any are wrong, the subsequent design will be invalid.*

1. **Traffic Profile:** [e.g., Read-heavy (90/10), highly bursty.]
2. **Consistency Need:** [e.g., Eventual consistency is acceptable for UI, but financial transactions must be strongly consistent.]
3. **Data Residency:** [e.g., Global users implies GDPR/CCPA compliance required; data must stay in-region.]

---

## 3. Critical Edge Cases & Failure Modes
*Scenarios that break naive implementations.*

| ID | Edge Case Scenario | Potential Impact | Required Defense |
|----|--------------------|------------------|------------------|
| EC-01 | [e.g., Network Partition between Region A and B] | [e.g., Split-brain data corruption] | [e.g., Quorum-based writes] |
| EC-02 | [e.g., Third-party API rate limits exceeded] | [e.g., Complete service halt] | [e.g., Circuit breakers + DLQ] |
| EC-03 | | | |

---

## 4. Architectural Trade-offs

We cannot finalize the design until the business prioritizes what matters most. Choose one:

### Option A: [e.g., High-Reliability, Event-Sourced]
- **Architecture:** [Brief description]
- **Pros:** Maximum resilience, complete audit log, zero data loss.
- **Cons:** High engineering complexity, 3x infrastructure cost.
- **Estimated TTM (Time to Market):** High

### Option B: [e.g., Cost-Optimized, CRUD-based]
- **Architecture:** [Brief description]
- **Pros:** Fast time-to-market, low operational overhead, simple debugging.
- **Cons:** 5-minute RPO risk, difficult to scale globally without refactoring.
- **Estimated TTM (Time to Market):** Low

---

## 5. The Interrogation List
*Questions the client/business must answer to unblock `requirements.md`.*

1. **Question:** [e.g., Are you willing to pay $10k/month to guarantee 99.99% uptime, or is 99.9% acceptable for $2k/month?]
2. **Question:** [e.g., When the payment gateway goes down, should we block users from boarding, or allow them to board and retry payment later?]
3. **Question:** [e.g., What is the absolute maximum latency a user will tolerate before abandoning the funnel?]
4. **Question:**
5. **Question:**

---
*Archpilot - Discovery Template*
