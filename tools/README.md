# Archpilot Tools

This directory contains executable tools and scripts to support the Archpilot framework.

## 1. Agentic Pipeline (`pipeline.py`)

The 5-phase agentic engine. Takes a project directory containing `Input.md` and runs SE Agent → PO Agent → Arch Agent (HLD) → Arch Agent (LLD×N) → Review Agent, writing each artifact to `.specs/`.

### Usage
```bash
# Run via the CLI (recommended)
python archpilot.py run my-project

# Or invoke directly
python tools/pipeline.py --project my-project --phases 0,1,2,3,4
```

### Phase outputs
| Phase | Agent | Output file |
|-------|-------|------------|
| 0 | SE Agent | `discovery.md` |
| 1 | PO Agent | `requirements.md` |
| 2 | Arch Agent | `Design_HLD.md` |
| 3 | Arch Agent | `Design_LLD_<ServiceName>.md` × 3–5 |
| 4 | Review Agent | `review_report.md` |

### Environment
Requires `ANTHROPIC_API_KEY`. When running inside Claude Code without an API key, Claude Code itself acts as each agent phase and writes artifacts directly via the Write tool.

### Quality gate
Phase 4 produces a score from 0–100. Score ≥ 80 = **PROCEED**. Score < 80 = **REVISE** with blocking findings listed.

---

## 2. NFR Physics Calculator (`nfr_calculator.py`)

A command-line utility that calculates the architectural physics required to support your Non-Functional Requirements (NFRs). It applies Little's Law for compute concurrency, estimates cross-AZ network egress costs, and calculates raw storage capacity.

### Usage
```bash
python nfr_calculator.py --tps 5000 --payload 2.5 --retention 30 --latency 150
```

### Arguments
- `--tps`: Target Requests Per Second (e.g., 5000)
- `--payload`: Average message/payload size in KB (e.g., 2.5)
- `--retention`: Data retention in days for storage calculation (e.g., 30)
- `--latency`: (Optional) Expected processing latency in milliseconds. Default is 50.

### Example Output
```text
============================================================
 🚀 ARCHPILOT NFR PHYSICS CALCULATOR
============================================================

📡 NETWORK & BANDWIDTH
Throughput:       12.21 MB/sec
Daily Egress:     1029.97 GB/day
Monthly Egress:   30.17 TB/month
Cross-AZ Cost:    ~$308.99 USD/month (if Kafka/DB crosses zones)

💾 STORAGE CAPACITY (Raw, uncompressed)
Daily Ingestion:  1029.97 GB/day
Total Retention:  39.21 TB (incl 30% index overhead)

⚙️  COMPUTE & CONCURRENCY (Little's Law)
Target TPS (λ):   5000 req/sec
Latency (W):      150 ms
Required Threads: 750 concurrent active threads (L)
Est. Pod Count:   4 pods (assuming 200 max active threads per pod)

⚡ DATABASE IOPS (Write-heavy estimation)
Baseline IOPS:    5000 Write IOPS
Surge IOPS (3x):  15000 Write IOPS (Provision for peaks)
```
