# Commands Executed

## Add ArgoCD Helm Repository

```bash
helm repo add argo https://argoproj.github.io/argo-helm
```

Purpose

Adds the official ArgoCD Helm repository.

---

## Update Helm Repositories

```bash
helm repo update
```

Purpose

Downloads the latest chart metadata.

---

## View Chart Information

```bash
helm show chart argo/argo-cd
```

Purpose

Displays chart metadata.

---

## View Default Values

```bash
helm show values argo/argo-cd
```

Purpose

Displays all configurable parameters.

---

## Install ArgoCD

```bash
helm install argocd argo/argo-cd \
  --namespace argocd
```

Purpose

Installs ArgoCD into the `argocd` namespace.

---

## Verify Helm Releases

```bash
helm list -A
```

Purpose

Lists all Helm releases installed in the cluster.

---

## Verify Pods

```bash
kubectl get pods -n argocd
```

Purpose

Ensures all ArgoCD Pods are running.

---

## Verify Services

```bash
kubectl get svc -n argocd
```

Purpose

Lists all Services created by ArgoCD.

---

## Verify Deployments

```bash
kubectl get deployments -n argocd
```

Purpose

Displays all Deployments created by the Helm chart.

---

## Inspect the ArgoCD Server Deployment

```bash
kubectl describe deployment argocd-server -n argocd
```

Purpose

Displays detailed information about the ArgoCD Server Deployment.

---

## View All Resources

```bash
kubectl get all -n argocd
```

Purpose

Lists all Kubernetes resources created in the `argocd` namespace.

---

## View ReplicaSets

```bash
kubectl get rs -n argocd
```

Purpose

Shows ReplicaSets created by Deployments.

---

## View ConfigMaps

```bash
kubectl get configmaps -n argocd
```

Purpose

Displays configuration used by ArgoCD.

---

## View Secrets

```bash
kubectl get secrets -n argocd
```

Purpose

Displays Secrets created for ArgoCD components.

---

## View Events

```bash
kubectl get events -n argocd --sort-by=.metadata.creationTimestamp
```
```bash
k port-forward svc/argocd-server -n argocd 8080:443

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
    -o jsonpath="{.data.password}" | base64 -d
```


Purpose

Shows recent events for troubleshooting.

