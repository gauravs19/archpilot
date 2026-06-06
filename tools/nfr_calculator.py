import argparse
import math

def calculate_nfrs(tps, payload_kb, retention_days, latency_ms, sla, rw_ratio):
    print("=" * 70)
    print(" ARCHPILOT ENTERPRISE NFR CALCULATOR (50+ METRICS)")
    print("=" * 70)
    
    # Pre-computations
    read_ratio = rw_ratio
    write_ratio = 1.0 - rw_ratio
    read_tps = tps * read_ratio
    write_tps = tps * write_ratio
    
    payload_bytes = payload_kb * 1024
    bytes_per_sec = tps * payload_bytes
    mb_per_sec = bytes_per_sec / (1024 * 1024)
    gb_per_hour = mb_per_sec * 3600 / 1024
    gb_per_day = gb_per_hour * 24
    tb_per_month = gb_per_day * 30 / 1024
    tb_per_year = tb_per_month * 12
    
    # 1. AVAILABILITY & RELIABILITY (10 Metrics)
    print("\n1. AVAILABILITY & RELIABILITY")
    uptime_year_mins = 365 * 24 * 60
    downtime_allowed_mins = uptime_year_mins * (1.0 - (sla / 100.0))
    downtime_allowed_month = downtime_allowed_mins / 12
    print(f" [01] Target SLA:               {sla}%")
    print(f" [02] Error Budget (Yearly):    {downtime_allowed_mins:.2f} minutes")
    print(f" [03] Error Budget (Monthly):   {downtime_allowed_month:.2f} minutes")
    print(f" [04] Max Allowed Failures/sec: {tps * (1 - (sla/100.0)):.2f} req/sec")
    print(f" [05] Recommended RTO:          < {max(5, int(downtime_allowed_month))} minutes")
    print(f" [06] Recommended RPO:          < 1 minute (Async Replication)")
    print(f" [07] Multi-Region Setup:       {'Mandatory (Active-Active)' if sla >= 99.99 else 'Recommended (Active-Passive)'}")
    print(f" [08] Circuit Breaker Trip:     >{max(500, latency_ms * 3)}ms or >50% failure rate")
    print(f" [09] Retry Policy:             Exponential backoff (Jitter + Max 3 retries)")
    print(f" [10] Chaos Engineering:        Fault injection required for {sla}% SLA validation")

    # 2. PERFORMANCE & LATENCY (10 Metrics)
    print("\n2. PERFORMANCE & LATENCY")
    processing_sec = latency_ms / 1000.0
    print(f" [11] Target P99 Latency:       {latency_ms} ms")
    print(f" [12] Target P95 Latency:       {latency_ms * 0.75:.0f} ms")
    print(f" [13] Target P50 Latency:       {latency_ms * 0.3:.0f} ms")
    print(f" [14] Read TPS:                 {read_tps:.0f} req/sec")
    print(f" [15] Write TPS:                {write_tps:.0f} req/sec")
    print(f" [16] Cache Hit Ratio Goal:     >80% for Reads")
    print(f" [17] Expected Cache Hits:      {read_tps * 0.8:.0f} req/sec")
    print(f" [18] DB Read Load (Post-Cache):{read_tps * 0.2:.0f} req/sec")
    print(f" [19] CDN Offload Target:       >90% for static assets")
    print(f" [20] DB Connection Pool Size:  {math.ceil((write_tps * processing_sec) * 1.5)} active connections")

    # 3. COMPUTE & SCALABILITY (10 Metrics)
    print("\n3. COMPUTE & CONCURRENCY (Little's Law)")
    concurrency = tps * processing_sec
    threads_per_pod = 200
    pods = math.ceil(concurrency / threads_per_pod)
    print(f" [21] Active Concurrency (L):   {math.ceil(concurrency)} simultaneous threads")
    print(f" [22] Min Pods (N):             {max(2, pods)} pods (HA minimum)")
    print(f" [23] Max Pods (N*3):           {max(2, pods) * 3} pods (Surge capacity)")
    print(f" [24] HPA Scale-Up Trigger:     CPU > 70% or Mem > 80%")
    print(f" [25] HPA Scale-Down Trigger:   CPU < 30% for 5 mins")
    print(f" [26] Kafka Partitions (Min):   {math.ceil(write_tps / 500)} partitions (assuming 500 msg/sec per partition)")
    print(f" [27] Web Server Max Threads:   {threads_per_pod + 50} limit per container")
    print(f" [28] Connection Queue Limit:   {math.ceil(tps * 2)} pending requests")
    print(f" [29] Max Payload Threshold:    10 MB (Hard rejection at API Gateway)")
    print(f" [30] Rate Limiting Target:     {math.ceil(tps / 100)} req/sec per user IP")

    # 4. STORAGE & DATA (10 Metrics)
    print("\n4. STORAGE & DATA RETENTION")
    daily_storage_gb = gb_per_day * write_ratio
    total_retention_gb = daily_storage_gb * retention_days
    index_overhead_gb = total_retention_gb * 0.4
    total_db_size_gb = total_retention_gb + index_overhead_gb
    print(f" [31] Raw Daily Write Vol:      {daily_storage_gb:.2f} GB/day")
    print(f" [32] Retention Period:         {retention_days} days")
    print(f" [33] Total Raw DB Size:        {total_retention_gb:.2f} GB")
    print(f" [34] DB Index Overhead (40%):  {index_overhead_gb:.2f} GB")
    print(f" [35] Total Provisioned DB:     {total_db_size_gb:.2f} GB")
    print(f" [36] Read Replica Count:       {math.ceil(read_tps / 2000)} replicas (assuming 2k reads/sec/node)")
    print(f" [37] Write IOPS Requirement:   {write_tps:.0f} IOPS baseline")
    print(f" [38] Surge Write IOPS (3x):    {write_tps * 3:.0f} IOPS provisioned")
    print(f" [39] Redis Cache Memory:       {total_retention_gb * 0.1:.2f} GB (assuming 10% hot working set)")
    print(f" [40] Cold Storage Archive:     {daily_storage_gb * 365 / 1024:.2f} TB/year to S3/Glacier")

    # 5. NETWORK & COST (10 Metrics)
    print("\n5. NETWORK & COST TOPOLOGY")
    print(f" [41] Ingress Bandwidth:        {mb_per_sec * write_ratio:.2f} MB/sec")
    print(f" [42] Egress Bandwidth:         {mb_per_sec * read_ratio:.2f} MB/sec")
    print(f" [43] Monthly Egress Data:      {tb_per_month:.2f} TB/month")
    cross_az_cost = tb_per_month * 1024 * 0.01  # $0.01 per GB
    print(f" [44] Est. Cross-AZ Egress:     ${cross_az_cost:.2f} / month")
    nat_cost = tb_per_month * 1024 * 0.045
    print(f" [45] Est. NAT Gateway Egress:  ${nat_cost:.2f} / month (Avoid if possible)")
    print(f" [46] WAF/DDoS Protection:      Mandatory at {tps} TPS scale")
    print(f" [47] LB Concurrent Conns:      {math.ceil(concurrency * 1.5)} persistent connections")
    print(f" [48] Inter-service Protocol:   gRPC (reduces JSON payload egress by ~40%)")
    print(f" [49] Compression:              Brotli/GZIP required on API Gateway")
    print(f" [50] VPC Subnet Sizing:        /24 per AZ minimum (254 IPs)")

    # 6. STATISTICAL VARIANCE & BURST WARNINGS
    print("\n6. VARIANCE & NON-LINEAR SCALING WARNINGS")
    print(" [!] Little's Law assumes uniform traffic distribution. It does not account for GC pauses or lock contention.")
    print(" [!] Always provision a 20% 'Burst Buffer' above the calculated maximums for CPU/Memory.")
    print(" [!] Database IOPS calculations assume linear write latency. Watch for index-bloat degradation.")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archpilot Enterprise NFR Calculator")
    parser.add_argument("--tps", type=int, required=True, help="Target Total Requests Per Second")
    parser.add_argument("--payload", type=float, required=True, help="Avg Payload Size in KB")
    parser.add_argument("--retention", type=int, required=True, help="Data Retention in Days")
    parser.add_argument("--latency", type=int, default=100, help="Target p99 Latency in MS")
    parser.add_argument("--sla", type=float, default=99.99, help="Target SLA (e.g., 99.9, 99.99)")
    parser.add_argument("--rw_ratio", type=float, default=0.8, help="Read to Write Ratio (e.g., 0.8 for 80% Reads)")
    
    args = parser.parse_args()
    calculate_nfrs(args.tps, args.payload, args.retention, args.latency, args.sla, args.rw_ratio)
