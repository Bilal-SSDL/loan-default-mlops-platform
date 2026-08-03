# Overall Architecture

## Objective

Build an enterprise-grade MLOps platform for Loan Default Prediction on Google Cloud Platform.

The focus of this project is learning and implementing production-grade MLOps practices rather than building a sophisticated ML model.

---

## Current Architecture

```text
Developer
│
├── GitHub Repository
│
├── Terraform
│
├── Google Cloud Platform
│   ├── Custom VPC
│   │   ├── Public Subnet
│   │   ├── Private Subnet
│   │   ├── Cloud Router
│   │   └── Cloud NAT
│   │
│   ├── Cloud Storage
│   │   └── Terraform Remote State
│   │
│   ├── Artifact Registry
│   │
│   ├── Service Account
│   │
│   └── Google Kubernetes Engine
│       ├── Control Plane
│       └── Managed Node Pool
│
└── Kubernetes
    ├── Ingress NGINX
    ├── ArgoCD (App-of-Apps GitOps)
    └── ML Platform (namespace: mlflow)
        ├── PostgreSQL (MLflow backend store)
        ├── MLflow Tracking Server (+ Model Registry)
        └── GCS Artifact Store
```

Training pipeline, experiment tracking, and Model Registry (`LoanDefaultModel@champion`)
are working against this MLflow deployment. The FastAPI inference service (Milestone 16)
and a KServe `InferenceService` in RawDeployment mode (Milestone 17) both serve the
`champion` model on GKE. Training is orchestrated by Kubeflow Pipelines standalone,
which retrains, registers, and promotes `champion` (Milestone 18). CI/CD with GitHub
Actions builds and delivers images and writes tags back to the manifests for ArgoCD
(Milestone 19). Monitoring runs on the kube-prometheus-stack with an instrumented
FastAPI `/metrics` endpoint and a Grafana inference dashboard (Milestone 20).
Centralized logging uses Loki + Promtail, queryable in the same Grafana (Milestone 21).
This completes the functional platform (Iteration 1); remaining work is Iteration 2
hardening (security, HA, alerting, durable storage).

---

## Current Components

| Component | Status |
|------------|--------|
| GCP Project | ✅ |
| Custom VPC | ✅ |
| Public & Private Subnets | ✅ |
| Cloud Router | ✅ |
| Cloud NAT | ✅ |
| Remote Terraform State | ✅ |
| Artifact Registry | ✅ |
| Service Account | ✅ |
| GKE Cluster | ✅ |
| Managed Node Pool | ✅ |
| Ingress NGINX | ✅ |
| GitOps (ArgoCD) | ✅ |
| PostgreSQL | ✅ |
| MLflow (Tracking + Registry) | ✅ |
| Training Pipeline & Experiment Tracking | ✅ |
| Model Serving (FastAPI) | ✅ |
| KServe (RawDeployment) | ✅ |
| Kubeflow Pipelines | ✅ |
| CI/CD (GitHub Actions) | ✅ |
| Monitoring (Prometheus + Grafana) | ✅ |
| Logging (Loki + Promtail) | ✅ |

---

## Future Architecture

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
    ├── FastAPI
    ├── MLflow
    ├── PostgreSQL
    ├── MinIO
    ├── Prometheus
    ├── Grafana
    ├── KServe
    └── Monitoring Stack
```