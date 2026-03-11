# Cloud Architecture Standards

> **Purpose:** Cloud-native design standards covering multi-cloud patterns, IaC,
> compute selection, networking, and Well-Architected Framework alignment.

---

## 1. Cloud-Native Design Principles

### 1.1 The Twelve-Factor App (Mandatory)

| Factor | Rule |
|--------|------|
| 1. **Codebase** | One codebase per service, tracked in version control |
| 2. **Dependencies** | Explicitly declare and isolate all dependencies |
| 3. **Config** | Store config in environment (not in code) |
| 4. **Backing Services** | Treat databases, caches, queues as attached resources |
| 5. **Build, Release, Run** | Strictly separate build, release, and run stages |
| 6. **Processes** | Execute as stateless processes — no sticky sessions |
| 7. **Port Binding** | Export services via port binding (self-contained) |
| 8. **Concurrency** | Scale out via the process model (horizontal scaling) |
| 9. **Disposability** | Fast startup, graceful shutdown — services are disposable |
| 10. **Dev/Prod Parity** | Keep development, staging, and production as similar as possible |
| 11. **Logs** | Treat logs as event streams (stdout, not files) |
| 12. **Admin Processes** | Run admin/management tasks as one-off processes |

---

## 2. Compute Selection Framework

| Workload | Default Choice | Alternative | When to Reconsider |
|----------|---------------|-------------|-------------------|
| **Web API (steady traffic)** | Containers (ECS/EKS/GKE) | VMs (EC2/GCE) | Simple apps, cost-sensitive |
| **Web API (spiky traffic)** | Serverless (Lambda/Cloud Functions) | Containers with auto-scaling | Cold start is acceptable |
| **Background processing** | Serverless or containers | Batch (AWS Batch) | Long-running jobs (>15 min) |
| **Scheduled jobs** | Serverless + EventBridge/Scheduler | Containers + cron | Simple scheduling needs |
| **ML inference** | Serverless (SageMaker/Vertex) | GPU containers | High-throughput inference |
| **Real-time streaming** | Containers | Serverless (Kinesis Data Analytics) | Stateful stream processing |

### 2.1 Container vs Serverless Decision

```
Is the workload...
├── Stateless, event-driven, <15 min execution? → Serverless
├── Steady-state, always-on, predictable traffic? → Containers
├── Need GPU, custom runtime, or long execution? → Containers/VMs
└── Minimal traffic (<1000 req/day)? → Serverless (cost wins)
```

---

## 3. Infrastructure as Code (IaC)

### 3.1 IaC Tool Selection

| Tool | Best For |
|------|---------|
| **Terraform** | Multi-cloud, infrastructure provisioning |
| **Pulumi** | Multi-cloud, developers who prefer real programming languages |
| **AWS CDK** | AWS-only, TypeScript/Python developers |
| **CloudFormation** | AWS-only, native integration |
| **Bicep** | Azure-only |

### 3.2 IaC Standards

| Rule | Standard |
|------|---------|
| All infrastructure in code | ZERO manual console changes in staging/production |
| Version controlled | Same repo as application, or dedicated infra repo |
| Code reviewed | Infrastructure PRs reviewed like application PRs |
| Environment parity | Same IaC modules for dev, staging, production (parameterized) |
| State management | Remote state backend (S3+DynamoDB, Terraform Cloud) — NEVER local state |
| Modular | Reusable modules for common patterns (VPC, ECS cluster, RDS) |
| Secrets | NEVER in IaC files — reference secrets manager by ARN/ID |
| Tagging | ALL resources tagged: `environment`, `service`, `team`, `cost-center` |
| Drift detection | Automated drift detection in CI/CD |

---

## 4. Networking Architecture

### 4.1 VPC Design

```
┌─────────────────────────────────────────────┐
│                    VPC                       │
│  CIDR: 10.0.0.0/16                          │
│                                             │
│  ┌──────────────┐  ┌──────────────┐         │
│  │Public Subnet │  │Public Subnet │  AZ-a/b │
│  │ 10.0.1.0/24  │  │ 10.0.2.0/24  │         │
│  │ [ALB, NAT]   │  │ [ALB, NAT]   │         │
│  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │
│  ┌──────▼───────┐  ┌──────▼───────┐         │
│  │Private Subnet│  │Private Subnet│  AZ-a/b │
│  │ 10.0.10.0/24 │  │ 10.0.20.0/24 │         │
│  │ [App Servers] │  │ [App Servers] │         │
│  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                  │
│  ┌──────▼───────┐  ┌──────▼───────┐         │
│  │Data Subnet   │  │Data Subnet   │  AZ-a/b │
│  │ 10.0.100.0/24│  │ 10.0.200.0/24│         │
│  │ [RDS, Redis] │  │ [RDS, Redis] │         │
│  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────┘
```

**Rules:**
- Multi-AZ deployment for ALL production workloads.
- Databases and caches in private/data subnets — NEVER public.
- NAT Gateway for outbound internet from private subnets.
- Security groups: least privilege, no `0.0.0.0/0` ingress (except ALB port 443).
- VPC Flow Logs enabled for all production VPCs.

### 4.2 DNS Strategy
- Use Route53/Cloud DNS for service discovery in the cloud.
- Internal DNS for service-to-service communication (e.g., `order-service.internal.example.com`).
- External DNS for customer-facing endpoints with latency-based or geolocation routing.

---

## 5. High Availability & Disaster Recovery

### 5.1 Availability Tiers

| Tier | Availability | Downtime/Year | Pattern | Cost |
|------|:-----------:|:-------------:|---------|:----:|
| Tier 1 | 99.0% | 3.65 days | Single-AZ | $ |
| Tier 2 | 99.9% | 8.76 hours | Multi-AZ | $$ |
| Tier 3 | 99.95% | 4.38 hours | Multi-AZ + automated failover | $$$ |
| Tier 4 | 99.99% | 52.6 minutes | Multi-Region active-passive | $$$$ |
| Tier 5 | 99.999% | 5.26 minutes | Multi-Region active-active | $$$$$ |

**Rule:** Default to Tier 2 (multi-AZ, 99.9%). Justify higher tiers with business impact analysis.

### 5.2 DR Strategy

| Strategy | RPO | RTO | Cost | Use When |
|----------|:---:|:---:|:----:|----------|
| **Backup & Restore** | Hours | Hours | $ | Non-critical systems |
| **Pilot Light** | Minutes | 30-60 min | $$ | Moderate criticality |
| **Warm Standby** | Seconds | Minutes | $$$ | Business-critical |
| **Multi-Region Active-Active** | Zero | Zero | $$$$ | Mission-critical (finance, healthcare) |

---

## 6. Multi-Cloud Considerations

### 6.1 When Multi-Cloud Makes Sense
- ✅ Regulatory requirement (data residency in regions where one cloud is absent).
- ✅ Avoiding vendor lock-in for strategic reasons (government contracts).
- ✅ Acquisitions brought different cloud stacks.
- ❌ "Just because" — the operational overhead of multi-cloud is significant.

### 6.2 Portability Layer
If multi-cloud is required:
- Use Kubernetes as the compute abstraction.
- Use Terraform for infrastructure provisioning.
- Avoid cloud-specific managed services for core business logic.
- Use cloud-specific services for commodity features (CDN, DNS, monitoring).

---

## 7. Cloud Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Lift-and-shift without redesign** | Cloud costs exceed on-prem | Re-architect for cloud-native |
| **Over-provisioning** | Paying for idle resources | Auto-scaling, right-sizing, spot instances |
| **No tagging strategy** | Cannot attribute costs or manage resources | Mandatory tagging policy |
| **Manual console changes** | Configuration drift, audit gaps | IaC for everything |
| **Single-AZ production** | Single point of failure | Multi-AZ minimum for production |
| **Public databases** | Security vulnerability | Private subnets, no public IP |
| **Long-lived credentials** | Security risk | Assume roles, short-lived tokens |
| **No cost alerts** | Budget overruns discovered months later | Budget alerts at 50%, 80%, 100% |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
