# MLOps Platform on Google Cloud Platform (GCP)

## Project Goal

Build an end-to-end, production-oriented MLOps platform on Google Cloud Platform using modern cloud-native technologies and GitOps practices.

---

# Completed

## Infrastructure

- Terraform
- Remote State Backend
- Custom VPC
- Private/Public Subnets
- Cloud Router
- Cloud NAT
- Artifact Registry
- GCS Bucket
- GKE Cluster
- Managed Node Pool
- Shielded Nodes

---

## Kubernetes Platform

- kubectl
- Helm
- Namespaces
- ArgoCD
- App of Apps Pattern
- GitOps Workflow

---

## Platform Services

- PostgreSQL
- MLflow
- GCS Artifact Store
- Custom MLflow Docker Image

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

## Phase 1 - MLflow Verification

- Create experiments
- Log parameters
- Log metrics
- Log artifacts
- Verify artifacts in GCS

---

## Phase 2 - Training Pipeline

- Build sample ML training pipeline
- Track experiments with MLflow
- Store artifacts in GCS
- Register trained models

---

## Phase 3 - MLflow Model Registry

- Register models
- Manage model versions
- Transition model stages
- Load models from registry

---

## Phase 4 - Kubeflow

- Install Kubeflow Pipelines
- Deploy Kubeflow on GKE
- Build reusable ML pipelines
- Integrate Kubeflow with MLflow
- Automate training workflow

---

## Phase 5 - KServe

- Install KServe
- Deploy inference service
- Serve models from MLflow Registry
- Perform online inference

---

## Phase 6 - Monitoring

- Prometheus
- Grafana
- Kubernetes Monitoring
- MLflow Metrics
- KServe Metrics

---

## Phase 7 - CI/CD

- GitHub Actions
- Build Docker Images
- Push Images to Artifact Registry
- GitOps Deployment with ArgoCD
- Automated Pipeline Deployment

---

## Phase 8 - Security & Production Improvements

- Workload Identity
- Remove Service Account Keys
- Secret Manager
- External Secrets
- TLS & HTTPS
- Network Policies
- RBAC Hardening
- High Availability
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

# Project Progress

| Component | Status |
|-----------|--------|
| Infrastructure | ✅ Completed |
| Kubernetes Platform | ✅ Completed |
| GitOps | ✅ Completed |
| MLflow Deployment | ✅ Completed |
| MLflow Verification | ⏳ Pending |
| Training Pipeline | ⏳ Pending |
| Model Registry | ⏳ Pending |
| Kubeflow | ⏳ Pending |
| KServe | ⏳ Pending |
| Monitoring | ⏳ Pending |
| CI/CD | ⏳ Pending |
| Security Improvements | ⏳ Planned (Iteration 2) |

**Overall Progress:** **~70% Complete**



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%










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
- ✅ MLflow

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

# Iteration 1 (Current)
** Focus on functionality:**

✅ Terraform infrastructure

✅ GKE

✅ Artifact Registry

✅ GCS

✅ ArgoCD

✅ PostgreSQL

✅ MLflow

✅ Training pipeline

✅ Model Registry

✅ KServe

✅ Monitoring

✅ CI/CD

✅ End-to-end prediction flow

For authentication, use a Google Service Account key mounted as a Kubernetes Secret.

This is acceptable for a learning project, provided we clearly document that it's temporary.

# Iteration 2 (Hardening)
After the platform is fully working, we'll improve it by:

Workload Identity Federation

Remove service account keys completely

Secret Manager integration

External Secrets Operator

TLS

Domain name

Network Policies

RBAC refinement

Pod Security Standards

Resource requests/limits tuning

High Availability

GitHub Actions OIDC authentication

Production-grade monitoring and alerting

At that point, the project becomes much closer to a production-grade reference architecture.

