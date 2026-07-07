# Milestone 07 - Ingress NGINX

## Objective

Deploy an NGINX Ingress Controller on the GKE cluster using Helm to provide a single entry point for external HTTP/HTTPS traffic.

This prepares the cluster for exposing future applications such as ArgoCD, MLflow, Grafana, and the FastAPI application.

---

# Why Ingress?

Applications running inside Kubernetes are only accessible within the cluster by default.

Instead of exposing every application using its own LoadBalancer Service, we deploy a single Ingress Controller.

Benefits:

- Reduces cloud cost
- Centralizes HTTP/HTTPS routing
- Supports host-based routing
- Supports path-based routing
- Enables SSL/TLS termination
- Standard production architecture

---

# Prerequisites

- GKE Cluster running
- kubectl configured
- Helm installed
- ingress-nginx namespace already created

---

# Tasks Completed

- Added the official Ingress NGINX Helm repository
- Updated Helm repositories
- Inspected the Helm chart
- Reviewed default configuration values
- Installed the Ingress NGINX Controller
- Verified Helm release
- Verified Kubernetes resources
- Verified LoadBalancer Service
- Verified IngressClass

---

# Implementation

## Step 1 - Add Helm Repository

Command:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
```

Purpose:

Registers the official Ingress NGINX repository so Helm can download the chart.

---

## Step 2 - Update Repository Metadata

Command:

```bash
helm repo update
```

Purpose:

Downloads the latest chart metadata from all configured repositories.

---

## Step 3 - Inspect the Chart

Command:

```bash
helm show chart ingress-nginx/ingress-nginx
```

Purpose:

Displays chart metadata such as:

- Chart Version
- App Version
- Description
- Maintainers

This helps understand what is going to be installed.

---

## Step 4 - Review Default Values

Command:

```bash
helm show values ingress-nginx/ingress-nginx
```

Purpose:

Displays all configurable parameters before installation.

In production, this file is commonly customized instead of accepting defaults.

---

## Step 5 - Install Ingress Controller

Command:

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx
```

Purpose:

Deploys the complete NGINX Ingress Controller into the cluster.

Helm automatically creates all required Kubernetes resources.

---

# Verification

## Verify Helm Release

Command

```bash
helm list -A
```

Purpose

Lists every Helm release currently installed in the cluster.

Expected Result

```
ingress-nginx
```

---

## Verify Pods

Command

```bash
kubectl get pods -n ingress-nginx
```

Purpose

Ensures the Ingress Controller Pods are running successfully.

Expected Result

Pods should be in the Running state.

---

## Verify Services

Command

```bash
kubectl get svc -n ingress-nginx
```

Purpose

Displays the Service created by Helm.

Expected Result

A Service of type:

```
LoadBalancer
```

Google Cloud automatically provisions an external Load Balancer.

---

## Verify All Resources

Command

```bash
kubectl get all -n ingress-nginx
```

Purpose

Displays every Kubernetes resource created by the Helm chart.

Typical resources include:

- Deployment
- ReplicaSet
- Pods
- Service
- Jobs

---

## Verify Ingress Class

Command

```bash
kubectl get ingressclass
```

Purpose

Confirms Kubernetes recognizes the installed Ingress Controller.

Expected Output

```
nginx
```

---

# Resources Created

## Deployment

Runs and manages the Ingress Controller Pods.

Ensures the desired number of replicas are always available.

---

## ReplicaSet

Maintains the required number of Pods created by the Deployment.

---

## Pods

Run the actual NGINX Ingress Controller containers.

---

## Service (LoadBalancer)

Creates a Google Cloud Load Balancer.

Provides an external IP address through which traffic enters the Kubernetes cluster.

---

## Admission Webhook

Validates Ingress resources before Kubernetes accepts them.

Helps prevent invalid configurations.

---

## IngressClass

Registers the NGINX Ingress Controller with Kubernetes.

Future Ingress resources reference this class.

---

# Architecture

```
Internet
    │
    ▼
Google Cloud Load Balancer
    │
    ▼
NGINX Ingress Controller
    │
    ├─────────────┐
    │             │
    ▼             ▼
ArgoCD        MLflow
    │             │
    ▼             ▼
Services     Services
    │             │
    ▼             ▼
Pods         Pods
```

---

# Commands Summary

| Command | Purpose |
|----------|---------|
| helm repo add | Add Helm repository |
| helm repo update | Update repository metadata |
| helm show chart | View chart information |
| helm show values | View configurable values |
| helm install | Install Helm chart |
| helm list -A | List installed Helm releases |
| kubectl get pods | Verify Pods |
| kubectl get svc | Verify Services |
| kubectl get all | View created resources |
| kubectl get ingressclass | Verify Ingress Controller |

---

# Key Takeaways

- Helm is the Kubernetes package manager.
- An Ingress Controller manages incoming HTTP/HTTPS traffic.
- NGINX Ingress is deployed using a Helm chart.
- The Helm chart creates multiple Kubernetes resources automatically.
- A Google Cloud LoadBalancer exposes the Ingress Controller to the internet.
- Future applications will be exposed through this single Ingress Controller instead of creating multiple LoadBalancers.