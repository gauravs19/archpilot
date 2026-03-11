# AI/ML Architecture Standards

> **Purpose:** Architecture standards for AI/ML systems — covering model serving,
> MLOps pipelines, data pipelines, feature stores, model monitoring, and responsible AI.
> Essential as organizations integrate AI/ML into their product architecture.

---

## How to Use This File

- **ML System Design:** Say to an LLM: *"Using these AI/ML architecture standards, design the ML infrastructure for: [your use case]"*
- **Architecture Review:** Audit ML systems against these standards for production readiness

---

## Related Standards

| Standard | Relationship |
|----------|-------------|
| [06 — Data Architecture](./06-data-architecture.md) | Data pipelines, storage for training data |
| [12 — Observability](./12-observability-standards.md) | Model monitoring and drift detection |
| [13 — DevOps & CI/CD](./13-devops-cicd.md) | MLOps pipelines extend CI/CD |
| [07 — Security Architecture](./07-security-architecture.md) | Data privacy for training data |

---

## 1. ML Architecture Patterns

### 1.1 Pattern Selection

| Pattern | When | Latency | Complexity |
|---------|------|:-------:|:----------:|
| **Batch Prediction** | Pre-compute predictions for all users/items | Minutes-hours | Low |
| **Real-Time Inference** | Predict on-demand per request | < 100ms | High |
| **Streaming Inference** | Process events as they arrive | Seconds | High |
| **Edge Inference** | Run model on device (mobile, IoT) | < 10ms | Medium |
| **Hybrid** | Batch for bulk + real-time for interactive | Mixed | High |

```
Use Case → Pattern Selection:
├── Product recommendations (homepage) → Batch (precompute)
├── Search ranking → Real-Time inference
├── Fraud detection → Streaming (event-driven)
├── Image classification (mobile) → Edge inference
└── Personalized pricing → Hybrid (batch segments + real-time adjustments)
```

### 1.2 Reference Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Data Source  │───▶│  Feature     │───▶│   Model      │
│  (Events,    │    │  Pipeline    │    │   Training   │
│  Databases)  │    │  (ETL/ELT)  │    │   Pipeline   │
└──────────────┘    └──────┬───────┘    └───────┬──────┘
                           │                     │
                    ┌──────▼───────┐    ┌───────▼──────┐
                    │   Feature    │    │   Model      │
                    │   Store     │    │   Registry   │
                    └──────┬───────┘    └───────┬──────┘
                           │                     │
                    ┌──────▼─────────────────────▼──────┐
                    │        Model Serving               │
                    │  (REST API / gRPC / Batch)         │
                    └──────────────┬─────────────────────┘
                                   │
                    ┌──────────────▼─────────────────────┐
                    │      Monitoring & Feedback          │
                    │  (Drift detection, A/B testing)     │
                    └────────────────────────────────────┘
```

---

## 2. MLOps Pipeline Standards

### 2.1 ML Lifecycle

| Stage | Activities | Artifacts |
|-------|-----------|----------|
| **Data Collection** | Source identification, ingestion, labeling | Raw datasets, data catalog |
| **Data Preparation** | Cleaning, feature engineering, splits | Training/test/validation sets |
| **Model Training** | Experiment tracking, hyperparameter tuning | Trained model, metrics |
| **Model Evaluation** | Accuracy, fairness, bias testing | Evaluation report |
| **Model Packaging** | Containerize, serialize model | Docker image, model artifact |
| **Model Deployment** | Deploy to serving infrastructure | API endpoint, batch job |
| **Model Monitoring** | Drift detection, performance tracking | Dashboards, alerts |
| **Model Retraining** | Triggered by drift or schedule | Updated model |

### 2.2 MLOps Maturity Levels

| Level | Description | Characteristics |
|:-----:|-----------|----------------|
| **0** | Manual | Jupyter notebooks, manual deployment, no versioning |
| **1** | ML Pipeline | Automated training pipeline, manual deployment |
| **2** | CI/CD for ML | Automated training + deployment + testing |
| **3** | Full MLOps | Automated retraining on drift, A/B testing, feature store |

**Target:** Level 2 minimum for production. Level 3 for critical ML systems.

### 2.3 Pipeline Standards

| Rule | Standard |
|------|---------|
| All experiments tracked | Use MLflow, W&B, or Neptune for experiment tracking |
| Models versioned | Model registry with version history (MLflow, SageMaker) |
| Data versioned | DVC or similar for training data versioning |
| Training reproducible | Same data + same code + same config = same model |
| Evaluation automated | Automated comparison against baseline before deploy |
| Deployment automated | CI/CD deploys approved models to serving |

---

## 3. Model Serving

### 3.1 Serving Patterns

| Pattern | Technology | Latency | Throughput | Use When |
|---------|-----------|:-------:|:----------:|----------|
| **REST API** | FastAPI + ONNX/TensorFlow Serving | 10-500ms | Medium | General-purpose |
| **gRPC** | TF Serving, Triton | 1-50ms | High | Low-latency, service-to-service |
| **Batch** | Spark, SageMaker Batch Transform | Minutes | Very High | Pre-computation |
| **Streaming** | Flink + model, Kafka ML | Seconds | High | Event-driven |
| **Serverless** | Lambda + SageMaker endpoint | 100ms-5s | Medium | Sporadic traffic |
| **Edge** | TFLite, ONNX Runtime, Core ML | < 10ms | Per-device | Mobile, IoT |

### 3.2 Model Serving Rules

| Rule | Standard |
|------|---------|
| Model isolated from application | Model served as separate service, not embedded in app code |
| Canary deployment | New models rolled out to 5% traffic first |
| Fallback strategy | If model fails, use rule-based or previous model |
| A/B testing | Compare new model vs baseline on live traffic |
| Latency SLA | p99 < 200ms for real-time serving |
| Model warm-up | Pre-load model on startup, not on first request |

---

## 4. Feature Store

### 4.1 Purpose

A feature store is a centralized repository for storing, serving, and sharing ML features.

```
Raw Data ──▶ Feature Pipeline ──▶ Feature Store ──▶ Model Training
                                       │
                                       └──▶ Model Serving (low-latency)
```

### 4.2 Feature Store Selection

| Tool | Type | Best For |
|------|------|---------|
| **Feast** | Open-source | Kubernetes environments, multi-cloud |
| **AWS SageMaker Feature Store** | Managed | AWS-native ML |
| **Vertex AI Feature Store** | Managed | GCP-native ML |
| **Databricks Feature Store** | Managed | Databricks/Spark environments |
| **Custom (Redis + PostgreSQL)** | DIY | Small teams, simple features |

---

## 5. Model Monitoring

### 5.1 What to Monitor

| Monitor | What | Alert When |
|---------|------|-----------|
| **Data Drift** | Input feature distributions shift | Statistical test (KS, PSI) exceeds threshold |
| **Concept Drift** | Relationship between features and target changes | Model accuracy drops > 5% |
| **Prediction Distribution** | Model output distribution shifts | Prediction skew > 2 standard deviations |
| **Latency** | Serving latency | p99 > SLA threshold |
| **Error Rate** | Prediction failures | Error rate > 1% |
| **Feature Freshness** | How stale the input features are | Features > [threshold] old |

### 5.2 Retraining Strategy

| Trigger | When | Automation |
|---------|------|:----------:|
| **Scheduled** | Weekly, monthly | Fully automated |
| **Performance-based** | Accuracy drops below threshold | Semi-automated (alert + approval) |
| **Data-based** | Significant new data available | Fully automated |
| **Event-based** | Business change (new product category, new market) | Manual trigger |

---

## 6. Responsible AI

### 6.1 Checklist

- [ ] Training data audited for bias (demographic, geographic)
- [ ] Model evaluated for fairness across protected groups
- [ ] Model explainability implemented (SHAP, LIME)
- [ ] Decisions are appealable by users (human-in-the-loop fallback)
- [ ] Training data does not contain PII without consent
- [ ] Model card documented (purpose, limitations, performance by group)
- [ ] Regulatory requirements met (GDPR Article 22 for automated decisions)

### 6.2 Model Card Template

```markdown
# Model Card: [Model Name]

## Overview
- **Purpose:** [What the model does]
- **Owner:** [Team]
- **Version:** [1.0]
- **Last Trained:** [Date]

## Training Data
- **Source:** [Dataset description]
- **Size:** [Number of samples]
- **Time Range:** [Date range]
- **Known Limitations:** [Biases, gaps]

## Performance
| Metric | Overall | Group A | Group B |
|--------|:-------:|:-------:|:-------:|
| Accuracy | 92% | 91% | 93% |
| Precision | 88% | 86% | 90% |
| Recall | 90% | 89% | 91% |

## Limitations
- [Known edge cases]
- [Not suitable for...]
- [Requires human review when...]
```

---

## 7. AI/ML Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Model in a notebook** | Not reproducible, not deployable | MLOps pipeline, containerized serving |
| **Training-serving skew** | Features computed differently in training vs serving | Feature store, shared feature logic |
| **No model monitoring** | Model degrades silently for months | Drift detection, accuracy monitoring |
| **Overfitting to offline metrics** | Model performs great in lab, fails in production | A/B testing, online evaluation |
| **Ignoring explainability** | "Black box" model makes questionable decisions | SHAP/LIME, model cards, human review |
| **One model for everything** | Single model serving different use cases | Domain-specific models |

---

*Archpilot — Enterprise Architecture Standards Library*
*Created by Gaurav Sharma*
