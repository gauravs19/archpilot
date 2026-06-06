# Archpilot User Guide

**Version:** 2.0 — Agentic Pipeline Edition  
**Covers:** CLI pipeline, lint tiers, static library mode, platform configs, reference example

---

## What Archpilot Is

Archpilot is two things in one repository:

| Mode | What it does | When to use |
|------|-------------|-------------|
| **Agentic Pipeline** | `archpilot run` — takes one requirement, runs 5 AI agent phases, produces 6 production-grade artifacts automatically | Greenfield projects, new services, ARB submissions |
| **Standards Library** | 36 rule files + 17 templates you load into Claude, Cursor, Kiro, or Copilot | Code reviews, ad-hoc design, enforcing standards in an existing project |

Both modes share the same rules and templates. The pipeline just automates the workflow that the library supports manually.

---

## Quick Start (3 Steps)

```bash
# 1. Initialize a project
python archpilot.py init my-project

# 2. Write your requirement
#    Edit: my-project/.specs/Input.md

# 3. Run the pipeline
python archpilot.py run my-project
```

Output in `my-project/.specs/`:
```
discovery.md                          ← Phase 0: 15-dimension deep discovery
requirements.md                       ← Phase 1: Epics + EARS stories + RTM
Design_HLD.md                         ← Phase 2: C4 diagrams + ADRs + cost model
Design_LLD_<ServiceName>.md           ← Phase 3: 3–5 service LLDs (repeated)
review_report.md                      ← Phase 4: Scored guardrail audit
```

Then validate everything:
```bash
python archpilot.py lint --tier 3 --dir my-project
```

---

## The 5-Phase Pipeline

Each phase is an AI agent with a defined mandate, a set of enforced rules, and a structured output contract. Every artifact feeds the next phase. The pipeline fails fast if a mandatory constraint is violated.

### Phase 0 — SE Agent: Deep Discovery

**Input:** `Input.md` (your requirement)  
**Output:** `discovery.md`  
**Rule enforced:** `rules/50-agent-pipeline.md` (15-dimension mandate)

The SE Agent fills 15 quantified dimensions before any design starts. No phase can proceed until all 15 are populated with real numbers — no placeholders, no "TBD".

| Dimension | What it captures |
|-----------|-----------------|
| Technical Physics | Throughput (TPS), Little's Law concurrency, latency budget breakdown |
| Regulatory & Compliance | FAA/EASA/GDPR/PCI requirements with specific citation |
| Security & Threat Surface | STRIDE model per component |
| Failure & Resilience | RPO/RTO per failure scenario; CAP decision per data domain |
| Cost & FinOps | 3-year TCO with infra, SaaS, and personnel breakdown |
| Data Residency & Sovereignty | Per-region storage constraints |
| Edge & Hardware Constraints | SDK versions, firmware limits, offline capability |
| Connectivity & Integration | Protocol choices, retry semantics, third-party SLAs |
| Observability Requirements | Metrics, trace coverage, alert SLAs |
| Lifecycle & Maintainability | Team size, runbook coverage, upgrade cadence |
| Human Interface & UX | Persona descriptions, latency expectations |
| Data Privacy & Ethics | PII fields, consent model, retention limits |
| Third-Party Dependencies | Vendor lock-in risk, EOL dates |
| Scaling & Multi-Tenancy | Tenant model, isolation mechanism, noisy-neighbor controls |
| Environmental & Sustainability | SCI score target, carbon-aware scheduling |

**10:10:15:50 Mandate (Rule 50):** ≥15 dimensions • 10–20 Epics • 50–150 Stories • 3–5 LLDs • Review ≥80/100

---

### Phase 1 — PO Agent: Requirements Breakdown

**Input:** `discovery.md`  
**Output:** `requirements.md`  
**Rules enforced:** EARS notation, MoSCoW, story point ranges, NFR tag coverage

The PO Agent produces a structured multi-level requirements document:
- **10–20 Epics** across 8 categories (Functional, Data, Security, Integration, NFR, DevOps, Testing, Migration)
- **50–150 User Stories** in full EARS notation with acceptance criteria
- **Requirements Traceability Matrix (RTM)** linking each story to a discovery dimension

**EARS notation — 5 patterns enforced:**

| Pattern | Template | Trigger |
|---------|----------|---------|
| Event-Driven | `WHEN [trigger], the [system] SHALL [action]` | State changes, user actions |
| Unwanted | `IF [condition], the [system] SHALL [action]` | Error paths, failures |
| State-Driven | `WHILE [state], the [system] SHALL [action]` | Ongoing conditions |
| Optional | `WHERE [feature], the [system] SHALL [action]` | Feature flags, regional |
| Ubiquitous | `The [system] SHALL [action]` | Always-on constraints |

Every acceptance criterion must be measurable (no "fast", "robust", "seamless" — must be `<200ms p95`, `≥99.9% uptime`, etc.).

---

### Phase 2 — Arch Agent: High-Level Design

**Input:** `discovery.md` + `requirements.md`  
**Output:** `Design_HLD.md`  
**Rules enforced:** `rules/03-hld-standards.md`, C4 mandatory, ADR mandatory

Mandatory HLD sections (all 14 must be present):

1. Architecture Goals (quantified)
2. System Context Diagram (C4 Level 1 — Mermaid)
3. Container Diagram (C4 Level 2 — Mermaid)
4. Data Flow Diagrams (≥3 sequence diagrams)
5. Technology Stack (per service with justification)
6. Data Architecture (storage per domain)
7. Security Architecture (zero-trust, mTLS, RBAC)
8. NFR Targets (12+ categories, all numeric)
9. Integration Catalog (all third-party with protocols)
10. Cost Model (monthly + peak, budget comparison)
11. Architecture Decision Records (≥3 ADRs)
12. Risk Register (with mitigations)
13. Roadmap (phased delivery)
14. Design Rationale + Implementation Strategy (narrative)

---

### Phase 3 — Arch Agent: Low-Level Designs (× 3–5 services)

**Input:** `Design_HLD.md` + `requirements.md` + `discovery.md`  
**Output:** `Design_LLD_<ServiceName>.md` per service  
**Rules enforced:** `rules/04-lld-standards.md`, 12 mandatory sections

The agent extracts the top 3–5 services from the HLD container diagram and writes a full LLD for each.

Mandatory LLD sections per service:

| Section | What it contains |
|---------|-----------------|
| Service Overview + Bounded Context | Purpose, invariants, critical safety constraints |
| Design Rationale | WHY this language/framework/pattern was chosen |
| Implementation Strategy | Phased delivery plan (Phase 1 MVP → Phase N) |
| Component Diagram | Internal modules (Mermaid) |
| Class / Data Structure Diagram | Key types with fields and methods (Mermaid) |
| Data Model | PostgreSQL schema SQL, Redis key design, S3 layout |
| API Specification | REST endpoints, WebSocket events, Kafka schemas (Avro) |
| State Machine | FSM diagram for stateful services (Mermaid) |
| Sequence Diagrams | ≥3: happy path, error path, edge case |
| Error Handling | Retry policies with explicit ms values, circuit breaker thresholds, DLQ strategy |
| Performance Design | Throughput targets per operation, scaling policy, KEDA YAML |
| Security Design | STRIDE mitigations, IRSA, NetworkPolicy |
| Observability | Structured log schema, 6+ metrics, trace spans, alert rules with thresholds |
| Deployment | Distroless Dockerfile, Kubernetes Deployment YAML, NetworkPolicy YAML |

---

### Phase 4 — Review Agent: Guardrail Audit

**Input:** All 5 preceding artifacts  
**Output:** `review_report.md`  
**Gate:** Score ≥80/100 to PROCEED; below 80 = REWORK

The Review Agent audits 12 dimensions and produces:
- Per-dimension score (0–100)
- Overall weighted score
- Findings by severity: Critical → High → Medium → Low
- PROCEED / REWORK gate decision

**12 Audit Dimensions:**

| Dimension | What's checked |
|-----------|---------------|
| Discovery Completeness | All 15 dimensions populated, quantified, and cited in HLD |
| Requirements Quality | EARS compliance, measurable ACs, story count in range |
| HLD Completeness | All 14 sections present, C4 diagrams valid, ADRs complete |
| LLD Completeness | All 12 sections per service, no placeholder values |
| NFR Coverage | All targets numeric, traced to HLD and LLD |
| Security Design | STRIDE per component, zero-trust, IRSA, NetworkPolicy |
| Regulatory Compliance | FAA/EASA/GDPR requirements traced to implementation |
| Observability Coverage | Golden signals covered, P1/P2 alert rules present |
| Cost Modeling | Monthly + peak costs, budget check, regional breakdown |
| Traceability | RTM complete, stories → HLD → LLD → tests |
| Anti-Pattern Detection | Tenant cross-contamination, shared mutable state, silent failure |
| Operational Readiness | Health checks, graceful shutdown, migration strategy |

---

## CLI Reference

```bash
# Initialize a project with .specs/ scaffold
python archpilot.py init [--dir <path>]

# Run the full 5-phase agentic pipeline
python archpilot.py run [--dir <path>] [--model <id>] [--from-phase N] \
                        [--max-tokens N] [--persona <slug>] [--dry-run]

# Run only Phase 4 (review) on existing artifacts
python archpilot.py review [--dir <path>] [--model <id>] [--max-tokens N]

# Lint artifacts against guardrail rules
python archpilot.py lint [--dir <path>] [--tier 1|2|3] [--format text|json]

# Detect drift between LLD spec endpoints and source code
python archpilot.py drift [--dir <path>] [--src <source-dir>] [--format text|json]

# Show help / version
python archpilot.py --help
python archpilot.py --version
```

### `run` Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--dir` | `.` | Directory containing `.specs/Input.md` |
| `--model` | `claude-sonnet-4-6` | Claude model ID |
| `--from-phase N` | `0` | Resume from phase N (0–4); reads existing artifacts for phases < N |
| `--max-tokens N` | `16000` | Max output tokens per Claude call |
| `--persona <slug>` | _(none)_ | Inject a persona to tune agent communication style (see Personas) |
| `--dry-run` | `false` | Print what each phase would do without calling the Claude API |

**Resume example** — regenerate only the HLD and LLD after editing `discovery.md`:
```bash
python archpilot.py run --dir my-project --from-phase 2
```

**Dry-run example** — check pipeline configuration without spending API credits:
```bash
python archpilot.py run --dir my-project --dry-run
```

### Lint Tiers

| Tier | What it checks | Use when |
|------|---------------|----------|
| `--tier 1` | Placeholder detection (TODO, TBD, FIXME), discovery dimension count | Quick pre-review scan |
| `--tier 2` | + weak-word errors, Epic/Story counts, measurable NFR targets | Before HLD handoff |
| `--tier 3` | + LLD narrative sections, governance artifacts, diagram count | Before ARB submission |

```bash
# Text output (default)
python archpilot.py lint --tier 2 --dir my-project

# JSON output for CI tools / scripting
python archpilot.py lint --tier 2 --dir my-project --format json
```

Lint exits with code 1 on any error — use as a CI gate:

```yaml
# .github/workflows/archpilot-lint.yml
- name: Lint architecture specs
  run: python archpilot.py lint --tier 2 --dir .
```

### `drift` Command

Compares API endpoints declared in `Design_LLD_*.md` files against actual HTTP route registrations found in source code (Python/FastAPI/Flask, Node/Express, Go/Gin, Java/Spring).

```bash
# Auto-detect source directory
python archpilot.py drift --dir my-project

# Specify source directory explicitly
python archpilot.py drift --dir my-project --src my-project/src

# JSON output for pipeline integration
python archpilot.py drift --dir my-project --format json
```

Exit codes: `0` = no drift, `1` = drift detected.

---

## Personas

Personas tune the communication style and emphasis of every AI agent in the pipeline without changing the underlying quality rules. Pass one with `--persona` when running the pipeline:

```bash
python archpilot.py run --dir my-project --persona startup-cto
```

| Persona slug | Best for | Communication style |
|---|---|---|
| `enterprise-architect` | Corporate ARB submissions, regulated industries | Formal, multi-stakeholder, ADR-heavy |
| `startup-cto` | Seed/Series-A products, fast iteration | Pragmatic, MVP-first, cost-aware |
| `security-architect` | BFSI, healthcare, defence systems | Threat-model-first, zero-trust by default |
| `presales-solutioner` | RFP responses, client-facing proposals | Business outcome focus, ROI framing |
| `vibe-code-reviewer` | Developer-facing LLD review | Direct, opinionated, code-idiomatic |

Persona files live in `llm-configs/personas/`. You can edit them or add custom personas — the pipeline picks them up automatically.

---

## Pushing to Jira / Azure DevOps

After the pipeline runs, push all generated Epics and User Stories directly to your issue tracker — no copy-paste.

```bash
# Push to Jira
archpilot push --target jira --dir my-project

# Push to Azure DevOps
archpilot push --target ado --dir my-project

# Preview without making any API calls
archpilot push --target jira --dir my-project --dry-run

# Create Epics only (check hierarchy before committing stories)
archpilot push --target jira --dir my-project --epics-only
```

### Configuration — env file (recommended)

Instead of exporting environment variables every session, create a `.archpilot.env` file in your project root (it is gitignored automatically):

```bash
cp .archpilot.env.example .archpilot.env
# then edit .archpilot.env with your credentials
```

```ini
# .archpilot.env  — never commit this file
JIRA_URL=https://yourorg.atlassian.net
JIRA_EMAIL=you@yourorg.com
JIRA_API_TOKEN=your_token_here
JIRA_PROJECT_KEY=ARCH

ADO_ORG=myorg
ADO_PROJECT=ArchProject
ADO_PAT=your_pat_here

ANTHROPIC_API_KEY=sk-ant-...
```

Search order: `<project>/.archpilot.env` → `<project>/archpilot.env` → `~/.archpilot.env`. Environment variables already set in the shell always take priority over file values.

### Jira setup

```bash
# Option A: config file (recommended)
cp .archpilot.env.example .archpilot.env  # fill in JIRA_* keys
archpilot push --target jira --dir my-project

# Option B: shell env vars
export JIRA_URL="https://yourorg.atlassian.net"
export JIRA_EMAIL="you@yourorg.com"
export JIRA_API_TOKEN="<token from id.atlassian.com → Security → API tokens>"
export JIRA_PROJECT_KEY="ARCH"
archpilot push --target jira --dir my-project
```

What gets created per Epic: **Epic** issue with category label, business value in description, and Definition of Done bullet list.

What gets created per Story: **Story** issue linked to its parent Epic, with the full `As a / I want / So that` narrative, EARS acceptance criteria as a numbered list, story points, MoSCoW priority, and NFR tags as labels.

### Azure DevOps setup

```bash
export ADO_ORG="myorg"
export ADO_PROJECT="ArchProject"
export ADO_PAT="<Personal Access Token — Work Items: Read & Write>"

archpilot push --target ado --dir my-project
```

ADO work item types: **Epic** (for epics) and **User Story** (for stories) with a parent-child hierarchy link. Acceptance criteria map to the ADO `Microsoft.VSTS.Common.AcceptanceCriteria` field. Story points map to `Microsoft.VSTS.Scheduling.StoryPoints`.

### Idempotency

A `.specs/push_manifest.json` file tracks every pushed ID. Re-running `archpilot push` skips already-pushed items — safe to run after adding new epics to `requirements.md`.

```json
{
  "target": "jira",
  "project": "ARCH",
  "pushed_at": "2026-06-07T10:00:00+00:00",
  "epics": {
    "EP-01": {"key": "ARCH-1", "url": "https://yourorg.atlassian.net/browse/ARCH-1"}
  },
  "stories": {
    "EP-01-S-01": {"key": "ARCH-13", "url": "..."}
  }
}
```

---

## MCP Server

Archpilot ships an [MCP](https://modelcontextprotocol.io) server (`mcp_server.py`) that exposes the entire standards library — rules, templates, personas, diagrams — as resources and tools. Any MCP-compatible client (Claude Code, Claude Desktop, Cursor) can read rules on demand without copy-pasting files.

### Setup

Add to your Claude Code settings (`~/.claude/settings.json` or workspace settings):

```json
{
  "mcpServers": {
    "archpilot": {
      "command": "python",
      "args": ["/path/to/archpilot/mcp_server.py"]
    }
  }
}
```

Then restart Claude Code. The server starts automatically via stdio transport.

### Resources

| Resource URI | Returns |
|---|---|
| `archpilot://rules/index` | Table of all rules with descriptions |
| `archpilot://rules/{name}` | Full content of a rule (e.g. `03-hld-standards.md` or just `03`) |
| `archpilot://templates/index` | Table of all templates |
| `archpilot://templates/{name}` | Full content of a template |
| `archpilot://personas/{name}` | Full content of a persona file |
| `archpilot://diagrams/{name}` | Mermaid archetype diagram |

### Tools

| Tool | Description |
|---|---|
| `list_rules()` | Structured index of all rules — call this first to discover what's available |
| `get_rule(name)` | Fetch a rule by filename or numeric prefix (`"03"` → `03-hld-standards.md`) |
| `search_rules(query)` | Full-text keyword search across all rule files — returns file, description, and matching excerpt |
| `list_templates()` | Index of all templates |
| `list_personas()` | List available persona slugs |
| `run_lint(directory, tier)` | Run archpilot lint and return structured JSON results |
| `calculate_nfrs(tps, payload_kb, retention_days, ...)` | Run the NFR physics calculator (50+ metrics) |

**Example Claude Code session:**

```
User: What does Rule 07 say about zero-trust?

Claude Code: [calls get_rule("07")]
             "Rule 07-security-architecture.md: All services must assume zero-trust..."
```

---

## NFR Physics Calculator

Before running the pipeline (or as part of Phase 2 design), calculate the engineering physics of your system:

```bash
python tools/nfr_calculator.py --tps 5000 --payload 2.5 --retention 30 --latency 150
```

Outputs 50+ calculated metrics including:
- **Throughput:** MB/sec, daily/monthly egress
- **Storage:** Total TB with index overhead
- **Compute:** Required threads (Little's Law), estimated pod count
- **Database:** Baseline + surge IOPS
- **Cost:** AWS Cross-AZ routing estimate

Use these numbers to populate the Physics dimension in `discovery.md` and to set NFR targets in `requirements.md`.

---

## Standards Library Mode (Without Pipeline)

If you prefer to work artifact-by-artifact with your existing LLM workflow, load individual rules as context:

### Option A: Claude Projects

1. Create a Claude Project
2. Paste `llm-configs/claude-project-instructions.md` as custom instructions
3. Upload relevant rule files as project knowledge
4. Ask: *"Create an LLD for a payment service using EARS notation"*

**Recommended rule set for LLD work:**
- `rules/00-architecture-principles.md`
- `rules/04-lld-standards.md`
- `rules/07-security-architecture.md`
- `rules/12-observability-standards.md`
- `templates/lld-template.md`

### Option B: AWS Kiro

```
.kiro/steering/archpilot-standards.md
```
Copy from `llm-configs/kiro-steering-instructions.md`. Kiro enforces EARS notation and the Specify → Plan → Task → Implement loop natively.

### Option C: Cursor IDE

```bash
cp llm-configs/cursor-rules.md .cursorrules
```

Then in Cursor composer:
```
Implement Task T-03 from .specs/tasks.md.
Follow constitution.md constraints.
Reference .specs/design.md §3 for data models.
```

### Option D: GitHub Copilot

```bash
cp llm-configs/vscode-copilot-instructions.md .github/copilot-instructions.md
```

### Option E: Any LLM (ChatGPT, Gemini, etc.)

Paste rule content directly into the conversation:
```
Follow these standards: [paste rules/04-lld-standards.md]

Now create an LLD for a notification service. Include:
- Class diagram
- Sequence diagrams (happy path + retry)
- PostgreSQL schema
- Error handling with explicit retry ms values
- KEDA autoscaling config
```

---

## Spec-Kit Workflow (Manual)

For projects where you want to apply the Specify → Plan → Task → Implement discipline without running the full pipeline:

```bash
mkdir -p .specs
cp templates/spec-template.md        .specs/requirements.md
cp templates/design-spec-template.md .specs/design.md
cp templates/task-list-template.md   .specs/tasks.md
cp templates/constitution-template.md constitution.md
```

**Workflow:**
1. Fill `requirements.md` with EARS stories (one per AC)
2. Fill `design.md` with component design, data models, API contracts
3. Break design into atomic tasks in `tasks.md` (each ≤4 hours, with verifiable ACs)
4. Lock non-negotiables in `constitution.md` (tech stack, security rules, AI agent boundaries)
5. Feed one task at a time to your AI agent: *"Implement Task T-03. Follow constitution.md."*

---

## Mermaid Diagram Library

22+ pre-built Mermaid archetypes in `diagrams/`. Copy the relevant pattern and adapt component names — don't write Mermaid syntax from scratch.

| # | Pattern | When to use |
|---|---------|-------------|
| 01 | C4 Context | System context diagram (HLD) |
| 02 | Saga Choreography | Distributed transaction rollback |
| 03 | Active-Active Failover | Multi-region HA |
| 04 | API Gateway | Routing + auth at the edge |
| 05 | Event Sourcing + CQRS | Audit trail, eventual consistency |
| 06 | Strangler Fig | Monolith migration |
| 07 | Micro-Frontend | Shell/remote composition |
| 08 | Outbox Pattern | Transactional event publishing |
| 09 | Circuit Breaker | Resilience state machine |
| 10 | Service Mesh Sidecar | Envoy/Istio traffic management |
| 11 | OAuth2 / OIDC Flow | Authentication sequence |
| 12 | Bulkhead | Thread pool isolation |
| 13 | Fan-out / Fan-in | Worker aggregation |
| 14 | CDC Pipeline | Debezium change data capture |
| 15 | Two-Phase Commit | Distributed XA commit |
| 16 | BFF | Backends for Frontends |
| 17 | Serverless | AWS Lambda event flow |
| 18 | Medallion Lake | Bronze/Silver/Gold data lake |
| 19 | Cell-Based Architecture | Partitioned cellular DBs |
| 20 | Blue-Green Deployment | Zero-downtime traffic splitting |
| 21 | Cache-Aside | Redis read-through pattern |
| 22 | Retry + Exponential Backoff | Resilient retry sequence |

---

## Reference Example: DroneOps Fleet Management

A complete, lint-clean pipeline run is available in `examples/droneops-fleet-management/`. It demonstrates all 5 phases against a multi-tenant drone fleet SaaS requirement.

**Review score: 94.1/100 — PROCEED**

| Artifact | Highlights |
|----------|-----------|
| [Input.md](../examples/droneops-fleet-management/Input.md) | Multi-tenant FAA/EASA/DGCA drone SaaS, $2M MVP budget, 500 customers Year 2 |
| [discovery.md](../examples/droneops-fleet-management/discovery.md) | Little's Law: 25K msg/sec · $10.09M 3-year TCO · STRIDE per component · CAP per domain |
| [requirements.md](../examples/droneops-fleet-management/requirements.md) | 12 Epics, 68 EARS stories, MoSCoW, RTM |
| [Design_HLD.md](../examples/droneops-fleet-management/Design_HLD.md) | C4 L1+L2, 4 ADRs, $18.3K/month cost model, zero-trust security |
| [Design_LLD_Telemetry_Processor.md](../examples/droneops-fleet-management/Design_LLD_Telemetry_Processor.md) | Go · Avro · Timestream · KEDA ScaledObject YAML · distroless Dockerfile |
| [Design_LLD_Mission_Planning_Service.md](../examples/droneops-fleet-management/Design_LLD_Mission_Planning_Service.md) | Python · 8-state FSM · PostGIS geofence · LAANC auth · KMS token signing |
| [Design_LLD_Incident_Detection_Service.md](../examples/droneops-fleet-management/Design_LLD_Incident_Detection_Service.md) | Python · Welford anomaly detection · Redis sliding windows · heartbeat scanner |
| [review_report.md](../examples/droneops-fleet-management/review_report.md) | 12-dimension audit · 16 findings across 4 severity tiers · PROCEED gate |

---

## Rule Selection Guide

Not every engagement needs all 36 rules. Use this table to pick the right subset:

| Engagement Type | Start with these rules |
|----------------|----------------------|
| Greenfield system design | 00, 03, 04, 07, 08, 11, 27 |
| API design review | 00, 05, 31 |
| Data architecture | 06, 22, 32 |
| Security review | 07, 11, 29 |
| Cloud cost / FinOps | 08, 14, 34 |
| Legacy migration | 17, 09, 25 |
| ML / AI system | 26, 28, 29, 35 |
| Platform engineering | 30, 13, 24 |
| Enterprise governance | 18, 02, 23 |
| Agentic pipeline (full) | 50 (orchestrates all above) |

---

## Rule Numbering

Rules are numbered `00`–`37` and `50`. Numbers 38–49 are reserved for domain-specific rule packs that are shipped separately (IoT, BFSI, Healthcare, Government). Rule `50` (`50-agent-pipeline.md`) is intentionally at `50` because it is the orchestration governance rule — it references all other rules and must sit above them numerically to avoid circular references in tooling that sorts by prefix.

---

## Guardrail Checklist (Pre-Submission)

Before submitting any artifact to an Architecture Review Board, run through this checklist:

```
Discovery
[ ] All 15 dimensions populated with quantified values
[ ] Physics section includes Little's Law calculation
[ ] 3-year TCO with infra + SaaS + personnel breakdown
[ ] STRIDE model per major component
[ ] RPO/RTO specified per failure scenario
[ ] CAP decision documented per data domain

Requirements
[ ] 10–20 Epics covering all 8 categories
[ ] 50–150 stories, all in EARS notation
[ ] Every AC is measurable (no vague adjectives)
[ ] MoSCoW priority on every story
[ ] RTM linking stories → HLD components

HLD
[ ] C4 Level 1 and Level 2 diagrams present
[ ] ≥3 ADRs with alternatives and consequences
[ ] Cost model within approved budget
[ ] All NFR targets are numeric
[ ] Zero-trust security architecture documented

LLD (per service)
[ ] Bounded context and invariants stated
[ ] Design Rationale explains WHY (not what)
[ ] Implementation Strategy gives phased plan
[ ] ≥3 sequence diagrams (happy path + errors)
[ ] Retry policies have explicit ms values
[ ] KEDA or HPA config present
[ ] NetworkPolicy restricts egress
[ ] Distroless Dockerfile

Review Gate
[ ] archpilot lint --tier 3 passes (0 errors)
[ ] Review score ≥80/100
[ ] All Critical findings have resolution plan
```

---

## Troubleshooting

**`anthropic` SDK not found**
```bash
pip install -r requirements.txt
```

**Pipeline runs but output quality is low**  
Ensure `ANTHROPIC_API_KEY` is set. Without it, the pipeline falls back to the installed default model. Alternatively, run in Claude Code (no API key needed — Claude Code acts as each agent directly).

**Lint fails with "Vague adjective" errors**  
Replace qualitative adjectives with quantified targets:
- `fast` → `<200ms p95`
- `efficient` → `<$50/tenant/month`
- `robust` → `≥99.9% uptime`
- `seamless` → `<500ms activation time`

**Lint fails with "Missing Design Rationale"**  
Add a `## 1b. Design Rationale` section to the LLD explaining WHY the technology/pattern was chosen (tradeoffs, rejected alternatives, the deciding constraint).

**Score below 80 on review**  
Check the Critical findings section first — each critical finding typically costs 6–10 points. Resolve all critical findings before re-running `archpilot review`.
