# Rule 35: Multi-Agent Contracts and Handoff Protocols
<!-- Category: Agentic Era | Level: Strategic | Enforces: Artifact-Driven Communication -->

## 1. Overview
As engineering workflows shift from single-agent coding to multi-agent orchestration (e.g., an Orchestrator Agent coordinating a Security Agent, a DBA Agent, and a Frontend Agent), unstructured agent-to-agent prompting leads to context degradation, hallucination loops, and loss of architectural intent.

This rule enforces **Artifact-Driven Handoffs**. Agents must *never* communicate via raw conversational memory. Instead, they must communicate by passing structured Archpilot artifacts (Specs, Tasks, Contracts) as the verifiable medium of exchange.

## 2. The Multi-Agent Trust Hierarchy
In a multi-agent system, authority must be clearly defined to prevent agents from overriding each other's work.

1. **The Lead Architect (Human):** Owns the `requirements.md` and `constitution.md`.
2. **The Orchestrator Agent:** Breaks down requirements into `tasks.md`. Has read/write access to design docs, but read-only access to code.
3. **Specialized Sub-Agents (DBA, SecOps, Frontend):** Execute specific tasks. Have read/write access *only* to code within their domain. Cannot alter the constitution or the primary spec.

## 3. The Artifact-Driven Handoff Protocol
When Agent A needs Agent B to perform a task, it must generate a structured **Handoff Contract**.

### 3.1 Handoff Contract Schema
A valid handoff must contain:
1. **Source Context:** Path to the relevant section of `design.md`.
2. **Bounding Box:** The exact files the sub-agent is permitted to read and modify.
3. **Task Definition:** The specific EARS requirement being fulfilled.
4. **Verification Gate:** How the orchestrator will verify the sub-agent's work (e.g., "Run `npm test`, zero lint errors").

### 3.2 Anti-Pattern: Conversational Delegation
**❌ Bad (Conversational):**
> *Orchestrator to DBA Agent:* "Hey, we need a users table for the auth service. Can you write the SQL migration for it? Make sure to include a password hash."

**✅ Good (Artifact-Driven):**
> *Orchestrator to DBA Agent:* 
> "Execute Task T-04 from `tasks.md`. 
> Context: `design.md` §3.1 (User Entity). 
> Allowed Files: `/migrations/*`. 
> Output: Generate Flyway migration script. 
> Constraints: Follow `constitution.md` (no PII in plaintext)."

## 4. Multi-Agent Code Reviews
When a Sub-Agent completes a task, the Orchestrator Agent or a dedicated Security Agent must perform an **Automated Code Review** before presenting it to the human.

The Review Agent must evaluate the diff against:
1. The original EARS requirement (Did it build the right thing?).
2. The `constitution.md` (Did it violate security or tech stack rules?).
3. The `data-contract.md` (Did it break producer/consumer compatibility?).

## 5. Dispute Resolution
If Sub-Agent B fails verification by the Review Agent 3 consecutive times (hallucination loop):
1. **Halt Execution:** The Orchestrator must immediately pause the loop.
2. **Escalate to Human (HITL):** Generate a summary of the failure (e.g., "DBA Agent cannot resolve schema conflict in `V2__add_users.sql`") and request human intervention. 
3. **Do Not Hallucinate Fixes:** The Orchestrator must not attempt to blindly rewrite the Sub-Agent's code to force a pass.

## 6. Token Economics & Context Passing
Do not pass the entire conversation history to a specialized agent.
* **Filter Context:** A Frontend Agent does not need the database schema design. Provide only the REST API payload definitions (`design.md` §4) and the specific UI task.
* **Max Context Budget:** Sub-agent context windows should be strictly budgeted to reduce latency and cost.
