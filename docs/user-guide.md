# Archpilot User Guide

Welcome to Archpilot. This guide outlines the end-to-end workflow for using the Archpilot Enterprise Standards Library to move from a vague client request to a production-ready, spec-driven engineering plan.

## The Archpilot End-to-End Workflow

### Phase 0: Discovery & Ambiguity Resolution
*Stop building systems for the wrong problems.*

When presented with a vague request (e.g., "Build a high-scale real-time dashboard"), do not jump to design.
1. **Apply Rule 36**: Trigger `rules/36-discovery-ambiguity.md`.
2. **Use the Template**: Generate a `discovery-template.md` to map out the 5 Vectors (Scale, Failure, Security, State, Cost) and establish clear architectural trade-offs (e.g., Event-Sourced vs CRUD).
3. **Log Risks**: Track unvalidated constraints using `assumption-log-template.md`.
4. **Size the Project**: If this is a presales/fixed-bid engagement, use `estimation-abacus-template.md` to apply complexity multipliers and risk buffers.

### Phase 1: Spec-Driven Requirements
*Write requirements that code can be tested against.*

Once Phase 0 constraints are validated by the business:
1. **Apply Rule 27**: Trigger Spec-Driven Development (`rules/27-spec-driven-development.md`).
2. **Write Requirements**: Use `spec-template.md` to define functional requirements using the strict EARS syntax (Event-Driven, Unwanted Behavior, State-Driven, Optional Feature, Complex).
3. **Establish RTM**: Every requirement must be tracked in the Requirements Traceability Matrix (RTM).

### Phase 2: Technical Design & Physics
*Design the system within the bounds of physics and enterprise standards.*

1. **Calculate Physics**: Run `tools/nfr_calculator.py` with your TPS, payload, and SLA targets to automatically generate your 50+ NFR limits (Database IOPS, AWS Egress, Concurrency).
2. **Draft the HLD/LLD**: Use either `hld-template.md` or `lld-template.md` depending on the scope.
3. **Use Diagram Archetypes**: Do not write Mermaid from scratch. Copy the required patterns (e.g., Saga, Outbox, Active-Active) from the `diagrams/` folder and adapt them to your specific components.
4. **Audit**: Ensure the design complies with the core principles (`rules/00-architecture-principles.md`) and specific domain rules (e.g., `05-api-design.md`, `07-security-architecture.md`).

### Phase 3: Task Breakdown & Constitution
*Prepare for Agentic AI or Human execution.*

1. **Write the Constitution**: Define the non-negotiable tech stack and bounded contexts in `constitution-template.md`. This prevents AI agents from hallucinating random libraries (e.g., importing React when the stack is Vue).
2. **Generate Tasks**: Break the design down into 2-4 hour atomic tasks using `task-list-template.md`. Every task MUST include verifiable Acceptance Criteria.

---

## Tooling Cheat Sheet

### NFR Physics Calculator
Calculate the exact physics of your architecture:
```bash
python tools/nfr_calculator.py --tps 2000 --payload 1.5 --retention 30 --latency 50 --sla 99.99
```

### Mermaid Archetype Generator
If you need to regenerate the 22+ archetypes:
```bash
python tools/generate_diagrams.py
```

### LLM Configurations
Load Archpilot into your favorite LLM:
*   **Claude Projects**: Upload the `rules/` folder and paste `llm-configs/claude-project-instructions.md`.
*   **Cursor IDE**: Copy `llm-configs/cursor-rules.md` to your repo as `.cursorrules`.
*   **GitHub Copilot**: Copy `llm-configs/vscode-copilot-instructions.md` to `.github/copilot-instructions.md`.
