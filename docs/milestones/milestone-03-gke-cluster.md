# Milestone 03 - GKE Cluster

## Objective

Deploy a production-ready Kubernetes cluster that will host all MLOps platform components.

---

## Cluster Configuration

| Setting | Value |
|---------|-------|
| Cluster Type | Standard |
| Region | us-central1 |
| Network | mlops-vpc |
| Subnet | mlops-private |

---

## Node Pool

| Setting | Value |
|---------|-------|
| Machine Type | e2-standard-2 |
| Initial Nodes | 2 |
| Autoscaling | Enabled |
| Auto Upgrade | Enabled |
| Auto Repair | Enabled |

---

## Namespaces

Created:

- argocd
- ingress-nginx
- mlflow
- kubeflow
- kserve
- monitoring
- applications

---

## Cluster Validation

Commands executed

```bash
kubectl get nodes

kubectl get pods -A

kubectl get svc -A

kubectl get deployments -A

kubectl get storageclass
```

Storage Classes

- dynamic-rwo
- premium-rwo
- standard
- standard-rwo (default)

Default Storage Class

```
standard-rwo
```

Provisioner

```
pd.csi.storage.gke.io
```

---

## Lessons Learned

- GKE uses CSI drivers for dynamic storage provisioning.
- Namespaces provide logical isolation for platform components.
- Storage Classes automate Persistent Volume provisioning.
