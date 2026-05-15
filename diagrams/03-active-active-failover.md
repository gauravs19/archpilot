# Active-Active Global Failover Archetype

Use this archetype for HLDs focused on global scale, High Availability (HA), and Disaster Recovery (DR).

```mermaid
graph TD
    classDef global fill:#1E293B,stroke:#0F172A,color:#fff
    classDef region fill:#F8FAFC,stroke:#CBD5E1,color:#000
    classDef component fill:#1E3A8A,stroke:#0F172A,color:#fff,rx:5
    classDef db fill:#B45309,stroke:#78350F,color:#fff,rx:5

    GlobalDNS["Global DNS / Global Accelerator<br/>(Route 53)"]:::global

    subgraph RegionA [US-East (Active)]
        direction TB
        ALB_A["Application Load Balancer"]:::component
        App_A["EKS Cluster (App Tier)"]:::component
        DB_A["Primary DB<br/>(Aurora / Spanner)"]:::db
        
        ALB_A --> App_A
        App_A --> DB_A
    end

    subgraph RegionB [EU-West (Active)]
        direction TB
        ALB_B["Application Load Balancer"]:::component
        App_B["EKS Cluster (App Tier)"]:::component
        DB_B["Primary DB<br/>(Aurora / Spanner)"]:::db
        
        ALB_B --> App_B
        App_B --> DB_B
    end

    GlobalDNS -->|"Latency-based routing"| ALB_A
    GlobalDNS -->|"Latency-based routing"| ALB_B

    %% Bi-directional cross-region replication
    DB_A <-->|"Cross-Region Active-Active Replication"| DB_B
```
