# Solution Design Document: Unified Customer Portal

## Project: UnifyQ — Customer Support & Self-Service Portal

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Author** | Gaurav Sharma, Solution Architect |
| **Date** | 2026-03-11 |
| **Status** | Draft → Review → Approved |
| **Stakeholders** | VP Product, Engineering Director, CTO |

---

## 1. Executive Summary

UnifyQ is a unified customer portal that consolidates three existing support channels
(email, phone ticketing, and WhatsApp) into a single self-service + agent-assisted platform.
The system will serve 200K customers, handle 5,000 tickets/day, and integrate with
Salesforce CRM, Freshdesk (existing), and an internal billing system.

**Why now:** Customer satisfaction (CSAT) has dropped from 4.2 to 3.6 over the past year
due to fragmented support channels. Customers report issues through email, receive responses
via WhatsApp, and escalations via phone — with no unified view.

**Expected outcomes:**
- CSAT from 3.6 → 4.2+ within 6 months
- First response time from 4 hours → 30 minutes
- 40% ticket deflection through self-service
- 25% reduction in support headcount cost

---

## 2. Problem Statement

### Current Pain Points

| # | Problem | Impact | Affected Users |
|---|---------|--------|:-------------:|
| 1 | Customers must repeat context across channels | Customer frustration, churn | 200K customers |
| 2 | Agents use 3 different tools simultaneously | Agent inefficiency, errors | 50 agents |
| 3 | No self-service for common queries (billing, order status) | High ticket volume for simple queries | All |
| 4 | No unified customer history | Can't prioritize high-value customers | All |
| 5 | Reporting is manual (Excel-based) | No visibility into support quality | Management |

### Current Architecture (As-Is)

```
Customer ──email──▶ Freshdesk
Customer ──phone──▶ Manual ticketing (Excel)
Customer ──WhatsApp──▶ WhatsApp Business (no ticket tracking)
                         
Freshdesk ──manual──▶ Salesforce CRM
Excel ──manual──▶ Salesforce CRM
WhatsApp ──no integration──▶ (lost data)
```

---

## 3. Scope

### In Scope

| Feature | Priority | Details |
|---------|:--------:|--------|
| Unified customer portal (self-service) | P0 | Knowledge base, order lookup, billing queries |
| Omnichannel ticket management | P0 | Email, WhatsApp, chat — single agent view |
| AI-powered ticket routing | P1 | Auto-classify and route to right team |
| Customer 360 view | P1 | Unified history across all channels |
| Analytics dashboard | P1 | CSAT, response time, resolution time, agent performance |
| AI chatbot for deflection | P2 | Handle FAQs, order status, billing queries automatically |

### Out of Scope (Phase 1)

- Phone/IVR integration (Phase 2)
- Video support (future)
- Multi-language support (Phase 2)
- Social media integration (Phase 3)

---

## 4. Proposed Solution

### 4.1 Architecture Overview (C4 Context)

```
┌──────────┐          ┌──────────────────────────────────┐
│ Customer │──web────▶│        UnifyQ Portal              │
│          │◀─notify──│  (Self-Service + Chat + Tickets)  │
└──────────┘          └──────────┬───────────────────────┘
                                 │
┌──────────┐          ┌──────────▼───────────────────────┐
│ Support  │──web────▶│      UnifyQ Agent Dashboard       │
│ Agent    │          │  (Omnichannel + Customer 360)     │
└──────────┘          └──────────┬───────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
  ┌─────▼──────┐          ┌─────▼──────┐          ┌─────▼──────┐
  │ Salesforce  │          │ Freshdesk   │          │  Billing    │
  │ CRM         │          │ (Phase 1:   │          │  System     │
  │             │          │  migrate)   │          │  (Internal) │
  └────────────┘          └────────────┘          └────────────┘
```

### 4.2 Solution Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Customer Portal** | Next.js (React) | Self-service UI: knowledge base, ticket submission, order lookup |
| **Agent Dashboard** | Next.js (React) | Unified agent workspace: tickets, customer 360, chat |
| **Ticket Service** | Python (FastAPI) | Ticket lifecycle: create, assign, escalate, resolve |
| **Chat Service** | Node.js (WebSocket) | Real-time chat between customer and agent |
| **AI Router** | Python (FastAPI + GPT-4 API) | Classify tickets, suggest responses, route to team |
| **Notification Service** | Python (FastAPI + SQS) | Email, SMS, WhatsApp notifications |
| **Integration Layer** | Python (FastAPI) | Salesforce sync, billing API wrapper, Freshdesk migration |
| **Analytics Service** | Python + PostgreSQL | CSAT, SLA, agent metrics, reporting |

### 4.3 Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js 14, shadcn/ui | Fast development, good DX, SSR for SEO |
| Backend | Python 3.12, FastAPI | Team expertise, ecosystem, AI/ML integration |
| Real-time | Node.js + Socket.io | WebSocket performance for chat |
| Database | PostgreSQL 16 | ACID, full-text search, JSONB for flexibility |
| Cache | Redis 7 | Chat sessions, ticket cache, rate limiting |
| Queue | AWS SQS | Async notifications, AI processing |
| Storage | AWS S3 | Attachments, knowledge base assets |
| AI/ML | OpenAI GPT-4 API | Ticket classification, response suggestions |
| Cloud | AWS (ECS Fargate) | Team expertise, managed services |
| CI/CD | GitHub Actions | Existing pipeline |
| Monitoring | Datadog | APM, logs, metrics, dashboards |

---

## 5. Key Architecture Decisions

| # | Decision | Chosen | Alternative Considered | Rationale |
|---|----------|--------|----------------------|-----------|
| ADR-001 | Build vs Buy ticketing | Build custom | Zendesk, Freshdesk | Need deep integration with billing + Salesforce; existing tools didn't support unified view |
| ADR-002 | AI classification | OpenAI GPT-4 API | AWS Comprehend, custom ML | Faster to market, 95%+ accuracy on our ticket data, can switch later |
| ADR-003 | WhatsApp integration | Twilio API for WhatsApp | WhatsApp Business API directly | Twilio abstracts complexity, multi-channel support built-in |
| ADR-004 | Real-time chat | WebSocket (Socket.io) | Polling, SSE | Need bidirectional, low-latency agent-customer chat |
| ADR-005 | Database | PostgreSQL (single DB) | Separate DB per service | Simplicity; can split later when team +complexity grows |

---

## 6. Non-Functional Requirements

| NFR | Target | How |
|-----|--------|-----|
| **Availability** | 99.9% | Multi-AZ, health checks, auto-scaling |
| **Latency (API p95)** | < 300ms | Caching, optimized queries, CDN |
| **Chat latency** | < 100ms | WebSocket, Redis pub/sub |
| **Concurrent users** | 2,000 agents + 10,000 customers | ECS auto-scaling, connection pooling |
| **Ticket throughput** | 5,000 new tickets/day | Queue-based processing for classification |
| **Data retention** | 3 years tickets, 7 years compliance | S3 archival, lifecycle policies |
| **Security** | SOC2 Type II compliant | RBAC, encryption, audit logs |
| **Disaster Recovery** | RPO: 1 hour, RTO: 4 hours | Multi-AZ, automated backups |

---

## 7. Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    UnifyQ System                         │
│                                                          │
│  Ticket ──REST──▶ Salesforce (bidirectional sync)       │
│  Service                                                 │
│              ──Webhook──▶ Freshdesk (read, then migrate) │
│                                                          │
│  Notif  ──Twilio API──▶ WhatsApp, SMS                   │
│  Service ──AWS SES──▶ Email                              │
│                                                          │
│  Integration ──REST──▶ Billing System (read-only)        │
│  Layer                                                   │
│                                                          │
│  AI Router ──OpenAI API──▶ GPT-4 (classify + suggest)    │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Data Migration

| Source | Target | Volume | Strategy | Timeline |
|--------|--------|:------:|:--------:|:--------:|
| Freshdesk tickets (3 years) | UnifyQ PostgreSQL | 500K tickets | Batch migration (Python script) | Week 3-4 |
| WhatsApp chat history | UnifyQ PostgreSQL | 50K conversations | Manual import (CSV) | Week 4 |
| Salesforce contacts | UnifyQ customer table | 200K contacts | REST API sync | Week 2-3 |
| Knowledge base (Confluence) | UnifyQ knowledge module | 300 articles | Export/import script | Week 3 |

---

## 9. Effort Estimate

| Phase | Effort (Person-Days) | Duration |
|-------|:-------------------:|:--------:|
| Discovery + Design | 30 | 2 weeks |
| MVP: Portal + Ticketing + Agent UI | 120 | 6 weeks |
| Integration: Salesforce + Billing + WhatsApp | 60 | 4 weeks |
| AI: Classification + Routing | 30 | 3 weeks |
| Chat: Real-time agent-customer | 40 | 3 weeks |
| Analytics Dashboard | 25 | 2 weeks |
| Testing + UAT + Security | 35 | 3 weeks |
| Go-Live + Hypercare | 20 | 2 weeks |
| **Total** | **360 person-days** | **~18 weeks** |

---

## 10. Risk Assessment

| # | Risk | Probability | Impact | Mitigation |
|---|------|:-----------:|:------:|-----------|
| 1 | Salesforce API rate limits | High | Medium | Batch sync + caching, request during off-peak |
| 2 | AI classification accuracy < 85% | Medium | High | Fallback to manual routing, continuous tuning |
| 3 | Agent resistance to new tool | Medium | Medium | Training program, phased rollout, champion users |
| 4 | WhatsApp API policy changes | Low | High | Abstraction via Twilio, multi-channel fallback |
| 5 | Data migration data quality issues | High | Medium | Data profiling before migration, reconciliation |

---

## 11. Success Criteria

| Metric | Baseline | 3 Months | 6 Months |
|--------|:--------:|:--------:|:--------:|
| CSAT Score | 3.6 | 3.9 | 4.2+ |
| First Response Time | 4 hours | 1 hour | 30 minutes |
| Ticket Deflection (self-service) | 0% | 20% | 40% |
| Agent Tickets/Day (capacity) | 25 | 35 | 45 |
| Channel Consolidation | 3 tools | 1 tool | 1 tool |

---

*Generated using Archpilot Solution Design Standards v1.0*
