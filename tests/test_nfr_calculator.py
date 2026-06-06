"""Tests for tools/nfr_calculator.py — no API key required."""

import sys
import os
import math
import io
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.nfr_calculator import calculate_nfrs


def _run(tps=1000, payload_kb=2.0, retention_days=30,
         latency_ms=100, sla=99.9, rw_ratio=0.8):
    """Run the calculator and capture stdout."""
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    calculate_nfrs(tps, payload_kb, retention_days, latency_ms, sla, rw_ratio)
    sys.stdout = old
    return buf.getvalue()


# ─── Basic smoke tests ────────────────────────────────────────────────────────

def test_runs_without_error():
    out = _run()
    assert "ARCHPILOT ENTERPRISE NFR CALCULATOR" in out

def test_all_sections_present():
    out = _run()
    assert "AVAILABILITY & RELIABILITY" in out
    assert "PERFORMANCE & LATENCY" in out
    assert "COMPUTE & CONCURRENCY" in out
    assert "STORAGE & DATA RETENTION" in out
    assert "NETWORK & COST" in out

def test_50_metrics_present():
    out = _run()
    # Last numbered metric is [50]
    assert "[50]" in out


# ─── Latency percentile ordering ─────────────────────────────────────────────

def test_p99_greater_than_p95_greater_than_p50():
    out = _run(latency_ms=200)
    lines = out.splitlines()
    p50 = next(l for l in lines if "P50 Latency" in l)
    p95 = next(l for l in lines if "P95 Latency" in l)
    p99 = next(l for l in lines if "P99 Latency" in l)

    def _ms(line):
        import re
        m = re.search(r'(\d+)\s*ms', line)
        return int(m.group(1)) if m else 0

    assert _ms(p99) >= _ms(p95) >= _ms(p50)


# ─── Little's Law concurrency ─────────────────────────────────────────────────

def test_little_law_concurrency_scales_with_tps():
    out_low  = _run(tps=100,  latency_ms=100)
    out_high = _run(tps=1000, latency_ms=100)

    def _concurrency(out):
        import re
        m = re.search(r'Active Concurrency.*?(\d+)', out)
        return int(m.group(1)) if m else 0

    assert _concurrency(out_high) > _concurrency(out_low)

def test_concurrency_matches_little_law():
    tps, latency_ms = 500, 200
    out = _run(tps=tps, latency_ms=latency_ms)
    expected = math.ceil(tps * (latency_ms / 1000))
    import re
    m = re.search(r'Active Concurrency.*?(\d+)', out)
    actual = int(m.group(1)) if m else -1
    assert actual == expected


# ─── SLA edge cases ───────────────────────────────────────────────────────────

def test_high_sla_triggers_active_active():
    out = _run(sla=99.99)
    assert "Active-Active" in out

def test_lower_sla_recommends_active_passive():
    out = _run(sla=99.9)
    assert "Active-Passive" in out


# ─── Read/write ratio ─────────────────────────────────────────────────────────

def test_read_heavy_increases_read_tps():
    import re
    out_read  = _run(tps=1000, rw_ratio=0.9)
    out_write = _run(tps=1000, rw_ratio=0.1)

    def _read_tps(out):
        m = re.search(r'Read TPS:\s+([\d.]+)', out)
        return float(m.group(1)) if m else 0

    assert _read_tps(out_read) > _read_tps(out_write)


# ─── Storage calculations ─────────────────────────────────────────────────────

def test_longer_retention_increases_db_size():
    import re

    def _db_size(out):
        m = re.search(r'Total Provisioned DB:\s+([\d.]+)', out)
        return float(m.group(1)) if m else 0

    out_30  = _run(retention_days=30)
    out_365 = _run(retention_days=365)
    assert _db_size(out_365) > _db_size(out_30)
