# 🏛️ Archpilot — Enterprise Architecture Standards Library

> **"Co-pilot for Enterprise Architects."**
>
> A portable, LLM-agnostic collection of architecture rules, templates, and system prompts
> that standardize how AI generates enterprise-grade design documents.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Architecture](https://img.shields.io/badge/Domain-Enterprise_Architecture-blue.svg)]()
[![LLM-Ready](https://img.shields.io/badge/LLM-Ready_Rules-brightgreen.svg)]()

---

## 🎯 What is Archpilot?

Archpilot is a **repository of rule files, templates, and AI instructions** that you plug into any LLM (Claude, ChatGPT, Gemini, Copilot, Cursor) to make it produce consistent, enterprise-grade architecture artifacts.

**It is NOT a CLI tool or application.** It is a **standards library** — think of it as `.eslintrc` but for enterprise architecture.

---

## 🚀 Quick Start (2 Minutes)

### Option A: Claude Projects
1. Create a new [Claude Project](https://claude.ai)
2. Paste [`llm-configs/claude-project-instructions.md`](./llm-configs/claude-project-instructions.md) as custom instructions
3. Upload these files as project knowledge:
   - `rules/00-architecture-principles.md`
   - `rules/04-lld-standards.md`
   - `templates/lld-template.md`
4. Ask: *"Create an LLD for a user authentication service using OAuth2 and JWT"*
5. Get a comprehensive, structured, enterprise-grade LLD ✨

### Option B: VS Code / GitHub Copilot
1. Copy [`llm-configs/vscode-copilot-instructions.md`](./llm-configs/vscode-copilot-instructions.md) to your project as `.github/copilot-instructions.md`
2. Copilot now follows your architecture standards for code suggestions

### Option C: Cursor IDE
1. Copy [`llm-configs/cursor-rules.md`](./llm-configs/cursor-rules.md) to your project as `.cursorrules`
2. Cursor follows your architecture standards automatically

### Option D: ChatGPT Custom GPT
1. Create a new Custom GPT
2. Paste [`llm-configs/claude-project-instructions.md`](./llm-configs/claude-project-instructions.md) as system instructions (works for ChatGPT too)
3. Upload rule files as knowledge

### Option E: Any LLM (Gemini, Groq, etc.)
1. Copy the relevant rule file content
2. Prefix your prompt: *"Follow these standards: [paste rules]. Now create..."*

---

## 📁 Repository Structure

```
archpilot/
├── rules/                              # 🧠 Architecture Standards & Guidelines (16 files)
│   ├── 00-architecture-principles.md   # Universal design principles, decision framework
│   ├── 01-solution-design.md           # SDD standards, when HLD vs LLD vs SDD
│   ├── 02-adr-standards.md             # ADR writing standards & lifecycle
│   ├── 03-hld-standards.md             # High-Level Design rules (C4 Context/Container)
│   ├── 04-lld-standards.md             # Low-Level Design rules (most detailed)
│   ├── 05-api-design.md                # REST API conventions, versioning, security
│   ├── 06-data-architecture.md         # Data modeling, storage selection, governance
│   ├── 07-security-architecture.md     # Zero trust, OWASP, STRIDE, compliance
│   ├── 08-cloud-architecture.md        # 12-Factor, IaC, networking, HA/DR
│   ├── 09-microservices-patterns.md    # Decomposition, sagas, resilience
│   ├── 10-integration-patterns.md      # Event-driven, CDC, webhooks, API gateway
│   ├── 11-nfr-checklist.md             # 69-point NFR audit checklist
│   ├── 12-observability-standards.md   # Logging, metrics, tracing, alerting
│   ├── 13-devops-cicd.md               # Pipelines, branching, deployments, Docker
│   ├── 14-cost-optimization.md         # FinOps, TCO, right-sizing, pricing models
│   └── 15-code-review-guidelines.md    # Architecture-aware code review standards
│
├── templates/                          # 📝 Document Templates (4 files)
│   ├── lld-template.md                 # Low-Level Design (13 sections)
│   ├── hld-template.md                 # High-Level Design (14 sections)
│   ├── sdd-template.md                 # Solution Design Document (11 sections)
│   └── adr-template.md                 # Architecture Decision Record
│
├── llm-configs/                        # 🤖 Platform-Specific LLM Instructions
│   ├── claude-project-instructions.md  # Ready for Claude Projects
│   ├── chatgpt-custom-gpt.md           # ChatGPT Custom GPT configuration
│   ├── vscode-copilot-instructions.md  # GitHub Copilot (.github/copilot-instructions.md)
│   ├── cursor-rules.md                 # Cursor IDE (.cursorrules)
│   └── personas/
│       ├── enterprise-architect.md     # Senior architect persona
│       ├── security-architect.md       # Security architecture reviewer
│       └── presales-solutioner.md      # Presales / proposal persona
│
├── examples/                           # 📄 Sample Outputs
│   ├── sample-lld.md                   # Notification Service — full LLD example
│   └── sample-adr.md                   # PostgreSQL vs DynamoDB — full ADR example
│
└── README.md                           # This file
```

**Total: 30 files | ~210 KB of enterprise architecture standards**

---

## 📖 Rule Files — What's Inside

| # | Rule File | What It Covers | Size |
|---|-----------|---------------|:----:|
| 00 | **Architecture Principles** | SOLID, SoC, API-First, Fail Fast, Least Privilege, FinOps, decision framework | 12.5 KB |
| 01 | **Solution Design** | SDD standards, when to use HLD vs LLD vs SDD, mandatory sections | 5.0 KB |
| 02 | **ADR Standards** | When to write, lifecycle, trade-off matrices, quality checklist, anti-patterns | 8.6 KB |
| 03 | **HLD Standards** | C4 diagrams, integration architecture, NFR summary, cost estimates | 6.9 KB |
| 04 | **LLD Standards** | 11 mandatory sections, API specs, DB schemas, error handling, security | 14.0 KB |
| 05 | **API Design** | REST conventions, status codes, error format, pagination, versioning, rate limiting | 8.6 KB |
| 06 | **Data Architecture** | Data modeling, storage selection matrix, governance, PII, migrations, indexing | 9.5 KB |
| 07 | **Security Architecture** | Zero trust, OAuth2/JWT, RBAC/ABAC, encryption, STRIDE, OWASP, compliance | 11.0 KB |
| 08 | **Cloud Architecture** | 12-Factor App, compute selection, IaC, VPC networking, HA/DR tiers | 8.6 KB |
| 09 | **Microservices Patterns** | Decomposition, sync/async, saga, circuit breakers, service mesh | 10.1 KB |
| 10 | **Integration Patterns** | Event-driven, CDC, ETL/ELT, webhooks, API gateway, BFF | 8.8 KB |
| 11 | **NFR Checklist** | 69 checks: performance, security, reliability, scalability, observability, DR | 7.4 KB |
| 12 | **Observability** | Structured logging, RED/USE metrics, distributed tracing, alerting, dashboards | 7.8 KB |
| 13 | **DevOps & CI/CD** | Pipeline stages, branching, deployments, Docker, GitOps, environments | 8.2 KB |
| 14 | **Cost Optimization** | FinOps, TCO modeling, right-sizing, pricing models, tagging, governance | 7.1 KB |
| 15 | **Code Review** | Architecture, security, performance, error handling, testing, observability checks | 6.1 KB |

---

## 🎯 Example Use Cases

### 1. Generate an LLD
Upload `rules/04-lld-standards.md` + `templates/lld-template.md`, then ask:
> *"Create an LLD for a payment processing service. Context: handles credit card payments via Stripe, must be PCI-DSS compliant, expected 10K transactions/day."*

### 2. Create an HLD
Upload `rules/03-hld-standards.md` + `templates/hld-template.md`, then ask:
> *"Create an HLD for an e-commerce platform. Expected: 50K daily users, multi-tenant, AWS deployment."*

### 3. Write a Solution Design
Upload `rules/01-solution-design.md` + `templates/sdd-template.md`, then ask:
> *"Write an SDD for migrating a legacy monolith to microservices. Budget: $200K, timeline: 6 months."*

### 4. Create an ADR
Upload `rules/02-adr-standards.md` + `templates/adr-template.md`, then ask:
> *"Create an ADR for choosing between PostgreSQL and DynamoDB for a multi-tenant SaaS app."*

### 5. Audit a Design
Upload `rules/11-nfr-checklist.md`, then ask:
> *"Audit this design against the NFR checklist: [paste your HLD/LLD]"*

### 6. Review Security
Upload `rules/07-security-architecture.md`, then ask:
> *"Review this API design for security vulnerabilities: [paste your API spec]"*

### 7. Estimate Cloud Costs
Upload `rules/14-cost-optimization.md`, then ask:
> *"Estimate the 3-year TCO for: 3 EKS services, 2 RDS instances, Redis, S3, CloudFront on AWS."*

### 8. Design Microservices
Upload `rules/09-microservices-patterns.md` + `rules/10-integration-patterns.md`, then ask:
> *"We have a monolithic e-commerce app. Propose a microservices decomposition with integration strategy."*

---

## 🏗️ Roadmap

### ✅ Phase 1 — Core (Complete)
- [x] Architecture Principles
- [x] LLD Standards + Template
- [x] HLD Standards + Template
- [x] ADR Standards + Template
- [x] API Design Standards
- [x] Security Architecture
- [x] Microservices Patterns
- [x] NFR Checklist (69 checks)
- [x] Claude Project Instructions
- [x] Enterprise Architect Persona

### ✅ Phase 2 — Extended Standards (Complete)
- [x] Solution Design Standards + Template
- [x] Data Architecture Standards
- [x] Integration Patterns (Event-Driven, CDC, Webhooks, API Gateway)
- [x] Cloud Architecture Standards (12-Factor, IaC, HA/DR)
- [x] Observability Standards (Logging, Metrics, Tracing, Alerting)
- [x] DevOps & CI/CD Standards (Pipelines, Docker, GitOps)
- [x] Cost Optimization / FinOps
- [x] Code Review Guidelines

### 📋 Phase 3 — Platform Configs & Examples (Complete)
- [x] VS Code Copilot Instructions
- [x] Cursor Rules
- [x] ChatGPT Custom GPT Config
- [x] Additional Personas (Security Architect, Presales Solutioner)
- [x] Example Outputs (Sample LLD, Sample ADR)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/data-architecture-rules`)
3. Add your rule file following the existing format
4. Submit a Pull Request

**Rule file format:**
- Start with a Purpose block explaining what and how to use
- Use tables for checklists and comparisons
- Include anti-patterns section
- End with the Archpilot footer

---

## 📜 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🏛️ Philosophy

> *"The quality of an architect's work is defined not by the buildings they design,
> but by the standards they maintain."*

Most architects carry their standards in their heads. Archpilot codifies them —
making enterprise architecture consistent, teachable, and AI-augmented.

---

*Created by [Gaurav Sharma](https://gauravs19.github.io/portfolio/) — 18+ Years of Architecture Delivery*
