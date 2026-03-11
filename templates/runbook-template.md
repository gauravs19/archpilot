# Operational Runbook Template

> **Purpose:** Template for creating per-service operational runbooks. Every production
> service MUST have a runbook accessible to on-call engineers.

---

## Service: [Service Name]

| Field | Value |
|-------|-------|
| **Owner Team** | [Team Name] |
| **On-Call Rotation** | [PagerDuty/OpsGenie schedule link] |
| **Slack Channel** | [#team-channel] |
| **Repository** | [GitHub/GitLab link] |
| **Dashboard** | [Datadog/Grafana link] |
| **Last Updated** | [YYYY-MM-DD] |

---

## 1. Service Overview

### What This Service Does
[2-3 sentences describing the service's business purpose]

### Key Dependencies

| Dependency | Type | Impact if Down |
|-----------|------|---------------|
| [e.g., PostgreSQL RDS] | Database | Service cannot read/write data |
| [e.g., Redis ElastiCache] | Cache | Degraded performance, higher DB load |
| [e.g., Payment Gateway API] | External | Payments fail, orders queued |
| [e.g., SQS Order Queue] | Messaging | Event processing stops |

### Architecture Diagram
[Embed or link to service architecture diagram]

---

## 2. Health Checks

| Endpoint | Expected Response | What It Checks |
|----------|:-----------------:|---------------|
| `GET /health` | 200 OK | Service is running |
| `GET /ready` | 200 OK | All dependencies connected |
| `GET /metrics` | 200 OK | Prometheus metrics exposed |

---

## 3. Key Metrics & Alerts

| Metric | Normal Range | Alert Threshold | Dashboard Link |
|--------|:-----------:|:---------------:|:-------------:|
| Request rate | 100-500 req/s | < 10 req/s (unexpected drop) | [link] |
| Error rate | < 0.5% | > 5% for 5 min | [link] |
| p95 latency | < 300ms | > 2000ms for 10 min | [link] |
| DB connection pool | < 50% utilized | > 80% for 5 min | [link] |
| Queue depth | < 100 messages | > 1000 for 5 min | [link] |
| Memory usage | < 70% | > 85% for 10 min | [link] |
| CPU usage | < 50% | > 80% for 10 min | [link] |

---

## 4. Common Issues & Resolution

### Issue 1: [High Error Rate]
**Symptoms:** Error rate > 5%, 5xx responses increasing
**Possible Causes:**
1. Bad deployment → Check recent deployments, rollback if needed
2. Database connection exhaustion → Check connection pool metrics
3. Downstream dependency failure → Check dependency health

**Resolution Steps:**
```
1. Check dashboard: [link]
2. Check recent deployments: git log -5 --oneline
3. If recent deploy → rollback: [rollback command/link]
4. If DB issue → restart connection pool: [command]
5. If dependency issue → check circuit breaker state
```

### Issue 2: [High Latency]
**Symptoms:** p95 latency > 2 seconds
**Possible Causes:**
1. Slow database queries → Check slow query log
2. Cache miss storm → Check Redis hit rate
3. Resource contention → Check CPU/memory

**Resolution Steps:**
```
1. Check slow query dashboard: [link]
2. Check Redis cache hit rate: [link]
3. If cache storm → verify cache is not expired/cleared
4. If resource → scale up: [auto-scaling or manual command]
```

### Issue 3: [Service Not Starting]
**Symptoms:** Health check failing, pods in CrashLoopBackOff
**Resolution Steps:**
```
1. Check logs: kubectl logs -f deployment/[service-name]
2. Common causes:
   - DB migration failed → check migration logs
   - Missing env vars → check config/secrets
   - Port conflict → check service definition
3. If migration issue → fix migration, redeploy
4. If config issue → verify secrets in [secrets manager link]
```

---

## 5. Restart Procedure

```bash
# ECS
aws ecs update-service --cluster [cluster] --service [service] --force-new-deployment

# Kubernetes
kubectl rollout restart deployment/[service-name] -n [namespace]

# Verify
kubectl get pods -n [namespace] -w
# Wait for all pods to be Running and Ready
```

**Post-restart checks:**
- [ ] Health check returns 200
- [ ] Error rate back to normal
- [ ] No data corruption (check recent transactions)

---

## 6. Rollback Procedure

```bash
# Get previous version
kubectl rollout history deployment/[service-name] -n [namespace]

# Rollback to previous version
kubectl rollout undo deployment/[service-name] -n [namespace]

# Verify rollback
kubectl rollout status deployment/[service-name] -n [namespace]
```

**Database rollback (if migration involved):**
```bash
# Check current migration version
flyway info

# Rollback last migration
flyway undo
```

---

## 7. Scaling Procedure

### Auto-scaling Configuration
| Parameter | Value |
|-----------|-------|
| Min replicas | [e.g., 2] |
| Max replicas | [e.g., 20] |
| Target CPU | [e.g., 60%] |
| Scale-up cooldown | [e.g., 3 min] |
| Scale-down cooldown | [e.g., 10 min] |

### Manual scaling (emergency)
```bash
kubectl scale deployment/[service-name] --replicas=[N] -n [namespace]
```

---

## 8. Database Operations

| Operation | Command/Procedure |
|-----------|-------------------|
| Connection string | `[Secrets Manager ARN or reference]` |
| Read replica | `[endpoint]` |
| Run migration | `flyway migrate` via CI/CD |
| Backup schedule | Daily at 02:00 UTC, retained 30 days |
| Restore from backup | `aws rds restore-db-instance-from-db-snapshot` |
| Manual query access | Bastion host → `psql -h [host] -U [user] -d [db]` |

---

## 9. Contacts & Escalation

| Level | Contact | Response Time |
|-------|---------|:------------:|
| **L1 — On-Call** | [PagerDuty rotation] | 15 min |
| **L2 — Team Lead** | [Name, phone, Slack] | 30 min |
| **L3 — Engineering Manager** | [Name, phone, Slack] | 1 hour |
| **L4 — VP Engineering** | [Name, phone] | 2 hours |
| **External — [Vendor]** | [Support email/phone, ticket portal] | Per SLA |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
