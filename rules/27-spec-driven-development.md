# Spec-Driven Development (SDD) Standards

> **Purpose:** This rule file defines the Spec-Driven Development methodology — the discipline
> of treating version-controlled specifications as the primary source of truth for all
> AI-assisted and team-based software delivery. It replaces "vibe coding" with repeatable,
> auditable engineering.
>
> **When used as LLM context**, this file ensures the AI produces structured, traceable,
> EARS-compliant specifications that can drive implementation without architectural drift.

---

## How to Use This File

- **Claude / Gemini Projects:** Upload as project knowledge. Ask: *"Using SDD standards, create a spec for [feature]"*
- **AWS Kiro:** Use as a steering file to enforce EARS notation and the Specify→Plan→Task→Implement loop
- **GitHub Copilot / Cursor:** Reference in `.github/copilot-instructions.md` or `.cursorrules`
- **Any LLM:** Prefix prompt with: *"Follow these SDD standards: [paste file]. Now specify: [your feature]"*

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [01 — Solution Design](./01-solution-design.md) | SDD enriches the requirements section of an SDD with EARS |
| [04 — LLD Standards](./04-lld-standards.md) | LLD is the design.md artifact in SDD terminology |
| [02 — ADR Standards](./02-adr-standards.md) | ADRs are design decisions captured during the Plan phase |
| [20 — Testing Strategy](./20-testing-strategy.md) | EARS requirements map directly to acceptance tests |
| [28 — Context Engineering](./28-context-engineering.md) | Specs are the primary context-engineering artifact |
| [templates/spec-template.md](../templates/spec-template.md) | Ready-to-fill EARS-based requirements spec |
| [templates/design-spec-template.md](../templates/design-spec-template.md) | Ready-to-fill design.md template |
| [templates/task-list-template.md](../templates/task-list-template.md) | Ready-to-fill tasks.md template |

---

## 1. Why Spec-Driven Development?

### 1.1 The Problem with Vibe Coding

| Symptom | Root Cause | SDD Solution |
|---------|-----------|--------------|
| AI produces generic, non-compliant designs | No constraint context | Spec = executable constraint |
| "Hallucinated" architecture choices | Ambiguous prompts | EARS notation eliminates ambiguity |
| Different outputs every time | No source of truth | Spec is version-controlled truth |
| Hard to audit or explain decisions | No traceability | Spec → Design → Task → Code chain |
| LLM forgets context mid-session | Context window limits | Modular specs = precise context loading |
| Junior-level suggestions from senior tool | No persona/principle injection | Constitution file enforces standards |

### 1.2 SDD Core Premise

> **The specification IS the product. Code is a derivative.**

In SDD:
- You write the spec → AI implements it → AI validates against the spec
- Updating a feature = updating the spec, then regenerating
- The spec is version-controlled, reviewed, and approved — just like code
- Specs become **executable contracts** in CI/CD pipelines

### 1.3 SDD vs Traditional Requirements

| Aspect | Traditional Requirements | Spec-Driven Development |
|--------|-------------------------|------------------------|
| Format | Natural language prose | EARS structured notation |
| Storage | Confluence / JIRA | Git-versioned markdown |
| Validation | Manual review | Automated conformance checks |
| Traceability | Manual matrices | Automated: spec → test → code |
| AI Compatibility | Low (ambiguous) | High (parseable, unambiguous) |
| Living document | Rarely updated | Always current (updated with code) |
| Test generation | Manual translation | Direct mapping from EARS to tests |

---

## 2. The SDD Artifact Triad (Spec Kit)

Every feature or service using SDD MUST produce these three artifacts before implementation begins:

```
.specs/
├── requirements.md    ← What to build (EARS notation)
├── design.md          ← How to build it (architecture + data models)
└── tasks.md           ← Atomic implementation steps (verifiable units)
```

Plus, at the project level:
```
constitution.md        ← Immutable project-wide principles (architecture law)
```

### 2.5 Artifact Density & Technical Rigor Standards

To prevent "shallow engineering," artifacts MUST meet minimum density thresholds based on the **Rule 37 Triage Matrix**.

#### 2.5.1 requirements.md Standards
- **Tier 1 (Fast-Track):** Not required.
- **Tier 2 (Medium):** Minimum 5 EARS requirements. 1 section on "Out of Scope."
- **Tier 3 (High-Risk):** Minimum 15 EARS requirements. MUST include a **Requirement Traceability Matrix (RTM)** linking requirements to Design (D-XXX) and Tasks (T-XXX).

#### 2.5.2 design.md Standards (The Technical Depth Gate)
- **Tier 2 (Medium):** Minimum 1 Mermaid Diagram (Sequence or Flow). Minimum 1 Data Schema table.
- **Tier 3 (High-Risk):** 
  - **Minimum 2 Mermaid Diagrams** (e.g., Sequence AND Architecture Topology).
  - **API Contract Table:** MUST specify gRPC/Protobuf or REST endpoints with exact types.
  - **Data Schema Table:** MUST specify Table/Column names, types, and Primary/Clustering keys.
  - **Failure Modes Matrix:** MUST analyze at least 3 failure scenarios (e.g., DB Failover, Network Partition).

#### 2.5.3 tasks.md Standards
- **Tier 2 (Medium):** Every task MUST have Acceptance Criteria.
- **Tier 3 (High-Risk):** 
  - Tasks MUST be < 4 hours of effort.
  - **Verification Section:** Every task MUST specify the exact unit test name or integration test scenario.
  - **Observability Task:** MUST include at least one task for Metrics/Logging implementation.

#### 2.5.4 Technical Exhaustiveness (The 1000-Line Rule)
- **Tier 3 (High-Risk):** Artifacts (`requirements.md`, `design.md`, `tasks.md`) MUST NOT be summaries. To ensure Principal-level technical depth, each file MUST exceed **1000 lines** of content.
- **Why?** If a design for a global HFT bridge is under 1000 lines, it has likely skipped Protobuf definitions, failure-state logic, and observability hook details. 
- **Non-Negotiable:** The `archpilot.py` linter will fail if line counts are insufficient.

### 2.1 requirements.md — The "What"

**Purpose:** Capture business intent, user needs, and system behaviors in machine-readable EARS format.

**Mandatory sections:**
1. **Overview** — 3-5 sentences: business problem, target users, success definition
2. **User Stories** — structured in standard format
3. **Functional Requirements** — written in EARS notation (see §4)
4. **Non-Functional Requirements** — quantified, testable NFRs
5. **Acceptance Criteria** — derived directly from EARS requirements
6. **Out of Scope** — explicit exclusions
7. **Open Questions** — blockers requiring human decision

**Quality rule:** Every functional requirement MUST map to at least one acceptance criterion.
**Quality rule:** Every acceptance criterion MUST be independently testable.

### 2.2 design.md — The "How"

**Purpose:** Translate requirements into technical architecture decisions, data models, interface definitions, and integration points.

**Mandatory sections:**
1. **Architecture Overview** — approach and key decisions (link to ADRs)
2. **Component Design** — services, modules, responsibilities
3. **Data Models** — entities, schemas, relationships
4. **API / Interface Design** — contracts (OpenAPI snippets or table format)
5. **State Machines** — for stateful components
6. **Error Handling Strategy** — by category
7. **Security Design** — auth/authz, data classification, threat model
8. **NFR Design** — how each NFR is technically achieved
9. **Dependency Map** — external systems, internal services

**Quality rule:** Every EARS functional requirement MUST be addressed by at least one component or interface in the design.
**Quality rule:** design.md MUST NOT contradict any item in constitution.md.

### 2.3 tasks.md — The "Steps"

**Purpose:** Decompose the design into atomic, independently verifiable implementation tasks for human or AI agents.

**Task anatomy:**
```markdown
## Task [N]: [Title]

**Status:** [ ] Not Started / [~] In Progress / [x] Done
**Depends on:** Task [M] (if any)

### Description
One paragraph: what needs to be done and why.

### Acceptance Criteria
- [ ] Criterion 1 (derived from EARS requirement FR-XXX)
- [ ] Criterion 2
- [ ] Criterion 3

### Files to Create/Modify
- `src/services/payment.service.ts` — create PaymentService class
- `src/repositories/payment.repository.ts` — create data access layer

### Test Requirements
- Unit test: `test/services/payment.service.test.ts`
- Integration test: `test/integration/payment-flow.test.ts`
```

**Quality rules:**
- Each task MUST be completable in 1-4 hours (if longer, decompose further)
- Each task MUST have ≥1 acceptance criterion traceable to a EARS requirement
- Tasks MUST list the files they create or modify
- Task dependencies MUST be explicitly stated

### 2.4 constitution.md — The "Law"

**Purpose:** Immutable, project-wide architectural principles that apply to every task, every AI session, and every code review.

**Mandatory sections:**
1. **Technology Stack** — locked versions and approved libraries
2. **Architecture Constraints** — what cannot change (e.g., "no shared databases")
3. **Coding Standards** — language-specific conventions
4. **Security Non-Negotiables** — zero-tolerance rules
5. **Naming Conventions** — files, classes, APIs, database objects
6. **Prohibited Patterns** — anti-patterns that will fail code review
7. **AI Agent Boundaries** — what agents may/may not do autonomously

---

## 3. The SDD Workflow Loop

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. SPECIFY  │────▶│   2. PLAN   │────▶│  3. TASK    │────▶│  4. IMPLEMENT│
│             │     │             │     │             │     │             │
│ requirements│     │  design.md  │     │  tasks.md   │     │ Code + Tests│
│    .md      │     │             │     │             │     │             │
│ (EARS)      │     │ (ADRs, ERD) │     │ (atomic)    │     │ (validated) │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
       ▲                                                              │
       └──────────────── Spec Updated if Reality Diverges ───────────┘
```

### Phase 1: SPECIFY
- **Who:** Business analyst, product owner, architect (with AI assistance)
- **Input:** Business requirements, user interviews, stakeholder briefs
- **Output:** `requirements.md` with EARS-formatted requirements
- **Gate:** Every requirement is unambiguous, testable, and has an ID
- **AI Prompt Pattern:** *"Convert these user stories to EARS notation following rule 27: [stories]"*

### Phase 2: PLAN
- **Who:** Solution architect, tech lead (with AI assistance)
- **Input:** `requirements.md` + `constitution.md`
- **Output:** `design.md` + ADRs for key decisions
- **Gate:** Every functional requirement maps to a design component; constitution constraints respected
- **AI Prompt Pattern:** *"Using design standards (rule 04) and this requirements.md, produce design.md"*

### Phase 3: TASK
- **Who:** Tech lead (with AI assistance)
- **Input:** `design.md`
- **Output:** `tasks.md` with atomic, ordered, dependency-mapped tasks
- **Gate:** Every task is independently testable and ≤4 hours effort
- **AI Prompt Pattern:** *"Decompose this design.md into atomic tasks following SDD task standards"*

### Phase 4: IMPLEMENT
- **Who:** Developer, AI agent, or paired human+AI
- **Input:** Single task from `tasks.md` + `constitution.md` + `design.md`
- **Output:** Code, tests, passing CI gates
- **Gate:** All acceptance criteria for the task pass; no constitution violations
- **AI Prompt Pattern:** *"Implement Task 3 from tasks.md. Follow constitution.md. Reference design.md for context."*

### Continuous Validation
- After each task: Run automated tests against acceptance criteria
- After each phase: Validate alignment with requirements.md
- Before merge: AI or human validates code against constitution.md
- Sprint retrospective: Update specs if implementation revealed new constraints

---

## 4. EARS Notation — Requirements Engineering Standard

EARS (Easy Approach to Requirements Syntax) transforms ambiguous natural language into machine-parseable, test-mappable requirements.

### 4.1 The Five EARS Patterns

| Pattern | Template | Test Type |
|---------|----------|-----------|
| **Ubiquitous** | `The [system] shall [action].` | Smoke / always-on |
| **Event-Driven** | `When [trigger], the [system] shall [action].` | Integration / behavioral |
| **State-Driven** | `While [state], the [system] shall [action].` | State machine / scenario |
| **Unwanted Behavior** | `If [condition], then the [system] shall [action].` | Error handling / negative |
| **Optional Feature** | `Where [feature is enabled], the [system] shall [action].` | Feature flag / variant |

### 4.2 EARS Examples — Correct vs Incorrect

| ❌ Vague Requirement | ✅ EARS Requirement | Pattern |
|---------------------|---------------------|---------|
| "The system should be fast" | "The Payment Service shall process 95% of payment requests within 500ms under normal load (≤1000 req/sec)." | Ubiquitous |
| "Handle errors gracefully" | "If the downstream Payment Gateway returns a 5xx error, then the Payment Service shall retry the request up to 3 times with exponential backoff (1s, 2s, 4s) before returning HTTP 503 to the caller." | Unwanted |
| "Support offline mode" | "While the mobile app is in offline mode, the system shall queue user actions in local storage and synchronize them when connectivity is restored, preserving action order." | State-Driven |
| "Users can log in" | "When a user submits valid credentials, the Authentication Service shall issue a signed JWT token with a 15-minute expiry and a refresh token with a 7-day expiry." | Event-Driven |
| "Support dark mode" | "Where the user has enabled dark mode in their profile settings, the UI shall apply the dark color palette to all screens within 100ms of the preference being loaded." | Optional |

### 4.3 EARS Quality Rules

- [ ] Every requirement uses one of the five EARS patterns
- [ ] The subject ([system]) names a specific component, not "the system" generically
- [ ] The action ([action]) is observable and measurable
- [ ] Numeric targets are specified where applicable (latency, throughput, size, count)
- [ ] Each requirement has a unique ID: `FR-001`, `FR-002`, etc.
- [ ] Compound requirements are split: one EARS statement = one behavior
- [ ] Negative requirements use the "Unwanted Behavior" pattern
- [ ] Requirements do not dictate implementation ("the system shall use Redis" is a design decision, not a requirement)

### 4.4 EARS Anti-Patterns

| Anti-Pattern | Example | Fix |
|-------------|---------|-----|
| Vague quantifier | "The system shall respond quickly" | Add specific target: "within 200ms at p95" |
| Implementation-as-requirement | "The system shall use a PostgreSQL database" | "The system shall persist order data with ACID guarantees" |
| Compound requirement | "The system shall authenticate and log the user and redirect them" | Split into 3 separate EARS statements |
| Passive voice ambiguity | "Errors shall be handled" | "If [error condition], then [specific system] shall [specific action]" |
| Missing actor | "Shall validate input" | "The API Gateway shall validate..." |
| Untestable | "The system shall be user-friendly" | Not an EARS requirement; convert to measurable UX metric or remove |

---

## 5. Requirement Traceability Matrix (RTM)

Every SDD project MUST maintain a traceability matrix linking each requirement to its design element, task, and test.

| Req ID | EARS Statement (Summary) | Design Component | Task ID | Test ID | Status |
|--------|--------------------------|------------------|---------|---------|--------|
| FR-001 | Payment Service shall process in ≤500ms | PaymentService.process() | T-03 | UT-007, IT-002 | ✅ Done |
| FR-002 | If gateway fails, retry 3× with backoff | RetryInterceptor | T-05 | UT-012 | 🔄 In Progress |
| NFR-001 | 99.9% uptime | HA architecture (design §4) | T-01 | PerfTest-001 | ✅ Done |

**Rule:** The RTM is the single source for measuring spec completeness.
**Rule:** No task may be marked "Done" if its linked test does not pass.
**Rule:** No feature may ship if any `FR-` or `NFR-` requirement has no mapped test.

---

## 6. Spec Governance — Lifecycle & Change Control

### 6.1 Spec States

| State | Meaning | Who Can Change |
|-------|---------|---------------|
| `DRAFT` | Being written, not reviewed | Author |
| `IN_REVIEW` | Under peer/stakeholder review | Reviewer (comments only) |
| `APPROVED` | Baseline — changes require formal amendment | Architecture board |
| `AMENDED` | Formally updated post-approval | Author + approver sign-off |
| `SUPERSEDED` | Replaced by a newer spec version | N/A — read-only |

### 6.2 Change Control Rules

- Any change to an `APPROVED` spec MUST be tracked in a Change Log section
- Changes that affect >20% of requirements MUST trigger a new spec version
- Implementation MUST NOT proceed if the spec is in `DRAFT` state
- If code contradicts the spec, the spec is amended or the code is reverted — **code does not override the spec**

### 6.3 Spec Change Log

Every spec MUST include:
```markdown
## Change Log

| Version | Date | Author | Change Summary | Approved By |
|---------|------|--------|---------------|-------------|
| 1.0 | YYYY-MM-DD | Name | Initial approved version | Name |
| 1.1 | YYYY-MM-DD | Name | Added FR-007 for rate limiting | Name |
```

---

## 7. SDD for AI Agent Orchestration

When using AI agents (Claude Code, Cursor, Copilot, Kiro, etc.), the spec kit serves as the **control plane**:

### 7.1 Agent Context Loading Strategy

Load context in this priority order to minimize token waste:

| Priority | Context | When to Load |
|----------|---------|-------------|
| 1 | `constitution.md` | Always — every session |
| 2 | Current `tasks.md` (single task) | Per task execution |
| 3 | `design.md` (relevant sections) | When task touches architecture |
| 4 | `requirements.md` (referenced FRs only) | When acceptance criteria needed |
| 5 | Related code files | Only files the task modifies |

**Rule:** Never load the entire codebase. Load only what the task requires.
**Rule:** Always load `constitution.md` first — it establishes non-negotiable constraints.

### 7.2 Agent Instruction Pattern

Use this prompt structure for AI-agent task execution:

```
You are implementing Task [N] from our project spec.

CONSTITUTION (non-negotiable rules):
[paste relevant constitution.md sections]

DESIGN CONTEXT (for reference):
[paste relevant design.md sections]

TASK:
[paste the single task from tasks.md]

CONSTRAINTS:
- Only modify the files listed in the task
- Implement acceptance criteria as tests first (TDD)
- Do not introduce dependencies not listed in the task
- If you encounter an ambiguity, stop and ask rather than assume

Implement Task [N].
```

### 7.3 Validation Agent Pattern

After implementation, run a validation pass:
```
You are a spec conformance auditor.

REQUIREMENTS to validate against: [paste relevant EARS requirements]
CONSTITUTION to validate against: [paste constitution.md]

CODE to audit:
[paste changed files]

Check:
1. Does each EARS requirement have a corresponding implementation?
2. Are all acceptance criteria satisfied?
3. Are there any constitution violations?
4. Are there any security, performance, or pattern anti-patterns?

Report findings as: [PASS], [WARN: description], or [FAIL: description]
```

---

## 8. SDD Quality Checklist

### requirements.md Review
- [ ] All requirements use valid EARS patterns (Ubiquitous / Event / State / Unwanted / Optional)
- [ ] Every requirement has a unique ID (FR-XXX, NFR-XXX)
- [ ] No compound requirements (one EARS = one behavior)
- [ ] All NFRs have numeric targets (not vague adjectives)
- [ ] Every FR has at least one mapped acceptance criterion
- [ ] Out-of-scope section explicitly lists exclusions
- [ ] No implementation details in requirements ("shall use Redis" = ❌)

### design.md Review
- [ ] Every FR from requirements.md is addressed by a component or interface
- [ ] No constitution.md constraints are violated
- [ ] All external dependencies are listed (services, APIs, databases)
- [ ] Data models have types, constraints, and relationships
- [ ] Security design addresses auth, authz, and data classification
- [ ] Error handling strategy covers all failure categories
- [ ] ADRs created for all significant architectural decisions

### tasks.md Review
- [ ] Each task is ≤4 hours of effort (decompose if larger)
- [ ] Each task's acceptance criteria trace back to a FR or NFR ID
- [ ] Task dependencies are explicit (no hidden sequencing assumptions)
- [ ] Files to create/modify are listed per task
- [ ] Test files are listed per task

### constitution.md Review
- [ ] Technology stack is locked with versions
- [ ] Security non-negotiables are explicit (e.g., "JWT tokens must be validated on every request")
- [ ] Prohibited patterns listed (e.g., "No shared mutable state between services")
- [ ] Naming conventions are comprehensive (files, classes, APIs, DB objects)
- [ ] AI agent boundaries defined (e.g., "Agents may not modify database migration files without human review")

---

## 9. SDD Anti-Patterns

| Anti-Pattern | Why It Fails | Correction |
|-------------|-------------|------------|
| Speccing after coding | Spec becomes documentation, not truth | Spec MUST be approved before implementation begins |
| One giant spec | Context overload for agents; hard to trace | Modular specs per feature/service |
| EARS without IDs | Untraceable, RTM impossible | Every EARS requirement gets FR-XXX |
| Design in requirements | Conflates "what" with "how" | Requirements describe behavior; design describes implementation |
| Tasks without acceptance criteria | No way to verify done-ness | Every task gets ≥1 testable criterion |
| Stale constitution | Agents follow outdated rules | Constitution reviewed at every sprint boundary |
| Skipping the RTM | No traceability, audit trail fails | RTM is mandatory before any story is closed |
| "TBD" in approved specs | Undefined behavior in production | TBDs must be resolved before state moves to APPROVED |
| Agent with full codebase context | Token waste, hallucination risk | Load only task-relevant files per session |

---

## 10. SDD Tooling Integration

| Tool | SDD Integration | Config |
|------|----------------|--------|
| **AWS Kiro** | Native SDD: requirements.md + design.md + tasks.md are first-class | `.kiro/steering/*.md` for constitution |
| **GitHub Copilot** | Load specs via `.github/copilot-instructions.md` | Point to spec files in instructions |
| **Cursor IDE** | `.cursorrules` = constitution.md equivalent | Load per-task specs in composer |
| **Claude Projects** | Project knowledge = constitution + spec files | Use project instructions for persona |
| **Archpilot Reviewer** | Validates docs against SDD compliance | Add `27-spec-driven-development.md` as rule source |
| **GitHub Actions** | Automated RTM completeness check | Run spec-conformance script on PR |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
