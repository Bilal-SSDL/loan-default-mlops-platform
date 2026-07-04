# ADR 0001 - Project Decisions

## Status

Accepted

---

## Project

Enterprise MLOps Platform for Loan Default Prediction

---

## Cloud Provider

Google Cloud Platform (GCP)

Reason

Managed Kubernetes and strong MLOps ecosystem.

---

## Region

us-central1

Reason

Lower cost while supporting all required GCP services.

---

## Infrastructure

Manual provisioning during the learning phase.

Terraform will be introduced after validating the manually created infrastructure.

---

## Dataset

Home Credit Default Risk

Reason

Large, realistic dataset suitable for demonstrating end-to-end MLOps workflows.

---

## Kubernetes

Google Kubernetes Engine (GKE)

Reason

Managed Kubernetes reduces operational overhead while remaining production-ready.

---

## CI/CD

GitHub Actions

Reason

Widely adopted, integrates well with GitHub, and suitable for platform automation.

---

## GitOps

ArgoCD

Reason

Declarative Kubernetes deployments with Git as the single source of truth.

---

## Future Migration

After completing the open-source platform, selected services will be migrated to managed GCP offerings where appropriate.

