#!/usr/bin/env python3
"""
Archpilot Drift Checker

Compares API endpoints declared in LLD spec files (Design_LLD_*.md) against
actual endpoint definitions found in source code.

Exit codes:
  0 — no drift detected
  1 — drift detected (endpoints in spec but not in code, or vice-versa)

Usage:
  python tools/drift_check.py --dir <project-root> [--src <src-dir>] [--format text|json]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ─── Regex patterns ──────────────────────────────────────────────────────────

# Matches API endpoint tables in LLD markdown:
#   | POST | /api/v1/payments | ...  or  | GET /users/{id} | ...
_MD_ENDPOINT = re.compile(
    r'\|\s*(?P<method>GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s*\|?\s*(?P<path>/[\w/{}.?=-]*)',
    re.IGNORECASE,
)

# Code patterns — covers common Python, JS/TS, Go, Java, Spring, FastAPI, Flask, Express
_CODE_PATTERNS = [
    # FastAPI / Flask decorators: @app.get("/path"), @router.post("/v1/...")
    re.compile(r'@\w+\.(?P<method>get|post|put|patch|delete)\s*\(\s*["\'](?P<path>/[^"\']+)["\']', re.IGNORECASE),
    # Express: router.get("/path", ...), app.post("/v1/...")
    re.compile(r'(?:router|app)\.(?P<method>get|post|put|patch|delete)\s*\(\s*["\'](?P<path>/[^"\']+)["\']', re.IGNORECASE),
    # Spring: @GetMapping("/path"), @PostMapping(value="/v1/...")
    re.compile(r'@(?P<method>Get|Post|Put|Patch|Delete)Mapping\s*\([^)]*["\'](?P<path>/[^"\']+)["\']', re.IGNORECASE),
    # Go / Gin: r.GET("/path", ...), mux.Handle("GET", "/path", ...)
    re.compile(r'\.(?P<method>GET|POST|PUT|PATCH|DELETE)\s*\(\s*["\'](?P<path>/[^"\']+)["\']', re.IGNORECASE),
    # Generic: method("GET", "/path") or Handle("POST", "/v1/...")
    re.compile(r'["\'](?P<method>GET|POST|PUT|PATCH|DELETE)["\'],\s*["\'](?P<path>/[^"\']+)["\']', re.IGNORECASE),
]

_SOURCE_EXTENSIONS = {".py", ".ts", ".js", ".go", ".java", ".rb", ".cs", ".rs"}


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _normalize_path(path: str) -> str:
    """Replace path params {foo} with {*} and strip trailing slashes."""
    return re.sub(r'\{[^}]+\}', '{*}', path).rstrip("/").lower()

def _extract_spec_endpoints(specs_dir: Path) -> dict[str, list[str]]:
    """Return {lld_filename: [(METHOD, /path), ...]} from LLD markdown files."""
    results: dict[str, list[str]] = {}
    for lld in sorted(specs_dir.glob("Design_LLD_*.md")):
        endpoints = []
        for line in lld.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = _MD_ENDPOINT.search(line)
            if m:
                endpoints.append((m.group("method").upper(), _normalize_path(m.group("path"))))
        if endpoints:
            results[lld.name] = list(dict.fromkeys(endpoints))  # dedupe, preserve order
    return results

def _extract_code_endpoints(src_dir: Path) -> list[tuple[str, str, str]]:
    """Return [(method, /path, relative_file_path), ...] from source files."""
    found = []
    for root, _, files in os.walk(src_dir):
        for fname in files:
            if Path(fname).suffix not in _SOURCE_EXTENSIONS:
                continue
            fpath = Path(root) / fname
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pattern in _CODE_PATTERNS:
                for m in pattern.finditer(text):
                    method = m.group("method").upper()
                    path   = _normalize_path(m.group("path"))
                    rel    = str(fpath.relative_to(src_dir))
                    found.append((method, path, rel))
    return list(dict.fromkeys(found))  # dedupe

def _find_src_dir(project_root: Path, hint: str | None) -> Path | None:
    if hint:
        p = Path(hint)
        return p if p.is_dir() else None
    # Common source directories — try in order
    for candidate in ["src", "app", "api", "server", "service", "backend", "."]:
        p = project_root / candidate
        if p.is_dir():
            return p
    return None


# ─── Main logic ──────────────────────────────────────────────────────────────

def drift_check(project_dir: str, src_hint: str | None = None, fmt: str = "text") -> None:
    root      = Path(project_dir)
    specs_dir = root / ".specs"

    if not specs_dir.exists():
        _output(fmt, {"fatal": f"No .specs/ found in {project_dir}. Run 'archpilot init' first."})
        sys.exit(1)

    src_dir = _find_src_dir(root, src_hint)
    if src_dir is None:
        msg = f"No source directory found in {project_dir}. Use --src to specify one."
        _output(fmt, {"fatal": msg})
        sys.exit(1)

    spec_eps  = _extract_spec_endpoints(specs_dir)
    code_eps  = _extract_code_endpoints(src_dir)

    code_set: set[tuple[str, str]] = {(m, p) for m, p, _ in code_eps}

    findings: list[dict] = []
    total_spec = 0

    for lld, endpoints in spec_eps.items():
        for method, path in endpoints:
            total_spec += 1
            if (method, path) not in code_set:
                findings.append({
                    "type":    "SPEC_NOT_IN_CODE",
                    "lld":     lld,
                    "method":  method,
                    "path":    path,
                    "message": f"Endpoint {method} {path} is declared in {lld} but not found in source code.",
                })

    # Endpoints in code that appear in no LLD spec — only flagged as advisory
    spec_set: set[tuple[str, str]] = {ep for eps in spec_eps.values() for ep in eps}
    for method, path, src_file in code_eps:
        if (method, path) not in spec_set:
            findings.append({
                "type":    "CODE_NOT_IN_SPEC",
                "source":  src_file,
                "method":  method,
                "path":    path,
                "message": f"Endpoint {method} {path} (in {src_file}) has no LLD spec entry.",
            })

    _output(fmt, {
        "project":         project_dir,
        "src_dir":         str(src_dir),
        "spec_endpoints":  total_spec,
        "code_endpoints":  len(code_eps),
        "findings":        findings,
        "drift_detected":  bool(findings),
    })

    if findings:
        sys.exit(1)
    sys.exit(0)


def _output(fmt: str, data: dict) -> None:
    if fmt == "json":
        print(json.dumps(data, indent=2))
        return

    if "fatal" in data:
        print(f"Error: {data['fatal']}")
        return

    print(f"\nArchpilot Drift Check")
    print(f"  Project   : {data['project']}")
    print(f"  Source    : {data['src_dir']}")
    print(f"  Spec EPs  : {data['spec_endpoints']}")
    print(f"  Code EPs  : {data['code_endpoints']}")
    print(f"  Findings  : {len(data['findings'])}")
    print("-" * 60)

    spec_not_code = [f for f in data["findings"] if f["type"] == "SPEC_NOT_IN_CODE"]
    code_not_spec = [f for f in data["findings"] if f["type"] == "CODE_NOT_IN_SPEC"]

    if spec_not_code:
        print("\n[ERROR] In spec but NOT in code (implementation gap):")
        for f in spec_not_code:
            print(f"  ✗ {f['method']:6s} {f['path']}  ← {f['lld']}")

    if code_not_spec:
        print("\n[WARN]  In code but NOT in spec (undocumented endpoint):")
        for f in code_not_spec:
            print(f"  ⚠ {f['method']:6s} {f['path']}  ← {f['source']}")

    if not data["findings"]:
        print("  ✓ No drift detected. All LLD endpoints match source code.")
    print()


# ─── Entry point ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Archpilot Drift Checker — LLD spec vs source code endpoint comparison"
    )
    parser.add_argument("--dir",    default=".", help="Project root directory (default: current)")
    parser.add_argument("--src",    default=None, help="Source code directory (auto-detected if omitted)")
    parser.add_argument("--format", dest="fmt", default="text", choices=["text", "json"])
    args = parser.parse_args()
    drift_check(args.dir, args.src, args.fmt)


if __name__ == "__main__":
    main()
