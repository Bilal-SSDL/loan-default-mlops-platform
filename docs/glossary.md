# Glossary

This glossary contains important terms used throughout the project. Each definition is intentionally brief and focuses on how the term is used in this MLOps platform.

---

## Artifact Registry

A Google Cloud service for storing and managing container images and other software artifacts.

**Used in this project:** Stores Docker images for training, inference, and platform services.

---

## ArgoCD

A GitOps tool that continuously synchronizes Kubernetes resources with a Git repository.

**Used in this project:** Automatically deploys and updates Kubernetes applications from Git.

---

## Cloud NAT

A Google Cloud networking service that allows private resources to access the internet without requiring public IP addresses.

**Used in this project:** Allows private GKE nodes to pull container images and download software packages.

---

## Cloud Storage

Google Cloud's object storage service.

**Used in this project:** Stores datasets, model artifacts, pipeline outputs, and Terraform state.

---

## Container Image

A packaged application containing the application code, runtime, libraries, and dependencies.

**Used in this project:** Every application deployed to Kubernetes will run as a container image.

---

## CSI (Container Storage Interface)

A standard interface that allows Kubernetes to communicate with different storage providers.

**Used in this project:** GKE uses the CSI driver to dynamically provision Google Persistent Disks.

---

## Docker

A platform for building, packaging, and running applications inside containers.

**Used in this project:** Packages the training application, inference service, and supporting components.

---

## GKE (Google Kubernetes Engine)

Google Cloud's managed Kubernetes service.

**Used in this project:** Hosts all MLOps platform components.

---

## GitOps

An operational model where Git is the single source of truth for infrastructure and application deployments.

**Used in this project:** Kubernetes deployments will be managed through ArgoCD.

---

## Helm

A package manager for Kubernetes.

**Used in this project:** Installs and manages applications such as ArgoCD, MLflow, and Prometheus.

---

## Ingress

A Kubernetes resource that exposes HTTP and HTTPS applications to external users.

**Used in this project:** Provides external access to platform services.

---

## Kubernetes

An open-source container orchestration platform.

**Used in this project:** Runs, scales, and manages all platform applications.

---

## Model Registry

A centralized repository that stores versioned machine learning models and their metadata.

**Used in this project:** MLflow will be used as the model registry.

---

## Namespace

A logical partition within a Kubernetes cluster used to isolate resources.

**Used in this project:** Separates platform components such as ArgoCD, MLflow, monitoring, and applications.

---

## Node

A virtual machine that runs Kubernetes workloads.

**Used in this project:** GKE worker nodes execute Pods.

---

## Persistent Disk

A durable block storage service provided by Google Cloud.

**Used in this project:** Stores data for stateful applications such as MLflow and PostgreSQL.

---

## Persistent Volume (PV)

A Kubernetes resource representing storage available to the cluster.

**Used in this project:** Provides persistent storage for stateful workloads.

---

## Persistent Volume Claim (PVC)

A request for persistent storage made by an application.

**Used in this project:** Applications request storage through PVCs instead of managing disks directly.

---

## Pod

The smallest deployable unit in Kubernetes. A Pod contains one or more containers.

**Used in this project:** Every application runs inside Pods.

---

## Service

A Kubernetes resource that provides a stable network endpoint for Pods.

**Used in this project:** Enables communication between platform components.

---

## Service Account

An identity used by applications to securely access cloud resources.

**Used in this project:** Grants platform components only the permissions they require.

---

## Storage Class

A Kubernetes resource that defines how persistent storage should be dynamically provisioned.

**Used in this project:** Automatically creates Google Persistent Disks when applications request storage.

---

## Terraform

An Infrastructure as Code (IaC) tool used to provision and manage cloud resources.

**Used in this project:** Recreates the entire cloud infrastructure from code.

---

## VPC (Virtual Private Cloud)

A logically isolated virtual network within Google Cloud.

**Used in this project:** Hosts the GKE cluster and all networking resources.

---

## Workload Identity

A GKE feature that allows Kubernetes workloads to securely authenticate to Google Cloud services without using service account keys.

**Used in this project:** Will be configured later for secure access to GCP resources.

## Artifact Registry

Managed service for storing Docker images and other software artifacts.

---

## Terraform Remote State

Terraform state stored remotely in Google Cloud Storage.

---

## Managed Node Pool

A collection of worker nodes managed independently from the Kubernetes control plane.

---

## Spot VM

Low-cost virtual machines that may be reclaimed by Google Cloud when capacity is required.

---

## Shielded Nodes

GKE nodes with Secure Boot and integrity monitoring enabled.

---

## Autoscaling

Automatically adjusts the number of worker nodes based on cluster demand.

---

## OAuth Scopes

Defines which Google Cloud APIs a VM instance can access.

---

## Least Privilege

Security principle of granting only the minimum permissions required.
