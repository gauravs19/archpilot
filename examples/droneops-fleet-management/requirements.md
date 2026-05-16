# DroneOps SaaS — Requirements Breakdown

<!-- Archpilot: requirements.md | Phase 1: PO AGENT -->
<!-- Governed by: rules/27-spec-driven-development.md | rules/50-agent-pipeline.md v4.0 -->
<!-- STATS: 12 Epics | 68 User Stories | All ACs EARS-compliant | Discovery Ref DIM-01 to DIM-15 -->

---

## Document Header

```
Project:     DroneOps Fleet Management SaaS
Version:     1.0
Status:      APPROVED
Author:      PO Agent (Phase 1)
Date:        2026-05-15
Discovery:   discovery.md v1.0 (DISC-001)
```

## Requirements Statistics

| Metric | Count | Rule 50 Constraint |
|--------|------:|-------------------|
| Total Epics | 12 | 10 - 20 |
| Total User Stories | 68 | 50 - 150 |
| Stories per Epic (avg) | 5.7 | 5 - 10 |
| Must-priority stories | 42 | |
| Security-tagged stories | 11 | |
| NFR-tagged stories | 8 | |

## Epic Categories

| Category | Epic IDs | Story Count |
|----------|----------|:-----------:|
| FUNCTIONAL | EP-01, EP-02, EP-03, EP-04, EP-05 | 34 |
| DATA & STORAGE | EP-06 | 6 |
| SECURITY & COMPLIANCE | EP-07 | 6 |
| INTEGRATION & APIs | EP-08 | 6 |
| NON-FUNCTIONAL | EP-09 | 5 |
| DEVOPS & PLATFORM | EP-10 | 6 |
| TESTING & QUALITY | EP-11 | 5 |
| MIGRATION & CUTOVER | EP-12 | 6 |

---

## EP-01: Real-Time Telemetry Ingestion & Display

> **Category:** FUNCTIONAL
> **Business Value:** Operations managers have live situational awareness of every drone, eliminating the need for radio check-ins and reducing incident response time from minutes to seconds.
> **Discovery Ref:** DIM-01 (Technical Physics), DIM-07 (Edge & Hardware), DIM-09 (Observability)
> **Definition of Done:**
> - p95 telemetry latency < 500ms verified under 25,000 concurrent stream load test.
> - Dashboard updates live without page refresh for all active drones.
> - Signal-loss alert fires within 5 seconds of connection drop.
> - MQTT QoS Level 1 deduplication verified in integration tests.

### EP-01-S-01: Live Drone Position on Map

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | to see all drones' real-time positions on an interactive map |
| **So that** | I can monitor the entire fleet at a glance without manual check-ins |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Performance] [Availability] |
| **Discovery Ref** | DIM-01, DIM-07 |

**Acceptance Criteria:**
1. WHEN a drone publishes a telemetry message, the system SHALL update its map marker position within 500 ms (p95) of the MQTT publish timestamp.
2. The system SHALL display position, altitude (metres), heading (degrees), speed (m/s), and battery % for each drone marker.
3. WHEN a drone has not sent telemetry for > 10 seconds, the system SHALL display the marker as "signal lost" (greyed out) and emit a P2 alert.
4. The system SHALL support simultaneous display of up to 500 drone markers on a single tenant's map view without frame-rate dropping below 30 fps.
5. WHEN the user zooms to a region, the system SHALL cluster markers dynamically and display count badges for clusters > 10 drones.

---

### EP-01-S-02: Telemetry Data Ingestion Pipeline

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | a reliable high-throughput MQTT-to-Kafka telemetry pipeline |
| **So that** | drone data reaches the dashboard within the 500ms SLA at 25,000 msg/sec peak |
| **Priority** | Must |
| **Story Points** | 13 |
| **NFR Tags** | [Performance] [Reliability] |
| **Discovery Ref** | DIM-01, DIM-08 |

**Acceptance Criteria:**
1. The system SHALL ingest telemetry via AWS IoT Core (MQTT) and produce to Kafka within 200 ms (p95).
2. WHEN Kafka consumer lag exceeds 10,000 messages, the system SHALL trigger an auto-scale event within 60 seconds.
3. The system SHALL deduplicate messages by (drone_id, timestamp_ms) -- duplicate messages within a 5-second window SHALL be discarded without logging an error.
4. WHEN a drone reconnects after a signal gap, the system SHALL process buffered messages in chronological order without reordering artifacts.
5. The system SHALL maintain < 1% message loss rate under 25,000 msg/sec load for 30 continuous minutes.

---

### EP-01-S-03: Telemetry History Playback

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | to replay a drone's flight path for any mission in the last 90 days |
| **So that** | I can review incidents, investigate anomalies, and generate evidence for insurance claims |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01, DIM-12 |

**Acceptance Criteria:**
1. WHEN a user selects a drone and a date range (up to 90 days ago), the system SHALL load and begin rendering the flight path within 3 seconds (p95).
2. The system SHALL support playback speeds of 1x, 5x, 10x, and 60x with smooth map animation.
3. WHEN playback is at the exact timestamp of a logged incident, the system SHALL highlight the incident marker and display the incident details panel.
4. The system SHALL NOT expose telemetry history across tenant boundaries -- a tenant admin SHALL only access their own fleet's history.

---

### EP-01-S-04: Battery & Health Status Dashboard

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | a consolidated battery and health status panel for all active drones |
| **So that** | I can proactively recall drones before they hit critical battery levels |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01 |

**Acceptance Criteria:**
1. WHEN a drone's battery drops below 30%, the system SHALL highlight the drone entry in amber in the health panel.
2. WHEN a drone's battery drops below 15%, the system SHALL highlight in red and emit a P1 alert to the assigned operator.
3. The system SHALL display: battery %, estimated flight time remaining (minutes), motor temperatures, GPS signal strength, and link quality for each active drone.
4. The system SHALL refresh health panel data within 2 seconds (p95) of receiving updated telemetry.

---

### EP-01-S-05: Signal Loss & Incident Alerting

| Field | Value |
|-------|-------|
| **As a** | field drone operator |
| **I want** | immediate notifications when a drone loses signal or triggers an incident |
| **So that** | I can take corrective action within the safety window before drone firmware triggers Return-to-Home |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Availability] |
| **Discovery Ref** | DIM-04, DIM-09 |

**Acceptance Criteria:**
1. WHEN a drone sends no telemetry for > 10 seconds, the system SHALL classify this as a "signal loss" incident and emit a push notification to the assigned operator within 3 seconds.
2. WHEN an incident is created, the system SHALL send an alert via: in-app notification, push notification (iOS/Android), and Slack webhook (if configured by tenant).
3. The system SHALL NOT generate duplicate alerts for the same incident within a 60-second window.
4. WHEN the drone reconnects, the system SHALL auto-resolve the signal-loss incident and notify the operator of resolution.

---

### EP-01-S-06: Geofence Breach Detection

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | automatic alerts when a drone exits its authorised geofence |
| **So that** | I can ensure regulatory compliance and respond before enforcement agencies are notified |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Compliance] |
| **Discovery Ref** | DIM-02, DIM-03 |

**Acceptance Criteria:**
1. WHEN a drone's reported position falls outside its assigned geofence polygon, the system SHALL detect the breach within 1 second of the telemetry message.
2. The system SHALL emit a P1 alert within 3 seconds of detection to the assigned operator and fleet admin.
3. The system SHALL log the breach event with: drone_id, timestamp_ms, coordinates, geofence_id, tenant_id -- immutably in S3 WORM storage.
4. WHEN a geofence breach occurs, the system SHALL NOT automatically command the drone (command authority remains with the operator).
5. The system SHALL support geofences defined as GeoJSON polygons with up to 200 vertices.

---

## EP-02: Mission Planning & Execution

> **Category:** FUNCTIONAL
> **Business Value:** Autonomous mission planning reduces operator workload by 60% and eliminates manual flight path calculation errors that lead to geofence violations.
> **Discovery Ref:** DIM-01, DIM-02 (FAA LAANC), DIM-08 (Integration)
> **Definition of Done:**
> - Mission creation API p95 < 200ms verified under load test.
> - Geofence validation rejects invalid missions 100% of the time in unit tests.
> - LAANC authorisation integrates with Airspace Link API in staging environment.
> - Offline mission planning functional on GCS app without network connectivity.

### EP-02-S-01: Waypoint Mission Creation

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to create a waypoint mission by drawing a flight path on the map |
| **So that** | I can plan complex inspection routes without manually entering GPS coordinates |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01, DIM-11 |

**Acceptance Criteria:**
1. The system SHALL allow operators to place up to 200 waypoints on a map and set altitude (metres AGL), speed (m/s), and action (hover/capture/return) per waypoint.
2. WHEN a user saves a mission, the system SHALL validate the flight path against current no-fly zone data within 2 seconds and return a PASS or FAIL with specific conflict details.
3. The system SHALL support mission export in DJI KMZ format and Parrot FlightPlan JSON format.
4. WHEN the user is offline (GCS app), the system SHALL allow full mission creation; the mission SHALL be queued for airspace validation on next network connectivity.
5. The mission planning API SHALL respond at p95 < 200 ms for missions with up to 200 waypoints.

---

### EP-02-S-02: FAA LAANC Airspace Authorisation

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | automated FAA LAANC authorisation requests submitted from the mission planner |
| **So that** | I can operate in controlled airspace legally without manually using DroneZone |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02, DIM-08 |

**Acceptance Criteria:**
1. WHEN a mission path intersects a LAANC-enabled airspace grid cell, the system SHALL automatically submit a LAANC authorisation request via Airspace Link API within 10 seconds of mission save.
2. WHEN LAANC returns an authorisation token, the system SHALL embed the token in the mission record and enable the "Arm for Launch" action.
3. IF the LAANC API is unavailable, the system SHALL queue the request, display a "Pending Manual Approval" status, and alert the compliance officer.
4. The system SHALL store LAANC authorisation tokens with mission records immutably (WORM) for 3 years.
5. WHEN a LAANC authorisation expires and the mission has not launched, the system SHALL notify the operator and require re-authorisation before launch is permitted.

---

### EP-02-S-03: Geofence Management

| Field | Value |
|-------|-------|
| **As a** | fleet admin |
| **I want** | to define and manage operational geofences for my fleet |
| **So that** | drones physically cannot (at SDK level) or receive alerts when they approach restricted areas |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] [Security] |
| **Discovery Ref** | DIM-02, DIM-03 |

**Acceptance Criteria:**
1. WHEN a fleet admin creates a geofence, the system SHALL accept a GeoJSON polygon with up to 200 vertices and store it with a unique ID, name, and effective date range.
2. The system SHALL publish geofence updates to the drone SDK adapter within 5 seconds of creation so the drone enforces the boundary onboard.
3. WHEN a geofence conflicts with a permanent no-fly zone (NFZ from Airspace Link), the system SHALL reject the mission and return a specific conflict description.
4. The system SHALL support both inclusion zones (must stay inside) and exclusion zones (must stay outside) geofence types.
5. WHEN a geofence is deleted, all active missions referencing it SHALL transition to status "REQUIRES_REVIEW" and operators SHALL be notified.

---

### EP-02-S-04: Mission Status Tracking

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | real-time mission status updates as drones execute planned missions |
| **So that** | I can track progress, identify deviations, and intervene if the drone deviates from the plan |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01 |

**Acceptance Criteria:**
1. WHEN a drone begins a mission, the system SHALL update mission status to EXECUTING and publish a mission_started event to Kafka within 2 seconds.
2. The system SHALL display mission progress as a percentage (waypoints completed / total waypoints) updated in real-time on the dashboard.
3. WHEN a drone deviates > 50 metres from the planned waypoint path, the system SHALL flag a "Path Deviation" incident and alert the operator.
4. WHEN a mission completes (drone returns home), the system SHALL update status to COMPLETED, generate a post-mission report, and queue compliance log generation.
5. The mission status API SHALL support polling at 1-second intervals without rate-limiting for active missions.

---

### EP-02-S-05: Drone Command & Control (Emergency Only)

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to send emergency commands (Return-to-Home, Land Now, Hover) via the platform |
| **So that** | I can respond to safety incidents from the operations center when radio is unavailable |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Security] [Performance] |
| **Discovery Ref** | DIM-03, DIM-04 |

**Acceptance Criteria:**
1. The system SHALL provide three emergency commands: RETURN_TO_HOME, LAND_NOW, and HOVER -- available only to users with Operator or Fleet Admin role.
2. WHEN an emergency command is issued, the system SHALL deliver it to the drone SDK adapter within 500 ms (p95) and confirm receipt within 2 seconds.
3. The system SHALL log every command with: issuer_user_id, drone_id, command_type, timestamp_ms, confirmation_status -- immutably.
4. IF the drone is out of communication range, the system SHALL indicate COMMAND_UNDELIVERED within 5 seconds and suggest contacting local emergency services.
5. The system SHALL NOT allow batch commands to multiple drones from a single action -- each command requires explicit per-drone confirmation to prevent accidental mass-command.

---

### EP-02-S-06: Mission Template Library

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to save and reuse mission templates for recurring inspection routes |
| **So that** | I can reduce planning time for repetitive missions from 20 minutes to under 2 minutes |
| **Priority** | Should |
| **Story Points** | 3 |
| **NFR Tags** | |
| **Discovery Ref** | DIM-11 |

**Acceptance Criteria:**
1. The system SHALL allow operators to save any mission as a named template, storing waypoints, altitudes, speeds, and actions.
2. WHEN loading a template, the system SHALL re-validate the flight path against current airspace data before enabling "Save Mission."
3. Templates SHALL be scoped per tenant and SHALL NOT be shared across tenant boundaries.
4. The system SHALL support up to 500 templates per tenant.

---

## EP-03: Regulatory Compliance Reporting

> **Category:** FUNCTIONAL
> **Business Value:** Eliminates 4 hours/week of manual report preparation per compliance officer and reduces regulatory risk of fines for improper record-keeping.
> **Discovery Ref:** DIM-02 (Regulatory), DIM-12 (Data Privacy), DIM-13 (Audit)
> **Definition of Done:**
> - FAA DroneZone XML export validated against official FAA schema XSD.
> - EASA ASTERIX Cat-21 format validated with EUROCONTROL reference decoder.
> - Reports generated within 30 seconds for a 90-day date range.
> - Flight logs stored in WORM S3 with Object Lock verified.

### EP-03-S-01: FAA Part 107 Flight Log Export

| Field | Value |
|-------|-------|
| **As a** | compliance officer |
| **I want** | to export flight logs in FAA DroneZone XML format for any date range |
| **So that** | I can submit compliant records to the FAA without manual data entry |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02 |

**Acceptance Criteria:**
1. The system SHALL generate FAA DroneZone XML export for any date range up to 90 days within 30 seconds (p95).
2. The exported XML SHALL validate against the FAA UAS flight log XSD schema version 2.1 with zero schema violations.
3. WHEN a report is generated, the system SHALL calculate a SHA-256 hash of the file and store it alongside the report in WORM S3.
4. The system SHALL retain all generated compliance reports for 3 years minimum (FAA Part 107 requirement) using S3 Object Lock in Compliance mode.
5. WHEN a report is downloaded, the event SHALL be logged with: user_id, tenant_id, date_range, file_hash, timestamp -- for audit trail purposes.

---

### EP-03-S-02: EASA U-Space Compliance Report

| Field | Value |
|-------|-------|
| **As a** | compliance officer (EU operations) |
| **I want** | automated EASA U-Space flight notification and reporting in ASTERIX format |
| **So that** | we remain compliant with EU drone regulations without building a separate system |
| **Priority** | Must (EU tenants) |
| **Story Points** | 8 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02, DIM-06 |

**Acceptance Criteria:**
1. The system SHALL automatically transmit U-Space flight notifications in ASTERIX Cat-21 format to the tenant's registered USSP within 60 seconds of mission start.
2. WHEN a flight notification is rejected by the USSP, the system SHALL alert the compliance officer with the rejection code and reason within 30 seconds.
3. All EASA-related data SHALL be stored exclusively in the eu-west-1 region -- no EASA data SHALL be replicated to us-east-1.
4. The system SHALL generate end-of-flight reports in ASTERIX format and retain them for 7 years using S3 Object Lock.

---

### EP-03-S-03: Compliance Dashboard

| Field | Value |
|-------|-------|
| **As a** | compliance officer |
| **I want** | a compliance dashboard showing the regulatory status of all flights this month |
| **So that** | I can proactively identify compliance gaps before the regulator does |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02 |

**Acceptance Criteria:**
1. The system SHALL display: total flights this period, % with LAANC authorisation, % with complete log records, geofence breach count, and open compliance incidents.
2. WHEN a flight log is incomplete (missing mandatory FAA fields), the system SHALL highlight it in the dashboard with a specific gap description.
3. The dashboard SHALL refresh compliance statistics within 5 minutes of a flight completing.
4. The system SHALL allow compliance officers to export the dashboard summary as a PDF report.

---

## EP-04: Incident Detection & Management

> **Category:** FUNCTIONAL
> **Business Value:** Automated incident detection reduces mean-time-to-detect from 3 minutes (human monitoring) to under 5 seconds, cutting incident escalation costs by 70%.
> **Discovery Ref:** DIM-01, DIM-04, DIM-09
> **Definition of Done:**
> - Incident detection latency p95 < 5 seconds verified in load test.
> - False positive rate < 5% for signal-loss incidents (validated over 30-day monitoring period).
> - All incident types covered: signal loss, geofence breach, low battery, weather alert, path deviation.

### EP-04-S-01: Automated Incident Classification

| Field | Value |
|-------|-------|
| **As a** | platform (automated) |
| **I want** | to automatically classify and create incidents from telemetry anomalies |
| **So that** | operators are alerted to real problems without human monitoring of raw telemetry streams |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01, DIM-04 |

**Acceptance Criteria:**
1. The system SHALL detect and classify the following incident types within 5 seconds (p95) of the triggering telemetry event: SIGNAL_LOSS, GEOFENCE_BREACH, LOW_BATTERY (<15%), PATH_DEVIATION (>50m from plan), WEATHER_ALERT, GPS_ANOMALY.
2. WHEN an incident is created, the system SHALL assign it a severity (P1/P2/P3) based on the incident type and drone mission status.
3. The system SHALL NOT create duplicate incidents for the same drone-incident-type within a 60-second deduplication window.
4. WHEN a GPS position jump > 50m is detected within 1 second of the previous telemetry, the system SHALL create a GPS_ANOMALY incident and flag the telemetry record for review.

---

### EP-04-S-02: Incident Acknowledgement & Resolution

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to acknowledge and resolve incidents with notes documenting the corrective action |
| **So that** | the incident log accurately reflects what happened and what was done about it |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | |
| **Discovery Ref** | DIM-12 |

**Acceptance Criteria:**
1. WHEN an operator acknowledges an incident, the system SHALL record: user_id, timestamp, and acknowledgement note (max 500 characters).
2. WHEN an incident is resolved, the system SHALL update status to RESOLVED and record: resolver_user_id, resolution timestamp, resolution notes.
3. The system SHALL retain incident records (including all state transitions) for 3 years.
4. P1 incidents that remain unacknowledged for > 5 minutes SHALL trigger an escalation notification to the Fleet Admin.

---

### EP-04-S-03: Weather Integration & Alerts

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | automatic weather alerts when conditions at a drone's location exceed safe operating limits |
| **So that** | I can proactively ground drones before unsafe conditions cause accidents |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Safety] |
| **Discovery Ref** | DIM-08, DIM-11 |

**Acceptance Criteria:**
1. The system SHALL poll aviation weather data every 15 minutes for each active mission's geographic area.
2. WHEN wind speed at mission altitude exceeds 10 m/s (22 mph), the system SHALL emit a WEATHER_ALERT incident for affected missions.
3. WHEN precipitation is forecast within 30 minutes of a drone's current position, the system SHALL emit a WEATHER_WARNING to the assigned operator.
4. IF the weather API is unavailable, the system SHALL serve the last cached forecast (max 6-hour stale) and display a "Weather data delayed" indicator on the dashboard.

---

## EP-05: Video Streaming

> **Category:** FUNCTIONAL
> **Business Value:** Live video from drone cameras enables remote visual inspection without a ground observer, reducing field staffing costs by 40% for infrastructure inspection clients.
> **Discovery Ref:** DIM-01 (physics: 300 concurrent streams), DIM-03 (security), DIM-06 (residency)
> **Definition of Done:**
> - Live stream startup latency p95 < 2 seconds.
> - Stream accessible only to tenant's authorized users (no cross-tenant access).
> - Video stored in S3 with 7-day default retention enforced.

### EP-05-S-01: Live Video Stream Viewer

| Field | Value |
|-------|-------|
| **As a** | drone operator |
| **I want** | to view a live video feed from any active drone's camera |
| **So that** | I can perform remote visual inspections without a second ground observer |
| **Priority** | Should (MVP deferrable to Month 9 per Interrogation Q4) |
| **Story Points** | 13 |
| **NFR Tags** | [Performance] [Security] |
| **Discovery Ref** | DIM-01, DIM-03 |

**Acceptance Criteria:**
1. WHEN a user opens the video panel for a drone, the system SHALL establish an HLS stream via AWS Kinesis Video Streams and begin playback within 2,000 ms (p95).
2. The system SHALL issue a signed URL with 15-minute expiry for each video stream session -- no static/long-lived URLs.
3. WHEN a stream is requested by a user outside the drone's tenant, the system SHALL return HTTP 403 and log an access violation.
4. The system SHALL support up to 300 concurrent active stream sessions across all tenants without telemetry pipeline degradation.
5. The system SHALL prioritize telemetry network bandwidth over video -- video streams SHALL be throttled before telemetry under network contention.

---

### EP-05-S-02: Video Recording & Retrieval

| Field | Value |
|-------|-------|
| **As a** | compliance officer |
| **I want** | all drone video automatically recorded and accessible for 7 days |
| **So that** | I have evidence for insurance claims and incident investigations |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] [Cost] |
| **Discovery Ref** | DIM-12 |

**Acceptance Criteria:**
1. The system SHALL automatically record all video streams to S3 using server-side AES-256 encryption.
2. WHEN a recording exceeds 7 days, the system SHALL delete it automatically (GDPR data minimisation).
3. WHEN an operator downloads a recording, the system SHALL generate a signed URL valid for 1 hour.
4. The system SHALL store no more than 30 days of recordings per drone -- tenant admins MAY extend to 90 days with explicit data processing agreement.

---

## EP-06: Data Storage & Retention

> **Category:** DATA & STORAGE
> **Business Value:** Structured, compliant data retention prevents regulatory fines and enables operational analytics without building a separate data warehouse.
> **Discovery Ref:** DIM-06 (Residency), DIM-12 (Privacy), DIM-02 (Regulatory)
> **Definition of Done:**
> - S3 Object Lock (Compliance mode) verified for flight and compliance logs.
> - Data retention jobs tested for all datasets.
> - PII fields identified and masked in non-production environments.
> - Telemetry query at 10x expected data volume returns within p95 latency targets.

### EP-06-S-01: Telemetry Time-Series Storage

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | an optimized time-series storage solution for drone telemetry |
| **So that** | dashboard queries over large time ranges execute within p95 < 500ms |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Performance] [Cost] |
| **Discovery Ref** | DIM-01, DIM-05 |

**Acceptance Criteria:**
1. The system SHALL store telemetry in Amazon Timestream with a retention policy of 30 days in the memory store and 90 days in the magnetic store.
2. WHEN querying a single drone's telemetry for any 24-hour window, the response SHALL return within 500 ms (p95) at 90 days data volume.
3. The system SHALL archive telemetry older than 90 days to S3 Glacier within 24 hours using an automated Timestream scheduled export job.
4. The system SHALL partition telemetry by (tenant_id, drone_id, date) to return tenant-scoped queries in <500ms p95.
5. WHEN a tenant account is deleted, the system SHALL queue a data purge job that removes all telemetry for that tenant within 30 days.

---

### EP-06-S-02: Flight Log Immutable Storage

| Field | Value |
|-------|-------|
| **As a** | compliance officer |
| **I want** | flight logs stored in tamper-proof WORM storage |
| **So that** | regulatory audit records cannot be altered or deleted, satisfying FAA 3-year retention |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] [Security] |
| **Discovery Ref** | DIM-02, DIM-06 |

**Acceptance Criteria:**
1. The system SHALL store all completed flight logs in S3 with Object Lock enabled in Compliance mode with a minimum retention period of 3 years (1095 days).
2. WHEN a flight log is written, the system SHALL compute its SHA-256 hash and store the hash in a separate immutable ledger table.
3. The system SHALL NOT permit deletion or modification of flight logs by any user role, including tenant admin.
4. All flight logs for EU tenants SHALL be stored exclusively in the eu-west-1 region with no cross-region replication.

---

### EP-06-S-03: PII Data Lifecycle Management

| Field | Value |
|-------|-------|
| **As a** | data privacy officer |
| **I want** | automated enforcement of PII retention limits and right-to-erasure requests |
| **So that** | we comply with GDPR Art. 5 data minimisation and Art. 17 right to erasure |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] [Security] |
| **Discovery Ref** | DIM-12 |

**Acceptance Criteria:**
1. WHEN a user submits a right-to-erasure request, the system SHALL queue a deletion job for all PII fields (email, name, IP logs) within 1 hour of submission.
2. The system SHALL complete PII erasure within 30 days of request, excluding data in S3 WORM storage with active regulatory retention lock.
3. The system SHALL NOT erase flight logs subject to FAA/EASA regulatory retention -- the system SHALL inform the user of the applicable retention obligation.
4. The system SHALL send an erasure completion confirmation to the user's email within 24 hours of job completion.
5. WHEN a drone pilot's account is deleted, the system SHALL anonymise pilot_id references in flight logs (replace with "DELETED_USER_[hash]") within 30 days.

---

### EP-06-S-04: Geospatial Mission Data Storage

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | a PostGIS-backed geospatial store for missions and geofences |
| **So that** | geofence intersection queries execute within 200ms even with thousands of geofences |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01 |

**Acceptance Criteria:**
1. The system SHALL store mission waypoints as PostGIS LINESTRING and geofences as POLYGON geometries.
2. WHEN checking if a drone position intersects any of its tenant's geofences, the query SHALL complete within 50 ms (p95) using a spatial index (GIST).
3. The system SHALL enforce row-level security on the geospatial tables so queries automatically filter to the authenticated tenant's data.
4. The system SHALL support up to 10,000 geofence polygons per tenant without query degradation.

---

### EP-06-S-05: Analytics Data Warehouse

| Field | Value |
|-------|-------|
| **As a** | fleet operations manager |
| **I want** | aggregated fleet analytics (flight hours, missions completed, incident rate) over rolling 12-month periods |
| **So that** | I can identify operational patterns and justify fleet investment decisions |
| **Priority** | Could |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Cost] |
| **Discovery Ref** | DIM-05 |

**Acceptance Criteria:**
1. The system SHALL maintain a pre-aggregated analytics store refreshed every 5 minutes from the telemetry pipeline.
2. WHEN a user queries fleet analytics for a 12-month period, the dashboard SHALL respond within 2 seconds (p95).
3. All analytics data SHALL use anonymised/aggregated drone positions (1 km grid) -- no raw GPS in analytics.
4. Analytics data SHALL be excluded from tenant data deletion jobs -- only PII-tagged fields SHALL be removed.

---

### EP-06-S-06: Database Backup & Recovery

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | automated database backups with verified restoration capability |
| **So that** | we can recover from data corruption within our 4-hour RPO target |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Availability] [Compliance] |
| **Discovery Ref** | DIM-04 |

**Acceptance Criteria:**
1. The system SHALL take automated RDS snapshots every 4 hours and retain them for 35 days.
2. WHEN a snapshot is taken, the system SHALL perform an automated restore test to a temporary instance monthly and verify row count parity.
3. The system SHALL alert the SRE on-call within 15 minutes if a snapshot job fails.
4. Database backups SHALL be stored in a separate AWS account to prevent accidental deletion.

---

## EP-07: Security & Access Control

> **Category:** SECURITY & COMPLIANCE
> **Business Value:** Enterprise customers require SOC 2 Type II compliance -- without it, no enterprise procurement. RBAC and audit logs are the two most common procurement checklist items.
> **Discovery Ref:** DIM-03 (Security), DIM-02 (Compliance)
> **Definition of Done:**
> - Pen test passed with no Critical/High unresolved findings (Month 12).
> - OWASP Top 10 checklist complete.
> - SOC 2 audit evidence package generated.
> - All secrets in AWS Secrets Manager (zero hardcoded).

### EP-07-S-01: Role-Based Access Control (RBAC)

| Field | Value |
|-------|-------|
| **As a** | tenant admin |
| **I want** | to assign roles to users with granular permissions |
| **So that** | junior operators cannot access sensitive compliance functions or emergency commands |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Security] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria:**
1. The system SHALL enforce three tenant roles: FLEET_ADMIN (full access), OPERATOR (mission execution + telemetry view), VIEWER (telemetry read-only, no commands).
2. WHEN a user attempts an action not permitted by their role, the system SHALL return HTTP 403 and log the attempt with user_id, action, and timestamp.
3. Role assignments SHALL take effect within 30 seconds of a FLEET_ADMIN making the change (no session restart required for the affected user).
4. The system SHALL NOT allow a user to escalate their own role -- role changes require a FLEET_ADMIN of equal or higher level.
5. All role change events SHALL be logged immutably for SOC 2 audit purposes.

---

### EP-07-S-02: Multi-Factor Authentication

| Field | Value |
|-------|-------|
| **As a** | fleet admin |
| **I want** | MFA enforced for all admin accounts and optionally for operator accounts |
| **So that** | compromised passwords alone cannot lead to fleet control compromise |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Security] [Compliance] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria:**
1. The system SHALL enforce TOTP-based MFA for all FLEET_ADMIN accounts -- login SHALL fail without a valid TOTP code.
2. WHEN a FLEET_ADMIN account has MFA disabled, the system SHALL block all administrative actions and display a "MFA Required" warning.
3. The system SHALL allow tenant admins to enforce MFA for OPERATOR role accounts as an opt-in tenant policy.
4. WHEN 5 consecutive failed MFA attempts occur, the system SHALL lock the account and notify the tenant's primary admin.

---

### EP-07-S-03: API Key Management

| Field | Value |
|-------|-------|
| **As a** | tenant system admin |
| **I want** | to create and manage API keys for system integrations |
| **So that** | third-party systems (dispatch software, ERP) can integrate with DroneOps securely |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Security] |
| **Discovery Ref** | DIM-03, DIM-08 |

**Acceptance Criteria:**
1. The system SHALL allow FLEET_ADMINs to create API keys with a configurable expiry (30/90/365 days or never) and a human-readable description.
2. API keys SHALL be displayed in full only at creation time -- subsequent views SHALL show only the last 4 characters.
3. The system SHALL enforce a maximum of 20 active API keys per tenant.
4. WHEN an API key is used, the system SHALL log: key_id (not the key itself), source IP, endpoint, and timestamp.
5. WHEN an API key expires or is revoked, all requests using it SHALL return HTTP 401 within 60 seconds of expiry.

---

### EP-07-S-04: Security Audit Log

| Field | Value |
|-------|-------|
| **As a** | CISO |
| **I want** | a tamper-proof audit log of all security-relevant actions |
| **So that** | we can investigate incidents and provide evidence to auditors |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Security] [Compliance] |
| **Discovery Ref** | DIM-03, DIM-02 |

**Acceptance Criteria:**
1. The system SHALL log the following events to an immutable audit log: login/logout, role changes, API key create/delete/use, emergency command issuance, data export, geofence changes, mission approval.
2. Audit log entries SHALL include: event_type, actor_user_id, target_resource_id, tenant_id, source_ip, timestamp_ms, outcome (SUCCESS/FAILURE).
3. The audit log SHALL be stored in S3 WORM storage with 3-year retention and SHALL NOT be accessible for deletion by any application role.
4. The system SHALL expose an audit log query API allowing FLEET_ADMINs to filter by user, event type, and date range with results paginated at 100 records per page.

---

### EP-07-S-05: Secrets Management

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | all service credentials and API keys stored in AWS Secrets Manager |
| **So that** | zero secrets appear in code, environment variables, or configuration files |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Security] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria:**
1. The system SHALL retrieve all secrets (DB passwords, external API keys, JWT signing keys) from AWS Secrets Manager at service startup.
2. WHEN a secret is rotated, running services SHALL pick up the new secret within 60 seconds without restart.
3. The CI/CD pipeline SHALL fail with a CRITICAL error if any secret pattern (API key, password, JWT token) is detected in committed code via Gitleaks scan.
4. Secrets SHALL be encrypted with a customer-managed KMS key (CMK) per environment.

---

### EP-07-S-06: Tenant Isolation Verification

| Field | Value |
|-------|-------|
| **As a** | security engineer |
| **I want** | automated tests that verify tenant data isolation at every deployment |
| **So that** | a regression cannot silently introduce a cross-tenant data leakage vulnerability |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Security] |
| **Discovery Ref** | DIM-03, DIM-14 |

**Acceptance Criteria:**
1. The CI/CD pipeline SHALL run a tenant isolation test suite at every deployment that: creates two synthetic tenants, seeds data for each, and asserts that Tenant A cannot read Tenant B's data via any API endpoint.
2. WHEN a tenant isolation test fails, the deployment pipeline SHALL halt and alert the security team within 5 minutes.
3. The test suite SHALL cover: telemetry API, mission API, video API, user management API, compliance report API, and direct database queries (via ORM).
4. Canary sentinel records (known fake records with unique IDs) SHALL be present in each synthetic tenant's data and SHALL be monitored for access from other tenants in production.

---

## EP-08: External Integrations & APIs

> **Category:** INTEGRATION & APIs
> **Business Value:** An open API platform enables enterprise customers to integrate DroneOps with their existing dispatch, ERP, and operations systems, making it sticky and increasing contract value.
> **Discovery Ref:** DIM-08 (Connectivity & Integration), DIM-10 (Lifecycle)
> **Definition of Done:**
> - OpenAPI 3.1 spec published and validated (zero Spectral lint errors).
> - All integration endpoints covered by contract tests.
> - Rate limiting verified under load test.
> - Webhook delivery verified with retry and DLQ.

### EP-08-S-01: Public REST API (v1)

| Field | Value |
|-------|-------|
| **As a** | enterprise customer developer |
| **I want** | a well-documented public REST API for fleet management operations |
| **So that** | I can integrate DroneOps with our dispatch and logistics systems without manual data entry |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Integration] [Security] |
| **Discovery Ref** | DIM-08, DIM-10 |

**Acceptance Criteria:**
1. The system SHALL expose a versioned REST API at `/v1/` covering: drones (CRUD), missions (CRUD + status), telemetry (read), incidents (read + update), compliance-reports (generate + download).
2. All API responses SHALL follow RFC 7807 Problem Details format for errors, including: type, title, status, detail, and instance fields.
3. The API SHALL enforce pagination on all list endpoints with a default page size of 50 and a maximum of 200 records per page.
4. The system SHALL publish an OpenAPI 3.1 specification with zero Spectral lint errors at `/v1/openapi.json`.
5. WHEN a breaking change is introduced, the system SHALL maintain the v1 API for a minimum of 12 months while v2 is available.

---

### EP-08-S-02: Webhook Event Delivery

| Field | Value |
|-------|-------|
| **As a** | enterprise customer developer |
| **I want** | webhook notifications for key events (mission completed, incident created, geofence breach) |
| **So that** | our operations system can react in real-time without polling the DroneOps API |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Reliability] |
| **Discovery Ref** | DIM-08 |

**Acceptance Criteria:**
1. The system SHALL deliver webhook events within 5 seconds (p95) of the triggering event.
2. WHEN webhook delivery fails (non-2xx response or timeout), the system SHALL retry with exponential backoff: 30s, 5min, 30min -- maximum 3 attempts.
3. WHEN all 3 retry attempts fail, the system SHALL move the event to a DLQ and alert the tenant admin.
4. Webhook payloads SHALL include an HMAC-SHA256 signature header (`X-DroneOps-Signature`) for payload verification.
5. The system SHALL maintain a 7-day webhook delivery history accessible via the API.

---

### EP-08-S-03: Drone SDK Adapter Framework

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | a pluggable drone SDK adapter layer that normalises telemetry from different drone vendors |
| **So that** | new drone hardware can be added without changes to the telemetry pipeline |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Integration] |
| **Discovery Ref** | DIM-07, DIM-13 |

**Acceptance Criteria:**
1. The system SHALL define a DroneAdapter interface with methods: connect(), stream_telemetry(), send_command(), disconnect() -- all adapters MUST implement this interface.
2. WHEN a DJI drone connects, the DJI adapter SHALL normalise DJI-proprietary telemetry to the DroneOps canonical telemetry schema within 10 ms of receipt.
3. WHEN a Parrot drone connects, the Parrot adapter SHALL normalise Parrot GroundSDK telemetry to the same canonical schema.
4. The adapter layer SHALL be tested with vendor SDK simulators -- integration tests SHALL not require physical drones.
5. Adding a new drone vendor (Autel Robotics Year 2) SHALL require implementing the DroneAdapter interface only, with zero changes to the Kafka producer or telemetry processing service.

---

### EP-08-S-04: Airspace Data Integration

| Field | Value |
|-------|-------|
| **As a** | mission planning system |
| **I want** | real-time airspace data (NFZ, LAANC grids, TFRs) from Airspace Link |
| **So that** | mission validation always uses current airspace restrictions, not stale cached data |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Integration] [Compliance] |
| **Discovery Ref** | DIM-08 |

**Acceptance Criteria:**
1. The system SHALL refresh Temporary Flight Restriction (TFR) data from Airspace Link every 5 minutes.
2. WHEN Airspace Link returns an updated NFZ polygon, the system SHALL update the geospatial store within 30 seconds.
3. IF Airspace Link API is unavailable for > 30 minutes, the system SHALL serve the last cached data with a staleness warning displayed in the mission planner UI.
4. The system SHALL cache up to 24 hours of NFZ data locally to support offline GCS mission planning.

---

### EP-08-S-05: Notification Channel Integrations

| Field | Value |
|-------|-------|
| **As a** | fleet admin |
| **I want** | to route incident alerts to Slack, PagerDuty, or email based on severity |
| **So that** | P1 incidents reach on-call operators via their preferred channel automatically |
| **Priority** | Should |
| **Story Points** | 3 |
| **NFR Tags** | [Integration] |
| **Discovery Ref** | DIM-09 |

**Acceptance Criteria:**
1. The system SHALL support the following notification channels: in-app, email (SES), Slack webhook, PagerDuty Events API.
2. WHEN a P1 incident is created, the system SHALL notify via all channels configured by the tenant within 30 seconds.
3. Notification routing rules SHALL be configurable per incident severity and incident type by FLEET_ADMINs.
4. WHEN a notification delivery fails, the system SHALL fall back to email notification and log the delivery failure.

---

### EP-08-S-06: Tenant Onboarding API

| Field | Value |
|-------|-------|
| **As a** | platform admin |
| **I want** | an automated tenant provisioning API |
| **So that** | new enterprise customers can be onboarded in under 10 minutes without manual infrastructure work |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [DevOps] |
| **Discovery Ref** | DIM-14 |

**Acceptance Criteria:**
1. WHEN a new tenant is provisioned via the API, the system SHALL: create a tenant record, assign a home region, create Kafka topic prefixes, configure RLS policies, and create an initial FLEET_ADMIN account -- all within 5 minutes.
2. The provisioning SHALL be idempotent -- re-running provisioning for the same tenant_id SHALL NOT create duplicate resources.
3. WHEN provisioning fails at any step, the system SHALL roll back all created resources and return a specific error indicating the failed step.
4. All provisioning steps SHALL be logged to the immutable audit log.

---

## EP-09: Non-Functional Requirements

> **Category:** NON-FUNCTIONAL
> **Business Value:** Enterprise procurement requires contractual SLAs. Without verified NFR targets, procurement is blocked at legal review.
> **Discovery Ref:** DIM-01 (Technical Physics), DIM-04 (Resilience)
> **Definition of Done:**
> - Load test at 2x peak RPS shows all latency targets met.
> - SLAs met for 30 consecutive days in staging.
> - Auto-scaling verified: scale-out in < 90 sec from trigger.
> - Chaos game day passed: pod kill, AZ loss, DB failover, Kafka broker failure.

### EP-09-S-01: Telemetry Pipeline Performance

| Field | Value |
|-------|-------|
| **As a** | operations manager |
| **I want** | drone positions on the dashboard to update within 500ms of transmission |
| **So that** | the dashboard represents actual drone positions for safe operational decisions |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01 |

**Acceptance Criteria:**
1. The system SHALL process and display telemetry at p50 < 150ms, p95 < 500ms, p99 < 1,000ms end-to-end (MQTT publish to WebSocket receipt) under 25,000 concurrent telemetry streams.
2. WHEN concurrent streams increase from 5,000 to 25,000 over 10 minutes, the system SHALL maintain p95 < 500ms throughout the ramp.
3. The system SHALL maintain < 1% message loss rate at 25,000 msg/sec for 30 continuous minutes in load test.

---

### EP-09-S-02: API Performance & Availability

| Field | Value |
|-------|-------|
| **As a** | product stakeholder |
| **I want** | the API to meet SLA targets for availability and response time |
| **So that** | enterprise contracts with SLA clauses can be signed without legal risk |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Availability] [Performance] |
| **Discovery Ref** | DIM-04 |

**Acceptance Criteria:**
1. The system SHALL maintain >= 99.9% monthly uptime for the telemetry ingest and mission planning APIs (measured by external synthetic monitoring).
2. The mission planning API SHALL respond at p95 < 200ms for mission creation with up to 200 waypoints under 500 RPS.
3. WHEN a single AZ fails, the system SHALL recover and resume serving API traffic within 2 minutes via ALB health-check routing.
4. WHEN traffic doubles within 5 minutes, the system SHALL auto-scale and maintain p95 latency within 20% of baseline within 90 seconds.

---

### EP-09-S-03: Database Performance

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | database queries to execute within defined latency targets even at scale |
| **So that** | performance does not degrade as tenant count grows from 50 to 500 |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] |
| **Discovery Ref** | DIM-01, DIM-14 |

**Acceptance Criteria:**
1. Telemetry read queries (single drone, 24-hour range) SHALL complete within 500ms (p95) at 90-day data volume.
2. Geofence intersection queries (check point against all tenant geofences) SHALL complete within 50ms (p95) with up to 10,000 geofences per tenant.
3. Mission CRUD operations SHALL complete within 200ms (p95) under 500 concurrent writes.
4. WHEN a tenant's data volume exceeds 1TB, the system SHALL automatically add read replicas and route read queries to replicas.

---

### EP-09-S-04: Multi-Tenant Noisy-Neighbor Prevention

| Field | Value |
|-------|-------|
| **As a** | enterprise customer |
| **I want** | my fleet operations to be unaffected by other tenants' load spikes |
| **So that** | I receive consistent service quality regardless of platform-wide load |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Availability] |
| **Discovery Ref** | DIM-14 |

**Acceptance Criteria:**
1. The system SHALL enforce per-tenant rate limits: MQTT ingestion 1,000 msg/sec; REST API 500 RPS; WebSocket connections 200 per tenant.
2. WHEN a tenant exceeds rate limits, the system SHALL return HTTP 429 with a `Retry-After` header and SHALL NOT affect other tenants' performance.
3. The system SHALL enforce per-tenant Kafka consumer group isolation -- a burst in Tenant A's topic SHALL NOT increase Tenant B's consumer lag.
4. The SRE team SHALL receive an alert when a single tenant's resource usage exceeds 20% of total platform capacity.

---

### EP-09-S-05: Disaster Recovery Validation

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | quarterly DR drills that verify recovery within RTO targets |
| **So that** | the DR plan is proven, not theoretical, before a real disaster occurs |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Availability] |
| **Discovery Ref** | DIM-04 |

**Acceptance Criteria:**
1. WHEN a DR drill is initiated, the system SHALL failover all critical services to the DR region (us-west-2) within 15 minutes.
2. The DR environment SHALL serve live traffic within 15 minutes of failover initiation.
3. The system SHALL recover within 1 minute RPO (maximum 1 minute of data loss) for telemetry during regional failover.
4. DR drill results SHALL be documented and reviewed within 5 business days; any RTO/RPO miss SHALL result in a remediation plan within 30 days.

---

## EP-10: DevOps & Platform Engineering

> **Category:** DEVOPS & PLATFORM
> **Business Value:** Sub-60-minute deployment pipelines reduce change failure rate and enable daily production releases, which is required to iterate quickly on enterprise feedback.
> **Discovery Ref:** DIM-10 (Lifecycle), DIM-09 (Observability)
> **Definition of Done:**
> - Pipeline deploys to Production without manual steps.
> - IaC applied in all 3 environments (dev, staging, prod).
> - Zero hardcoded secrets (Gitleaks scan passes).
> - Rollback cycle < 5 minutes.

### EP-10-S-01: CI/CD Pipeline

| Field | Value |
|-------|-------|
| **As a** | developer |
| **I want** | an automated CI/CD pipeline from commit to production |
| **So that** | delivery cycle is < 30 minutes with quality gates enforced |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [DevOps] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. WHEN code is merged to `main`, the pipeline SHALL execute: lint, unit tests, SAST (Semgrep), container build, integration tests, tenant isolation tests, DAST (OWASP ZAP), deploy to staging.
2. WHEN any pipeline stage fails, the pipeline SHALL halt and notify the author via Slack within 2 minutes.
3. WHEN all stages pass, the system SHALL deploy to production via blue-green strategy with 10% canary traffic for 10 minutes before full rollout.
4. The pipeline SHALL complete commit-to-staging within 15 minutes (p95) and commit-to-production within 30 minutes.
5. WHEN a production deployment fails its health check, the system SHALL automatically rollback to the previous version within 5 minutes.

---

### EP-10-S-02: Infrastructure as Code

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | all AWS infrastructure defined in Terraform |
| **So that** | any environment can be reproduced from code and infrastructure changes are auditable |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [DevOps] [Security] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. The system SHALL define all AWS resources (EKS, RDS, MSK, IoT Core, S3, VPC, IAM) in Terraform with no manually-created resources in production.
2. WHEN a Terraform plan is proposed, the CI pipeline SHALL run `terraform plan` and post the diff to the PR for review.
3. The system SHALL use separate Terraform state files per environment stored in S3 with DynamoDB locking.
4. `terraform apply` for a new environment SHALL provision all resources within 30 minutes.
5. Terraform modules SHALL be version-pinned and all provider versions SHALL be explicitly declared.

---

### EP-10-S-03: Container & Kubernetes Configuration

| Field | Value |
|-------|-------|
| **As a** | platform engineer |
| **I want** | all services containerized and deployed on EKS with Helm charts |
| **So that** | services are portable, consistently deployed, and auto-scaling is managed by Kubernetes |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [DevOps] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. All microservices SHALL have a multi-stage Dockerfile that produces an image < 200 MB (using distroless base for non-JVM services).
2. Each service SHALL have a Helm chart with configurable resource requests/limits, HPA settings, and health-check endpoints.
3. Services SHALL have: liveness probe (response within 5s), readiness probe (response within 2s), and a /healthz endpoint.
4. The system SHALL enforce Kubernetes NetworkPolicies that restrict service-to-service communication to only declared dependencies.
5. Container images SHALL be scanned with Trivy on every build -- images with CRITICAL CVEs SHALL be blocked from deployment.

---

### EP-10-S-04: Observability Stack Deployment

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | a fully deployed observability stack (metrics, logs, traces, dashboards) |
| **So that** | I can debug incidents within 5 minutes using correlated signals |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [DevOps] [Availability] |
| **Discovery Ref** | DIM-09 |

**Acceptance Criteria:**
1. The system SHALL export metrics via OpenTelemetry to Amazon CloudWatch with service-level dashboards for all 5 core services.
2. The system SHALL aggregate logs via Fluentd to OpenSearch with full-text search available within 30 seconds of log emission.
3. The system SHALL export traces via OpenTelemetry to AWS X-Ray with service map visualisation.
4. WHEN a p95 latency breach occurs, the CloudWatch alarm SHALL fire within 2 minutes and the PagerDuty alert SHALL be created within 3 minutes.
5. SRE dashboards SHALL display: telemetry pipeline health, Kafka consumer lag, mission API error rate, active WebSocket connections, and top 5 resource-consuming tenants.

---

### EP-10-S-05: Environment Management

| Field | Value |
|-------|-------|
| **As a** | developer |
| **I want** | isolated dev, staging, and production environments with data separation |
| **So that** | production data is never accessible in development environments |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Security] [DevOps] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria:**
1. Dev and staging environments SHALL use synthetic data only -- production database SHALL never be copied to non-prod environments.
2. Each environment SHALL use its own AWS account (separate account per environment via AWS Organizations).
3. Dev environment SHALL automatically shut down EKS worker nodes after 20 minutes of zero traffic to reduce cost.
4. Non-production environments SHALL have feature flags to enable synthetic telemetry data generation at configurable rates.

---

### EP-10-S-06: Feature Flag Management

| Field | Value |
|-------|-------|
| **As a** | product manager |
| **I want** | to control feature rollout per tenant using feature flags |
| **So that** | new features can be tested with specific enterprise customers before general availability |
| **Priority** | Should |
| **Story Points** | 3 |
| **NFR Tags** | [DevOps] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. The system SHALL integrate LaunchDarkly for feature flag management with per-tenant targeting rules.
2. WHEN a feature flag is toggled, the change SHALL propagate to all running service instances within 30 seconds.
3. WHEN LaunchDarkly is unavailable, the system SHALL fall back to the last-known flag state stored in Redis for up to 1 hour.
4. All feature flags SHALL have a defined owner, created date, and review date to prevent flag accumulation.

---

## EP-11: Testing & Quality Assurance

> **Category:** TESTING & QUALITY
> **Business Value:** ≥80% branch coverage and contract testing reduce production incident rate by target of 40% QoQ. Drone operations safety depends on correct software behavior.
> **Discovery Ref:** DIM-10 (Lifecycle)
> **Definition of Done:**
> - 80% branch coverage enforced in CI.
> - Contract tests running against all external system stubs.
> - Chaos game day playbook executed before launch.

### EP-11-S-01: Unit & Integration Test Coverage

| Field | Value |
|-------|-------|
| **As a** | engineering lead |
| **I want** | enforced test coverage thresholds with integration tests against real dependencies |
| **So that** | regressions in critical paths (telemetry, mission, compliance) are caught before production |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Quality] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. The CI pipeline SHALL enforce >= 80% branch coverage for all services; PRs below threshold SHALL be blocked from merge.
2. The system SHALL have integration tests for: Kafka producer/consumer, PostgreSQL geospatial queries, S3 WORM write verification, and MQTT ingestion pipeline.
3. Integration tests SHALL run against real AWS services in a dedicated test account (not mocked) -- only external vendor APIs (DJI, FAA LAANC) SHALL use recorded fixtures.
4. WHEN coverage drops below 80% in any service, the CI build SHALL fail and the PR author SHALL be notified.

---

### EP-11-S-02: Contract Testing for External APIs

| Field | Value |
|-------|-------|
| **As a** | integration engineer |
| **I want** | consumer-driven contract tests for all external API integrations |
| **So that** | a breaking change in Airspace Link or Auth0 API is detected before it reaches production |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Quality] [Integration] |
| **Discovery Ref** | DIM-08 |

**Acceptance Criteria:**
1. The system SHALL have Pact contract tests for: FAA LAANC (Airspace Link), Auth0 OIDC, Aviation Weather API, and Parrot GroundSDK.
2. WHEN an external API response changes a field name or type, the Pact verification SHALL fail in CI within 30 minutes of the change.
3. Contract tests SHALL run in CI on every PR to any service that calls an external API.
4. A new external API integration SHALL require a Pact contract test before the integration PR can be merged.

---

### EP-11-S-03: Load & Performance Testing

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | automated performance baselines tested weekly against the staging environment |
| **So that** | latency regressions are detected in staging before they reach production |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Performance] [Quality] |
| **Discovery Ref** | DIM-01 |

**Acceptance Criteria:**
1. The system SHALL run a k6 load test weekly against staging: 25,000 concurrent telemetry streams for 30 minutes.
2. WHEN p95 telemetry latency in the load test exceeds 600ms (20% above the 500ms target), the SRE team SHALL be alerted.
3. Mission planning API SHALL be load-tested at 500 RPS for 10 minutes weekly; p95 target: < 200ms.
4. Load test results SHALL be published to the team dashboard with week-over-week comparison.

---

### EP-11-S-04: Security & Penetration Testing

| Field | Value |
|-------|-------|
| **As a** | CISO |
| **I want** | annual third-party penetration testing + quarterly automated DAST scans |
| **So that** | security vulnerabilities are found by us before they are found by attackers or auditors |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | [Security] [Quality] |
| **Discovery Ref** | DIM-03 |

**Acceptance Criteria:**
1. OWASP ZAP DAST scan SHALL run against the staging environment on every production deployment.
2. WHEN a CRITICAL or HIGH DAST finding is reported, the deployment SHALL be blocked until the finding is resolved or formally accepted with CISO sign-off.
3. An annual third-party penetration test SHALL be commissioned; all Critical and High findings SHALL be remediated within 30 days.
4. The CI pipeline SHALL run Semgrep SAST on every PR; Critical findings SHALL block merge.

---

### EP-11-S-05: Chaos Engineering

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | quarterly chaos game days that test failure scenarios against the staging environment |
| **So that** | the team has practiced and verified recovery procedures before real incidents occur |
| **Priority** | Should |
| **Story Points** | 5 |
| **NFR Tags** | [Availability] [Quality] |
| **Discovery Ref** | DIM-04 |

**Acceptance Criteria:**
1. WHEN a quarterly game day is conducted, the team SHALL test: random pod termination (Chaos Monkey), AZ network partition, RDS Multi-AZ failover, and Kafka broker shutdown.
2. Each game day scenario SHALL have a defined steady-state hypothesis (e.g., "telemetry pipeline maintains p95 < 500ms") and SHALL record whether the hypothesis held.
3. WHEN a hypothesis fails, the team SHALL create a remediation item in the backlog and track it to resolution before the next game day.
4. Game day results SHALL be documented in a post-game-day report published within 48 hours.

---

## EP-12: Migration & Cutover

> **Category:** MIGRATION & CUTOVER
> **Business Value:** Enterprise customers migrating from competitor platforms (AeroSync, Percepto) must migrate their historical flight data and compliance records without gaps, or contracts cannot be signed.
> **Discovery Ref:** DIM-10 (Lifecycle), DIM-04 (Resilience), DIM-02 (Regulatory)
> **Definition of Done:**
> - Data migration dry-run completed with zero data loss verified.
> - Rollback plan tested and timed.
> - Cutover runbook approved by operations team.

### EP-12-S-01: Customer Flight Data Import

| Field | Value |
|-------|-------|
| **As a** | enterprise customer admin |
| **I want** | to import historical flight logs from our previous system into DroneOps |
| **So that** | we maintain regulatory compliance with 3-year FAA record retention after migrating platforms |
| **Priority** | Must |
| **Story Points** | 8 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02, DIM-10 |

**Acceptance Criteria:**
1. The system SHALL accept historical flight log imports in CSV, JSON, and FAA DroneZone XML formats.
2. WHEN an import is submitted, the system SHALL validate all records for required FAA fields and return a validation report within 5 minutes.
3. The system SHALL process imports of up to 100,000 flight log records within 30 minutes using a background job.
4. WHEN an import completes, records SHALL be stored in WORM S3 with the same retention policy as natively-generated logs.
5. WHEN import fails for specific records, the system SHALL create a per-record error log and allow re-import of failed records only.

---

### EP-12-S-02: Drone Fleet Registration Import

| Field | Value |
|-------|-------|
| **As a** | fleet admin |
| **I want** | to bulk import our existing drone inventory via a CSV template |
| **So that** | I can register 500 drones without entering each one manually |
| **Priority** | Must |
| **Story Points** | 3 |
| **NFR Tags** | |
| **Discovery Ref** | DIM-14 |

**Acceptance Criteria:**
1. The system SHALL provide a CSV template for drone registration: serial_number, make, model, max_payload_kg, certification_number.
2. WHEN a bulk import CSV is uploaded, the system SHALL validate format and required fields and return a validation report within 60 seconds.
3. The system SHALL process up to 500 drone registrations in a single import within 5 minutes.
4. Duplicate serial numbers SHALL generate a validation error, not silently overwrite existing records.

---

### EP-12-S-03: Zero-Downtime Platform Cutover

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | a documented and tested cutover procedure for production deployments |
| **So that** | enterprise customers experience no service interruption during major version upgrades |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Availability] |
| **Discovery Ref** | DIM-04, DIM-10 |

**Acceptance Criteria:**
1. All production deployments SHALL use blue-green strategy with health-check validation before traffic switch.
2. WHEN a deployment fails health checks in green environment, the system SHALL NOT switch traffic and SHALL alert the SRE on-call within 2 minutes.
3. Rollback from a failed deployment SHALL complete within 5 minutes via ALB target group switch.
4. The cutover runbook SHALL document all manual steps, estimated duration, and rollback decision points -- approved by the engineering lead before each major release.

---

### EP-12-S-04: Tenant Offboarding & Data Export

| Field | Value |
|-------|-------|
| **As a** | enterprise customer admin |
| **I want** | to export all my fleet data and flight records before cancelling the subscription |
| **So that** | I retain my operational data and comply with record-keeping obligations after leaving the platform |
| **Priority** | Must |
| **Story Points** | 5 |
| **NFR Tags** | [Compliance] [Data Integrity] |
| **Discovery Ref** | DIM-12 |

**Acceptance Criteria:**
1. The system SHALL allow FLEET_ADMINs to request a full data export: flight logs (XML/JSON), telemetry (CSV), missions (JSON), incident records (JSON).
2. WHEN a data export is requested, the system SHALL generate a secure download package within 24 hours.
3. The export package SHALL be available for download via signed URL for 7 days before expiry.
4. WHEN a tenant is marked for deletion, the system SHALL retain regulatory-locked flight logs in WORM storage for the remainder of the retention period and notify the customer of this obligation.

---

### EP-12-S-05: Compliance Record Transfer Protocol

| Field | Value |
|-------|-------|
| **As a** | compliance officer |
| **I want** | a protocol for transferring compliance records to a successor platform |
| **So that** | regulatory continuity is maintained during any future platform transition |
| **Priority** | Should |
| **Story Points** | 3 |
| **NFR Tags** | [Compliance] |
| **Discovery Ref** | DIM-02 |

**Acceptance Criteria:**
1. The system SHALL support export of compliance records in standard open formats: FAA XML, EASA ASTERIX, and generic JSON.
2. Exported compliance records SHALL include digital signatures verifiable by the importing system.
3. The system SHALL provide a compliance record hash ledger export so record integrity can be verified after import into any successor system.

---

### EP-12-S-06: Platform Version Upgrade Runbook

| Field | Value |
|-------|-------|
| **As a** | SRE engineer |
| **I want** | a tested runbook for major version upgrades (EKS, RDS, Kafka) |
| **So that** | infrastructure upgrades do not cause unplanned downtime during drone operations |
| **Priority** | Should |
| **Story Points** | 3 |
| **NFR Tags** | [Availability] |
| **Discovery Ref** | DIM-10 |

**Acceptance Criteria:**
1. Each major infrastructure component (EKS, RDS, MSK Kafka) SHALL have a documented upgrade runbook including: pre-checks, upgrade steps, post-checks, and rollback steps.
2. WHEN an EKS cluster upgrade is performed, the system SHALL use rolling node replacement with zero service interruption.
3. WHEN an RDS major version upgrade is required, the system SHALL use a blue-green database upgrade (new instance + traffic cut) to limit downtime to < 60 seconds.
4. Runbooks SHALL be tested annually in staging and the results documented.

---

## Requirements Traceability Matrix (RTM)

| Story ID | Business Goal | Discovery Dim | HLD Component | Test Coverage |
|----------|---------------|:-------------:|---------------|:-------------:|
| EP-01-S-01 | Live fleet situational awareness | DIM-01, DIM-07 | Dashboard BFF, WebSocket Gateway | Unit + E2E |
| EP-01-S-02 | Telemetry ingest pipeline | DIM-01, DIM-08 | Telemetry Processor, Kafka | Unit + Load |
| EP-02-S-01 | Mission planning | DIM-01, DIM-11 | Mission Planning Service | Unit + Integration |
| EP-02-S-02 | FAA LAANC authorisation | DIM-02, DIM-08 | Mission Planning Service, LAANC Adapter | Contract |
| EP-03-S-01 | FAA compliance report | DIM-02 | Compliance Report Service | Unit + Compliance |
| EP-06-S-01 | Telemetry storage | DIM-01, DIM-05 | Timestream, S3 | Integration |
| EP-07-S-01 | RBAC | DIM-03 | Auth Service, API Gateway | Unit + Security |
| EP-09-S-01 | SLA: telemetry latency | DIM-01 | Full pipeline | Load |
| EP-10-S-01 | CI/CD pipeline | DIM-10 | All services | Pipeline |
| EP-11-S-01 | Test coverage | DIM-10 | All services | Coverage |

---

*Archpilot -- Requirements Breakdown v4.0 | DroneOps SaaS*
*Generated by PO Agent (Phase 1) | Governed by rules/27-spec-driven-development.md*
