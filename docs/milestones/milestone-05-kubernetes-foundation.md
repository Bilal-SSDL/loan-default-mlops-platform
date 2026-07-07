# Milestone 05 - Kubernetes Platform Preparation

## Objective

Prepare a production-ready Kubernetes platform before deploying workloads.

---

## Tasks Completed

- Created GKE Cluster
- Created Managed Node Pool
- Enabled Autoscaling
- Enabled Spot Nodes
- Enabled Shielded Nodes
- Connected kubectl to the cluster

# Commands

- gcloud container clusters get-credentials mlops-gke \
    --region us-central1
- kubectl create namespace argocd
kubectl create namespace ingress-nginx
kubectl create namespace mlflow
kubectl create namespace kubeflow
kubectl create namespace kserve
kubectl create namespace monitoring
kubectl create namespace applications


---

## Outcome

A Kubernetes cluster is now available for deploying platform services such as:

- ArgoCD
- MLflow
- FastAPI
- PostgreSQL
- Monitoring Stack