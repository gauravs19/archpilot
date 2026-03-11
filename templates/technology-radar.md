# Technology Radar

> **Purpose:** A living document tracking the organization's technology landscape.
> Technologies are placed in rings based on their adoption status.
> Updated quarterly by the ARB. See [18 — Architecture Governance](../rules/18-architecture-governance.md) for process.

---

## Last Updated: [YYYY-MM-DD] | Next Review: [YYYY-MM-DD]

---

## Ring Definitions

| Ring | Meaning | Action | Who Decides |
|------|---------|--------|------------|
| 🟢 **Adopt** | Proven, recommended for new projects | Use by default, no ARB needed | ARB |
| 🟡 **Trial** | Promising, being evaluated in 1-2 projects | Can use with team lead approval | ARB + Team Lead |
| 🔵 **Assess** | Worth exploring via PoC/spike | Research/PoC only, not production | Any engineer |
| 🔴 **Hold** | Do not use for new projects | Migration plan required for existing usage | ARB |

---

## Languages & Runtimes

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| Python 3.12 | 🟢 Adopt | Primary backend language | Q1 2024 | |
| TypeScript 5.x | 🟢 Adopt | Frontend + Node.js services | Q1 2024 | |
| Node.js 20 LTS | 🟢 Adopt | API services, tooling | Q2 2024 | |
| Go 1.22 | 🟡 Trial | Performance-critical services | Q3 2025 | |
| Rust | 🔵 Assess | Core infrastructure, CLI tools | Q1 2026 | |
| Java 8/11 | 🔴 Hold | Migrate to Java 21 or Python | Q1 2025 | |
| PHP | 🔴 Hold | Legacy only, no new projects | Q3 2024 | |

## Frameworks

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| FastAPI | 🟢 Adopt | Python REST APIs | Q1 2024 | |
| Next.js 14 | 🟢 Adopt | React SSR/SSG frontend | Q2 2024 | |
| Django | 🟢 Adopt | Admin panels, content sites | Q1 2024 | |
| Express.js | 🟢 Adopt | Node.js APIs | Q1 2024 | |
| Spring Boot 3 | 🟡 Trial | Java services (where Java is mandated) | Q1 2025 | |
| Hono | 🔵 Assess | Edge-first API framework | Q1 2026 | |
| jQuery | 🔴 Hold | Legacy only | Q1 2024 | |
| Angular.js (1.x) | 🔴 Hold | Migrate to React/Next.js | Q1 2024 | |

## Databases

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| PostgreSQL 16 | 🟢 Adopt | Default OLTP | Q1 2024 | |
| Redis 7 | 🟢 Adopt | Caching, sessions, queues | Q1 2024 | |
| Elasticsearch / OpenSearch | 🟢 Adopt | Full-text search, log aggregation | Q2 2024 | |
| MongoDB 7 | 🟡 Trial | Document-heavy, flexible schema | Q3 2025 | |
| DynamoDB | 🟡 Trial | Serverless, high-throughput key-value | Q2 2025 | |
| CockroachDB | 🔵 Assess | Distributed SQL | Q1 2026 | |
| Oracle | 🔴 Hold | Migrate away, cost reduction | Q1 2024 | |
| MySQL 5.x | 🔴 Hold | Migrate to PostgreSQL or MySQL 8 | Q2 2024 | |

## Cloud & Infrastructure

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| AWS | 🟢 Adopt | Primary cloud provider | Q1 2024 | |
| Terraform | 🟢 Adopt | IaC, multi-cloud | Q1 2024 | |
| Docker | 🟢 Adopt | Container standard | Q1 2024 | |
| ECS Fargate | 🟢 Adopt | Serverless containers | Q2 2024 | |
| GitHub Actions | 🟢 Adopt | CI/CD | Q1 2024 | |
| Kubernetes (EKS) | 🟡 Trial | For teams with K8s expertise | Q3 2025 | |
| Azure | 🟡 Trial | Specific GCC requirements | Q1 2026 | |
| GCP | 🔵 Assess | BigQuery, Vertex AI exploration | Q1 2026 | |
| Pulumi | 🔵 Assess | IaC alternative to Terraform | Q1 2026 | |

## Messaging & Integration

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| AWS SQS/SNS | 🟢 Adopt | Default async messaging | Q1 2024 | |
| Apache Kafka | 🟡 Trial | High-throughput event streaming | Q3 2025 | |
| RabbitMQ | 🟡 Trial | Complex routing, legacy support | Q2 2025 | |
| AWS EventBridge | 🔵 Assess | Event bus, serverless integration | Q1 2026 | |

## Observability

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| Datadog | 🟢 Adopt | APM + logs + metrics | Q2 2024 | |
| Sentry | 🟢 Adopt | Error tracking | Q1 2024 | |
| Prometheus + Grafana | 🟡 Trial | Cost-conscious alternative | Q3 2025 | |
| OpenTelemetry | 🟡 Trial | Vendor-neutral instrumentation | Q1 2026 | |

## AI/ML

| Technology | Ring | Notes | Entered | Last Moved |
|-----------|:----:|-------|:-------:|:----------:|
| OpenAI GPT-4 API | 🟢 Adopt | LLM integration | Q1 2025 | |
| LangChain | 🟡 Trial | LLM orchestration | Q2 2025 | |
| MLflow | 🟡 Trial | Experiment tracking, model registry | Q3 2025 | |
| AWS SageMaker | 🔵 Assess | Managed ML training/serving | Q1 2026 | |
| Hugging Face | 🔵 Assess | Open-source models | Q1 2026 | |

---

## Change Log

| Date | Technology | Change | Reason |
|------|-----------|--------|--------|
| [YYYY-MM-DD] | [e.g., Go] | Assess → Trial | Successful PoC for API gateway |
| [YYYY-MM-DD] | [e.g., Oracle] | Adopt → Hold | Cost reduction initiative |

---

## How to Propose Changes

1. Any engineer can propose a technology change
2. Submit via ARB process (see [18 — Architecture Governance](../rules/18-architecture-governance.md))
3. Include: technology name, proposed ring, justification, PoC results (if applicable)
4. ARB reviews and decides quarterly (or ad-hoc for urgency)

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
