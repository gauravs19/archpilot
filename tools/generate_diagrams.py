import os

archetypes = {
    "04-api-gateway-pattern.md": """# API Gateway Pattern Archetype
```mermaid
graph TD
    Client["Client (Web/Mobile)"] -->|"HTTPS"| APIGW["API Gateway<br/>(Auth, Rate Limit, Routing)"]
    APIGW -->|"Route: /users"| UserSVC["User Service"]
    APIGW -->|"Route: /orders"| OrderSVC["Order Service"]
    APIGW -->|"Route: /catalog"| CatalogSVC["Catalog Service"]
```""",
    "05-event-sourcing-cqrs.md": """# Event Sourcing & CQRS Archetype
```mermaid
graph TD
    Client["Client"] -->|"POST (Command)"| CommandAPI["Command Service (Write)"]
    CommandAPI -->|"Append Event"| EventStore["Event Store<br/>(Kafka/EventStoreDB)"]
    EventStore -->|"Publish Event"| Projector["Read Model Projector"]
    Projector -->|"Update View"| ReadDB["Read Database<br/>(ElasticSearch/Redis)"]
    Client -->|"GET (Query)"| QueryAPI["Query Service (Read)"]
    QueryAPI -->|"Fetch View"| ReadDB
```""",
    "06-strangler-fig-pattern.md": """# Strangler Fig Pattern Archetype
```mermaid
graph TD
    Client["Client"] --> Router["Reverse Proxy / Router"]
    Router -->|"/v1/legacy"| Monolith["Legacy Monolith"]
    Router -->|"/v2/new-feature"| NewService["Modern Microservice"]
    NewService -->|"Anti-Corruption Layer"| MonolithDB[(Legacy DB)]
```""",
    "07-micro-frontend-pattern.md": """# Micro-Frontend Pattern Archetype
```mermaid
graph TD
    AppShell["App Shell (Host)"]
    subgraph Browser
        AppShell -->|"Loads"| MFE_Header["Header MFE<br/>(React)"]
        AppShell -->|"Loads"| MFE_Cart["Cart MFE<br/>(Vue)"]
        AppShell -->|"Loads"| MFE_Catalog["Catalog MFE<br/>(React)"]
    end
```""",
    "08-outbox-pattern.md": """# Transactional Outbox Pattern Archetype
```mermaid
graph TD
    Service["Business Service"] -->|"1. Local Tx"| DB[(Primary DB)]
    subgraph DB Transaction
        DB_State["Business Data Table"]
        DB_Outbox["Outbox Table"]
    end
    DB --> DB_State
    DB --> DB_Outbox
    Relay["Message Relay (Debezium/Poller)"] -->|"2. Read Outbox"| DB_Outbox
    Relay -->|"3. Publish"| Broker["Message Broker (Kafka)"]
```""",
    "09-circuit-breaker-pattern.md": """# Circuit Breaker Pattern Archetype
```mermaid
stateDiagram-v2
    [*] --> CLOSED : Normal Operation
    CLOSED --> OPEN : Failure Threshold Exceeded
    OPEN --> HALF_OPEN : Timeout Expired
    HALF_OPEN --> CLOSED : Success Threshold Met
    HALF_OPEN --> OPEN : Request Failed
```""",
    "10-service-mesh-sidecar.md": """# Service Mesh (Sidecar) Archetype
```mermaid
graph TD
    subgraph Pod A
        SvcA["Service A"] <--> ProxyA["Envoy Proxy (Sidecar)"]
    end
    subgraph Pod B
        SvcB["Service B"] <--> ProxyB["Envoy Proxy (Sidecar)"]
    end
    ProxyA <-->|"mTLS Traffic"| ProxyB
    ControlPlane["Mesh Control Plane<br/>(Istio)"] -.->|"Config/Certs"| ProxyA
    ControlPlane -.->|"Config/Certs"| ProxyB
```""",
    "11-oauth2-oidc-flow.md": """# OAuth2 / OIDC Auth Flow Archetype
```mermaid
sequenceDiagram
    participant User
    participant App as SPA / Client
    participant IDP as Identity Provider (Auth0/Okta)
    participant API as Resource Server
    
    User->>App: Click Login
    App->>IDP: Redirect to IDP (Authorize)
    IDP->>User: Prompt Credentials
    User->>IDP: Submit Credentials
    IDP->>App: Redirect with Auth Code
    App->>IDP: Exchange Code for Tokens
    IDP-->>App: Access Token + ID Token
    App->>API: API Request + Bearer Token
    API->>API: Validate Token Signature
    API-->>App: Protected Resource Data
```""",
    "12-bulkhead-pattern.md": """# Bulkhead Pattern Archetype
```mermaid
graph TD
    APIGW["API Gateway"]
    subgraph Service
        PoolA["Thread Pool A<br/>(High Priority)"]
        PoolB["Thread Pool B<br/>(Low Priority)"]
    end
    APIGW -->|"Critical Traffic"| PoolA
    APIGW -->|"Background Tasks"| PoolB
    PoolA --> DB[(Database)]
    PoolB --> DB
```""",
    "13-fan-out-fan-in.md": """# Fan-out / Fan-in Pattern Archetype
```mermaid
graph TD
    Trigger["Trigger Event"] --> FanOut["Fan-Out Router (Pub/Sub)"]
    FanOut --> Worker1["Worker A (Task Part 1)"]
    FanOut --> Worker2["Worker B (Task Part 2)"]
    FanOut --> Worker3["Worker C (Task Part 3)"]
    Worker1 --> FanIn["Fan-In Aggregator"]
    Worker2 --> FanIn
    Worker3 --> FanIn
    FanIn --> Result["Final Consolidated Result"]
```""",
    "14-change-data-capture-cdc.md": """# Change Data Capture (CDC) Archetype
```mermaid
graph TD
    App["Application"] -->|"Writes"| SourceDB[(Primary DB<br/>PostgreSQL)]
    SourceDB -.->|"WAL (Write-Ahead Log)"| Debezium["CDC Connector<br/>(Debezium)"]
    Debezium -->|"Streams changes"| Kafka["Kafka Topic"]
    Kafka -->|"Consumes"| Sink1["Data Warehouse (Snowflake)"]
    Kafka -->|"Consumes"| Sink2["Search Index (ElasticSearch)"]
```""",
    "15-two-phase-commit-2pc.md": """# Two-Phase Commit (2PC) Archetype
```mermaid
sequenceDiagram
    participant Coordinator
    participant NodeA as DB Node A
    participant NodeB as DB Node B
    
    Note over Coordinator: Phase 1: Prepare
    Coordinator->>NodeA: Prepare to Commit?
    Coordinator->>NodeB: Prepare to Commit?
    NodeA-->>Coordinator: Yes (Ready)
    NodeB-->>Coordinator: Yes (Ready)
    
    Note over Coordinator: Phase 2: Commit
    Coordinator->>NodeA: Commit
    Coordinator->>NodeB: Commit
    NodeA-->>Coordinator: Acknowledged
    NodeB-->>Coordinator: Acknowledged
```""",
    "16-backends-for-frontends-bff.md": """# Backends for Frontends (BFF) Archetype
```mermaid
graph TD
    MobileUI["Mobile App"] --> MobileBFF["Mobile BFF"]
    WebUI["Web SPA"] --> WebBFF["Web BFF"]
    
    MobileBFF --> SvcA["Core Service A"]
    MobileBFF --> SvcB["Core Service B"]
    
    WebBFF --> SvcA
    WebBFF --> SvcB
    WebBFF --> SvcC["Core Service C"]
```""",
    "17-serverless-lambda-arch.md": """# Serverless Architecture Archetype
```mermaid
graph TD
    Client["Client"] --> APIGW["AWS API Gateway"]
    APIGW --> Lambda1["AWS Lambda (Auth)"]
    APIGW --> Lambda2["AWS Lambda (Process)"]
    Lambda2 --> Dynamo[(DynamoDB)]
    Dynamo -.->|"DynamoDB Streams"| Lambda3["AWS Lambda (Async Worker)"]
    Lambda3 --> SNS["SNS Topic"]
```""",
    "18-data-lake-medallion.md": """# Medallion Data Lake Archetype
```mermaid
graph TD
    Raw["Raw Data Sources"] --> Bronze[(Bronze Zone<br/>Raw/Ingested)]
    Bronze -->|"Cleanse & Filter"| Silver[(Silver Zone<br/>Validated/Conformed)]
    Silver -->|"Aggregate & Join"| Gold[(Gold Zone<br/>Business/Analytics)]
    Gold --> BI["BI Dashboards (Tableau/PowerBI)"]
    Gold --> ML["Machine Learning Models"]
```""",
    "19-cell-based-architecture.md": """# Cell-Based Architecture Archetype
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
```""",
    "20-blue-green-deployment.md": """# Blue/Green Deployment Archetype
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
```""",
    "21-cache-aside-pattern.md": """# Cache-Aside Pattern Archetype
```mermaid
sequenceDiagram
    participant App as Application
    participant Cache as Redis Cache
    participant DB as Database
    
    App->>Cache: 1. Get Data(Key)
    alt Cache Hit
        Cache-->>App: Return Data
    else Cache Miss
        Cache-->>App: Null
        App->>DB: 2. Query Data(Key)
        DB-->>App: Return Data
        App->>Cache: 3. Set Data(Key) + TTL
    end
```""",
    "22-retry-exponential-backoff.md": """# Retry with Exponential Backoff Archetype
```mermaid
sequenceDiagram
    participant Client
    participant Service
    
    Client->>Service: Request 1 (T=0s)
    Service-->>Client: 503 Unavailable
    Note over Client: Wait 1s
    
    Client->>Service: Request 2 (T=1s)
    Service-->>Client: 503 Unavailable
    Note over Client: Wait 2s
    
    Client->>Service: Request 3 (T=3s)
    Service-->>Client: 503 Unavailable
    Note over Client: Wait 4s
    
    Client->>Service: Request 4 (T=7s)
    Service-->>Client: 200 OK
```"""
}

def main():
    target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diagrams")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    for filename, content in archetypes.items():
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
