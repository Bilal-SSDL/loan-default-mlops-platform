# Milestone 03 - Terraform Networking

## Objective

Codify the previously hand-provisioned network foundation as a reusable Terraform module, establishing Infrastructure as Code for the MLOps platform.

---

## Resources Created

- Custom VPC (`mlops-vpc`)
- Public subnet (`mlops-public`, 10.10.1.0/24)
- Private subnet (`mlops-private`, 10.10.2.0/24) with Private Google Access
- Secondary ranges on the private subnet for GKE pods and services
- Cloud Router
- Cloud NAT for outbound access from private resources

---

## Terraform Concepts Learned

- Module structure (`main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`)
- Input variables and typed defaults
- Outputs for exposing resource attributes to other modules
- Provider and version constraints
- Resource dependencies and implicit ordering

---

## Commands Executed

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

---

## Verification Commands

```bash
gcloud compute networks list
gcloud compute networks subnets list --network=mlops-vpc
gcloud compute routers list
gcloud compute routers nats list --router=<router-name> --region=us-central1
```

---

## Key Learning Points

- Terraform state tracks real infrastructure and enables safe, incremental changes.
- Modules promote reuse and separate configuration from implementation.
- Private Google Access lets private nodes reach Google APIs without public IPs.
- Cloud NAT provides controlled outbound internet access for private resources.

---

# Additional Infrastructure

## Storage Module

Implemented:

- Terraform Remote State Bucket
- Bucket Versioning
- Prevent Destroy
- Uniform Bucket Level Access

Purpose:

Provide secure centralized storage for Terraform state.

---

## Artifact Registry Module

Implemented:

- Docker Repository

Purpose:

Store Docker images for Kubernetes deployments.

---

## Service Account Module

Implemented:

- Dedicated Service Account

Purpose:

Avoid using personal credentials and prepare for least-privilege IAM.

---

## GKE Module

Implemented:

- GKE Cluster
- Separate Managed Node Pool
- Autoscaling
- Spot Nodes
- Shielded Nodes
- Reduced OAuth Scopes

Purpose:

Provide a production-style Kubernetes cluster using Terraform modules.

---

# Code Explanation

## google_container_cluster

Creates the Kubernetes control plane.

Important configuration:

- `remove_default_node_pool`
- `initial_node_count`
- `network`
- `subnetwork`
- `deletion_protection`

---

## google_container_node_pool

Creates worker nodes.

Important configuration:

- Machine Type
- Autoscaling
- Spot Nodes
- Service Account
- Auto Repair
- Auto Upgrade
- Shielded Nodes
- OAuth Scopes

---

# Verification

terraform fmt -recursive

Purpose

Format all Terraform files.

---

terraform validate

Purpose

Validate Terraform syntax and configuration.

---

terraform plan

Purpose

Preview infrastructure changes.

---

terraform apply

Purpose

Apply infrastructure changes.

---

terraform state list

Purpose

Display resources tracked by Terraform.

---

kubectl get nodes

Purpose

Verify worker nodes have joined the cluster.

---

gcloud container node-pools list

Purpose

Verify node pools from GCP.
