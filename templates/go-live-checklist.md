# Go-Live Readiness Checklist

> **Purpose:** Comprehensive pre-launch verification checklist. Every item must be verified
> before a system goes to production. Feed this to an LLM with your system details
> to get a customized go-live assessment.

---

## Instructions

For each item, mark:
- ✅ **Done** — Verified and complete
- ⚠️ **Partial** — In progress or with exceptions (document exception)
- ❌ **Not Done** — Missing, needs action before go-live
- N/A — Not applicable (with justification)

---

## 1. Infrastructure & Environment

- [ ] Production environment provisioned via IaC (Terraform/CDK)
- [ ] Multi-AZ deployment for all critical services
- [ ] Auto-scaling configured and tested (min/max/target)
- [ ] DNS records configured (A/CNAME, TTL appropriate)
- [ ] SSL/TLS certificates installed and auto-renewal configured
- [ ] CDN configured for static assets
- [ ] VPC, subnets, security groups follow standards
- [ ] Databases not publicly accessible
- [ ] Environment variables and config verified for production values
- [ ] Resource tagging complete (environment, service, team, cost-center)

## 2. Security

- [ ] All endpoints require authentication (unless explicitly public)
- [ ] RBAC/ABAC configured and tested for all user roles
- [ ] WAF rules configured and enabled
- [ ] Security headers set (HSTS, X-Content-Type, X-Frame-Options, CSP)
- [ ] Secrets stored in secrets manager (not in code, env vars, or config files)
- [ ] API keys, tokens, credentials rotated from dev/staging values
- [ ] Dependency vulnerability scan clean (no critical/high)
- [ ] Rate limiting configured on all public endpoints
- [ ] CORS configured restrictively (specific origins, not *)
- [ ] PII encryption at rest verified
- [ ] Penetration test completed (or scheduled within 30 days)
- [ ] Security incident response plan documented

## 3. Data

- [ ] Database migrations applied successfully in production
- [ ] Backup strategy configured and first backup verified
- [ ] Backup restoration tested successfully
- [ ] Data retention policies configured
- [ ] PII fields identified and masking applied in logs/non-prod
- [ ] RPO and RTO documented and achievable
- [ ] Data replication (multi-AZ) verified
- [ ] Seed/reference data loaded

## 4. Monitoring & Observability

- [ ] Structured logging configured (JSON, not plain text)
- [ ] Log aggregation working (ELK/CloudWatch/Datadog)
- [ ] Key metrics exposed (request rate, error rate, latency)
- [ ] Dashboards created (service health, business KPIs)
- [ ] Alert rules configured with severity levels
- [ ] Alert notification channels set (Slack, PagerDuty, email)
- [ ] Distributed tracing enabled across services
- [ ] Health check endpoints responding (/health, /ready)
- [ ] Uptime monitoring configured (external ping)
- [ ] Log retention settings verified

## 5. Testing

- [ ] Unit tests passing (≥ 80% coverage)
- [ ] Integration tests passing
- [ ] Contract tests passing (all inter-service APIs)
- [ ] UAT sign-off from product owner/business
- [ ] Performance/load test completed (meets NFR targets)
- [ ] Security scan clean (SAST, DAST)
- [ ] Smoke tests automated for post-deployment verification
- [ ] Rollback tested and documented

## 6. Deployment

- [ ] CI/CD pipeline tested end-to-end (build → test → deploy → verify)
- [ ] Deployment strategy configured (blue-green, canary, rolling)
- [ ] Rollback procedure documented and tested
- [ ] Feature flags configured for new features
- [ ] Database migration runs before application deployment
- [ ] Deployment runbook documented

## 7. Operations

- [ ] On-call rotation set up with at least 4 people
- [ ] Service runbook created for each production service
- [ ] Escalation path documented (on-call → team lead → manager → VP)
- [ ] Incident response process documented
- [ ] Post-mortem template ready
- [ ] Support channel created (internal + external if user-facing)
- [ ] Contact list for all external dependencies (vendors, partners)

## 8. Documentation

- [ ] API documentation (OpenAPI/Swagger) published
- [ ] Architecture decision records (ADRs) for key decisions
- [ ] HLD and LLD documents up to date
- [ ] Run book for operations team
- [ ] User documentation / help guides (if user-facing)
- [ ] known issues / limitations documented

## 9. Business & Compliance

- [ ] Legal/compliance approval for data handling
- [ ] Privacy policy updated (if user-facing)
- [ ] Terms of service updated (if applicable)
- [ ] Data residency verified (correct cloud region)
- [ ] Regulatory requirements met (PCI, GDPR, HIPAA as applicable)
- [ ] Business stakeholder sign-off obtained
- [ ] Go-live date communicated to all stakeholders

## 10. Rollout Plan

- [ ] Rollout strategy defined (% of users, geography, time)
- [ ] Rollback criteria defined (error rate > X%, latency > Y)
- [ ] First 30-minute monitoring plan documented
- [ ] First 24-hour watch plan (who monitors what)
- [ ] Success criteria defined (business metrics to track)
- [ ] Hypercare period defined (duration, team, SLA)

---

## Summary

| Category | Total | ✅ Done | ⚠️ Partial | ❌ Not Done |
|----------|:-----:|:------:|:---------:|:---------:|
| Infrastructure | 10 | | | |
| Security | 12 | | | |
| Data | 8 | | | |
| Monitoring | 10 | | | |
| Testing | 8 | | | |
| Deployment | 6 | | | |
| Operations | 7 | | | |
| Documentation | 6 | | | |
| Business | 7 | | | |
| Rollout | 6 | | | |
| **TOTAL** | **80** | | | |

**Go/No-Go Decision:**
- All ❌ items must be resolved OR have an approved exception
- All ⚠️ items must have a remediation plan with timeline
- Minimum 90% ✅ for go-live approval

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
