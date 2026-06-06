# Agentic AI Governance Standards

> **Purpose:** This rule file defines governance, safety, and oversight standards for
> autonomous AI agents used in enterprise software delivery. As AI agents gain the ability
> to write code, execute commands, call APIs, and make architectural decisions, disciplined
> governance becomes a non-negotiable engineering concern.

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [27 - Spec-Driven Development](./27-spec-driven-development.md) | Specs constrain agent behavior |
| [28 - Context Engineering](./28-context-engineering.md) | Context design for agent isolation |
| [07 - Security Architecture](./07-security-architecture.md) | Security controls for agents |
| [18 - Architecture Governance](./18-architecture-governance.md) | Broader governance framework |

---

## 1. Why Agentic Governance?

AI agents in 2025+ can: write and commit code, execute terminal commands, call external APIs,
modify infrastructure, provision cloud resources, and chain decisions across multiple steps.

Without governance, agents create: unreviewed code merges, unauthorized API calls, data leakage,
runaway cloud costs, compliance violations, and irreversible system changes.

---

## 2. Agent Classification

### 2.1 Autonomy Levels

| Level | Name | Behavior | Human Gate |
|-------|------|---------|-----------|
| L0 | Suggestion | Agent proposes; human executes | Every action |
| L1 | Supervised | Agent executes within pre-approved scope | Review before commit |
| L2 | Verified | Agent executes; human reviews artifact before propagation | Review before deploy |
| L3 | Monitored | Agent executes autonomously; alerts on anomaly | Anomaly-triggered only |
| L4 | Autonomous | Agent fully autonomous within policy bounds | Audit log review only |

**Rule:** Production infrastructure changes MUST NOT exceed L2.
**Rule:** Regulated system changes (PII, financial, health) MUST NOT exceed L1.
**Rule:** New service creation or database migrations MUST NOT exceed L1.

### 2.2 Agent Risk Classification

| Risk Level | Agent Capabilities | Required Controls |
|-----------|--------------------|------------------|
| **Critical** | Infra provisioning, DB writes, secret access | L1 max, dual approval, immutable audit log |
| **High** | Code commit, API calls with side effects, file writes | L2 max, automated scan, human review |
| **Medium** | Read-only API calls, spec generation, analysis | L3 acceptable, output validation |
| **Low** | Summarization, documentation, search | L4 acceptable, sampling audit |

---

## 3. Agent Safety Controls

### 3.1 Mandatory Safety Boundaries (Constitution Enforcement)

Every agent deployment MUST enforce:

- [ ] **Scope boundary:** Agent can ONLY access files/APIs listed in its task context
- [ ] **No-write zones:** Define protected paths/resources agents cannot modify (e.g., `/.env`, migration files, production configs)
- [ ] **Command allowlist:** Shell/CLI commands available to agents are explicitly allowlisted � deny by default
- [ ] **External network isolation:** Agents in dev/test MUST NOT call production APIs
- [ ] **Secret protection:** Agents MUST NOT log, print, or include secrets in any artifact
- [ ] **Cost guardrails:** Max spend per agent run defined and enforced via budget alerts
- [ ] **Time-to-live:** Agent runs have a maximum execution time (prevent infinite loops)

### 3.2 Human-in-the-Loop (HITL) Gates

Define checkpoints where human review is mandatory:

| Gate | Trigger | Required Action |
|------|---------|----------------|
| **Spec Gate** | Before implementation begins | Architect approves requirements.md and design.md |
| **Security Gate** | Any change to auth, secrets, or PII handling | Security architect sign-off |
| **Schema Gate** | Database migration scripts | DBA/architect review |
| **Infra Gate** | IaC changes affecting production | Platform team review |
| **Merge Gate** | PR with agent-generated code | Human code review (cannot be agent-reviewed agent code) |
| **Anomaly Gate** | Agent behavior deviates from spec | Automatic stop; human investigation required |

### 3.3 Blast Radius Minimization

- Agents MUST operate on feature branches � never directly on `main` or `release`
- Each agent task MUST be scoped to the minimum set of files required
- Destructive operations (deletes, truncates, revokes) MUST require explicit human confirmation
- Agent changes MUST be reversible: no irreversible action without a documented rollback

---

## 4. Agent Audit and Traceability

### 4.1 Mandatory Audit Log Fields

Every agent action MUST be logged with:

```json
{
  "agent_id": "coder-agent-001",
  "agent_type": "CodingAgent",
  "session_id": "sess-abc123",
  "task_id": "T-03",
  "action_type": "file_write | api_call | command_exec | code_commit",
  "timestamp": "2026-05-14T10:00:00Z",
  "resource_affected": "src/services/payment.service.ts",
  "input_summary": "Implementing PaymentService.process() per Task T-03",
  "output_summary": "Created file, 87 lines, 3 methods",
  "constitution_check": "PASS | WARN | FAIL",
  "human_review_required": false,
  "triggered_by": "human | orchestrator-agent | schedule"
}
```

### 4.2 Audit Retention and Access

- Audit logs MUST be immutable (write-once, append-only storage)
- Retention: minimum 1 year for general agents; 7 years for agents in regulated domains
- Access: audit logs MUST be accessible to security and compliance teams at all times
- Alerting: anomalous patterns (high failure rate, unexpected resource access) MUST trigger real-time alerts

---

## 5. Multi-Agent Orchestration Governance

### 5.1 Orchestrator Responsibilities

The orchestrator agent is the trust boundary manager:
- Maintains the master task plan
- Routes tasks to appropriate sub-agents with minimal context
- Enforces sequencing and dependency constraints
- Escalates to human when any sub-agent fails or returns unexpected results
- Aggregates audit events from all sub-agents

### 5.2 Agent Trust Hierarchy

```
Human (highest trust)
   +-- Orchestrator Agent (system-level trust)
         +-- Spec Agent (read: specs; write: spec files only)
         +-- Design Agent (read: specs; write: design files only)
         +-- Coder Agent (read: design + code; write: feature branch only)
         +-- Test Agent (read: code + spec; write: test files only)
         +-- Security Agent (read: code; write: security report only)
```

**Rule:** Sub-agents cannot elevate their own trust level.
**Rule:** Sub-agents cannot directly communicate with each other � all routing goes through orchestrator.
**Rule:** Orchestrator cannot execute code directly; it delegates to specialist agents.

### 5.3 Agent Failure Handling

| Failure Type | Response |
|-------------|---------|
| Agent produces output violating constitution | Discard output; notify human; stop chain |
| Agent hits token limit mid-task | Checkpoint state; resume with fresh context |
| Agent produces contradictory results (vs spec) | Flag contradiction; human resolution required |
| Agent timeout | Mark task failed; human re-scopes or resumes |
| Agent API rate limit | Exponential backoff; surface cost warning |

---

## 6. Agentic CI/CD Integration

### 6.1 Agent-in-the-Pipeline Standards

When AI agents are part of CI/CD:

| Pipeline Stage | Agent Role | Gate |
|---------------|-----------|------|
| **Pre-commit** | Lint + constitution check | Block commit on constitution violation |
| **PR creation** | Spec conformance check | Require EARS traceability for changed features |
| **Code review** | Security scan + pattern check | Annotate PR; block merge on Critical findings |
| **Pre-deploy** | Infrastructure drift check | Block deploy if IaC diverges from approved design |
| **Post-deploy** | Anomaly detection (30-min watch) | Alert on SLO breach or unexpected behavior |

### 6.2 Agent Output Validation Gates

Before merging any agent-generated artifact:

- [ ] **Spec conformance:** Every changed function maps to a task in tasks.md
- [ ] **Constitution compliance:** No prohibited patterns (checked by static analysis or secondary agent)
- [ ] **Test presence:** No code change without corresponding test file change
- [ ] **Security scan:** SAST scan passes on agent-generated code
- [ ] **No credential exposure:** Secret scanner runs on all agent commits
- [ ] **Signed provenance:** Agent commits tagged with agent ID, task ID, and constitution version

---

## 7. Governance Checklist

- [ ] Agent autonomy level defined and enforced per environment (dev < staging < prod)
- [ ] Agent risk classification assigned; corresponding controls implemented
- [ ] No-write zones and command allowlist configured
- [ ] HITL gates defined for security, schema, infra, and merge events
- [ ] Audit log format implemented with all mandatory fields
- [ ] Audit logs are immutable with defined retention
- [ ] Orchestrator is sole routing authority; sub-agents cannot peer-communicate
- [ ] Agent failure handling covers timeout, contradiction, and violation
- [ ] CI/CD pipeline has pre-commit constitution check and pre-merge spec conformance check
- [ ] Agent commits signed with provenance (agent ID + task ID + constitution version)

---

*Archpilot � Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
