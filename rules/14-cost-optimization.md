# Cost Optimization Standards (FinOps)

> **Purpose:** Standards for cost-aware architecture, TCO modeling, right-sizing, and
> ongoing cost governance. Ensures every design considers financial impact as a
> first-class architectural attribute.

---

## How to Use This File

- **Claude Projects:** Upload for cloud cost estimation and optimization reviews
- **Any LLM:** Say: *"Using these FinOps standards, estimate the TCO for: [your architecture]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Compute, storage, and networking choices |
| [00 — Architecture Principles](./00-architecture-principles.md) | FinOps Principles (§8) expanded here |
| [03 — HLD Standards](./03-hld-standards.md) | Cost estimate section of HLD |
| [01 — Solution Design](./01-solution-design.md) | TCO section (§3.8) of SDD |

---

## 1. FinOps Principles

### 1.1 Core Rules
- **Cost is an architecture attribute** — equal to performance, security, and reliability.
- **Everyone is accountable** — engineers own the cost of what they build.
- **Decisions are data-driven** — measure before optimizing.
- **Start cheap, scale smart** — begin with the smallest viable resource, scale based on metrics.
- **Managed over self-hosted** — unless self-hosted saves >40% at scale.

---

## 2. Cloud Cost Estimation Framework

### 2.1 TCO Model Template

| Category | Service | Monthly | Annual | 3-Year |
|----------|---------|:-------:|:------:|:------:|
| **Compute** | EKS/ECS/Lambda | | | |
| **Database** | RDS/DynamoDB/Aurora | | | |
| **Cache** | ElastiCache/Redis | | | |
| **Storage** | S3/EBS/EFS | | | |
| **Networking** | Data transfer, NAT GW, LB | | | |
| **CDN** | CloudFront/Fastly | | | |
| **Messaging** | SQS/SNS/Kafka | | | |
| **Monitoring** | CloudWatch/Datadog | | | |
| **Security** | WAF, KMS, Secrets Manager | | | |
| **CI/CD** | CodePipeline/GitHub Actions | | | |
| **Support** | Enterprise support plan | | | |
| **Total** | | | | |

### 2.2 Hidden Cost Checklist
Costs that architects commonly miss:

- [ ] **Data transfer costs** — cross-AZ, cross-region, NAT Gateway, internet egress
- [ ] **NAT Gateway charges** — $0.045/GB processed (can exceed compute costs)
- [ ] **CloudWatch/logging costs** — log ingestion + storage
- [ ] **Monitoring tool licensing** — Datadog, New Relic per-host fees
- [ ] **SSL certificate management** — ACM is free on AWS, paid on others
- [ ] **DNS query costs** — Route53 charges per million queries
- [ ] **Idle/unused resources** — unattached EBS volumes, idle load balancers
- [ ] **Over-provisioned databases** — RDS instances running at 10% CPU
- [ ] **License costs** — commercial databases, enterprise middleware
- [ ] **Staffing/training** — ops cost of running complex infrastructure

---

## 3. Right-Sizing Rules

### 3.1 Compute Right-Sizing

| Signal | Action |
|--------|--------|
| CPU consistently < 20% | Downsize instance type |
| CPU consistently > 70% | Upsize or add auto-scaling |
| Memory consistently < 30% | Switch to compute-optimized |
| Memory consistently > 80% | Switch to memory-optimized |
| Highly variable traffic | Use auto-scaling, not large fixed instances |
| Predictable off-hours drop | Schedule scale-down (nights, weekends) |

### 3.2 Database Right-Sizing

| Signal | Action |
|--------|--------|
| CPU < 15%, memory < 30% | Downsize instance class |
| Storage growing < 1%/month | Reduce allocated storage (or use auto-scaling) |
| Read replicas at < 5% CPU | Remove unnecessary replicas |
| Connection pool rarely > 50% | Reduce max connections |

### 3.3 Pricing Model Selection

| Model | Savings | Commitment | Use When |
|-------|:-------:|:----------:|----------|
| **On-Demand** | 0% | None | Unpredictable, short-term, experimentation |
| **Reserved (1yr)** | 30-40% | 1 year | Steady-state production workloads |
| **Reserved (3yr)** | 50-60% | 3 years | Long-term stable workloads |
| **Savings Plans** | 30-40% | 1-3 years | Flexible across instance types |
| **Spot Instances** | 60-90% | None (can be reclaimed) | Batch processing, stateless workers, CI/CD |

**Default Strategy:**
- Production (steady): Reserved Instances or Savings Plans
- Production (variable): On-Demand with auto-scaling
- Non-production: Spot instances + scheduled shutdown
- CI/CD: Spot instances

---

## 4. Cost-Saving Architecture Patterns

### 4.1 Caching to Reduce Compute/DB Costs
```
Request → [CDN Cache] → [API Gateway Cache] → [Application Cache (Redis)] → [Database]
```
- CDN: Static assets, cacheable API responses → saves compute + bandwidth
- Redis: Frequent DB reads → saves database compute
- Application: Computed/aggregated data → saves processing time

### 4.2 Async Processing to Reduce Compute Costs
- Move non-real-time work off the critical path to queues.
- Process in batch during off-peak hours (cheaper spot instances).
- Example: Email sending, report generation, image processing.

### 4.3 Tiered Storage
| Tier | Storage | Use For | Cost |
|------|---------|---------|:----:|
| Hot | SSD/EBS gp3 | Active data, recent records | $$$ |
| Warm | S3 Standard | Archived data, accessed occasionally | $$ |
| Cold | S3 Glacier | Compliance archives, rarely accessed | $ |
| Frozen | S3 Glacier Deep Archive | Legal hold, 7+ year retention | ¢ |

### 4.4 Serverless for Low-Traffic Workloads
- Lambda/Cloud Functions: $0 when idle. Perfect for <1000 requests/day.
- API Gateway + Lambda: No fixed infrastructure cost.
- Break-even vs containers: ~1M requests/month (above this, containers are cheaper).

---

## 5. Cost Governance

### 5.1 Tagging Strategy (Mandatory)

| Tag | Purpose | Example |
|-----|---------|---------|
| `environment` | Cost by environment | `production`, `staging`, `dev` |
| `service` | Cost by service | `order-service`, `payment-service` |
| `team` | Cost by team | `platform`, `payments`, `growth` |
| `cost-center` | Finance attribution | `CC-12345` |
| `managed-by` | IaC tool tracking | `terraform`, `manual` |
| `auto-shutdown` | Non-prod scheduling | `true`, `false` |

### 5.2 Budget Alerts

| Threshold | Action |
|:---------:|--------|
| 50% of monthly budget | Informational notification to team |
| 80% of monthly budget | Warning notification to team + manager |
| 100% of monthly budget | Alert to team + manager + finance |
| 120% of monthly budget | Escalation to VP/CTO |

### 5.3 Cost Review Cadence

| Frequency | What | Who |
|-----------|------|-----|
| Weekly | Anomaly detection, spot checks | Engineering team |
| Monthly | Cost vs budget review, optimization actions | Team leads + finance |
| Quarterly | Architecture cost review, right-sizing, reservation planning | Architects + finance |

---

## 6. Cost Anti-Patterns

| Anti-Pattern | Impact | Fix |
|-------------|--------|-----|
| **Running dev/staging 24/7** | 70% waste outside business hours | Schedule shutdown (nights, weekends) |
| **On-demand for steady workloads** | Paying 40-60% more than necessary | Use reserved instances / savings plans |
| **No data transfer awareness** | Silently expensive cross-AZ/region traffic | Minimize cross-AZ calls, use VPC endpoints |
| **Over-provisioned "just in case"** | Paying for idle capacity | Auto-scaling, start small |
| **Monitoring tool sprawl** | Multiple paid tools doing the same thing | Consolidate to 1-2 tools |
| **No expiration on temporary resources** | Forgotten test instances running for months | TTL tags, automated cleanup |
| **Large EBS volumes "because disk is cheap"** | IOPS and snapshots cost more than storage | Right-size, use S3 for cold data |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
