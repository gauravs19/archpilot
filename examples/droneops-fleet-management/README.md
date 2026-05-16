# Example: DroneOps Fleet Management SaaS

**Pipeline Run:** archpilot-test-run-02  
**Review Score:** 94.1 / 100 — PROCEED  
**Date:** 2026-05-16

This folder contains the complete output of an Archpilot 5-phase pipeline run against a real enterprise requirement: a multi-tenant SaaS platform for drone fleet management serving logistics, agriculture, and infrastructure inspection companies.

---

## Requirement Summary

Multi-tenant SaaS platform supporting:
- Real-time telemetry ingestion from 10–500 drones per tenant
- Autonomous mission planning with geofence enforcement and LAANC authorization
- Regulatory compliance for FAA Part 107 (USA), EASA U-Space (EU), and DGCA (India)
- Automated incident detection (low battery, geofence breach, signal loss, weather alerts)
- Live video streaming to operations dashboards
- DJI and Parrot SDK integrations at launch

Budget: $2M MVP (12 months) → $5M full platform (24 months)  
Scale: 50 enterprise customers at launch → 500 at Year 2

---

## Artifacts

| Phase | Agent | File | What It Contains |
|-------|-------|------|-----------------|
| Input | — | [Input.md](Input.md) | Original high-level requirement |
| Phase 0 | SE Agent | [discovery.md](discovery.md) | 15-dimension deep discovery: physics (Little's Law, 25K msg/sec), 3-year TCO ($10.09M), STRIDE threat models, RPO/RTO per failure scenario, CAP decisions per data domain, 7 edge cases |
| Phase 1 | PO Agent | [requirements.md](requirements.md) | 12 Epics, 68 EARS-compliant User Stories with MoSCoW priority, story points, NFR tags, and RTM |
| Phase 2 | Arch Agent | [Design_HLD.md](Design_HLD.md) | C4 L1 + L2 diagrams, 4 ADRs, cost model ($18.3K/month expected), 12 NFR categories with numeric targets, zero-trust security architecture |
| Phase 3 | Arch Agent | [Design_LLD_Telemetry_Processor.md](Design_LLD_Telemetry_Processor.md) | Go service: Avro schema, Timestream schema, Redis dedup, KEDA ScaledObject YAML, distroless Dockerfile |
| Phase 3 | Arch Agent | [Design_LLD_Mission_Planning_Service.md](Design_LLD_Mission_Planning_Service.md) | Python FastAPI: mission FSM (8 states, 14 transitions), PostGIS geofence queries, LAANC async flow, KMS-signed authorization tokens |
| Phase 3 | Arch Agent | [Design_LLD_Incident_Detection_Service.md](Design_LLD_Incident_Detection_Service.md) | Python: Welford's online anomaly detection, Redis sliding windows, heartbeat scanner for signal loss, KEDA autoscaling |
| Phase 4 | Review Agent | [review_report.md](review_report.md) | 12-dimension guardrail audit, 94.1/100 score, 16 findings across 4 severity tiers, PROCEED gate |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Multi-tenancy | Pool model + PostgreSQL RLS | <$50/tenant/month at 500 tenants vs $2K+ for silo |
| MQTT broker | AWS IoT Core | Managed, 25K concurrent connections, no ops overhead |
| Telemetry storage | Amazon Timestream | Native time-series, auto-tiering 30d/90d/Glacier |
| DR strategy | Active-Passive | $35K/month vs $87K for Active-Active; RPO 1min acceptable |
| Telemetry service | Go | 25K msg/sec throughput requirement; 3× lower memory than JVM |
| Mission service | Python FastAPI | I/O-bound (LAANC polling, PostGIS, Redis); async model sufficient |

---

## Review Scorecard

| Dimension | Score |
|-----------|-------|
| Discovery Completeness | 98/100 |
| Requirements Quality | 95/100 |
| HLD Completeness | 96/100 |
| LLD Completeness (avg) | 97/100 |
| NFR Coverage | 94/100 |
| Security Design | 96/100 |
| Regulatory Compliance | 92/100 |
| Observability Coverage | 98/100 |
| Cost Modeling | 88/100 |
| Traceability | 90/100 |
| Anti-Pattern Detection | 94/100 |
| Operational Readiness | 91/100 |
| **Overall** | **94.1/100 — PROCEED** |

---

## How to Reproduce

```bash
# Initialize a new project
python archpilot.py init droneops-fleet-management

# Copy the requirement
cp examples/droneops-fleet-management/Input.md droneops-fleet-management/.specs/Input.md

# Run the full pipeline (requires ANTHROPIC_API_KEY or Claude Code)
python archpilot.py run droneops-fleet-management

# Validate all artifacts
python archpilot.py lint --tier 3 --dir droneops-fleet-management
```
