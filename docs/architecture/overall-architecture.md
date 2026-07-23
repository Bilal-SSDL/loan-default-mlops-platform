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
are working against this MLflow deployment. The next workload is the FastAPI
inference service (Milestone 16).

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
| Model Serving (FastAPI) | ⏳ In Progress |
| KServe | Planned |
| Kubeflow | Planned |
| Monitoring | Planned |

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