# [Project Name] - Estimation Abacus (Fixed-Bid Framework)

<!-- Archpilot: estimation-abacus.md | Phase 0/1 Presales -->
<!-- Governed by: rules/16-estimation-framework.md -->

> **Purpose:** To calculate realistic, risk-adjusted engineering estimates for fixed-bid or enterprise presales engagements. Prevents systematic under-estimation by enforcing complexity multipliers and explicit risk buffers.

---

## 1. Project Parameters
- **Client/Project:** [Name]
- **Delivery Model:** [Fixed-Bid / T&M / Staff Aug]
- **Target Launch Date:** [YYYY-MM-DD]
- **Estimation Confidence:** [e.g., ROM (Rough Order of Magnitude) ±50%, Detailed ±10%]

---

## 2. Complexity Multipliers
*Apply these multipliers to base component estimates based on hidden complexity vectors.*

| Complexity Vector | Low (1.0x) | Medium (1.5x) | High (2.5x) |
|-------------------|------------|---------------|-------------|
| **Legacy Integration** | Modern REST/JSON | SOAP, Poor Docs | Mainframe, No Docs, TCP sockets |
| **Data Migration** | None | Same schema, 1 DB | Diff schema, multiple sources, zero-downtime |
| **NFR Extremes** | Standard web traffic | High throughput | Sub-millisecond latency, massive scale |
| **Security/Compliance**| Standard auth | PII/PCI involved | HIPAA, FedRAMP, Military-grade |

**Calculated Project Blended Multiplier:** `[e.g., 1.5x]`

---

## 3. Work Breakdown Structure (WBS) & Effort (Days)
*Base Estimate = Ideal days. Adjusted Estimate = Base * Complexity Multiplier.*

| ID | Component / Module | Base Est. | Multiplier | Adjusted Est. | Assigned Role |
|----|--------------------|:---------:|:----------:|:-------------:|---------------|
| `M-01`| Auth & User Management | 5 | 1.0x | **5.0** | Fullstack Dev |
| `M-02`| Legacy DB Synchronization | 10 | 2.5x | **25.0** | Data Engineer |
| `M-03`| Core Transaction Engine | 15 | 1.5x | **22.5** | Backend Dev |
| `M-04`| Mobile App UI (iOS) | 20 | 1.0x | **20.0** | Mobile Dev |
| **SUM**| | | | **72.5 days** | |

---

## 4. Cross-Functional Pipeline (The "Hidden Effort")
*Developers write code, but shipping requires a village. Add standard percentages to the Total Adjusted Estimate.*

| Activity | Standard Allocation | Calculated Days | Notes |
|----------|---------------------|-----------------|-------|
| **Base Engineering** | - | `72.5` | From WBS above |
| Project Management | +15% of Base | `10.8` | Scrum, Client Syncs |
| QA & Testing | +20% of Base | `14.5` | Manual & Automation |
| DevOps & CI/CD | +10% of Base | `7.2` | Pipelines, IaC, Env setup |
| UAT Bug Fixing | +10% of Base | `7.2` | Post-handoff stabilization |
| **SUBTOTAL** | | **112.2 days** | |

---

## 5. Risk Buffers (The Unknown-Unknowns)
*Based on the Assumption Log (A-XXX) and general project maturity.*

| Risk Type | Allocation | Calculated Days | Justification |
|-----------|------------|-----------------|---------------|
| Architecture Unknowns | +10% to 20% | `16.8` (15%) | 3 High-Risk Assumptions Open |
| **TOTAL EFFORT** | | **129.0 days** | |

---

## 6. Commercial Summary (For Presales)

- **Total Estimated Effort:** `129 Person-Days`
- **Recommended Team Size:** `4 resources` (1 PM, 2 Devs, 1 QA)
- **Estimated Duration:** `~6.5 Weeks` (129 days / 4 people = 32.25 days)
- **Rough Order of Magnitude (ROM) Cost:** `[$$$]` (Calculate via regional blended rate)

---
*Archpilot - Estimation Abacus*
