# Changelog

All notable changes to the Archpilot standards library are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased] — Phase 7 (Planned)
### Planned
- Drift Detection script comparing implementation vs `design.md`
- Fitness Function runner (ArchUnit/Spectral CI gating)
- ADR DAG Visualizer for living decision graph

---

## [4.1.0] — 2026-06-07 — Pipeline Hardening, MCP Server, 3 New LLM Configs

### Added
- **MCP Server (`mcp_server.py`):** Exposes all 37 rules, 17 templates, and 5 personas as MCP resources (`archpilot://rules/{name}`, `archpilot://templates/{name}`, `archpilot://personas/{name}`). Tools: `list_rules()`, `get_rule()`, `list_templates()`, `list_personas()`, `run_lint()`, `calculate_nfrs()`. Add to Claude Code or Claude.ai with a single JSON config entry.
- **`pyproject.toml`:** `pip install -e .` now works; exposes `archpilot` as a proper CLI entry point — no more `cd` to repo root.
- **`llm-configs/gemini-instructions.md`:** System instructions for Google AI Studio, Vertex AI, and Gemini in Google Workspace.
- **`llm-configs/windsurf-rules.md`:** `.windsurfrules` for Windsurf (Codeium) IDE including Cascade-specific workflow guidance.
- **`llm-configs/aider-conventions.md`:** Recommended `.aider.conf.yml`, Python/TS conventions, and step-by-step Archpilot workflow for Aider terminal AI.
- **`.github/workflows/archpilot-lint.yml`:** Real GitHub Actions CI workflow that runs `archpilot lint --tier 2` on PRs touching `.specs/` or `rules/` (replaces the broken `workflows/archpilot-review.yml`).
- **`.gitignore`:** Covers `.specs/` (generated client docs), Python cache, venv, OS artefacts.

### Changed
- **Pipeline — Parallel LLD generation:** Phase 3 now uses `ThreadPoolExecutor` (max 4 workers). LLDs are independent — 3-5 services now generate concurrently, ~4× faster wall-clock.
- **Pipeline — Retry logic:** Exponential backoff on `RateLimitError` and HTTP 5xx errors (3 attempts). Pipeline no longer crashes on transient API issues.
- **Pipeline — Context budget doubled:** `cap()` limits raised across all phases (discovery 4k→8k, requirements 6k→12k, HLD 4k→8k, review artifacts 3k→6k). Claude sees significantly more of each artifact.
- **Pipeline — `max_tokens` default 8000→16000:** All phases produce materially more complete documents.
- **CLI — `--from-phase N`:** Resume `archpilot run` from any phase (0–4). Reads existing `.specs/` artifacts for earlier phases — saves re-burning tokens when iterating.
- **CLI — `--max-tokens`:** Override output token limit per Claude call from the command line.
- **CLI — `--format json` on `lint`:** Machine-readable `{"errors": [...], "warnings": [...]}` output for CI tooling.
- **CLI — `--version`:** `archpilot --version` now prints `archpilot 4.1.0`.
- **Lint tier fix:** Weak-word violations (`fast`, `scalable`, etc.) are `[WARN]` at Tier 1, `[ERROR]` at Tier 2+ (was always ERROR regardless of tier).
- **Lint false-positive fix:** Fenced code blocks are stripped before weak-word scanning — no more false positives on `fast` inside a Dockerfile or code example.
- **`init` message:** Uses `sys.argv[0]` instead of hardcoded `"python archpilot.py"`.
- **`requirements.txt`:** Added `mcp>=1.0.0`.

### Fixed
- **`tools/generate_diagrams.py`:** Hardcoded absolute Windows path (`d:\_elfor\...`) replaced with `Path(__file__)`-relative path — any contributor can now run this tool without editing source.
- **`rules/29-agentic-ai-governance.md`:** Repaired UTF-8 mojibake on related-standards table (rendered as broken boxes on GitHub).

### Removed
- **`workflows/archpilot-review.yml`:** Deleted — was in wrong directory (never ran), referenced non-existent published Action, used wrong API key. Superseded by `.github/workflows/archpilot-lint.yml`.
- **`dashboard/`:** Removed abandoned `dashboard/index.html` + `dashboard/style.css`. Production site is `docs/index.html`.

---

## [6.1.0] — 2026-05-15 — Enterprise Hardening
### Changed
- **Rule 00 (Architecture Principles):** Expanded to 25 KB+ with engineering physics, CI fitness functions, GreenOps, and chaos engineering standards
- **Rule 01 (Solution Design):** Expanded to 14.5 KB with queueing theory math, STRIDE threat modelling, 3-year TCO templates, and C4 Mermaid diagrams
- **Rule 02 (ADR Standards):** Expanded to 13.6 KB with DAG governance, Weighted Product Model scoring, Spectral CI linting YAML, and real-world Confluent Cloud ADR example
- **Rule 03 (HLD Standards):** Expanded to 7.6 KB with Integration Calculus, network egress math, capacity planning formulas, and Little's Law application
- **Rule 04 (LLD Standards):** Expanded to 14.4 KB with Saga Pattern sequence diagrams, Hexagonal Architecture Java examples, B-Tree indexing math, and Fencing Token distributed lock physics
- **Rule 05 (API Design):** Expanded to 10.9 KB with gRPC Protobuf immutability rules, GraphQL DataLoader N+1 defense, cursor pagination math, and Spectral CI/CD YAML
- **Mermaid Diagrams:** Fixed all diagrams to use universally supported `graph TD` syntax with ASCII fallbacks

### Fixed
- Typo in README: "architecure" → "architecture"
- README file tree alignment (`│` missing from persona section)
- Stale file size figures in README rule table
- Stale `~760 KB` total count (actual: ~410 KB)
- Stale `~750KB` count in docs/index.html hero

### Removed
- Duplicate file `rules/27-ai-assisted-development.md` (superseded by `27-spec-driven-development.md`)

### Cleaned
- Removed `⭐ NEW` labels from Phase 6 items in README tree (no longer "new")
- Updated README total count: `36 rules | 17 templates | 5 LLM configs`

---

## [6.0.0] — 2026-05-14 — Spec-Driven & Agentic Era
### Added
- **Rule 27:** Spec-Driven Development (EARS notation, Spec-Kit triad, RTM)
- **Rule 28:** Context Engineering (5-layer LLM context stack, RAG standards, token budgets)
- **Rule 29:** Agentic AI Governance (5-level autonomy model, HITL gates, blast radius)
- **Rule 30:** Platform Engineering (IDP, golden paths, service catalog, platform SLOs)
- **Rule 31:** API Governance (full lifecycle, versioning policy, DX checklist)
- **Rule 32:** Data Contracts (YAML contract schema, compatibility matrix, drift detection)
- **Rule 33:** Resilience & Chaos Engineering (GameDay playbook, 7-step chaos loop)
- **Rule 34:** Sustainability & Green Architecture (SCI formula, carbon-aware patterns)
- **Rule 35:** Multi-Agent Contracts (artifact-driven handoffs, trust hierarchy, bounding boxes)
- **Templates:** spec-template.md, design-spec-template.md, task-list-template.md, constitution-template.md, data-contract-template.md, multi-agent-handoff-template.md
- **LLM Config:** kiro-steering-instructions.md for AWS Kiro

---

## [5.0.0] — Deep Coverage
### Added
- Rule 22: Multi-Tenancy (Silo/Bridge/Pool, SaaS patterns)
- Rule 23: Stakeholder Communication (STAR-T, audience adaptation)
- Rule 24: Team Topology (Conway's Law, team types, scaling)
- Rule 25: Domain-Driven Design (bounded contexts, aggregates, events)
- Rule 26: AI/ML Architecture (MLOps, model serving, responsible AI)
- Templates: capacity-planning.md, technology-radar.md
- Sample output: sample-sdd.md (Customer Portal)

---

## [4.0.0] — Lifecycle & Governance
### Added
- Rule 16: Estimation Framework (T-shirt, Story Points, FPA, PERT)
- Rule 17: Migration & Modernization (Strangler Fig, dual-write)
- Rule 18: Architecture Governance (ARB, tech radar)
- Rule 19: Incident Management & Post-Mortem
- Rule 20: Testing Strategy (Test Pyramid, contract testing, chaos)
- Rule 21: Tech Debt Management Framework
- Templates: go-live-checklist.md, runbook-template.md, post-mortem-template.md, rfp-response-template.md, handover-checklist.md
- Persona: startup-cto.md
- Examples: sample-migration-plan.md, sample-estimation.md

---

## [3.0.0] — Platform Configs & Examples
### Added
- LLM Config: vscode-copilot-instructions.md
- LLM Config: cursor-rules.md
- LLM Config: chatgpt-custom-gpt.md
- Personas: security-architect.md, presales-solutioner.md
- Examples: sample-lld.md, sample-hld.md, sample-adr.md

---

## [2.0.0] — Extended Standards
### Added
- Rule 01: Solution Design Standards + template
- Rule 06: Data Architecture
- Rule 10: Integration Patterns (Event-Driven, CDC, Webhooks, API Gateway)
- Rule 08: Cloud Architecture (12-Factor, IaC, HA/DR)
- Rule 12: Observability (Logging, Metrics, Tracing, Alerting)
- Rule 13: DevOps & CI/CD (Pipelines, Docker, GitOps)
- Rule 14: Cost Optimization / FinOps

---

## [1.0.0] — Core
### Added
- Rule 00: Architecture Principles
- Rule 04: LLD Standards + Template
- Rule 03: HLD Standards + Template
- Rule 02: ADR Standards + Template
- Rule 05: API Design Standards
- Rule 07: Security Architecture
- Rule 09: Microservices Patterns
- Rule 11: NFR Checklist (69 checks)
- LLM Config: claude-project-instructions.md
- Persona: enterprise-architect.md
