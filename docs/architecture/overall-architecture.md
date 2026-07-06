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
    └── Ready for Workloads
```

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
| GitOps | Planned |
| ML Platform | Planned |
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