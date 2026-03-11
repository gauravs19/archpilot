# Capacity Planning Model

> **Purpose:** Template for forecasting infrastructure capacity needs based on
> business growth projections, traffic patterns, and resource consumption metrics.

---

# Capacity Plan: [System/Service Name]

| Field | Value |
|-------|-------|
| **Date** | [YYYY-MM-DD] |
| **Author** | [Name] |
| **Period** | [Q1 2026 → Q4 2026] |
| **Review Cadence** | Quarterly |

---

## 1. Current Baseline

### 1.1 Traffic Metrics (Current)

| Metric | Current (Avg) | Current (Peak) | Measurement Period |
|--------|:------------:|:--------------:|:-----------------:|
| Requests/second | [e.g., 200] | [e.g., 800] | Last 30 days |
| Daily Active Users (DAU) | [e.g., 25,000] | [e.g., 40,000] | Last 30 days |
| Monthly Active Users (MAU) | [e.g., 150,000] | | Last 3 months |
| API calls/day | [e.g., 5M] | [e.g., 12M] | Last 30 days |
| Data ingestion/day | [e.g., 2 GB] | [e.g., 5 GB] | Last 30 days |

### 1.2 Resource Utilization (Current)

| Resource | Provisioned | Avg Usage | Peak Usage | Headroom |
|----------|:----------:|:---------:|:----------:|:--------:|
| **Compute (CPU)** | [e.g., 16 vCPU] | [e.g., 35%] | [e.g., 70%] | [e.g., 30%] |
| **Compute (Memory)** | [e.g., 32 GB] | [e.g., 50%] | [e.g., 75%] | [e.g., 25%] |
| **Database (CPU)** | [e.g., 8 vCPU] | [e.g., 25%] | [e.g., 60%] | [e.g., 40%] |
| **Database (Storage)** | [e.g., 500 GB] | [e.g., 320 GB] | | [e.g., 36%] |
| **Database (Connections)** | [e.g., 200 max] | [e.g., 45] | [e.g., 120] | [e.g., 40%] |
| **Cache (Memory)** | [e.g., 8 GB] | [e.g., 4.5 GB] | [e.g., 6 GB] | [e.g., 25%] |
| **Storage (S3)** | [Unlimited] | [e.g., 250 GB] | | |
| **Network (egress)** | [e.g., 1 Gbps] | [e.g., 200 Mbps] | [e.g., 600 Mbps] | [e.g., 40%] |

---

## 2. Growth Projections

### 2.1 Business Growth Forecast

| Metric | Current | +3 Months | +6 Months | +12 Months |
|--------|:-------:|:---------:|:---------:|:----------:|
| DAU | [25K] | [35K] | [50K] | [100K] |
| Transactions/day | [10K] | [15K] | [25K] | [50K] |
| Data storage (total) | [320 GB] | [450 GB] | [650 GB] | [1.2 TB] |
| API calls/day | [5M] | [7M] | [12M] | [25M] |

### 2.2 Growth Drivers

| Event | Expected Date | Impact |
|-------|:------------:|--------|
| [e.g., Marketing campaign launch] | [Q2 2026] | +40% traffic for 2 weeks |
| [e.g., New market launch] | [Q3 2026] | +100% DAU sustained |
| [e.g., Mobile app launch] | [Q3 2026] | +60% API calls |
| [e.g., Holiday sale event] | [Q4 2026] | 5x peak vs normal for 48 hours |

---

## 3. Capacity Forecast

### 3.1 Resource Needs by Quarter

| Resource | Current | Q2 2026 | Q3 2026 | Q4 2026 | Action |
|----------|:-------:|:-------:|:-------:|:-------:|--------|
| **Compute (tasks/pods)** | 4 | 6 | 10 | 15 | Auto-scaling config |
| **DB instance** | db.r6g.large | db.r6g.large | db.r6g.xlarge | db.r6g.xlarge | Upsize in Q3 |
| **DB storage** | 500 GB | 500 GB | 1 TB | 1 TB | Enable auto-scaling |
| **Read replicas** | 0 | 1 | 2 | 2 | Add in Q2 |
| **Cache** | 8 GB | 8 GB | 16 GB | 16 GB | Upsize in Q3 |
| **CDN bandwidth** | 500 GB/mo | 700 GB/mo | 1 TB/mo | 2 TB/mo | Auto-scales |

### 3.2 Scaling Triggers

| Trigger | Threshold | Action | Automation |
|---------|:---------:|--------|:----------:|
| CPU > 70% for 5 min | ECS/K8s auto-scale | Add 2 tasks/pods | ✅ Automated |
| DB CPU > 60% for 15 min | Add read replica or upsize | Manual decision | ⚠️ Alert + manual |
| DB storage > 80% | Increase storage | Automated scaling | ✅ Automated |
| Cache memory > 80% | Upsize cache node | Manual decision | ⚠️ Alert + manual |
| API latency p95 > 1s | Investigate + scale | Varies | ⚠️ Alert + manual |

---

## 4. Cost Projection

| Resource | Current $/mo | Q2 $/mo | Q3 $/mo | Q4 $/mo |
|----------|:----------:|:-------:|:-------:|:-------:|
| Compute | | | | |
| Database | | | | |
| Cache | | | | |
| Storage | | | | |
| Networking | | | | |
| Monitoring | | | | |
| **Total** | | | | |

### 4.1 Cost Optimization Opportunities

| Opportunity | Potential Savings | When |
|-------------|:----------------:|------|
| [e.g., Reserved instances for DB] | [e.g., $200/mo] | [Q2] |
| [e.g., Spot instances for batch] | [e.g., $150/mo] | [Q2] |
| [e.g., S3 lifecycle policy] | [e.g., $50/mo] | [Q2] |

---

## 5. Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|---|------|:-----------:|:------:|-----------|
| 1 | Traffic exceeds forecast by 2x | Medium | High | Auto-scaling + load test at 3x |
| 2 | Database hits IOPS limit | Low | High | Monitor IOPS, upgrade path ready |
| 3 | Surprise viral event | Low | Critical | CDN caching, rate limiting, queue buffering |

---

## 6. Review & Sign-Off

| Reviewer | Approved? | Date | Notes |
|----------|:---------:|------|-------|
| [Engineering Lead] | ☐ | | |
| [Finance/FinOps] | ☐ | | |
| [Infrastructure Lead] | ☐ | | |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
