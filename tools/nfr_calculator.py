import argparse
import math

def calculate_nfrs(tps, payload_kb, retention_days, processing_ms):
    print("=" * 60)
    print(" 🚀 ARCHPILOT NFR PHYSICS CALCULATOR")
    print("=" * 60)
    
    # 1. Bandwidth & Egress
    payload_bytes = payload_kb * 1024
    bytes_per_sec = tps * payload_bytes
    mb_per_sec = bytes_per_sec / (1024 * 1024)
    gb_per_day = (mb_per_sec * 86400) / 1024
    tb_per_month = (gb_per_day * 30) / 1024
    
    print("\n📡 NETWORK & BANDWIDTH")
    print(f"Throughput:       {mb_per_sec:.2f} MB/sec")
    print(f"Daily Egress:     {gb_per_day:.2f} GB/day")
    print(f"Monthly Egress:   {tb_per_month:.2f} TB/month")
    
    # AWS Cross AZ cost estimate (~$0.01/GB)
    cross_az_cost = gb_per_day * 30 * 0.01
    print(f"Cross-AZ Cost:    ~${cross_az_cost:.2f} USD/month (if Kafka/DB crosses zones)")

    # 2. Storage Capacity
    print("\n💾 STORAGE CAPACITY (Raw, uncompressed)")
    daily_storage_gb = gb_per_day
    total_retention_gb = daily_storage_gb * retention_days
    
    # Add 30% overhead for indexes/metadata
    indexed_storage_gb = total_retention_gb * 1.3
    
    if indexed_storage_gb > 1024:
        print(f"Daily Ingestion:  {daily_storage_gb:.2f} GB/day")
        print(f"Total Retention:  {indexed_storage_gb/1024:.2f} TB (incl 30% index overhead)")
    else:
        print(f"Daily Ingestion:  {daily_storage_gb:.2f} GB/day")
        print(f"Total Retention:  {indexed_storage_gb:.2f} GB (incl 30% index overhead)")

    # 3. Compute Concurrency (Little's Law: L = λW)
    print("\n⚙️  COMPUTE & CONCURRENCY (Little's Law)")
    # W must be in seconds
    processing_sec = processing_ms / 1000.0
    concurrency = tps * processing_sec
    print(f"Target TPS (λ):   {tps} req/sec")
    print(f"Latency (W):      {processing_ms} ms")
    print(f"Required Threads: {math.ceil(concurrency)} concurrent active threads (L)")
    
    # Pod sizing assumption (e.g., Spring Boot Tomcat handles ~200 active threads safely)
    pods_required = math.ceil(concurrency / 200)
    print(f"Est. Pod Count:   {max(1, pods_required)} pods (assuming 200 max active threads per pod)")

    # 4. Database IOPS
    print("\n⚡ DATABASE IOPS (Write-heavy estimation)")
    print(f"Baseline IOPS:    {tps} Write IOPS")
    print(f"Surge IOPS (3x):  {tps * 3} Write IOPS (Provision for peaks)")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Architecture NFR Physics")
    parser.add_argument("--tps", type=int, required=True, help="Target Requests Per Second")
    parser.add_argument("--payload", type=float, required=True, help="Average Payload Size in KB")
    parser.add_argument("--retention", type=int, required=True, help="Data Retention in Days")
    parser.add_argument("--latency", type=int, default=50, help="Expected Processing Latency in MS (default: 50)")
    
    args = parser.parse_args()
    calculate_nfrs(args.tps, args.payload, args.retention, args.latency)
