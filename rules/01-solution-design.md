# Solution Design Standards

> **Purpose:** This rule file defines when and how to write a Solution Design Document (SDD) —
> the "one document" that connects business requirements to technical architecture.
> It bridges the gap between what stakeholders want and what engineers build.

---

## 1. When to Write an SDD

| Situation | SDD Required? |
|-----------|:------------:|
| New product or platform | ✅ Always |
| Major feature spanning multiple services | ✅ Always |
| Significant vendor/technology evaluation | ✅ Always |
| RFP/SOW response requiring technical approach | ✅ Always |
| Internal refactor with no external impact | ❌ LLD is sufficient |
| Bug fix or configuration change | ❌ No |

**Rule:** An SDD is the umbrella document. It may reference separate HLD, LLD, and ADR documents rather than duplicating them.

---

## 2. SDD vs HLD vs LLD

| Aspect | SDD | HLD | LLD |
|--------|-----|-----|-----|
| **Audience** | All stakeholders (business + technical) | Architects, leads, PMs | Developers, reviewers |
| **Scope** | End-to-end solution (business + technical) | System architecture | Single service/feature |
| **Depth** | Broad: covers requirements, arch, plan, cost, risks | Moderate: logical components | Deep: classes, APIs, schemas |
| **Business Content** | ✅ Extensive | ⚠️ Brief context | ❌ Minimal |
| **Cost Estimate** | ✅ Required | ⚠️ Optional | ❌ No |
| **Timeline/Phasing** | ✅ Required | ⚠️ Optional | ❌ No |

---

## 3. Mandatory SDD Sections

### 3.1 Executive Summary
- 5-7 sentences maximum.
- Business problem, proposed solution, key benefits, estimated cost, timeline.
- A CTO should be able to make a go/no-go decision from this section alone.

### 3.2 Business Context
- Business drivers and strategic objectives.
- Problem statement — what pain exists today?
- Target users/personas with their needs.
- Success metrics — measurable KPIs (e.g., reduce order processing from 4 hours to 15 minutes).
- Business constraints (budget, regulatory, contractual).

### 3.3 Requirements

**Functional Requirements:**

| ID | Requirement | Priority | Source |
|----|-----------|:--------:|--------|
| FR-001 | | Must/Should/Could | |

**Non-Functional Requirements:**

| ID | Category | Requirement | Target |
|----|----------|-----------|--------|
| NFR-001 | Performance | API response time | p95 < 500ms |
| NFR-002 | Availability | System uptime | 99.9% |
| NFR-003 | Security | Data encryption | AES-256 at rest, TLS 1.3 in transit |

### 3.4 Solution Overview
- High-level architecture diagram (C4 Context level).
- Key architectural decisions (with links to ADRs).
- Technology stack with rationale for each choice.
- Integration points with existing systems.

### 3.5 Detailed Architecture
- Reference HLD document if separate, or include HLD content inline.
- Component architecture.
- Data architecture (entities, flows, storage).
- Integration architecture (APIs, events, ETL).
- Security architecture (summary).

### 3.6 Alternatives Considered
- At least 2 alternative approaches evaluated.
- Evaluation criteria and scoring matrix.
- Rationale for the selected approach.
- This section prevents "Why didn't you consider X?" questions later.

### 3.7 Implementation Plan

| Phase | Scope | Duration | Team | Dependencies |
|-------|-------|----------|------|-------------|
| Phase 1 (MVP) | | weeks | people | |
| Phase 2 | | weeks | people | Phase 1 |
| Phase 3 | | weeks | people | Phase 2 |

### 3.8 Cost Estimate

| Category | Monthly | Annual | 3-Year |
|----------|:-------:|:------:|:------:|
| Cloud Infrastructure | | | |
| Software Licenses | | | |
| Development Effort | | | |
| Operations / Support | | | |
| **Total** | | | |

### 3.9 Risk Assessment

| # | Risk | Probability | Impact | Mitigation | Owner |
|---|------|:-----------:|:------:|-----------|-------|
| 1 | | H/M/L | H/M/L | | |

### 3.10 Assumptions & Dependencies
- What is assumed to be true (and what happens if it isn't).
- External dependencies (teams, vendors, infrastructure).
- Timeline dependencies (what must happen first).

### 3.11 Out of Scope
- Explicitly list what this solution does NOT cover.
- Prevents scope creep and sets expectations.

### 3.12 Appendix
- Glossary of terms.
- References to related documents (HLD, LLD, ADRs).
- Detailed data models or API specs (if not in a separate LLD).

---

## 4. SDD Quality Checklist

- [ ] Executive summary is understandable by a non-technical executive
- [ ] Business metrics are specific and measurable
- [ ] Requirements are traceable (each has an ID and source)
- [ ] Architecture diagram shows all external integrations
- [ ] At least 2 alternatives were evaluated
- [ ] Cost estimate covers infrastructure + development + operations
- [ ] Risks have owners and mitigation plans
- [ ] Implementation plan has phases with dependencies
- [ ] Out-of-scope section prevents future arguments

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
