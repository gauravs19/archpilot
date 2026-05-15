# Archpilot Tools

This directory contains executable tools and scripts to support the Archpilot framework.

## 1. NFR Physics Calculator (`nfr_calculator.py`)

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
