# Enterprise MLOps Platform on Google Cloud Platform (GCP) — Loan Default Prediction

An end-to-end, production-style MLOps platform built on **Google Cloud Platform (GCP)** using modern cloud-native, DevOps, and MLOps practices with GitOps workflows.

The primary focus of this project is **MLOps engineering**: infrastructure automation, GitOps, CI/CD, model lifecycle management, deployment, monitoring, and production best practices.

---

## Project Goal

Build an end-to-end, production-ready MLOps platform for a **Loan Default Prediction** model on Google Cloud Platform using modern cloud-native technologies and GitOps practices.

The ML model itself will remain intentionally simple while the platform demonstrates a complete production workflow.

By the end of this project, the platform will include:

- Terraform
- Google Cloud Platform
- Kubernetes (GKE)
- GitOps (ArgoCD)
- Docker
- GitHub Actions
- MLflow
- Kubeflow
- KServe
- Monitoring & Logging
- Production deployment practices

---

# Completed

## Infrastructure

- GCP Project
- Terraform (modular structure, reusable modules, environment-based layout)
- Remote State Backend (GCS)
- Custom VPC
- Public & Private Subnets
- Cloud Router
- Cloud NAT
- Artifact Registry
- GCS Bucket
- Service Account
- GKE Cluster
- Managed / Custom Node Pool
- Shielded Nodes

---

## Kubernetes Platform

- Cluster Access
- kubectl
- Helm
- Namespaces
- Ingress NGINX

---

## GitOps

- ArgoCD Installation
- ArgoCD UI
- First GitOps Application
- GitOps Repository Structure
- App of Apps Pattern
- GitOps Workflow

---

## Platform Services

- PostgreSQL
- MLflow
- GCS Artifact Store
- Custom MLflow Docker Image

> Note: MinIO was evaluated but we use a GCS bucket instead, since MinIO targets the S3 API and we are on GCP.

---

## CI/CD

- GitHub Repository
- ArgoCD Auto Sync

---

# Current Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
ArgoCD
    │
    ▼
Google Kubernetes Engine
    │
    ├──────────────► PostgreSQL
    │
    ├──────────────► GCS Bucket
    │
    └──────────────► MLflow
```

---

# Remaining Roadmap

> **Delivery plan (finalized).** Training runs against the in-cluster MLflow service
> and is orchestrated as a **Kubeflow pipeline in Phase 5** — there is **no standalone
> Kubernetes `Job`** for training (it would only duplicate what Kubeflow owns).
> Model serving is delivered **FastAPI first (Phase 4a), then KServe (Phase 4b)**.
> Phases 1–3 are complete; the current focus is Phase 4a (Milestone 16).

## Phase 1 - MLflow Verification

- Create experiments
- Log parameters
- Log metrics
- Log artifacts
- Verify artifacts in GCS

---

## Phase 2 - Training Pipeline & Experiment Tracking

- Build sample ML training pipeline
- Track experiments with MLflow
- Store artifacts in GCS
- Register trained models
- Model versioning

---

## Phase 3 - MLflow Model Registry

- Register models
- Manage model versions
- Transition model stages
- Load models from registry

---

## Phase 4 - Model Serving

### Phase 4a - FastAPI Inference API (Milestone 16)

- FastAPI Inference API
- Deploy inference service on GKE (GitOps)
- Serve models from MLflow Registry (`LoanDefaultModel@champion`)
- Perform online inference

### Phase 4b - KServe

- KServe
- Serverless model serving
- Canary Deployments

---

## Phase 5 - Workflow Orchestration (Kubeflow)

- Install Kubeflow Pipelines
- Deploy Kubeflow on GKE
- Build reusable ML pipelines
- Integrate Kubeflow with MLflow
- Automate training workflow

---

## Phase 6 - CI/CD

- GitHub Actions
- Build Docker Images
- Push Images to Artifact Registry
- GitOps Deployment with ArgoCD
- Automated Pipeline Deployment

---

## Phase 7 - Monitoring

- Prometheus
- Grafana
- Kubernetes Monitoring / Metrics
- Application Metrics
- MLflow Metrics
- KServe Metrics
- Alerts

---

## Phase 8 - Logging

- Loki
- Fluent Bit
- Log Aggregation

---

## Phase 9 - Security

- Workload Identity
- Remove Service Account Keys
- Secret Manager
- External Secrets
- Secrets Management
- TLS & HTTPS
- Network Policies
- RBAC Hardening

---

## Phase 10 - Production Improvements

- Horizontal Pod Autoscaler (HPA)
- Resource Requests & Limits
- Pod Disruption Budgets
- Multi-Environment Deployment (Dev/Prod)
- High Availability
- Backup & Restore
- Disaster Recovery
- Production Optimizations

---

# Target Architecture

```text
                     GitHub
                        │
                        ▼
                  GitHub Actions
                        │
                        ▼
                Artifact Registry
                        │
                        ▼
                     ArgoCD
                        │
                        ▼
               Google Kubernetes Engine
                        │
      ┌─────────────────┼─────────────────┐
      │                 │                 │
      ▼                 ▼                 ▼
 PostgreSQL          MLflow          Kubeflow
      │                 │                 │
      │                 │                 ▼
      │                 │        Training Pipelines
      │                 │
      ▼                 ▼
Model Metadata      GCS Bucket
      │
      ▼
MLflow Model Registry
      │
      ▼
    KServe
      │
      ▼
Inference API
```

---

# Final Architecture (Component View)

```text
GitHub
    │
    ▼
GitHub Actions
    │
    ▼
Artifact Registry
    │
    ▼
ArgoCD (GitOps)
    │
    ▼
GKE Cluster
    ├── PostgreSQL
    ├── GCS
    ├── MLflow
    ├── Kubeflow
    ├── KServe
    ├── FastAPI
    ├── Prometheus
    ├── Grafana
    └── Loki
```

---

# End-to-End Workflow

```text
Code
  │
  ▼
GitHub
  │
  ▼
GitHub Actions
  │
  ▼
Docker Image
  │
  ▼
Artifact Registry
  │
  ▼
ArgoCD
  │
  ▼
Kubernetes (GKE)
  │
  ▼
MLflow + Kubeflow
  │
  ▼
Model Registry
  │
  ▼
KServe
  │
  ▼
Inference API
  │
  ▼
Monitoring & Logging
```

---

# Project Progress

| Component | Status |
|-----------|--------|
| Infrastructure | ✅ Completed |
| Kubernetes Platform | ✅ Completed |
| GitOps | ✅ Completed |
| MLflow Deployment | ✅ Completed |
| MLflow Verification | ✅ Completed |
| Training Pipeline & Experiment Tracking | ✅ Completed |
| Model Registry (`@champion` alias) | ✅ Completed |
| Model Serving (FastAPI) | ⏳ In Progress (Milestone 16) |
| KServe Serving | ⏳ Pending |
| Kubeflow Orchestration | ⏳ Pending |
| Monitoring | ⏳ Pending |
| CI/CD | ⏳ Pending |
| Security Improvements | ⏳ Planned (Iteration 2) |

**Overall Progress:** **~75% Complete**

---

# Repository Structure

```text
loan-default-mlops-platform/
│
├── .github/
├── datasets/
├── docs/
├── kubernetes/
│   ├── applications/
│   ├── bootstrap/
│   ├── infrastructure/
│   ├── platform/
│   └── workloads/
├── scripts/
├── src/
└── terraform/
    ├── environments/
    └── modules/
```

---

# Documentation

Project documentation is available under the `docs/` directory and includes:

- Architecture
- Project Decisions (ADRs)
- Milestones
- Implementation Guides
- Commands Executed
- Infrastructure Documentation

---

# Current Status

**Infrastructure Foundation:** ✅ Complete

**GitOps Foundation:** ✅ Complete

**ML Platform:** ✅ MLflow, PostgreSQL, GCS artifact store deployed and verified

**Model Lifecycle:** ✅ Training pipeline + experiment tracking + Model Registry (`LoanDefaultModel@champion`) working against the in-cluster MLflow

**Current Phase:** Model Serving — deploying the FastAPI inference service on GKE (Milestone 16)

---

# Iteration 1 (Current)

**Focus on functionality:**

✅ Terraform infrastructure

✅ GKE

✅ Artifact Registry

✅ GCS

✅ ArgoCD

✅ PostgreSQL

✅ MLflow

✅ Training pipeline

✅ Model Registry

⏳ Model Serving (FastAPI) — in progress

⏳ KServe

⏳ Kubeflow orchestration

⏳ Monitoring

⏳ CI/CD

⏳ End-to-end prediction flow

For authentication, use a Google Service Account key mounted as a Kubernetes Secret.

This is acceptable for a learning project, provided we clearly document that it's temporary.

---

# Iteration 2 (Hardening)

After the platform is fully working, we'll improve it by:

- Workload Identity Federation
- Remove service account keys completely
- Secret Manager integration
- External Secrets Operator
- TLS
- Domain name
- Network Policies
- RBAC refinement
- Pod Security Standards
- Resource requests/limits tuning
- High Availability
- GitHub Actions OIDC authentication
- Production-grade monitoring and alerting

At that point, the project becomes much closer to a production-grade reference architecture.
