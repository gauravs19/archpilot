# DevOps & CI/CD Standards

> **Purpose:** Standards for CI/CD pipelines, branching strategies, deployment patterns,
> release management, and GitOps practices.

---

## How to Use This File

- **Claude Projects:** Upload for CI/CD pipeline design and deployment strategy
- **Any LLM:** Say: *"Using these DevOps standards, design the CI/CD pipeline for: [your project]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [08 — Cloud Architecture](./08-cloud-architecture.md) | Infrastructure and container deployment |
| [12 — Observability](./12-observability-standards.md) | Post-deploy monitoring and alerting |
| [07 — Security Architecture](./07-security-architecture.md) | Security scanning in pipeline |
| [15 — Code Review](./15-code-review-guidelines.md) | PR standards that feed into CI |

---

## 1. CI/CD Pipeline Standards

### 1.1 Pipeline Stages (Minimum)

```
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│ Lint │→ │Build │→ │ Test │→ │ Scan │→ │Deploy│→ │Verify│
│      │  │      │  │      │  │      │  │ Stg  │  │      │
└──────┘  └──────┘  └──────┘  └──────┘  └──┬───┘  └──────┘
                                           │
                                    ┌──────▼─────┐
                                    │ Deploy Prod │
                                    │ (approval)  │
                                    └──────┬─────┘
                                           │
                                    ┌──────▼─────┐
                                    │ Post-Deploy │
                                    │   Verify    │
                                    └────────────┘
```

| Stage | What | Gate |
|-------|------|:----:|
| **Lint** | Code style, formatting (Ruff, ESLint, Prettier) | Auto |
| **Build** | Compile/package, Docker image build | Auto |
| **Unit Test** | Unit tests with code coverage (≥80%) | Auto |
| **Integration Test** | API tests, database tests, contract tests | Auto |
| **Security Scan** | SAST, dependency scan (Snyk, Trivy, SonarQube) | Auto |
| **Deploy Staging** | Automated deployment to staging | Auto |
| **Smoke Test** | Key user journeys verified in staging | Auto |
| **Deploy Production** | Deployment with selected strategy | Manual approval |
| **Post-Deploy Verify** | Health checks, smoke tests, metric monitoring | Auto |

### 1.2 Pipeline Rules

| Rule | Standard |
|------|---------|
| Build once, deploy many | Same artifact to staging and production |
| Pipeline as code | Jenkinsfile, GitHub Actions YAML, GitLab CI — in repo |
| Fast feedback | Pipeline completes in < 15 minutes (excluding long-running tests) |
| No secrets in pipeline code | Use CI/CD secret management (GitHub Secrets, Vault) |
| Artifact versioning | Semantic versioning or commit SHA |
| Immutable artifacts | Built images are never modified, only replaced |
| Pipeline notifications | Failure notifications to team channel (Slack, Teams) |

---

## 2. Branching Strategy

### 2.1 Trunk-Based Development (Recommended)

```
main ────●────●────●────●────●────●─── (always deployable)
         │         │              │
         └─ feat-1 ┘              └─ feat-2 (short-lived, <2 days)
```

**Rules:**
- `main` branch is ALWAYS deployable.
- Feature branches are short-lived (< 2 days).
- Pull requests required with at least 1 reviewer.
- Feature flags for incomplete features (not long-lived branches).
- No release branches — deploy from main.

### 2.2 Git Flow (When Required)

Use Git Flow only when:
- Multiple versions are maintained simultaneously.
- Release cycle is > 2 weeks.
- Regulatory approval required before release.

```
main ──────────────────────────────── (production)
develop ──●──●──●──●──●──●──●─────── (integration)
           │     │        │
           └feat ┘     └release-1.2
```

### 2.3 Commit Standards

**Conventional Commits format:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance (deps, CI, build) |
| `perf` | Performance improvement |
| `security` | Security fix |

---

## 3. Deployment Strategies

### 3.1 Strategy Selection

| Strategy | Risk | Rollback Speed | Complexity | Use When |
|----------|:----:|:--------------:|:----------:|----------|
| **Rolling Update** | Medium | Slow | Low | Default for non-critical services |
| **Blue-Green** | Low | Instant (switch LB) | Medium | Stateless services, fast rollback needed |
| **Canary** | Very Low | Fast (route traffic back) | High | Critical services, production validation |
| **Feature Flags** | Very Low | Instant (toggle off) | Medium | Gradual rollout, A/B testing |
| **Big Bang** | High | Very Slow | Low | NEVER for production |

### 3.2 Deployment Rules

| Rule | Standard |
|------|---------|
| Zero-downtime deployments | ALWAYS for production |
| Automated rollback | If health checks fail post-deploy, auto-rollback |
| Database migrations first | Run migrations BEFORE application deployment |
| Backward-compatible migrations | New code works with old schema AND new schema |
| Canary duration | Minimum 15 minutes at 5% traffic before full rollout |
| Deployment window | Avoid Friday deployments and end-of-day deployments |
| Deploy != Release | Use feature flags to separate deployment from feature release |

---

## 4. Environment Strategy

| Environment | Purpose | Data | Access | Deploy Frequency |
|------------|---------|------|--------|:----------------:|
| **Development** | Developer testing | Synthetic/mock | All developers | On merge |
| **Staging** | Pre-production validation | Anonymized production-like | Engineering team | On merge to main |
| **Production** | Live users | Real | Restricted (SRE + on-call) | Controlled releases |

**Rules:**
- Staging MUST mirror production configuration (same IaC, same secrets structure).
- Production data MUST NEVER be used in development or staging without anonymization.
- Each environment has its own secrets, credentials, and API keys.

---

## 5. Container Standards (Docker)

### 5.1 Dockerfile Best Practices

| Practice | Rule |
|----------|------|
| Use multi-stage builds | Separate build dependencies from runtime |
| Minimal base images | `alpine` or distroless — not `ubuntu:latest` |
| Pin versions | `python:3.12-slim` not `python:latest` |
| Non-root user | `USER 1001` — never run as root |
| `.dockerignore` | Exclude `.git`, `node_modules`, `__pycache__`, `.env` |
| Single concern | One process per container |
| Health checks | `HEALTHCHECK CMD curl -f http://localhost:8080/health` |
| No secrets in images | Use runtime injection, not build-time ARGs |

### 5.2 Image Tagging
```
{registry}/{service}:{version}-{git-sha}
```
Example: `ecr.aws/myapp/order-service:1.4.2-abc123f`

**Rules:**
- NEVER use `latest` tag in production.
- Images are immutable — same tag always produces same image.
- Scan images for vulnerabilities before pushing (Trivy, Snyk Container).

---

## 6. GitOps Practices

| Principle | Implementation |
|-----------|---------------|
| **Declarative** | Desired state defined in Git (not imperative scripts) |
| **Versioned** | All changes tracked in Git history |
| **Automated** | Reconciliation loop applies Git state to infrastructure |
| **Observable** | Drift detection alerts when actual ≠ desired state |

**Tools:** ArgoCD, Flux, Jenkins X

**Repository Structure:**
```
infra-repo/
├── base/                    # Common resources
│   ├── namespace.yaml
│   └── network-policies.yaml
├── environments/
│   ├── dev/
│   │   └── kustomization.yaml
│   ├── staging/
│   │   └── kustomization.yaml
│   └── production/
│       └── kustomization.yaml
└── services/
    ├── order-service/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   └── hpa.yaml
    └── payment-service/
        └── ...
```

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
