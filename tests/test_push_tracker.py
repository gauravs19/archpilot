"""Tests for tools/push_tracker.py requirements parser — no API calls."""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tools.push_tracker import parse_requirements


SAMPLE_REQUIREMENTS = """\
# DroneOps — Requirements Breakdown

<!-- Archpilot: requirements.md | Phase 1: PO AGENT -->
<!-- STATS: 2 Epics | 3 User Stories -->

---

## EP-01: Real-Time Telemetry Ingestion

> **Category:** FUNCTIONAL
> **Business Value:** Operations managers have live situational awareness of all drones.
> **Discovery Ref:** DIM-01, DIM-07, DIM-09
> **Definition of Done:**
> - p95 telemetry latency < 500ms verified under 25,000 concurrent streams.
> - Dashboard updates live without page refresh.

### EP-01-S-01: Live Drone Position on Map

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | to see all drones' real-time positions on an interactive map |
| **So that** | I can monitor the entire fleet at a glance |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Performance] [Availability] |
| **Discovery Ref** | DIM-01, DIM-07 |

**Acceptance Criteria:**
1. WHEN a drone publishes telemetry, the system SHALL update the map within 500 ms (p95).
2. The system SHALL display altitude, heading, speed, and battery % for each drone.
3. IF the connection drops, the system SHALL show a stale-data indicator within 5 seconds.

---

### EP-01-S-02: Signal Loss Alert

| Field | Value |
|-------|-------|
| **As a** | safety officer |
| **I want** | to receive an alert when a drone goes offline |
| **So that** | I can initiate a recovery procedure |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Safety] [Reliability] |
| **Discovery Ref** | DIM-04 |

**Acceptance Criteria:**
1. WHEN a drone stops sending telemetry for > 5 seconds, the system SHALL fire a P1 alert.
2. The system SHALL NOT suppress alerts during planned maintenance windows without operator confirmation.

---

## EP-02: Flight Authorization & LAANC Integration

> **Category:** SECURITY & COMPLIANCE
> **Business Value:** Operators can submit and receive FAA authorizations in < 60 seconds.
> **Discovery Ref:** DIM-02, DIM-08
> **Definition of Done:**
> - LAANC approval returned in < 60 seconds for 99% of requests.
> - All authorization records retained for 7 years per FAA requirement.

### EP-02-S-01: Submit LAANC Authorization Request

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to submit a LAANC authorization request from the app |
| **So that** | I can legally fly in controlled airspace |
| **Priority** | Must |
| **Story Points** | 13 |
| **NFR Tags** | [Compliance] [Performance] |
| **Discovery Ref** | DIM-02, DIM-08 |

**Acceptance Criteria:**
1. WHEN an operator submits a request, the system SHALL return a LAANC decision in < 60 seconds (p99).
2. The system SHALL retain all authorization records for 7 years in immutable storage.
3. IF the LAANC API is unavailable, the system SHALL queue the request and notify the operator.
"""


@pytest.fixture
def requirements_file(tmp_path):
    sd = tmp_path / ".specs"
    sd.mkdir()
    f = sd / "requirements.md"
    f.write_text(SAMPLE_REQUIREMENTS, encoding="utf-8")
    return f


# ─── Epic parsing ─────────────────────────────────────────────────────────────

def test_correct_epic_count(requirements_file):
    epics = parse_requirements(requirements_file)
    assert len(epics) == 2

def test_epic_ids(requirements_file):
    epics = parse_requirements(requirements_file)
    assert [e.id for e in epics] == ["EP-01", "EP-02"]

def test_epic_titles(requirements_file):
    epics = parse_requirements(requirements_file)
    assert "Real-Time Telemetry" in epics[0].title
    assert "Flight Authorization" in epics[1].title

def test_epic_category(requirements_file):
    epics = parse_requirements(requirements_file)
    assert epics[0].category == "FUNCTIONAL"
    assert epics[1].category == "SECURITY & COMPLIANCE"

def test_epic_business_value(requirements_file):
    epics = parse_requirements(requirements_file)
    assert "Operations managers" in epics[0].business_value

def test_epic_discovery_refs(requirements_file):
    epics = parse_requirements(requirements_file)
    assert "DIM-01" in epics[0].discovery_refs
    assert "DIM-09" in epics[0].discovery_refs

def test_epic_definition_of_done(requirements_file):
    epics = parse_requirements(requirements_file)
    dod = epics[0].definition_of_done
    assert len(dod) >= 1
    assert any("500ms" in d for d in dod)


# ─── Story parsing ────────────────────────────────────────────────────────────

def test_story_count_per_epic(requirements_file):
    epics = parse_requirements(requirements_file)
    assert len(epics[0].stories) == 2
    assert len(epics[1].stories) == 1

def test_story_ids(requirements_file):
    epics = parse_requirements(requirements_file)
    ids = [s.id for s in epics[0].stories]
    assert "EP-01-S-01" in ids
    assert "EP-01-S-02" in ids

def test_story_epic_id_linkage(requirements_file):
    epics = parse_requirements(requirements_file)
    for story in epics[0].stories:
        assert story.epic_id == "EP-01"
    for story in epics[1].stories:
        assert story.epic_id == "EP-02"

def test_story_fields_parsed(requirements_file):
    epics = parse_requirements(requirements_file)
    s = epics[0].stories[0]
    assert "fleet operations manager" in s.as_a
    assert "positions on an interactive map" in s.i_want
    assert "monitor the entire fleet" in s.so_that

def test_story_priority(requirements_file):
    epics = parse_requirements(requirements_file)
    assert epics[0].stories[0].priority == "Must"

def test_story_points(requirements_file):
    epics = parse_requirements(requirements_file)
    assert epics[0].stories[0].story_points == 8
    assert epics[0].stories[1].story_points == 5
    assert epics[1].stories[0].story_points == 13

def test_story_nfr_tags(requirements_file):
    epics = parse_requirements(requirements_file)
    tags = epics[0].stories[0].nfr_tags
    assert "Performance" in tags
    assert "Availability" in tags

def test_story_discovery_refs(requirements_file):
    epics = parse_requirements(requirements_file)
    refs = epics[0].stories[0].discovery_refs
    assert "DIM-01" in refs
    assert "DIM-07" in refs

def test_story_acceptance_criteria_count(requirements_file):
    epics = parse_requirements(requirements_file)
    assert len(epics[0].stories[0].acceptance_criteria) == 3
    assert len(epics[0].stories[1].acceptance_criteria) == 2

def test_story_acceptance_criteria_content(requirements_file):
    epics = parse_requirements(requirements_file)
    ac = epics[0].stories[0].acceptance_criteria
    assert any("500 ms" in c for c in ac)
    assert any("battery" in c for c in ac)

def test_total_story_count(requirements_file):
    epics = parse_requirements(requirements_file)
    total = sum(len(e.stories) for e in epics)
    assert total == 3

def test_no_epics_in_empty_file(tmp_path):
    f = tmp_path / "requirements.md"
    f.write_text("# Empty\n\nNo epics here.\n", encoding="utf-8")
    epics = parse_requirements(f)
    assert epics == []
