"""Tests for archpilot lint_specs() — no API key required."""

import json
import sys
import os
import pytest

# Allow importing from repo root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from archpilot import lint_specs, _strip_code_blocks


# ─── _strip_code_blocks ───────────────────────────────────────────────────────

def test_strip_code_blocks_removes_fenced():
    text = "Some text\n```python\nfast code here\n```\nAfter"
    result = _strip_code_blocks(text)
    assert "fast" not in result
    assert "Some text" in result
    assert "After" in result

def test_strip_code_blocks_leaves_prose():
    text = "This is fast prose without code blocks."
    result = _strip_code_blocks(text)
    assert result == text


# ─── lint: placeholder detection ─────────────────────────────────────────────

def test_lint_catches_todo(specs_dir, capsys, tmp_path):
    (specs_dir / "discovery.md").write_text(
        "# Discovery\n\n## Technical Physics Dimension\nTODO: fill this in\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=1, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert any("TODO" in e for e in out["errors"])

def test_lint_catches_tbd(specs_dir, capsys, tmp_path):
    (specs_dir / "requirements.md").write_text(
        "# Requirements\n\nTBD: fill requirements\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=1, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert any("TBD" in e for e in out["errors"])

def test_lint_catches_unfilled_placeholder(specs_dir, capsys, tmp_path):
    (specs_dir / "requirements.md").write_text(
        "# Requirements\n\n[Your requirement here]\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=1, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert any("placeholder" in e.lower() for e in out["errors"])


# ─── lint: weak word tier behaviour ──────────────────────────────────────────

def test_weak_word_is_warn_at_tier1(specs_dir, capsys, tmp_path):
    (specs_dir / "discovery.md").write_text(
        "# Discovery\n\n## Technical Physics Dimension\nThe system must be fast and scalable.\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=1, fmt="json")
    # Tier 1: weak words are warnings only, so exit code 0
    assert exc.value.code == 0
    out = json.loads(capsys.readouterr().out)
    assert any("fast" in w for w in out["warnings"])
    assert not any("fast" in e for e in out["errors"])

def test_weak_word_is_error_at_tier2(specs_dir, capsys, tmp_path):
    (specs_dir / "discovery.md").write_text(
        "# Discovery\n\n## Technical Physics Dimension\nThe system must be fast.\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=2, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert any("fast" in e for e in out["errors"])

def test_weak_word_not_flagged_inside_code_block(specs_dir, capsys, tmp_path):
    (specs_dir / "discovery.md").write_text(
        "# Discovery\n\n## Technical Physics Dimension\n"
        "Latency target: p99 < 100 ms.\n\n"
        "```bash\n# fast build script\npip install fast-api\n```\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=2, fmt="json")
    out = json.loads(capsys.readouterr().out)
    # "fast" inside code block must not appear in errors
    assert not any("fast" in e for e in out["errors"])


# ─── lint: missing governance artifacts ──────────────────────────────────────

def test_lint_errors_on_missing_governance_file(tmp_path, capsys):
    sd = tmp_path / ".specs"
    sd.mkdir()
    # Only create one governance file — rest missing
    (sd / "assumptions.md").write_text("# Assumptions Log\n", encoding="utf-8")
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=1, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    missing = [e for e in out["errors"] if "Missing governance" in e]
    assert len(missing) >= 2   # volumetrics, dependencies, critical_path


# ─── lint: HLD mandatory sections ────────────────────────────────────────────

def test_lint_errors_on_missing_design_rationale(specs_dir, capsys, tmp_path):
    (specs_dir / "Design_HLD.md").write_text(
        "# HLD\n\n## Implementation Strategy\nWe will build iteratively.\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=2, fmt="json")
    assert exc.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert any("Design Rationale" in e for e in out["errors"])

def test_lint_passes_clean_specs(specs_dir, capsys, tmp_path):
    (specs_dir / "discovery.md").write_text(
        "# Discovery\n\n## Technical Physics Dimension\n"
        "Throughput: 5000 TPS. Latency p99 < 100 ms. Concurrency L=50.\n\n"
        "## Regulatory Dimension\nGDPR applies. Audit logs retained 7 years.\n\n"
        "## Security Dimension\nSTRIDE model applied.\n\n"
        "## Resilience Dimension\nRPO 1 min, RTO 5 min.\n\n"
        "## Cost Dimension\nTCO $120,000/year at 3 years.\n",
        encoding="utf-8"
    )
    (specs_dir / "Design_HLD.md").write_text(
        "# HLD\n\n## Design Rationale\nChose microservices for independent scaling.\n\n"
        "## Implementation Strategy\nPhased delivery over 3 sprints.\n\n"
        "```mermaid\ngraph TD\n    A --> B\n```\n",
        encoding="utf-8"
    )
    with pytest.raises(SystemExit) as exc:
        lint_specs(str(tmp_path), tier=2, fmt="json")
    out = json.loads(capsys.readouterr().out)
    assert out["errors"] == [], f"Unexpected errors: {out['errors']}"
    assert exc.value.code == 0


# ─── lint: JSON output format ─────────────────────────────────────────────────

def test_lint_json_output_structure(specs_dir, capsys, tmp_path):
    with pytest.raises(SystemExit):
        lint_specs(str(tmp_path), tier=1, fmt="json")
    raw = capsys.readouterr().out
    data = json.loads(raw)
    assert "errors" in data
    assert "warnings" in data
    assert isinstance(data["errors"], list)
    assert isinstance(data["warnings"], list)
