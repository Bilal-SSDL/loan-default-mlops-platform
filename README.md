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
    ├──────────────► MLflow (Tracking + Model Registry)
    │
    ├──────────────► FastAPI Inference Service
    │
    ├──────────────► KServe (RawDeployment)
    │
    └──────────────► Kubeflow Pipelines
```

---

# How the Platform Works (Concepts)

## Where things are stored

The word "artifact" means two unrelated things in this project. Keep them separate:

| What is stored | Where | Notes |
|----------------|-------|-------|
| Run metadata — params, metrics, tags, run history | **PostgreSQL** | MLflow *backend store* |
| Model files + plots (ROC, confusion matrix, etc.) | **GCS bucket** | MLflow *artifact store*, written by the tracking server (proxied) |
| Container images — `mlflow`, `loan-api`, `loan-trainer` | **GCP Artifact Registry** | Docker images only — **not** ML models |

> The trained model lives in **GCS**, not Artifact Registry. Artifact Registry only
> holds container images. MLflow "artifacts" (GCS) and a container image "registry"
> (Artifact Registry) are different things that happen to share the word.

## Two automation loops

The platform automates two separate lifecycles. Conflating them is the most common
point of confusion:

- **Model lifecycle — Kubeflow Pipelines.** Automates *retraining*: `preprocess ->
  train -> log to MLflow -> register -> promote champion`, on demand or on a
  schedule. Output: a new model version with the `champion` alias.
- **Software lifecycle — GitHub Actions + ArgoCD.** Automates *code -> image ->
  deployed*: on a push under `ml/` or `platform/mlflow/`, it tests, builds and pushes
  the changed image, writes the new tag into the manifests, and ArgoCD rolls it out.
  Output: new code running in the cluster.
- **The bridge — `model-refresh` CronJob.** Serving pods cache the model in memory,
  so when Kubeflow promotes a new `champion`, the CronJob restarts them to load it.

## Serving paths

Two serving paths currently run in parallel against the same `champion` model, for
learning purposes:

- **FastAPI Deployment** (Milestone 16) — a hand-written inference service.
- **KServe InferenceService** (Milestone 17) — standardized serving with autoscaling.

In a production setup you would pick one; here both exist to demonstrate the
difference.

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

### Phase 4b - KServe (RawDeployment) — Milestone 17

- Install cert-manager + KServe (no Knative/Istio)
- `InferenceService` in RawDeployment mode
- Custom container (reuses the `loan-api` image; proxied registry loading)
- HPA autoscaling
- KServe V1 inference protocol

> RawDeployment keeps Iteration 1 lightweight (no scale-to-zero, limited canary).
> Upgrading KServe to **Serverless (Knative)** for scale-to-zero and clean canary
> traffic splitting is deferred to **Iteration 2** (see below).

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
| Model Serving (FastAPI) | ✅ Completed |
| KServe Serving | ✅ Completed |
| Kubeflow Orchestration | ✅ Completed |
| CI/CD | ✅ Completed |
| Monitoring | ✅ Completed |
| Logging | ⏳ In Progress (Milestone 21) |
| Security Improvements | ⏳ Planned (Iteration 2) |

**Overall Progress:** **~93% Complete**

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

**Model Serving:** ✅ FastAPI inference service (Milestone 16) and KServe `InferenceService` in RawDeployment mode (Milestone 17) deployed on GKE, serving `LoanDefaultModel@champion` via ArgoCD

**Workflow Orchestration:** ✅ Kubeflow Pipelines (standalone) running the single-step training pipeline that retrains, registers, and promotes `champion` (Milestone 18)

**CI/CD:** ✅ GitHub Actions builds/pushes changed images and writes tags back to the manifests for ArgoCD to deploy; a CronJob refreshes serving pods on new `champion` (Milestone 19)

**Monitoring:** ✅ kube-prometheus-stack (Prometheus + Grafana + Alertmanager) deployed; FastAPI instrumented with `/metrics`, scraped via ServiceMonitor, with a GitOps-provisioned inference dashboard (Milestone 20)

**Current Phase:** Phase 8 — Logging with Loki + Fluent Bit (Milestone 21)

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

✅ Model Serving (FastAPI)

✅ KServe

✅ Kubeflow orchestration

✅ End-to-end prediction flow

✅ CI/CD

✅ Monitoring

⏳ Logging

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
- **KServe: upgrade RawDeployment → Serverless (Knative)** for scale-to-zero and canary traffic splitting (requires a node-pool capacity bump)
- **Kubeflow: upgrade KFP standalone → full Kubeflow platform** (dashboard, Istio, Katib, Notebooks, Profiles)
- **Training pipeline: split single-step → multi-step** KFP pipeline with artifact passing between `preprocess` and `train` components
- **Monitoring: add alerting** — PrometheusRule alert rules + Alertmanager receiver routing (Slack/email); dashboards for MLflow/Kubeflow; a ServiceMonitor for the KServe predictor

At that point, the project becomes much closer to a production-grade reference architecture.
