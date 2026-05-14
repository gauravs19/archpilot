# Sustainability & Green Architecture Standards

> **Purpose:** This rule file defines standards for designing carbon-aware, energy-efficient
> software systems. As cloud infrastructure becomes a significant source of enterprise carbon
> emissions, sustainability must be treated as a first-class architectural attribute — alongside
> performance, security, and cost.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Cloud efficiency principles |
| [14 — Cost Optimization](./14-cost-optimization.md) | GreenOps extends FinOps |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | Green CI/CD pipeline practices |
| [11 — NFR Checklist](./11-nfr-checklist.md) | Carbon efficiency as an NFR |

---

## 1. Why Green Architecture?

| Fact | Implication |
|------|------------|
| Data centers consume ~1–2% of global electricity | Architecture decisions directly affect carbon output |
| Cloud workloads can be 30–90% over-provisioned | Right-sizing is both a cost and sustainability win |
| AI/ML training runs can emit as much CO2 as 5 cars over their lifetime | AI architecture needs carbon budgets |
| Carbon-aware scheduling can reduce emissions 30–70% with zero quality loss | Time-shifting workloads is free sustainability |
| Regulators (EU CSRD, SEC) are mandating carbon reporting | Sustainability is becoming a compliance requirement |

---

## 2. Green Architecture Principles

### 2.1 Carbon Efficiency First

- **Measure before optimizing:** Establish a carbon baseline (kgCO2e per 1000 requests) before optimization
- **Carbon as an NFR:** Every new system MUST have a carbon efficiency target in its NFR section
- **Carbon ? cost:** Optimize for carbon, not just cost (sometimes they diverge — carbon wins)

### 2.2 Energy Proportionality

- Systems SHOULD consume energy proportional to their workload — minimal energy when idle
- Scale to zero for non-critical workloads (serverless, scale-to-zero containers)
- Prefer event-driven over polling (polling consumes energy even when there is no work)

### 2.3 Hardware Efficiency

- Higher utilization of fewer machines is greener than spreading across many underutilized machines
- Newer hardware generations are typically more energy-efficient per unit of compute
- ARM-based instances (AWS Graviton, Azure Ampere) provide 20–40% better performance-per-watt than x86

---

## 3. Carbon Measurement

### 3.1 Key Carbon Metrics

| Metric | Definition | Tool |
|--------|-----------|------|
| **SCI Score** (Software Carbon Intensity) | CO2e per functional unit (request, user, transaction) | Green Software Foundation SCI spec |
| **Carbon per request** | gCO2e / 1000 API requests | Cloud Carbon Footprint, AWS CCF |
| **PUE** (Power Usage Effectiveness) | Total facility power / IT equipment power | Cloud provider transparency reports |
| **CUE** (Carbon Usage Effectiveness) | Carbon emissions / IT equipment power | Data center reporting |
| **Embodied carbon** | CO2e from hardware manufacturing | Boavizta API, manufacturer data |

### 3.2 SCI Formula

```
SCI = (E × I) + M per [R]

Where:
  E = Energy consumed by software (kWh)
  I = Location-based marginal carbon intensity (gCO2e/kWh) 
  M = Embodied emissions from hardware
  R = Functional unit (1000 API requests / 1 user / 1 transaction)
```

**Rule:** Every system with >$1,000/month cloud spend MUST have a documented SCI baseline.

---

## 4. Carbon-Aware Design Patterns

### 4.1 Demand Shaping

Move workloads to when and where electricity is cleanest:

| Pattern | Description | When to Use |
|---------|------------|------------|
| **Time-shifting** | Defer batch jobs to hours of low carbon intensity (e.g., solar peak, night) | All non-real-time batch jobs |
| **Geographic routing** | Route requests to cloud regions with lower carbon intensity | Globally distributed apps |
| **Carbon-aware scheduling** | Use Grid Intensity APIs to pause workloads during high-carbon periods | ML training, data processing |
| **Demand smoothing** | Reduce burst behavior (queue instead of spike) | Event-driven systems |

**Tool:** [Electricity Maps API](https://api.electricitymap.org) or [WattTime API](https://www.watttime.org) for real-time grid carbon intensity.

### 4.2 Right-Sizing & Efficiency

| Practice | Carbon Saving Potential |
|---------|:----------------------:|
| Scale to zero (serverless/idle) | Up to 80% for bursty workloads |
| ARM instances (Graviton) | 20–40% compute efficiency gain |
| Container packing (bin packing) | 30–50% resource utilization improvement |
| Eliminate zombie resources | 100% (zero work = zero carbon) |
| Compress data transfers | 20–60% egress energy reduction |
| HTTP/3 + efficient protocols | 10–30% network energy reduction |
| Database connection pooling | 15–25% DB energy reduction |

### 4.3 Green CI/CD

- **Build only what changed:** Incremental builds, dependency caching
- **Parallelize safely:** Maximize CI runner utilization
- **Prune environments:** Tear down ephemeral environments when not in use
- **Schedule heavy scans off-peak:** SAST, dependency scans ? off-peak CI
- **Artifact retention:** Delete old build artifacts; do not store indefinitely

### 4.4 Data Efficiency

- Compress data at rest and in transit (Zstd, Brotli, LZ4 for different trade-offs)
- Use columnar formats (Parquet, ORC) for analytical data — 5–10× smaller than row formats
- Implement data tiering: hot ? warm ? cold ? archive (S3 Glacier, Azure Cool)
- Set retention policies: delete data that is no longer needed (carbon and cost)
- Avoid redundant data copies: single source of truth via data contracts

---

## 5. Green NFRs

Add these NFRs to systems with significant scale or sustainability commitments:

| NFR ID | Category | Requirement | Target |
|--------|---------|------------|:------:|
| GNFR-001 | Carbon Efficiency | SCI score | =X gCO2e/1000 requests |
| GNFR-002 | Energy Proportionality | CPU utilization at idle | <5% |
| GNFR-003 | Idle scaling | Scale to zero when idle for | >15 minutes |
| GNFR-004 | ARM compute | % of workloads on ARM (Graviton) | >60% |
| GNFR-005 | Data compression | Compression ratio for cold data | >5:1 |
| GNFR-006 | Batch scheduling | Batch jobs scheduled during low-carbon window | 100% |

---

## 6. GreenOps Governance

### 6.1 Carbon Tagging

All cloud resources MUST be tagged with:
```
carbon:team    = [team-name]
carbon:product = [product-name]
carbon:env     = [prod | staging | dev]
carbon:workload-type = [real-time | batch | ml-training | analytics]
```

### 6.2 Carbon Budgets

Similar to FinOps cost budgets:
- Each product team has a **carbon budget** (kgCO2e/month)
- Carbon budget reviewed quarterly alongside cost budget
- Systems exceeding carbon budget trigger architecture review

### 6.3 Carbon Reporting

Minimum reporting cadence: quarterly
Report MUST include:
- SCI score trend (vs baseline)
- Top 3 carbon-intensive resources
- Actions taken this quarter
- Target for next quarter

---

## 7. Green Architecture Anti-Patterns

| Anti-Pattern | Carbon Impact | Fix |
|-------------|:------------:|-----|
| Always-on batch jobs (no schedule) | High | Carbon-aware scheduling |
| 5% CPU utilization in production | Very High | Right-size or consolidate |
| Polling every second (nothing to process) | High | Event-driven trigger |
| Duplicate data copies (5 teams, 5 copies) | Medium | Shared data lake with contracts |
| No data retention policy | Medium | Auto-expire cold data |
| x86 when Graviton available | Medium | Migrate to ARM instances |
| Store logs forever | Medium | 90-day hot, archive or delete thereafter |
| Test environments running 24/7 | High | Schedule off and scale to zero |

---

## 8. Green Architecture Checklist

- [ ] SCI baseline documented for systems with >$1K/month cloud spend
- [ ] Carbon efficiency NFR included in system NFR table
- [ ] Batch/ETL jobs scheduled during low grid intensity windows
- [ ] Scale-to-zero configured for non-real-time workloads
- [ ] ARM instances used where available (>60% target)
- [ ] Data retention policies set for all storage (cold/archive tiers)
- [ ] Data compressed at rest (Parquet/columnar for analytics)
- [ ] Carbon resource tagging applied to all cloud resources
- [ ] Carbon budget defined and monitored quarterly
- [ ] Zombie resource detection in place (auto-alert on <5% CPU for >7 days)

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
