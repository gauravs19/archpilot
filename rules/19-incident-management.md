# Incident Management & Post-Mortem Standards

> **Purpose:** Standards for incident response, escalation, on-call, blameless post-mortems,
> and operational runbooks. Covers the architect's role during and after production incidents —
> essential for hypercare and production support phases.

---

## How to Use This File

- **Incident Setup:** Say to an LLM: *"Using these incident management standards, create an incident response process for: [your organization]"*
- **Post-Mortems:** Use the template to write blameless post-mortems after incidents
- **Runbooks:** Use the runbook template to create per-service operational guides

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [12 — Observability](./12-observability-standards.md) | Alerting that triggers incidents |
| [08 — Cloud Architecture](./08-cloud-architecture.md) | HA/DR patterns that prevent incidents |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | Deployment rollback during incidents |
| [07 — Security Architecture](./07-security-architecture.md) | Security incident response |

---

## 1. Incident Severity Levels

| Severity | Definition | Response Time | Example |
|:--------:|-----------|:------------:|---------|
| **SEV-1** (Critical) | Complete service outage or data loss | 15 minutes | All users cannot checkout |
| **SEV-2** (Major) | Major feature degraded, workaround exists | 30 minutes | Payment failures for 30% of users |
| **SEV-3** (Minor) | Minor feature broken, limited user impact | 4 hours | Search results slightly inaccurate |
| **SEV-4** (Low) | Cosmetic or minimal impact | Next business day | Typo in email template |

**Severity Escalation Rules:**
- If SEV-2 is not resolved within 2 hours → escalate to SEV-1
- If SEV-3 is not resolved within 8 hours → escalate to SEV-2
- Security incidents start at minimum SEV-2

---

## 2. Incident Response Process

### 2.1 Response Flow

```
Alert Fires ──▶ On-Call Acknowledges (15 min SLA)
     │
     ▼
Triage: Severity Assessment
     │
     ├── SEV-1/SEV-2 ──▶ War Room (dedicated channel)
     │                    ├── Incident Commander assigned
     │                    ├── Communicate to stakeholders
     │                    └── Resolve → Post-Mortem (mandatory)
     │
     └── SEV-3/SEV-4 ──▶ On-Call handles directly
                          └── Resolve → Document fix
```

### 2.2 Incident Roles

| Role | Responsibility | Who |
|------|---------------|-----|
| **Incident Commander (IC)** | Coordinates response, makes decisions, manages communication | Senior engineer or architect |
| **Technical Lead** | Investigates root cause, implements fix | Most experienced engineer for affected service |
| **Communications Lead** | Updates stakeholders every 30 min (SEV-1) or 60 min (SEV-2) | Engineering manager or PM |
| **Scribe** | Documents timeline, actions taken, decisions made | Any team member |

### 2.3 During an Incident

| Step | Action | Owner |
|:----:|--------|-------|
| 1 | Acknowledge alert, join incident channel | On-call |
| 2 | Assess severity, assign IC | On-call → IC |
| 3 | Check recent deployments (rollback if suspect) | Tech lead |
| 4 | Check dashboards: errors, latency, dependencies | Tech lead |
| 5 | Communicate initial assessment to stakeholders | Comms lead |
| 6 | Implement fix or workaround | Tech lead |
| 7 | Verify fix in production (monitor for 30 min) | Tech lead |
| 8 | Close incident, update status page | IC |
| 9 | Schedule post-mortem (within 48 hours) | IC |

### 2.4 Communication Templates

**Initial notification (within 15 min):**
```
🔴 INCIDENT: [Title]
Severity: SEV-[X]
Impact: [What users are experiencing]
Status: Investigating
IC: [Name]
Channel: #incident-YYYY-MM-DD
Next update: [Time]
```

**Resolution notification:**
```
✅ RESOLVED: [Title]
Duration: [X hours Y minutes]
Root Cause: [One-line summary]
Impact: [Users affected, transactions failed]
Post-Mortem: Scheduled for [date]
```

---

## 3. On-Call Standards

### 3.1 On-Call Rotation

| Rule | Standard |
|------|---------|
| Rotation period | Weekly, rotating across team |
| Team size for on-call | Minimum 4 people (avoid burnout) |
| Response SLA | Acknowledge alert within 15 minutes |
| Handoff | Written handoff at rotation change (open issues, context) |
| Compensation | Time-off-in-lieu or on-call allowance |
| Escalation | If on-call can't resolve in 30 min, escalate to secondary |

### 3.2 On-Call Toolkit

Every on-call engineer MUST have access to:
- [ ] Production dashboards (Datadog/Grafana)
- [ ] Log aggregation (ELK/CloudWatch)
- [ ] Deployment pipeline (rollback capability)
- [ ] Service runbooks (per-service operational guide)
- [ ] Incident channel (Slack/Teams)
- [ ] PagerDuty/OpsGenie account
- [ ] VPN or bastion access to production
- [ ] Contact list for escalation (phone numbers, not just Slack)

---

## 4. Blameless Post-Mortem

### 4.1 When to Write

| Severity | Post-Mortem Required? |
|:--------:|:--------------------:|
| SEV-1 | ✅ Always, within 48 hours |
| SEV-2 | ✅ Always, within 1 week |
| SEV-3 | ⚠️ If it reveals a systemic issue |
| SEV-4 | ❌ Not required |
| Near-miss | ✅ If it could have been SEV-1/SEV-2 |

### 4.2 Post-Mortem Template

```markdown
# Post-Mortem: [Incident Title]

**Date:** [YYYY-MM-DD]
**Severity:** SEV-[X]
**Duration:** [Start time] → [End time] ([X hours Y minutes])
**Author:** [Name]
**Incident Commander:** [Name]

## Summary
[2-3 sentences: what happened, impact, resolution]

## Impact
- Users affected: [number or percentage]
- Revenue impact: [estimated, if applicable]
- SLA impact: [was SLA breached?]
- Data impact: [any data loss or corruption?]

## Timeline
| Time (IST) | Event |
|-----------|-------|
| 09:00 | Alert: Error rate > 5% |
| 09:05 | On-call acknowledged |
| 09:10 | IC assigned, war room opened |
| 09:15 | Root cause identified: bad deployment |
| 09:20 | Rollback initiated |
| 09:30 | Service restored, monitoring |
| 10:00 | Incident closed |

## Root Cause
[Detailed technical analysis. What actually broke and why?]

## Contributing Factors
- [Factor 1: e.g., Missing validation in deployment pipeline]
- [Factor 2: e.g., No canary deployment for this service]
- [Factor 3: e.g., Alert threshold too high, delayed detection]

## What Went Well
- [e.g., Fast detection due to good alerting]
- [e.g., Rollback was smooth and quick]

## What Went Wrong
- [e.g., No automated canary — went straight to 100% traffic]
- [e.g., Runbook was outdated]

## Action Items
| # | Action | Owner | Priority | Due Date |
|---|--------|-------|:--------:|----------|
| 1 | Add canary deployment for this service | DevOps | High | 2026-03-25 |
| 2 | Update runbook with new DB failover steps | SRE | Medium | 2026-03-20 |
| 3 | Add integration test for the failing scenario | Dev team | High | 2026-03-18 |

## Lessons Learned
[What did we learn that applies beyond this incident?]
```

### 4.3 Post-Mortem Rules

- **Blameless:** Focus on systems and processes, not people
- **Action items are mandatory:** No post-mortem without at least 3 actionable items
- **Action items are tracked:** Added to backlog with owners and deadlines
- **Shared broadly:** Post-mortems are shared with the engineering org (not hidden)
- **Review:** Action items reviewed in next post-mortem retrospective

---

## 5. Operational Runbook Standards

### 5.1 Every Production Service MUST Have

| Section | Content |
|---------|--------|
| **Service Overview** | What the service does, key dependencies |
| **Architecture Diagram** | Component diagram with data flows |
| **Health Check URLs** | Endpoints to verify service is healthy |
| **Key Metrics** | What to monitor, normal ranges, alert thresholds |
| **Common Issues** | Top 5 known issues with resolution steps |
| **Restart Procedure** | How to safely restart the service |
| **Rollback Procedure** | How to rollback to the previous version |
| **Scaling Procedure** | How to scale up/down, auto-scaling config |
| **Database Operations** | Connection strings, migration procedures, backup restore |
| **Dependency Failure** | What happens when each dependency is down |
| **Contacts** | Team Slack channel, on-call rotation, escalation path |

---

## 6. Incident Management Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Blame culture** | People hide incidents, don't report | Blameless post-mortems, celebrate learning |
| **Hero-driven resolution** | One person always fixes things | Knowledge sharing, pair on-call, runbooks |
| **Action items that die** | Post-mortem written, never acted on | Track in backlog, review monthly |
| **Alert fatigue** | 50 alerts/day, all ignored | Tune thresholds, every alert must be actionable |
| **No runbooks** | Every incident is ad-hoc debugging | Mandatory runbook per production service |
| **Post-mortem months later** | Context lost, lessons forgotten | Within 48 hours for SEV-1, 1 week for SEV-2 |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
