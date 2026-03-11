# Team Topology & Organizational Architecture

> **Purpose:** Standards for structuring engineering teams aligned with architecture —
> Conway's Law applied. Covers team types, interaction modes, ownership models,
> and scaling team structures as organizations grow.

---

## How to Use This File

- **Org Design:** Say to an LLM: *"Using these team topology patterns, design the team structure for a [size] engineering org building [product type]"*
- **Architecture Review:** Use Conway's Law to evaluate if team structure supports or conflicts with target architecture

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [09 — Microservices Patterns](./09-microservices-patterns.md) | One service per team alignment |
| [18 — Architecture Governance](./18-architecture-governance.md) | ARB composition and governance |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | Team autonomy in deployment |

---

## 1. Conway's Law (The Foundation)

> *"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."* — Melvin Conway

**Inverse Conway Maneuver:** Design your team structure to match your desired architecture. If you want microservices, organize into small, autonomous teams — each owning a service.

```
Team Structure          →          System Architecture
                                  
5-person backend team   →   Monolith
3 cross-functional      →   3 Microservices
  teams of 6-8
Platform team + 4       →   4 Services on
  product teams              shared platform
```

---

## 2. Team Types (Team Topologies Model)

| Team Type | Purpose | Size | Examples |
|-----------|---------|:----:|---------|
| **Stream-Aligned** | Delivers business value in a product domain | 5-9 | Order Team, Catalog Team, Payments Team |
| **Platform** | Provides self-service capabilities to stream-aligned teams | 4-8 | Cloud Platform, Developer Experience, CI/CD |
| **Enabling** | Helps stream-aligned teams adopt new capabilities | 2-4 | Architecture, Security, Quality Engineering |
| **Complicated Subsystem** | Owns complex domain requiring deep expertise | 3-6 | ML/AI Engine, Video Processing, Billing Engine |

### 2.1 Stream-Aligned Teams (Primary)

Own a slice of the business domain end-to-end:

```
┌──────────────────────────────────────────┐
│         Stream-Aligned Team              │
│                                          │
│  Product ↔ Frontend ↔ Backend ↔ QA ↔ Ops │
│                                          │
│  Owns: Service + Data + Deployment +     │
│        On-call + Monitoring              │
└──────────────────────────────────────────┘
```

**Rules:**
- Cross-functional: includes devs, QA, and ideally product + ops
- Owns their service(s) end-to-end (build it, run it, own it)
- Can deploy independently without coordinating with other teams
- Aligned to business domain, not technology layer

### 2.2 Platform Teams

```
┌─────────────────────────────────────┐
│         Platform Team               │
│                                     │
│  Provides self-service:             │
│  • CI/CD pipelines                  │
│  • Infrastructure provisioning      │
│  • Monitoring & logging             │
│  • Service templates & scaffolding  │
│  • Internal developer portal        │
│                                     │
│  Does NOT build product features    │
└─────────────────────────────────────┘
```

**Rules:**
- Treat internal teams as customers — the platform is a product
- Self-service over ticket-based requests
- Document and maintain APIs for platform services
- Measure success by developer satisfaction and time-to-deploy

### 2.3 Enabling Teams

| Activity | Description |
|----------|-----------|
| Architecture guidance | Helping teams make good design decisions |
| Technology introduction | Training teams on new tools/patterns |
| Security coaching | Embedding security practices into teams |
| Performance coaching | Helping teams optimize their services |

**Rule:** Enabling teams don't do the work FOR stream-aligned teams. They coach and unblock.

---

## 3. Team Interaction Modes

| Mode | Description | When |
|------|-----------|------|
| **Collaboration** | Two teams work closely together (pairing, shared work) | Learning a new technology, complex integration |
| **X-as-a-Service** | One team provides a service consumed by others via API | Platform team provides CI/CD, infra |
| **Facilitating** | One team helps another adopt a new capability | Enabling team coaches security practices |

**Rule:** Collaboration is expensive — use it temporarily for learning, then shift to X-as-a-Service.

---

## 4. Team Sizing & Structure

### 4.1 Amazon's Two-Pizza Rule

A team should be small enough to feed with two pizzas (6-9 people).

| Team Size | Characteristics |
|:---------:|----------------|
| 3-5 | Too small for on-call, single point of failure | 
| **6-9** | **Ideal: enough for on-call rotation, diverse skills** |
| 10-12 | Starting to lose communication efficiency |
| 13+ | Split the team — communication overhead is killing you |

### 4.2 Team Composition (Typical Stream-Aligned)

| Role | Count | Responsibility |
|------|:-----:|---------------|
| Tech Lead | 1 | Technical direction, code reviews, mentoring |
| Senior Developer | 1-2 | Complex features, architecture within the service |
| Developer | 2-3 | Feature development |
| QA Engineer | 1 | Test strategy, automation |
| Product Owner | 1 (shared OK) | Prioritization, requirements |
| **Total** | **6-8** | |

---

## 5. Scaling Team Structures

### 5.1 By Organization Size

| Org Size | Team Structure | Architecture |
|:--------:|---------------|-------------|
| **5-10 engineers** | 1 team, everyone does everything | Monolith |
| **10-25 engineers** | 2-3 stream-aligned teams | Modular monolith or 2-3 services |
| **25-60 engineers** | 4-7 stream-aligned + 1 platform team | Microservices |
| **60-150 engineers** | 8-15 stream-aligned + platform + enabling | Microservices + internal platform |
| **150+ engineers** | Multiple domains with domain leads | Domain-driven org + platform org |

### 5.2 When to Split a Team

- Team is > 9 people
- Team owns > 3 services (cognitive overload)
- Team has too many competing priorities
- Deployment frequency is declining because of coordination needs
- On-call rotation is suffering

### 5.3 When NOT to Split

- To match a desired architecture (split the architecture, but keep the team if < 9)
- Because another company did it (context matters)
- Without an available tech lead for the new team

---

## 6. Ownership Model

### 6.1 Service Ownership Matrix

| Aspect | Owner |
|--------|-------|
| **Code** | Stream-aligned team |
| **Deployment** | Stream-aligned team (self-service via platform) |
| **On-call** | Stream-aligned team |
| **API contract** | Stream-aligned team + consumers (contract tests) |
| **Infrastructure** | Platform team (provisioning); stream-aligned (config) |
| **Security** | Shared: stream-aligned (implementation) + enabling (standards) |
| **Monitoring** | Stream-aligned team (service); platform (infrastructure) |

### 6.2 Rules

- **You build it, you run it.** No throwing code over the wall to ops.
- Every production service has a clear owning team in the service catalog.
- On-call is shared across the team (not dumped on juniors).
- API changes require consumer notification (contract testing).

---

## 7. Team Topology Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Layer-oriented teams** (frontend team, backend team, DB team) | Handoffs, slow delivery, finger-pointing | Cross-functional stream-aligned teams |
| **Shared ownership** ("everyone owns it") | Nobody owns it, nobody fixes it | Clear ownership in service catalog |
| **Too many teams, too few services** | Teams fighting for work | Merge teams, each team needs enough scope |
| **Platform team as bottleneck** | Ticket-based infra requests, days of wait | Self-service platform with golden paths |
| **Heroics culture** | One person always saves the day | Knowledge sharing, pair programming, docs |
| **Architecture team builds things** | Becomes bottleneck, loses touch with reality | Architecture team enables, doesn't build |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
