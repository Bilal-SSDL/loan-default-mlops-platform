# created argocd application, to automatically create applications on hte bases of git repo

## Architecture

```text
GitHub
   │
   ▼
Root Application
   │
   ▼
kubernetes/applications
   │
   ├── postgres.yaml
   ├── mlflow.yaml
   ├── grafana.yaml
   └── prometheus.yaml
```


```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application

metadata:
  name: root-application
  namespace: argocd

spec:
  project: default

  source:
    repoURL: https://github.com/Bilal-SSDL/loan-default-mlops-platform.git
    targetRevision: HEAD
    path: kubernetes/applications

  destination:
    server: https://kubernetes.default.svc
    namespace: argocd

  syncPolicy:
    automated:
      prune: true
      selfHeal: true

    syncOptions:
      - CreateNamespace=true
```

```bash
kubectl apply -f argocd-root.yaml
```

## Key Takeaways

- One parent application manages all child applications.
- New applications are deployed by adding YAML files to Git.
- Manual application creation is no longer required.
