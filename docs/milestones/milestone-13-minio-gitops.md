# Milestone 13 - MinIO Deployment using ArgoCD

## Objective

Deploy MinIO on GKE using ArgoCD and Helm as the object storage service for MLflow artifacts.

---

## Why MinIO?

MLflow stores two different types of data.

- Metadata → PostgreSQL
- Artifacts (models, datasets, plots, checkpoints) → Object Storage

MinIO provides an S3-compatible object storage service and is widely used in Kubernetes environments.

---

## Prerequisites

- GKE Cluster
- ArgoCD
- Root Application (App of Apps)
- PostgreSQL

---

## Tasks Completed

- Added MinIO Application manifest
- Deployed Bitnami MinIO Helm Chart
- Created Persistent Volume Claim
- Created MinIO Service
- Created MinIO Deployment
- Enabled automatic synchronization using ArgoCD

---

## Implementation

Repository Structure

```text
kubernetes/
├── applications/
│   └── minio.yaml
```

ArgoCD continuously monitors the repository.

After pushing the manifest, ArgoCD automatically deployed MinIO into the `mlflow` namespace.

---

## New Code Explanation

### repoURL

Specifies the Helm repository.

```yaml
repoURL: https://charts.min.io/
```

---

### chart

Specifies which Helm chart to deploy.

```yaml
chart: minio
```

---

### targetRevision
5.4.0
Pins the chart version for reproducible deployments.

---

### auth

Creates the initial MinIO credentials.

```yaml
auth:
  rootUser: admin
  rootPassword: admin123
```

---

### defaultBuckets

Automatically creates the required bucket.

```yaml
defaultBuckets: mlflow
```

---

### persistence

Creates a Persistent Volume Claim.

```yaml
persistence:
  enabled: true
  size: 10Gi
```

This ensures uploaded artifacts survive Pod restarts.

---

### mode

```yaml
mode: standalone
```

Deploys a single MinIO instance suitable for development.

---

## Commands Executed

```bash
mkdir -p kubernetes/platform/minio

git add .

git commit -m "Add MinIO ArgoCD application"

git push origin main
```

---

## Resources Created

- ArgoCD Application
- Deployment
- Service
- PersistentVolumeClaim
- Persistent Volume
- MinIO Pod

---

## Architecture

```
GitHub
    │
    ▼
Root Application
    │
    ▼
MinIO Application
    │
    ▼
ArgoCD
    │
    ▼
Helm Chart
    │
    ▼
MinIO
```

---

## Key Takeaways

- Implemented GitOps deployment using ArgoCD.
- Deployed MinIO using Helm.
- Enabled persistent storage.
- MinIO will act as the artifact store for MLflow.

---

## Next Milestone

Deploy MLflow and connect it with:

- PostgreSQL (Backend Store)
- MinIO (Artifact Store)