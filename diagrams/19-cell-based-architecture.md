# Cell-Based Architecture Archetype
```mermaid
graph TD
    Router["Global Router / API Gateway"]
    
    subgraph Cell 1 [Cell 1 (Europe)]
        Svc1["App Services"] --> DB1[(Cell DB)]
    end
    
    subgraph Cell 2 [Cell 2 (US East)]
        Svc2["App Services"] --> DB2[(Cell DB)]
    end
    
    subgraph Cell N [Cell N (APAC)]
        SvcN["App Services"] --> DBN[(Cell DB)]
    end
    
    Router -->|"Partition Key = EU"| Cell 1
    Router -->|"Partition Key = US"| Cell 2
    Router -->|"Partition Key = AP"| Cell N
```