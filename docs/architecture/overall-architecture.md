# Overall Architecture

## Objective

Build an enterprise-grade MLOps platform for Loan Default Prediction on Google Cloud Platform.

The project focuses on MLOps engineering rather than model development. The ML model will remain intentionally simple, while the platform will demonstrate production-ready infrastructure, deployment, monitoring, and automation.

---

## Current Architecture

Developer
│
├── GitHub Repository
│
├── Google Cloud Platform
│   ├── Custom VPC
│   ├── Public Subnet
│   ├── Private Subnet
│   ├── Cloud NAT
│   ├── Artifact Registry
│   ├── Cloud Storage
│   └── GKE Cluster
│
└── Kubernetes
    └── Namespaces

---

## Current Components

| Component | Status |
|-----------|--------|
| GCP Project | ✅ |
| Networking | ✅ |
| Artifact Registry | ✅ |
| Cloud Storage | ✅ |
| Service Account | ✅ |
| GKE Cluster | ✅ |
| GitOps | Planned |
| ML Platform | Planned |
| Monitoring | Planned |

---

## Future Architecture

Terraform
        │
        ▼
Google Cloud Infrastructure
        │
        ▼
GKE Cluster
        │
        ▼
ArgoCD
        │
        ▼
MLflow
Kubeflow
KServe
Prometheus
Grafana
