
---

## Infrastructure as Code

### Decision

Terraform

### Reason

Infrastructure should be reproducible, version-controlled, modular, and reusable across environments.

---

## Terraform State

### Decision

Google Cloud Storage Remote Backend

### Reason

Provides centralized state management, versioning, collaboration, and disaster recovery.

---

## Container Registry

### Decision

Google Artifact Registry

### Reason

Provides secure, regional container image storage with native integration to GKE.

---

## Kubernetes Deployment Strategy

### Decision

Separate GKE Cluster and Managed Node Pools

### Reason

Allows independent lifecycle management, autoscaling, and production-grade infrastructure management.

---

## Cost Optimization

### Decision

Use Spot VMs for Development

### Reason

Reduce cloud costs while keeping production configuration unchanged.

---

## Security

### Decision

Least Privilege IAM

### Reason

Grant only the permissions required by workloads instead of broad administrative access.