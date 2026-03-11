# Blameless Post-Mortem Template

> **Purpose:** Template for documenting production incidents. Focus on systems
> and processes, not blame. Every SEV-1/SEV-2 incident MUST have a post-mortem.

---

# Post-Mortem: [Incident Title]

| Field | Value |
|-------|-------|
| **Date of Incident** | [YYYY-MM-DD] |
| **Severity** | SEV-[1/2/3] |
| **Duration** | [Start time] → [End time] ([X hours Y minutes]) |
| **Author** | [Name] |
| **Incident Commander** | [Name] |
| **Status** | [Draft | Reviewed | Complete] |

---

## 1. Executive Summary

[2-3 sentences: What happened? What was the impact? How was it resolved?]

---

## 2. Impact

| Dimension | Detail |
|-----------|--------|
| **Users affected** | [Number / percentage of users impacted] |
| **Duration** | [How long were users affected?] |
| **Revenue impact** | [Estimated financial impact, if applicable] |
| **SLA impact** | [Was SLA breached? By how much?] |
| **Data impact** | [Any data loss or corruption?] |
| **Reputational impact** | [Customer complaints, social media, press?] |

---

## 3. Timeline

| Time | Event |
|------|-------|
| [HH:MM] | [First anomaly detected / alert fired] |
| [HH:MM] | [On-call acknowledged] |
| [HH:MM] | [Incident declared, IC assigned] |
| [HH:MM] | [Root cause identified] |
| [HH:MM] | [Fix implemented / rollback initiated] |
| [HH:MM] | [Service restored] |
| [HH:MM] | [Incident closed after monitoring period] |

---

## 4. Root Cause Analysis

### What Happened
[Detailed technical explanation of the root cause. Be specific — "the database connection pool
was exhausted because..." not just "the database was slow."]

### Why It Happened
Use the "5 Whys" technique:

1. **Why** did the service return 500 errors?
   → Because the database connection pool was exhausted.
2. **Why** was the connection pool exhausted?
   → Because a new feature created a long-running transaction per request.
3. **Why** did the long-running transaction happen?
   → Because the N+1 query pattern was not detected in code review.
4. **Why** was it not detected in code review?
   → Because there was no performance test for this endpoint.
5. **Why** was there no performance test?
   → Because the testing strategy didn't cover performance for new endpoints.

**Root Cause:** Missing performance testing in the CI/CD pipeline for new endpoints.

---

## 5. Contributing Factors

- [ ] [Factor 1: e.g., Recent deployment introduced the change]
- [ ] [Factor 2: e.g., No load testing before deployment]
- [ ] [Factor 3: e.g., Alert threshold was too high — late detection]
- [ ] [Factor 4: e.g., Runbook was outdated — delayed resolution]

---

## 6. What Went Well

- [e.g., Alert fired within 2 minutes of the issue starting]
- [e.g., Incident Commander was assigned quickly]
- [e.g., Rollback process worked smoothly]
- [e.g., Team communication was clear and organized]

---

## 7. What Went Wrong

- [e.g., No canary deployment — went straight to 100% of traffic]
- [e.g., Runbook didn't cover this specific failure mode]
- [e.g., External stakeholders were not notified for 45 minutes]
- [e.g., Monitoring dashboard was missing a key metric]

---

## 8. Action Items

| # | Action | Type | Owner | Priority | Due Date | Status |
|---|--------|:----:|-------|:--------:|----------|:------:|
| 1 | [e.g., Add load test for checkout endpoint] | Prevention | [Name] | High | [Date] | ⬜ |
| 2 | [e.g., Add canary deployment for this service] | Prevention | [Name] | High | [Date] | ⬜ |
| 3 | [e.g., Update runbook with DB connection pool troubleshooting] | Process | [Name] | Medium | [Date] | ⬜ |
| 4 | [e.g., Add alert for DB connection pool utilization > 70%] | Detection | [Name] | High | [Date] | ⬜ |
| 5 | [e.g., Review code review checklist for performance items] | Process | [Name] | Medium | [Date] | ⬜ |

**Action Item Rules:**
- Minimum 3 action items per post-mortem
- Each action item MUST have an owner and due date
- Action items are tracked in the backlog (not just this document)
- Review completion in the next post-mortem retrospective

---

## 9. Lessons Learned

[What broader lessons can we take from this incident? What would we tell our future selves?]

---

## 10. Appendix

### Related Links
- [Incident channel link]
- [Dashboard screenshot during incident]
- [Relevant ADRs or design decisions]
- [Previous related incidents]

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
