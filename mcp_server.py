#!/usr/bin/env python3
"""
Archpilot MCP Server

Exposes all Archpilot rules, templates, and personas as MCP resources,
and provides lint + NFR-calculator tools — so any MCP-compatible client
(Claude Code, Claude.ai, Cursor, etc.) can read standards on demand
without copy-pasting files.

Usage
-----
  # stdio transport (Claude Code / Claude.ai)
  python mcp_server.py

  # Add to Claude Code settings:
  # {
  #   "mcpServers": {
  #     "archpilot": {
  #       "command": "python",
  #       "args": ["/path/to/archpilot/mcp_server.py"]
  #     }
  #   }
  # }

Resources exposed
-----------------
  archpilot://rules/index          — table of all rules with descriptions
  archpilot://rules/{name}         — full content of a named rule file
  archpilot://templates/index      — table of all templates
  archpilot://templates/{name}     — full content of a named template
  archpilot://personas/{name}      — full content of a persona file
  archpilot://diagrams/{name}      — Mermaid archetype diagram

Tools exposed
-------------
  list_rules()                     — structured index of all rules
  get_rule(name)                   — fetch a single rule by filename or number
  list_templates()                 — index of all templates
  run_lint(directory, tier)        — run archpilot lint and return JSON results
  calculate_nfrs(tps, payload_kb, retention_days, latency_ms, sla, rw_ratio)
                                   — run the NFR physics calculator
"""

import sys
import json
import subprocess
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "mcp SDK not installed. Run: pip install mcp\n"
        "Or: pip install -r requirements.txt",
        file=sys.stderr,
    )
    sys.exit(1)

# ─── Paths ────────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).parent
RULES_DIR  = ROOT / "rules"
TMPL_DIR   = ROOT / "templates"
PERSONA_DIR = ROOT / "llm-configs" / "personas"
DIAG_DIR   = ROOT / "diagrams"

# ─── Server ───────────────────────────────────────────────────────────────────
mcp = FastMCP(
    "Archpilot Standards Library",
    instructions=(
        "You have access to the full Archpilot enterprise architecture standards library. "
        "Use the resources to read specific rule files, templates, and personas. "
        "Use list_rules() to discover available rules before fetching them. "
        "When a user asks for architecture help, read the relevant rule(s) first."
    ),
)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Not found: {path.name}")
    return path.read_text(encoding="utf-8")

def _rule_description(stem: str) -> str:
    """Extract the first non-empty non-heading line from a rule file as a short desc."""
    path = RULES_DIR / f"{stem}.md"
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("<!--"):
            return stripped[:120]
    return ""

def _index_dir(directory: Path, ext: str = ".md") -> str:
    """Build a markdown table index for files in a directory."""
    files = sorted(directory.glob(f"*{ext}"))
    if not files:
        return f"No {ext} files found in {directory.name}/"
    lines = ["| File | Description |", "|------|-------------|"]
    for f in files:
        stem = f.stem
        first = _rule_description(stem) if directory == RULES_DIR else ""
        lines.append(f"| `{f.name}` | {first} |")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# RESOURCES
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.resource("archpilot://rules/index")
def rules_index() -> str:
    """Index of all 37 Archpilot rule files with brief descriptions."""
    return f"# Archpilot Rules Index\n\n{_index_dir(RULES_DIR)}"

@mcp.resource("archpilot://rules/{name}")
def get_rule_resource(name: str) -> str:
    """Full content of a named rule file (e.g. 'rules/03-hld-standards.md')."""
    # Accept bare name, with or without .md
    stem = name.removesuffix(".md")
    # Try exact match first
    path = RULES_DIR / f"{stem}.md"
    if not path.exists():
        # Try numeric prefix match (e.g. "03" → "03-hld-standards.md")
        matches = list(RULES_DIR.glob(f"{stem}*.md"))
        if not matches:
            raise FileNotFoundError(
                f"Rule '{name}' not found. Call archpilot://rules/index to list available rules."
            )
        path = matches[0]
    return _read(path)

@mcp.resource("archpilot://templates/index")
def templates_index() -> str:
    """Index of all Archpilot template files."""
    return f"# Archpilot Templates Index\n\n{_index_dir(TMPL_DIR)}"

@mcp.resource("archpilot://templates/{name}")
def get_template_resource(name: str) -> str:
    """Full content of a named template file (e.g. 'templates/hld-template.md')."""
    path = TMPL_DIR / name if name.endswith(".md") else TMPL_DIR / f"{name}.md"
    return _read(path)

@mcp.resource("archpilot://personas/{name}")
def get_persona_resource(name: str) -> str:
    """Full content of a persona file (enterprise-architect, security-architect, startup-cto, presales-solutioner, vibe-code-reviewer)."""
    path = PERSONA_DIR / name if name.endswith(".md") else PERSONA_DIR / f"{name}.md"
    return _read(path)

@mcp.resource("archpilot://diagrams/{name}")
def get_diagram_resource(name: str) -> str:
    """Mermaid archetype diagram (e.g. 'diagrams/01-c4-context-archetype.md')."""
    path = DIAG_DIR / name if name.endswith(".md") else DIAG_DIR / f"{name}.md"
    return _read(path)


# ═══════════════════════════════════════════════════════════════════════════════
# TOOLS
# ═══════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_rules() -> str:
    """
    Return a structured index of all Archpilot rule files with descriptions.
    Call this first to discover what rules are available before fetching one.
    """
    files = sorted(RULES_DIR.glob("*.md"))
    rows = []
    for f in files:
        desc = _rule_description(f.stem)
        rows.append({"file": f.name, "description": desc})
    return json.dumps(rows, indent=2)

@mcp.tool()
def get_rule(name: str) -> str:
    """
    Fetch the full content of a specific Archpilot rule file.

    Args:
        name: Rule filename (e.g. '03-hld-standards.md') or numeric prefix (e.g. '03').
              Use list_rules() to discover available rules.
    """
    stem = name.removesuffix(".md")
    path = RULES_DIR / f"{stem}.md"
    if not path.exists():
        matches = list(RULES_DIR.glob(f"{stem}*.md"))
        if not matches:
            available = [f.name for f in sorted(RULES_DIR.glob("*.md"))]
            return json.dumps({
                "error": f"Rule '{name}' not found.",
                "available_rules": available,
            })
        path = matches[0]
    return _read(path)

@mcp.tool()
def list_templates() -> str:
    """Return a structured index of all Archpilot template files."""
    files = sorted(TMPL_DIR.glob("*.md"))
    return json.dumps([f.name for f in files], indent=2)

@mcp.tool()
def list_personas() -> str:
    """
    Return the available Archpilot personas.
    Each persona tunes the LLM's expertise and communication style for a specific role.
    """
    files = sorted(PERSONA_DIR.glob("*.md"))
    return json.dumps([f.stem for f in files], indent=2)

@mcp.tool()
def run_lint(directory: str = ".", tier: int = 2) -> str:
    """
    Run the Archpilot linter on a project's .specs/ directory and return JSON results.

    Args:
        directory: Path to the project root (must contain .specs/). Default: current directory.
        tier:      Compliance tier — 1=Starter, 2=Standard, 3=Enterprise. Default: 2.

    Returns:
        JSON object with 'errors' and 'warnings' arrays, and a 'passed' boolean.
    """
    archpilot = ROOT / "archpilot.py"
    result = subprocess.run(
        [sys.executable, str(archpilot), "lint", "--dir", directory, "--tier", str(tier), "--format", "json"],
        capture_output=True,
        text=True,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        data = {"raw_output": result.stdout, "stderr": result.stderr}
    data["passed"] = result.returncode == 0
    return json.dumps(data, indent=2)

@mcp.tool()
def calculate_nfrs(
    tps: int,
    payload_kb: float,
    retention_days: int,
    latency_ms: int = 100,
    sla: float = 99.99,
    rw_ratio: float = 0.8,
) -> str:
    """
    Run the Archpilot NFR physics calculator (50+ metrics using Little's Law).
    Returns computed targets for latency, throughput, storage, compute, and cost.

    Args:
        tps:            Target total transactions per second.
        payload_kb:     Average payload size in KB.
        retention_days: Data retention period in days.
        latency_ms:     Target p99 latency in milliseconds. Default: 100.
        sla:            Target availability SLA (e.g. 99.99). Default: 99.99.
        rw_ratio:       Read-to-write ratio 0.0–1.0 (e.g. 0.8 = 80% reads). Default: 0.8.
    """
    nfr = ROOT / "tools" / "nfr_calculator.py"
    result = subprocess.run(
        [
            sys.executable, str(nfr),
            "--tps", str(tps),
            "--payload", str(payload_kb),
            "--retention", str(retention_days),
            "--latency", str(latency_ms),
            "--sla", str(sla),
            "--rw_ratio", str(rw_ratio),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return json.dumps({"error": result.stderr})
    return result.stdout


# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
