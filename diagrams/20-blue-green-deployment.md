# Blue/Green Deployment Archetype
```mermaid
graph TD
    Router["Load Balancer / Ingress"]
    
    subgraph Blue [Blue Env (Current Prod)]
        V1["App v1.0"] --> DB[(Shared DB)]
    end
    
    subgraph Green [Green Env (New Release)]
        V2["App v1.1"] --> DB
    end
    
    Router -->|"100% Traffic"| Blue
    Router -.->|"0% Traffic (Testing)"| Green
```