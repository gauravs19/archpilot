"""Shared pytest fixtures for Archpilot tests."""

import os
import pytest


@pytest.fixture
def specs_dir(tmp_path):
    """Create a minimal .specs/ directory with all required governance files."""
    sd = tmp_path / ".specs"
    sd.mkdir()

    governance = {
        "assumptions.md":  "# Assumptions Log\n\n| ID | Assumption | Owner | Status |\n|----|-----------:|-------|--------|\n| A1 | Cloud-native deployment | Arch | Open |\n",
        "volumetrics.md":  "# Volumetrics\n\n| Metric | Nominal | Peak | Basis |\n|--------|--------:|-----:|-------|\n| RPS | 1000 | 5000 | load test |\n",
        "dependencies.md": "# External Dependencies\n\n| Name | Owner | Type | Risk |\n|------|-------|------|------|\n| Stripe | Payments | API | Medium |\n",
        "critical_path.md":"# Critical Path\n\n| Milestone | Dependency | Owner | Date |\n|-----------|------------|-------|------|\n| MVP | None | Tech Lead | 2026-09-01 |\n",
    }
    for name, content in governance.items():
        (sd / name).write_text(content, encoding="utf-8")

    return sd
