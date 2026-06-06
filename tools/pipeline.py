#!/usr/bin/env python3
"""
Archpilot Agentic Pipeline Engine v4.1
Orchestrates the 5-stage pipeline:
  Phase 0: SE Agent     — Deep Discovery (15 dimensions)
  Phase 1: PO Agent     — Requirements Breakdown (Epics / Stories / Tasks)
  Phase 2: Arch Agent   — High-Level Design (HLD)
  Phase 3: Arch Agent   — Low-Level Design(s) (LLD per service, parallel)
  Phase 4: Review Agent — Guardrail Audit & Compliance Scorecard
"""

import os
import sys
import re
import json
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import anthropic
except ImportError:
    print("anthropic SDK not found. Run: pip install anthropic")
    sys.exit(1)

# ─── Paths ────────────────────────────────────────────────────────────────────
ARCHPILOT_ROOT = Path(__file__).parent.parent
RULES_DIR      = ARCHPILOT_ROOT / "rules"
TEMPLATES_DIR  = ARCHPILOT_ROOT / "templates"

# ─── Terminal color helpers ───────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def banner(phase_num, label):
    bar = "─" * 62
    print(f"\n{BOLD}{CYAN}{bar}{RESET}")
    print(f"{BOLD}{CYAN}  Phase {phase_num}: {label}{RESET}")
    print(f"{BOLD}{CYAN}{bar}{RESET}\n")

def ok(msg):   print(f"  {GREEN}✓{RESET} {msg}")
def info(msg): print(f"  {CYAN}→{RESET} {msg}")
def warn(msg): print(f"  {YELLOW}⚠{RESET} {msg}")
def err(msg):  print(f"  {RED}✗{RESET} {msg}")


# ─── File helpers ─────────────────────────────────────────────────────────────
def read_file(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def write_artifact(specs_dir: Path, filename: str, content: str) -> Path:
    path = specs_dir / filename
    path.write_text(content, encoding="utf-8")
    ok(f"Artifact saved → {path.name}")
    return path

def rule(name: str) -> str:
    return read_file(RULES_DIR / name)

def tmpl(name: str) -> str:
    return read_file(TEMPLATES_DIR / name)

def cap(text: str, chars: int) -> str:
    """Truncate text for context budget management."""
    return text[:chars] + "\n...[truncated for context]" if len(text) > chars else text


# ─── Claude caller (streaming) with retry ─────────────────────────────────────
def call_claude(
    client: anthropic.Anthropic,
    system_prompt: str,
    user_message: str,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 16000,
    max_retries: int = 3,
) -> str:
    for attempt in range(max_retries):
        try:
            full = []
            print(f"  {DIM}", end="", flush=True)
            with client.messages.stream(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            ) as stream:
                for chunk in stream.text_stream:
                    print(chunk, end="", flush=True)
                    full.append(chunk)
            print(f"{RESET}")
            return "".join(full)
        except anthropic.RateLimitError:
            wait = (2 ** attempt) * 10
            warn(f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Retrying in {wait}s...")
            time.sleep(wait)
        except anthropic.APIStatusError as e:
            if e.status_code in (529, 503, 502) and attempt < max_retries - 1:
                wait = (2 ** attempt) * 5
                warn(f"API error {e.status_code} (attempt {attempt + 1}/{max_retries}). Retrying in {wait}s...")
                time.sleep(wait)
            else:
                err(f"API error {e.status_code}: {e.message}")
                raise
    raise RuntimeError(f"Claude API failed after {max_retries} attempts.")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 0 — SE AGENT: DEEP DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════

_DISCOVERY_SYSTEM = """\
You are the SE Agent (Senior Solutions Engineer) in the Archpilot Agentic Pipeline.

YOUR MANDATE
Perform deep, multi-dimensional discovery on the high-level business requirement.
You MUST cover ALL 15 discovery dimensions below — no dimension may be omitted.
Every answer must be specific and quantified. Replace every placeholder. Write zero vague adjectives.

THE 15 MANDATORY DISCOVERY DIMENSIONS (Rule 50 v4.0)
 1. Technical Physics        — throughput (TPS/RPS), latency targets (p50/p95/p99), concurrency,
                               Little's Law calculations, data volumes, bandwidth envelopes.
 2. Regulatory & Compliance  — which regulations apply (GDPR, HIPAA, SOX, PCI-DSS, CCPA, regional),
                               certification requirements, audit trail obligations.
 3. Security & Threat Surface — STRIDE threat model per major component, zero-trust posture,
                               authentication mechanisms, authorization model (RBAC/ABAC/ReBAC).
 4. Failure & Resilience     — RPO and RTO targets per tier, CAP theorem choice, failure modes,
                               graceful degradation states, blast-radius limits.
 5. Cost & FinOps            — TCO model (3-year), cloud spend envelope, margin profile,
                               FinOps strategy (reserved vs spot vs on-demand), build vs buy decisions.
 6. Data Residency & Sovereignty — geo-fencing requirements, cross-border data transfer rules,
                               data classification levels, jurisdiction-specific storage obligations.
 7. Edge & Hardware Constraints — IoT/device requirements, edge compute nodes, offline operation,
                               firmware/OS constraints, connectivity quality assumptions.
 8. Connectivity & Integration — external systems inventory, integration protocols (REST/gRPC/events),
                               legacy adapters, API contracts, dependency SLAs.
 9. Observability Requirements — logging standard (structured JSON), metric dimensions (RED/USE),
                               distributed tracing strategy, alerting thresholds and on-call tiers.
10. Lifecycle & Maintainability — versioning strategy (SemVer/CalVer), upgrade paths, deprecation
                               policy, backward-compatibility windows, support timelines.
11. Human Interface & UX     — user personas and devices, accessibility requirements (WCAG level),
                               internationalization/localization, offline UX, progressive enhancement.
12. Data Privacy & Ethics    — PII inventory, anonymization/pseudonymization strategy, retention
                               limits, right-to-delete/portability obligations, consent model.
13. Third-Party Dependencies — vendor list, lock-in risk score per vendor, exit strategy,
                               open-source license compliance, supply-chain security posture.
14. Scaling & Multi-Tenancy  — horizontal vs vertical scaling triggers, tenant isolation model
                               (silo/bridge/pool), noisy-neighbor controls, elasticity SLAs.
15. Environmental & Sustainability — SCI score estimate, carbon-aware scheduling opportunities,
                               GreenOps targets, region selection for renewable energy, ARM migration.

OUTPUT RULES
- Produce a complete, populated discovery.md using the template structure provided.
- Every field must be answered. No [placeholder], no TBD, no TODO.
- Use tables, bullet lists, and mermaid diagrams where they add clarity.
- Finish with "## Interrogation List" — the exact questions the client must answer before Phase 1.
"""

def run_discovery(client, specs_dir: Path, input_req: str, model: str, max_tokens: int, persona: str = "") -> str:
    banner(0, "SE Agent — Deep Discovery (15 Dimensions)")
    info("Analysing requirement across all 15 mandatory dimensions...")

    user_msg = f"""\
HIGH-LEVEL REQUIREMENT
{input_req}

DISCOVERY TEMPLATE (fill every section — replace all placeholders):
{tmpl("discovery-template.md")}

RULE 36 — Discovery & Ambiguity Standards:
{cap(rule("36-discovery-ambiguity.md"), 4000)}

RULE 50 — Pipeline Governance Constraints:
{cap(rule("50-agent-pipeline.md"), 2500)}

Produce the complete discovery.md. Minimum 15 dimensions. No placeholders. No TODOs.
"""
    result = call_claude(client, _inject_persona(_DISCOVERY_SYSTEM, persona), user_msg, model, max_tokens)
    write_artifact(specs_dir, "discovery.md", result)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — PO AGENT: REQUIREMENTS BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════

_REQUIREMENTS_SYSTEM = """\
You are the PO Agent (Product Owner / Business Analyst) in the Archpilot Agentic Pipeline.

YOUR MANDATE
Transform the discovery artifact into a structured, multi-level requirements breakdown.

STRUCTURAL CONSTRAINTS (Rule 50 v4.0 — non-negotiable)
- Exactly 10 to 20 Epics, organized by domain category.
- Each Epic: 5 to 10 User Stories.
- Total User Stories: minimum 50, maximum 150.
- Each Epic must belong to one of these categories:
    FUNCTIONAL | DATA & STORAGE | SECURITY & COMPLIANCE | INTEGRATION & APIs |
    NON-FUNCTIONAL | DEVOPS & PLATFORM | TESTING & QUALITY | MIGRATION & CUTOVER

STORY FORMAT (all fields mandatory)
  ID:                  [EPIC-ID]-[S-NN]   e.g. EP-01-S-01
  Title:               <imperative verb phrase>
  As a:                <persona>
  I want:              <action>
  So that:             <business outcome>
  Acceptance Criteria: (3-5 measurable, EARS-compliant conditions)
  Priority:            Must / Should / Could / Won't (MoSCoW)
  Story Points:        <Fibonacci: 1/2/3/5/8/13>
  NFR Tags:            [Performance] [Security] [Availability] [Cost] [Compliance] (where applicable)

EARS NOTATION (mandatory for all requirements)
  Ubiquitous:      "The system SHALL <action>"
  Event-driven:    "WHEN <trigger>, the system SHALL <action>"
  State-driven:    "WHILE <state>, the system SHALL <action>"
  Unwanted:        "IF <precondition>, the system SHALL NOT <action>"
  Optional:        "WHERE <feature> is included, the system SHALL <action>"

QUALITY GATES
- Every NFR acceptance criterion must include a numeric target (e.g., p95 < 200 ms, 99.9% uptime).
- No vague adjectives: fast, scalable, reliable, efficient are forbidden.
- Every Epic must have a "Definition of Done" block.
- Every story must link back to a discovery dimension via a [DIM-XX] tag.
"""

def run_requirements(client, specs_dir: Path, discovery_content: str, model: str, max_tokens: int, persona: str = "") -> str:
    banner(1, "PO Agent — Requirements Breakdown")
    info("Generating categorized multi-level requirements (10-20 Epics, 50-150 Stories)...")

    user_msg = f"""\
DISCOVERY DOCUMENT:
{cap(discovery_content, 12000)}

REQUIREMENTS BREAKDOWN TEMPLATE (populate fully):
{tmpl("requirements-breakdown-template.md")}

RULE 27 — Spec-Driven Development:
{cap(rule("27-spec-driven-development.md"), 3000)}

RULE 50 — Pipeline Constraints:
{cap(rule("50-agent-pipeline.md"), 1500)}

Generate requirements.md. 10-20 Epics. 50-150 Stories. Every story fully populated. No placeholders.
"""
    result = call_claude(client, _inject_persona(_REQUIREMENTS_SYSTEM, persona), user_msg, model, max_tokens)
    write_artifact(specs_dir, "requirements.md", result)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — ARCH AGENT: HIGH-LEVEL DESIGN
# ═══════════════════════════════════════════════════════════════════════════════

_HLD_SYSTEM = """\
You are the Arch Agent (Senior Enterprise Architect) in the Archpilot Agentic Pipeline.

YOUR MANDATE
Produce a comprehensive High-Level Design document. Every section is mandatory.

MANDATORY SECTIONS (all 14 required — Rule 03)
 1.  Executive Summary        — 3-5 sentences; a CTO must understand the system from this alone.
 2.  Business Context         — drivers, key use cases table, stakeholder matrix.
 3.  System Context Diagram   — C4 Level 1 (Mermaid graph TB).
 4.  Container Diagram        — C4 Level 2 (Mermaid graph TB) + container table.
 5.  Data Flow                — primary flow (Mermaid sequenceDiagram) + async flow.
 6.  Technology Stack         — every layer justified; no undecided slots.
 7.  Integration Architecture — protocols, auth method, SLA, data format per integration.
 8.  Non-Functional Requirements — 8 categories, all with numeric targets.
 9.  Security Architecture    — zero-trust model; auth, authz, encryption, network, secrets.
10.  Deployment Architecture  — infra diagram (Mermaid), environments table, CI/CD pipeline.
11.  Cost Estimate            — per-service monthly cost (expected + peak); 3-year TCO.
12.  Key Architecture Decisions — ADR table with IDs and rationale.
13.  Risks & Mitigations      — probability × impact matrix.
14.  Roadmap                  — phased delivery with milestones.

DESIGN NARRATIVE RULE (Rule 50 — mandatory)
Every component block MUST include:
  Design Rationale:       WHY this technology / pattern was chosen over alternatives.
  Implementation Strategy: HOW this will be built; key engineering decisions.

ARCHITECTURE STANDARDS
- All Mermaid diagrams must be syntactically valid (test mentally before writing).
- Security is zero-trust by default — never bolt-on.
- All NFRs must have measurable targets.
- Call out anti-patterns explicitly where they were avoided and why.
"""

def run_hld(client, specs_dir: Path, discovery_content: str, requirements_content: str, model: str, max_tokens: int, persona: str = "") -> str:
    banner(2, "Arch Agent — High-Level Design")
    info("Generating HLD (14 sections, C4 diagrams, NFRs, cost estimate)...")

    user_msg = f"""\
DISCOVERY DOCUMENT:
{cap(discovery_content, 8000)}

REQUIREMENTS (key epics and NFRs):
{cap(requirements_content, 6000)}

HLD TEMPLATE (populate all 14 sections):
{tmpl("hld-template.md")}

RULE 03 — HLD Standards:
{cap(rule("03-hld-standards.md"), 3000)}

RULE 07 — Security Architecture:
{cap(rule("07-security-architecture.md"), 2000)}

RULE 08 — Cloud Architecture:
{cap(rule("08-cloud-architecture.md"), 2000)}

RULE 09 — Microservices Patterns:
{cap(rule("09-microservices-patterns.md"), 1500)}

Produce the complete Design_HLD.md. All 14 sections mandatory. Mermaid diagrams must be syntactically valid.
Include real technology choices with rationale. No placeholders.
"""
    result = call_claude(client, _inject_persona(_HLD_SYSTEM, persona), user_msg, model, max_tokens)
    write_artifact(specs_dir, "Design_HLD.md", result)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — ARCH AGENT: LOW-LEVEL DESIGN(S) — parallel execution
# ═══════════════════════════════════════════════════════════════════════════════

_LLD_SYSTEM = """\
You are the Arch Agent (Senior Enterprise Architect) in the Archpilot Agentic Pipeline.

YOUR MANDATE
Produce a detailed Low-Level Design for a specific service identified in the HLD.

MANDATORY SECTIONS (all 12 required — Rule 04)
 1.  Scope & Objectives        — in-scope, out-of-scope, success criteria table.
 2.  Assumptions, Constraints & Dependencies — dependency table with owner + risk.
 3.  Detailed Component Design  — class/module diagram (Mermaid), SOLID analysis.
 4.  API Specification          — every endpoint: method, path, request/response schema, error codes.
 5.  Database Schema            — table/collection definitions, indexes, partitioning, constraints.
 6.  Sequence Diagrams          — happy path + 2 error paths per critical flow (Mermaid).
 7.  Error Handling & Resilience — retry policy, circuit-breaker config, DLQ design, idempotency.
 8.  Performance Design         — caching layers, query optimization plan, connection pool sizing.
 9.  Security Implementation    — auth flow sequence, input validation rules, secrets management.
10.  Testing Strategy           — unit/integration/contract/performance test hooks + coverage targets.
11.  Observability              — structured log schema (JSON), metric names (RED/USE), trace spans, alert rules.
12.  Deployment Notes           — Dockerfile hints, env vars, health-check endpoints, scaling policy.

DESIGN NARRATIVE RULE
Each component and decision requires:
  Design Rationale:       WHY this approach over alternatives.
  Implementation Strategy: HOW the team will build it (first principles).

QUALITY STANDARDS
- Every API endpoint must include at least one example request/response.
- Every DB table must specify primary key, indexes, and estimated row growth rate.
- Circuit-breaker thresholds must be numeric (e.g., 50% error rate over 10s window → OPEN).
- Cache TTLs, pool sizes, retry counts must be explicit numbers — not "TBD".
"""

def _extract_services(client, hld_content: str, model: str) -> list:
    """Ask Claude to extract the top 3-5 service names from the HLD container diagram."""
    info("Extracting services from HLD container diagram...")
    raw = call_claude(
        client,
        "You extract service names from HLD documents. Return ONLY a valid JSON array of strings. No prose.",
        f"From this HLD, list the top 3-5 services that need individual LLD documents.\n"
        f"Return ONLY a JSON array, e.g.: [\"Payment Service\", \"User Service\"]\n\n"
        f"HLD (containers section):\n{cap(hld_content, 5000)}",
        model=model,
        max_tokens=400,
    )
    try:
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        return json.loads(match.group()) if match else ["Core Service", "API Service", "Data Service"]
    except Exception:
        return ["Core Service", "API Service", "Data Service"]

def _generate_single_lld(
    client, specs_dir: Path, svc: str,
    hld_content: str, requirements_content: str, discovery_content: str,
    lld_template: str, r04: str, r05: str, r06: str,
    model: str, max_tokens: int,
) -> tuple:
    """Generate a single LLD document. Runs in a thread."""
    safe = re.sub(r'[^A-Za-z0-9_]', '_', svc)
    user_msg = f"""\
SERVICE: {svc}

HLD DOCUMENT:
{cap(hld_content, 6000)}

DISCOVERY CONTEXT (key constraints for this service):
{cap(discovery_content, 4000)}

RELEVANT REQUIREMENTS:
{cap(requirements_content, 4000)}

LLD TEMPLATE (populate all 12 sections):
{lld_template}

RULE 04 — LLD Standards:
{r04}

RULE 05 — API Design:
{r05}

RULE 06 — Data Architecture:
{r06}

Produce the complete LLD for "{svc}". All 12 sections mandatory.
Include sequence diagrams, DB schema with indexes, API specs with examples.
All numeric thresholds explicit (no TBD). No placeholders.
"""
    result = call_claude(client, _inject_persona(_LLD_SYSTEM, ""), user_msg, model, max_tokens)
    fname = f"Design_LLD_{safe}.md"
    write_artifact(specs_dir, fname, result)
    return svc, result

def run_lld(
    client,
    specs_dir: Path,
    hld_content: str,
    requirements_content: str,
    discovery_content: str,
    model: str,
    max_tokens: int,
) -> dict:
    banner(3, "Arch Agent — Low-Level Designs (parallel)")

    services = _extract_services(client, hld_content, model)
    info(f"Generating LLDs for {len(services)} services in parallel: {', '.join(services)}")

    lld_template = tmpl("lld-template.md")
    r04 = cap(rule("04-lld-standards.md"), 3000)
    r05 = cap(rule("05-api-design.md"),     2500)
    r06 = cap(rule("06-data-architecture.md"), 2500)

    lld_results: dict = {}
    # LLDs are independent — generate them concurrently
    with ThreadPoolExecutor(max_workers=min(len(services), 4)) as executor:
        futures = {
            executor.submit(
                _generate_single_lld,
                client, specs_dir, svc,
                hld_content, requirements_content, discovery_content,
                lld_template, r04, r05, r06,
                model, max_tokens,
            ): svc
            for svc in services
        }
        for future in as_completed(futures):
            try:
                svc, result = future.result()
                lld_results[svc] = result
            except Exception as e:
                svc = futures[future]
                err(f"LLD generation failed for '{svc}': {e}")

    return lld_results


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — REVIEW AGENT: GUARDRAIL AUDIT
# ═══════════════════════════════════════════════════════════════════════════════

_REVIEW_SYSTEM = """\
You are the Review Agent (Architecture Guardrail Auditor) in the Archpilot Agentic Pipeline.

YOUR MANDATE
Audit ALL generated artifacts against Archpilot enterprise standards and produce a structured
review report. Findings at CRITICAL or HIGH severity block delivery.

12-DIMENSION AUDIT FRAMEWORK
 1.  Discovery Completeness   — all 15 dimensions present and quantified? No vague adjectives?
 2.  Requirements Quality     — EARS notation correct? ACs measurable? 10:10:50 ratio met?
 3.  NFR Coverage             — all 8 NFR categories present with numeric targets?
 4.  Security Guardrails      — zero-trust posture? auth/authz explicit? OWASP Top 10 addressed?
                                STRIDE threat model present in discovery?
 5.  Architecture Patterns    — correct pattern for the problem? anti-patterns absent?
                                Design Rationale and Implementation Strategy present for every component?
 6.  Data Architecture        — schema defined? indexes justified? PII handling explicit?
                                data retention and right-to-delete addressed?
 7.  Resilience Design        — RPO/RTO defined per tier? circuit-breaker thresholds numeric?
                                retry policy with backoff? DLQ designed?
 8.  Observability            — structured logging schema present? RED metrics defined?
                                distributed tracing spans named? alert thresholds numeric?
 9.  API Design               — REST conventions followed? versioning strategy stated?
                                RFC 7807 error format? pagination? rate-limiting?
10.  Cost & Sustainability     — TCO estimated for 3 years? GreenOps / SCI considered?
                                FinOps tagging strategy defined?
11.  ADR Coverage             — major decisions have ADR IDs? decision rationale not just "because"?
12.  Template Completeness    — all mandatory template sections populated? zero placeholders?
                                no TODO / TBD / FIXME in any artifact?

SEVERITY DEFINITIONS
  CRITICAL — Blocks design approval. Must be resolved before Phase 1 implementation starts.
             Examples: missing auth model, no RPO/RTO, security vectors unaddressed.
  HIGH     — Must be resolved before any coding begins.
             Examples: missing NFR targets, no error-handling strategy, vague ACs.
  MEDIUM   — Must be resolved before go-live sign-off.
             Examples: missing observability hooks, no cost estimate, weak test strategy.
  LOW      — Best-practice recommendations for the next iteration.

OUTPUT FORMAT — produce review_report.md with these sections:
  1. Executive Summary        — PASS / CONDITIONAL PASS / FAIL + one-paragraph rationale.
  2. Guardrail Compliance Scorecard — table: dimension, score (0-10), status (✓/⚠/✗).
  3. Overall Score            — weighted average (0-100); ≥80 = PASS, 60-79 = CONDITIONAL, <60 = FAIL.
  4. Critical & High Findings — table: ID, artifact, section, finding, recommended fix.
  5. Medium & Low Findings    — table: ID, artifact, section, finding.
  6. Per-Artifact Summary     — one paragraph per artifact with key gaps.
  7. Recommended Next Actions — ordered action list with owner (SE / PO / Arch / Dev).
"""

def run_review(
    client,
    specs_dir: Path,
    discovery: str,
    requirements: str,
    hld: str,
    lld_results: dict,
    model: str,
    max_tokens: int,
) -> str:
    banner(4, "Review Agent — Guardrail Audit & Compliance Scorecard")
    info("Auditing all artifacts across 12 guardrail dimensions...")

    lld_summary = "\n\n".join(
        f"### LLD: {svc}\n{cap(content, 2500)}" for svc, content in lld_results.items()
    )

    user_msg = f"""\
ARTIFACT: discovery.md (Phase 0)
{cap(discovery, 6000)}

ARTIFACT: requirements.md (Phase 1)
{cap(requirements, 6000)}

ARTIFACT: Design_HLD.md (Phase 2)
{cap(hld, 6000)}

ARTIFACT: LLD Documents (Phase 3)
{lld_summary}

GUARDRAIL STANDARDS:
Rule 00 — Architecture Principles:
{cap(rule("00-architecture-principles.md"), 2500)}

Rule 07 — Security Architecture:
{cap(rule("07-security-architecture.md"), 2000)}

Rule 11 — NFR Checklist (69 checks):
{cap(rule("11-nfr-checklist.md"), 2000)}

Rule 29 — Agentic AI Governance:
{cap(rule("29-agentic-ai-governance.md"), 1500)}

Rule 50 — Pipeline Governance:
{cap(rule("50-agent-pipeline.md"), 1200)}

Produce the complete review_report.md.
- Score every dimension 0-10.
- Calculate overall weighted score (0-100).
- Every finding must cite: artifact name, section heading, and specific line/claim.
- Recommended fixes must be actionable (not generic advice).
"""
    result = call_claude(client, _inject_persona(_REVIEW_SYSTEM, ""), user_msg, model, max_tokens)
    write_artifact(specs_dir, "review_report.md", result)
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def _load_persona(persona: str | None) -> str:
    """Read persona file content; return empty string if persona is None or file missing."""
    if not persona:
        return ""
    path = ARCHPILOT_ROOT / "llm-configs" / "personas" / f"{persona}.md"
    if not path.exists():
        warn(f"Persona file not found: {path.name} — running without persona overlay.")
        return ""
    return path.read_text(encoding="utf-8")


def _inject_persona(system_prompt: str, persona_content: str) -> str:
    """Prepend persona content to a system prompt if provided."""
    if not persona_content:
        return system_prompt
    return f"PERSONA & COMMUNICATION STYLE\n{persona_content}\n\n---\n\n{system_prompt}"


def _elapsed(seconds: float) -> str:
    """Human-readable elapsed time: '1m 23s' or '45s'."""
    m, s = divmod(int(seconds), 60)
    return f"{m}m {s:02d}s" if m else f"{s}s"


def run_pipeline(
    specs_dir_base: str,
    model: str = "claude-sonnet-4-6",
    from_phase: int = 0,
    max_tokens: int = 16000,
    persona: str | None = None,
    dry_run: bool = False,
) -> None:
    """
    Execute the full 5-stage Archpilot agentic pipeline.

    Args:
        specs_dir_base: directory containing .specs/
        model:          Claude model ID
        from_phase:     resume from this phase (0-4); reads existing artifacts for earlier phases
        max_tokens:     maximum output tokens per Claude call
        persona:        optional persona slug to tune agent communication style
        dry_run:        if True, print what each phase would do without calling Claude
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key and not dry_run:
        err("ANTHROPIC_API_KEY is not set. Export it before running the pipeline.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key or "dry-run") if not dry_run else None
    specs_dir = Path(specs_dir_base) / ".specs"

    if not specs_dir.exists():
        err(f"'{specs_dir}' does not exist. Run 'archpilot init' first.")
        sys.exit(1)

    input_file = specs_dir / "Input.md"
    if not input_file.exists():
        err("'.specs/Input.md' not found. Add your high-level requirement there.")
        sys.exit(1)

    input_req = (specs_dir / "Input.md").read_text(encoding="utf-8")
    if len(input_req.strip()) < 50:
        err("Input.md is too short. Provide a meaningful high-level requirement (min 50 chars).")
        sys.exit(1)

    persona_content = _load_persona(persona)

    bar = "═" * 62
    print(f"\n{BOLD}{GREEN}{bar}{RESET}")
    print(f"{BOLD}{GREEN}  Archpilot Agentic Pipeline v4.2{RESET}")
    print(f"{BOLD}{GREEN}{bar}{RESET}")
    print(f"  Model      : {model}")
    print(f"  Specs      : {specs_dir}")
    print(f"  Max tokens : {max_tokens}")
    print(f"  From phase : {from_phase}")
    print(f"  Persona    : {persona or '(none)'}")
    print(f"  Dry run    : {'yes — no API calls will be made' if dry_run else 'no'}")
    print(f"  Started    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Input      : {input_req[:100].strip()}...")
    print(f"{BOLD}{GREEN}{bar}{RESET}\n")

    if from_phase > 0:
        info(f"Resuming from Phase {from_phase} — reading existing artifacts for earlier phases.")

    phase_timings: list[tuple[str, float]] = []
    pipeline_start = time.perf_counter()

    def _timed_phase(label: str, fn, *args, **kwargs):
        """Run a pipeline phase and record elapsed time."""
        t0 = time.perf_counter()
        if dry_run:
            print(f"  {DIM}[dry-run] Would run: {label}{RESET}")
            return ""
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        phase_timings.append((label, elapsed))
        ok(f"{label} completed in {_elapsed(elapsed)}")
        return result

    # ── Phase 0 ─────────────────────────────────────────────────────────────
    if from_phase <= 0:
        discovery = _timed_phase(
            "Phase 0: SE Agent — Deep Discovery",
            run_discovery, client, specs_dir, input_req, model, max_tokens, persona_content,
        )
    else:
        discovery = (specs_dir / "discovery.md").read_text(encoding="utf-8")
        ok("Phase 0: loaded existing discovery.md")

    # ── Phase 1 ─────────────────────────────────────────────────────────────
    if from_phase <= 1:
        requirements = _timed_phase(
            "Phase 1: PO Agent — Requirements Breakdown",
            run_requirements, client, specs_dir, discovery, model, max_tokens, persona_content,
        )
    else:
        requirements = (specs_dir / "requirements.md").read_text(encoding="utf-8")
        ok("Phase 1: loaded existing requirements.md")

    # ── Phase 2 ─────────────────────────────────────────────────────────────
    if from_phase <= 2:
        hld = _timed_phase(
            "Phase 2: Arch Agent — High-Level Design",
            run_hld, client, specs_dir, discovery, requirements, model, max_tokens, persona_content,
        )
    else:
        hld = (specs_dir / "Design_HLD.md").read_text(encoding="utf-8")
        ok("Phase 2: loaded existing Design_HLD.md")

    # ── Phase 3 ─────────────────────────────────────────────────────────────
    if from_phase <= 3:
        lld_results = _timed_phase(
            "Phase 3: Arch Agent — Low-Level Designs",
            run_lld, client, specs_dir, hld, requirements, discovery, model, max_tokens,
        )
        if dry_run:
            lld_results = {}
    else:
        lld_results = {}
        for f in specs_dir.glob("Design_LLD_*.md"):
            lld_results[f.stem.replace("Design_LLD_", "").replace("_", " ")] = f.read_text(encoding="utf-8")
        ok(f"Phase 3: loaded {len(lld_results)} existing LLD(s)")

    # ── Phase 4 ─────────────────────────────────────────────────────────────
    review = _timed_phase(
        "Phase 4: Review Agent — Guardrail Audit",
        run_review, client, specs_dir, discovery, requirements, hld, lld_results, model, max_tokens,
    )

    total_elapsed = time.perf_counter() - pipeline_start

    # ── Final summary ────────────────────────────────────────────────────────
    print(f"\n{BOLD}{GREEN}{bar}{RESET}")
    print(f"{BOLD}{GREEN}  Pipeline Complete!  (total: {_elapsed(total_elapsed)}){RESET}")
    if phase_timings:
        print(f"{GREEN}  Phase timings:{RESET}")
        for label, secs in phase_timings:
            print(f"    {label:<45} {_elapsed(secs):>6}")
    print(f"{GREEN}  All artifacts written to: {specs_dir}{RESET}")
    print(f"{BOLD}{GREEN}{bar}{RESET}\n")

    if review:
        exec_start = review.find("## 1. Executive Summary")
        if exec_start == -1:
            exec_start = review.find("## Executive Summary")
        if exec_start > -1:
            print(review[exec_start : exec_start + 600])
            print()


def run_review_only(specs_dir_base: str, model: str = "claude-sonnet-4-6", max_tokens: int = 16000) -> None:
    """
    Run only Phase 4 (Review) against existing .specs/ artifacts.
    Useful for re-auditing after manual edits.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        err("ANTHROPIC_API_KEY is not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    specs_dir = Path(specs_dir_base) / ".specs"

    discovery    = (specs_dir / "discovery.md").read_text(encoding="utf-8") if (specs_dir / "discovery.md").exists() else ""
    requirements = (specs_dir / "requirements.md").read_text(encoding="utf-8") if (specs_dir / "requirements.md").exists() else ""
    hld          = (specs_dir / "Design_HLD.md").read_text(encoding="utf-8") if (specs_dir / "Design_HLD.md").exists() else ""

    lld_results: dict = {}
    for f in specs_dir.glob("Design_LLD_*.md"):
        lld_results[f.stem.replace("Design_LLD_", "").replace("_", " ")] = f.read_text(encoding="utf-8")

    if not any([discovery, requirements, hld]):
        err("No artifacts found. Run 'archpilot run' first to generate them.")
        sys.exit(1)

    run_review(client, specs_dir, discovery, requirements, hld, lld_results, model, max_tokens)
    ok("Review report written to .specs/review_report.md")
