# C4 Context / Container Archetype

Use this archetype for High-Level Design (HLD) architecture diagrams. It uses strict color definitions to differentiate between personas, internal components, external systems, and databases.

```mermaid
graph TD
    %% Styling Definitions
    classDef persona fill:#0EA5E9,stroke:#0284C7,color:#fff,stroke-width:2px,rx:20,ry:20
    classDef component fill:#1E3A8A,stroke:#0F172A,color:#fff,stroke-width:2px,rx:5,ry:5
    classDef database fill:#B45309,stroke:#78350F,color:#fff,stroke-width:2px,rx:5,ry:5
    classDef eventbus fill:#15803D,stroke:#14532D,color:#fff,stroke-width:2px,rx:5,ry:5
    classDef external fill:#64748B,stroke:#334155,color:#fff,stroke-width:2px,rx:5,ry:5

    %% Nodes
    User["Mobile App User<br/>(Persona)"]:::persona
    Admin["Internal Admin<br/>(Persona)"]:::persona

    APIGW["API Gateway<br/>(Kong / AWS API GW)"]:::component
    ServiceA["Core Business Service<br/>(Spring Boot / Go)"]:::component
    ServiceB["Secondary Service<br/>(Node.js)"]:::component
    
    Kafka["Event Bus<br/>(Apache Kafka)"]:::eventbus
    DB1["Primary Database<br/>(PostgreSQL)"]:::database
    Cache["In-Memory Cache<br/>(Redis)"]:::database

    Stripe["Payment Gateway<br/>(External System)"]:::external

    %% Edges
    User -->|"HTTPS / REST"| APIGW
    Admin -->|"HTTPS / REST"| APIGW

    APIGW -->|"Routes requests"| ServiceA
    APIGW -->|"Routes requests"| ServiceB

    ServiceA -->|"Publishes events"| Kafka
    ServiceB -->|"Consumes events"| Kafka

    ServiceA -->|"Reads/Writes"| DB1
    ServiceA -->|"Checks session"| Cache

    ServiceB -->|"Authorizes Payment"| Stripe
```
