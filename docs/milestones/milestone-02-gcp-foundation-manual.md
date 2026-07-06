# Milestone 02 - GCP Foundation

## Objective

Prepare the foundational cloud infrastructure required for the MLOps platform.

---

## Resources Created

### APIs

- Kubernetes Engine API
- Compute Engine API
- Artifact Registry API
- Cloud Storage API
- IAM API
- Cloud Monitoring API
- Cloud Logging API

---

### Networking

Created a custom VPC.

VPC Name

```
mlops-vpc
```

Subnets

| Name | CIDR |
|------|------|
| mlops-public | 10.10.1.0/24 |
| mlops-private | 10.10.2.0/24 |

Private Google Access enabled on the private subnet.

---

### Cloud NAT

Configured Cloud NAT to allow private resources to access the internet without assigning public IP addresses.

---

### Artifact Registry

Repository

```
mlops-images
```

Purpose

Store Docker images for training, inference, and platform services.

---

### Cloud Storage

Created a bucket for project assets.

Purpose

- Dataset storage
- Model artifacts
- Pipeline outputs
- Backups

---

### Service Account

```
mlops-platform
```

Purpose

Dedicated identity for platform components following the principle of least privilege.

---

## Validation

- VPC created successfully
- Subnets created
- Cloud NAT operational
- Artifact Registry accessible
- Storage bucket available
