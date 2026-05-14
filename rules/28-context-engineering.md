# Context Engineering Standards

> **Purpose:** This rule file defines how to design, structure, and optimize context
> for Large Language Models (LLMs) in enterprise workflows. Context engineering is the
> practice of deliberately crafting information fed to an AI model to maximize output
> quality, consistency, and safety — while minimizing token waste and hallucination risk.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [27 — Spec-Driven Development](./27-spec-driven-development.md) | Specs are the primary context artifact |
| [26 — AI/ML Architecture](./26-ai-ml-architecture.md) | Infrastructure for LLM-based systems |
| [29 — Agentic AI Governance](./29-agentic-ai-governance.md) | Safety and oversight for agents |
| [07 — Security Architecture](./07-security-architecture.md) | Prompt injection, PII in context |

---

## 1. Context vs Prompt Engineering

| Aspect | Prompt Engineering | Context Engineering |
|--------|--------------------|---------------------|
| Scope | Single prompt optimization | Entire information architecture |
| Artifacts | Prompt text | System instructions, knowledge bases, specs, tools |
| Duration | Per-request | Across sessions, systems, and agents |
| Scale | Individual use | Team and enterprise-wide |
| Outcome | Better single response | Consistent, auditable, repeatable system behavior |

---

## 2. The Context Stack (5 Layers)

```
Layer 5: Dynamic Context (per request)    ? User input, current state
Layer 4: Task Context (per task)          ? tasks.md, relevant code files
Layer 3: Feature Context (per feature)   ? design.md, relevant requirements
Layer 2: Project Context (session)        ? constitution.md, ADRs, style guide
Layer 1: System Context (always-on)       ? Persona, safety rules, output format
```

**Rule:** Always load lower layers before upper layers.
**Rule:** Never load more context than the task requires.

---

## 3. System Instructions (Layer 1) — Mandatory Elements

| Element | Purpose | Example |
|---------|---------|---------|
| **Persona definition** | Sets expertise, tone, behavior | "You are a Senior Enterprise Architect with 15+ years of experience" |
| **Domain scope** | What the model IS and IS NOT | "You assist with software architecture. Do not provide legal advice." |
| **Output format** | Consistency in responses | "Always respond with: Summary ? Reasoning ? Decision ? Next Steps" |
| **Safety rails** | Non-negotiable prohibitions | "Never generate code that bypasses authentication" |
| **Escalation policy** | When to stop and ask | "If a requirement contradicts a security principle, flag it — do not proceed" |

**Anti-Patterns:**
- System instructions >2,000 tokens (dilutes focus; use knowledge base for details)
- Contradictory rules (model behavior becomes unpredictable)
- No format specification (inconsistent output structure)
- No escalation policy (model hallucinates rather than asking)

---

## 4. Knowledge Base Design (Layers 2–3)

### 4.1 Knowledge Architecture Principles

- **Modular:** One file = one domain. Never mix topics.
- **Metadata-first:** Every file MUST have title, purpose, scope, owner, and last-reviewed date.
- **Version-controlled:** Knowledge lives in Git; changes go through PR review.
- **Freshness SLA:** Every file has a review cadence (quarterly minimum).

### 4.2 RAG Standards

| Standard | Rule |
|----------|------|
| **Chunk size** | 200–500 tokens. Preserve semantic boundaries (paragraphs/sections). |
| **Overlap** | 10–20% overlap between adjacent chunks |
| **Relevance threshold** | Only inject chunks with similarity score >0.75 |
| **Max chunks per query** | Cap at 5–8 chunks |
| **Citation** | Responses citing RAG content MUST include source document |
| **Freshness gate** | Chunks >90 days without review MUST be flagged or excluded |

### 4.3 Embedding Strategy

| Approach | Use Case |
|----------|---------|
| Dense embeddings | General semantic search (default) |
| Sparse (BM25) | Keyword-heavy technical docs |
| Hybrid (dense + sparse) | Production enterprise RAG (recommended) |
| Fine-tuned embeddings | Domain-specific terminology |

---

## 5. Token Budget Management

| Component | Typical Budget |
|-----------|:------------:|
| System instructions | 500–1,500 tokens |
| Injected context (RAG/specs) | 1,000–8,000 tokens |
| Conversation history | 500–3,000 tokens |
| User input | 100–2,000 tokens |
| Output reservation | 1,000–4,000 tokens |
| **Total** | **< model context limit (10% buffer)** |

### Context Compression Techniques (apply in order when budget exceeded)
1. **Summarize** long conversation history
2. **Prune** low-relevance context using scoring
3. **Load progressively** — reset context between tasks
4. **Use pointer references** — "See design.md §3.2" instead of full text

---

## 6. Multi-Agent Context Routing

### Agent Context Contracts

| Agent Type | MUST Receive | MUST NOT Receive |
|-----------|-------------|-----------------|
| **Orchestrator** | constitution, task plan, agent capabilities | Detailed code, full specs |
| **Spec Agent** | EARS rules, user story, domain glossary | Code, infrastructure details |
| **Design Agent** | requirements.md, constitution, ADR templates | Code, implementation details |
| **Coder Agent** | Single task, relevant design.md section, constitution | Other tasks, full spec, unrelated files |
| **Reviewer Agent** | Changed code, relevant requirements, constitution | Unrelated history, full codebase |
| **Security Agent** | Security rules, changed code, data classification | Business requirements, cost details |

**Isolation Rule:** Each agent receives ONLY the context relevant to its specific role. No agent sees another agent's full context.

---

## 7. Context Security

### 7.1 Prompt Injection Defense

- [ ] User input MUST be delimited: `<user_input>...</user_input>`
- [ ] Validate input length, format, and content BEFORE injecting into prompts
- [ ] Detect override patterns: "ignore previous instructions", "you are now", "act as"
- [ ] Log all prompts for security audit (exclude PII)
- [ ] System instructions separated from user content in API role structure

### 7.2 PII in Context — Non-Negotiable Rules

- **NEVER** inject raw PII (names, SSN, credit cards, health data) into LLM context
- Use **pseudonymization**: replace real values with reference IDs before injection
- Implement **output filtering**: scan LLM responses for PII before returning to users
- Apply **data residency**: ensure LLM API calls comply with GDPR/CCPA requirements

| Classification | May Be in Context? | Handling |
|---------------|:------------------:|---------|
| Public | ? Yes | No restrictions |
| Internal | ? With auth | Authenticated sessions only |
| Confidential | ?? Minimized | Anonymize where possible |
| Restricted (PII, PHI) | ?? Never | Use reference IDs only |

---

## 8. Context Quality Metrics

| Metric | Target |
|--------|:------:|
| Context relevance score (avg cosine similarity) | >0.80 |
| Context utilization rate (tokens referenced/injected) | >60% |
| Hallucination rate (fact-checked) | <5% |
| Context freshness (within review SLA) | 100% |
| PII leak incidents | 0 |

---

## 9. Context Engineering Checklist

- [ ] System instructions =1,500 tokens, free of contradictions
- [ ] Persona is specific (role, expertise level, behavioral constraints)
- [ ] Escalation policy defined (when to stop vs. proceed)
- [ ] Safety rails explicitly stated
- [ ] Output format specified
- [ ] Knowledge is modular with metadata on all chunks
- [ ] RAG relevance threshold set (>0.75)
- [ ] Token budget documented per workflow
- [ ] User input delimited and validated before injection
- [ ] PII excluded from context; pseudonymization applied
- [ ] Output PII scanning enabled
- [ ] Agent context contracts defined (no cross-agent context leakage)

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
