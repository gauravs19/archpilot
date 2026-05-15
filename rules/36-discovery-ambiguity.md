# Discovery & Ambiguity Resolution Standards

> **Purpose:** This rule defines how to handle highly ambiguous, high-level business requests (typically seen in Presales, RFP discovery, or early product ideation). It forces the AI or Architect to stop "hallucinating assumptions" and instead systematically deconstruct the ambiguity into explicit edge cases, architectural trade-offs, and targeted client questions before writing a single line of a final specification.

---

## 1. The Ambiguity Trap

When presented with a vague requirement (e.g., *"We need a scalable ride-matching system that works globally"*), the standard LLM or Junior Architect response is to immediately jump to Phase 1 (Specifying) or Phase 2 (Designing). 

This leads to the **Ambiguity Trap**: designing a perfect system for the wrong assumptions.

**The Discovery Standard mandates Phase 0: DISCOVERY.**
Before `requirements.md` can be written, you must produce a `discovery.md` artifact that exposes the hidden complexities.

---

## 2. The Discovery Sieve (5 Vectors)

When faced with an ambiguous prompt, the Architect MUST analyze it through the Discovery Sieve to extract missing dimensions:

### 2.1 The Scale Vector
Vague: *"It needs to handle a lot of traffic."*
**Resolution Questions:**
- What is the expected ratio of Reads vs. Writes?
- What is the definition of "Peak"? (e.g., Stadium event, Black Friday, daily rush hour).
- Is traffic globally distributed evenly, or heavily localized causing hot-partitions?

### 2.2 The Failure Vector (Edge Cases)
Vague: *"It should be reliable."*
**Resolution Questions:**
- What happens during a network partition? (Consistency vs Availability)
- Define the "Worst Case Scenario" (e.g., Payment gateway goes down while a ride is active).
- What is the gracefully degraded state? (e.g., If the ETA engine fails, do we fallback to straight-line distance math?)

### 2.3 The Malicious Actor Vector
Vague: *"Make it secure."*
**Resolution Questions:**
- How could a user game the system for financial gain? (e.g., Driver spoofing GPS to simulate long rides).
- What happens if a bad actor spams the primary ingestion endpoint?

### 2.4 The State & Time Vector
Vague: *"Real-time updates."*
**Resolution Questions:**
- What is the tolerance for stale data? (Read-after-write consistency).
- How do we handle out-of-order events? (e.g., Driver goes through a tunnel, ping 3 arrives before ping 2).

### 2.5 The Cost & Financial Vector
Vague: *"Built for enterprise."*
**Resolution Questions:**
- Is the business model high-margin/low-volume or low-margin/high-volume? This dictates whether we can over-provision infrastructure or if we must ruthlessly optimize compute.

---

## 3. Formulating Trade-offs (The Presales Method)

During discovery, you never give the client *one* architecture. You give them **Two Options with Trade-offs**. This forces the business to reveal their true priorities.

**Format:**
*   **Option A (The High-Reliability/High-Cost Route):** Multi-region Active-Active, Event-Sourced, sub-second latency.
    *   *Trade-off:* 3x infrastructure cost, higher engineering complexity.
*   **Option B (The Eventual Consistency/Cost-Optimized Route):** Single-region Active-Passive, Batch-processing matching.
    *   *Trade-off:* 5-second matching delay, risk of regional failover downtime, but 70% cheaper to run.

---

## 4. The `discovery.md` Artifact

Before moving to the SDD Triad (`requirements.md` -> `design.md` -> `tasks.md`), the Architect must generate `discovery.md`.

### Mandatory Sections in `discovery.md`:
1. **The Deconstructed Prompt:** What the client asked vs. what they actually meant.
2. **Implicit Assumptions:** A list of technical assumptions the architect is making, which the client must sign off on.
3. **Critical Edge Cases:** 5-7 edge cases that break naive implementations (e.g., GPS drift, out-of-order telemetry, simultaneous matching conflicts).
4. **Architectural Trade-offs (Options A vs B):** Cost vs Performance vs Time-to-Market options.
5. **The Interrogation List:** The exact 3-5 questions the client MUST answer before `requirements.md` can be finalized.

---

## 5. AI Prompting for Ambiguity Resolution

When feeding a vague client request to an LLM using Archpilot, use this prompt prefix:

> *"You are a Principal Solutions Architect in a presales discovery session. I am going to give you a highly ambiguous client request. DO NOT design the final system. Instead, apply Archpilot Rule 36 (Discovery & Ambiguity Resolution). Generate a `discovery.md` that identifies the hidden edge cases, defines the unknown scale vectors, presents two architectural trade-off options, and lists the 5 critical questions I must ask the client to unblock the design."*
