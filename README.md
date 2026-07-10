# Enterprise MLOps Platform - Loan Default Prediction

An end-to-end, production-style MLOps platform built on **Google Cloud Platform (GCP)** using modern DevOps and MLOps practices.

The primary focus of this project is **MLOps engineering**, infrastructure automation, GitOps, CI/CD, model lifecycle management, deployment, monitoring, and production best practices.

---

# Project Goal

Build a production-ready MLOps platform for a **Loan Default Prediction** model.

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

# Current Progress

## Infrastructure

- ✅ GCP Project
- ✅ Custom VPC
- ✅ Public & Private Subnets
- ✅ Cloud Router
- ✅ Cloud NAT
- ✅ Artifact Registry
- ✅ GCS Remote Terraform State
- ✅ Service Account
- ✅ GKE Cluster
- ✅ Custom Node Pool

---

## Terraform

- ✅ Modular Structure
- ✅ Remote State
- ✅ Environment-based Structure
- ✅ Reusable Modules

---

## Kubernetes

- ✅ Cluster Access
- ✅ Namespaces
- ✅ Helm
- ✅ Ingress NGINX

---

## GitOps

- ✅ ArgoCD Installation
- ✅ ArgoCD UI
- ✅ First GitOps Application
- ✅ GitOps Repository Structure
- ✅ App of Apps Pattern

---

# Remaining Roadmap

## Phase 1 - Platform Services

- ✅ PostgreSQL
- ✅ MinIO # we will use GCS bucket instead as MinIO need S3 and we are on GCP
- MLflow

---

## Phase 2 - MLOps Components

- Model Training Pipeline
- Experiment Tracking
- Model Registry
- Model Versioning

---

## Phase 3 - Model Serving

- FastAPI Inference API
- KServe
- Canary Deployments

---

## Phase 4 - Workflow Orchestration

- Kubeflow Pipelines
- Automated Training Pipeline

---

## Phase 5 - CI/CD

- GitHub Actions
- Docker Image Build
- Push Images to Artifact Registry
- GitOps-based Deployment

---

## Phase 6 - Monitoring

- Prometheus
- Grafana
- Application Metrics
- Kubernetes Metrics
- Alerts

---

## Phase 7 - Logging

- Loki
- Fluent Bit
- Log Aggregation

---

## Phase 8 - Security

- RBAC
- Secrets Management
- Workload Identity
- Network Policies

---

## Phase 9 - Production Improvements

- Horizontal Pod Autoscaler (HPA)
- Resource Requests & Limits
- Pod Disruption Budgets
- Multi-Environment Deployment (Dev/Prod)
- Backup & Restore
- Disaster Recovery

---

# Final Architecture

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

**Current Phase:** Platform Services Deployment (PostgreSQL → MinIO → MLflow)