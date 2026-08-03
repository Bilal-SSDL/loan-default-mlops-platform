
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

### 
For the first implementation, MLflow authenticates to GCS using a Google Service Account key stored as a Kubernetes Secret.

---

## MLflow Artifact Store Bucket

### Decision

Reuse the existing GCS bucket (`gs://lendo-mlops-terraform-state/mlflow`) as the MLflow artifact store for Iteration 1.

### Reason

Keeps setup minimal while validating the platform. Known trade-off: this bucket also holds Terraform remote state, which mixes lifecycles and permissions. A dedicated `mlflow-artifacts` bucket is deferred to Iteration 2 (hardening).

---

## Model Registry Strategy

### Decision

Use MLflow **model aliases** (`LoanDefaultModel@champion`) rather than legacy model **stages**.

### Reason

Stages are deprecated in MLflow 3. Aliases give a stable, human-readable pointer (`@champion`) that the training pipeline moves on each successful run and the serving service resolves at load time.

---

## Training Orchestration

### Decision

Training runs against the in-cluster MLflow service and is orchestrated by **Kubeflow Pipelines (Phase 5)**. No standalone Kubernetes `Job` is used for training.

### Reason

A standalone `Job` would duplicate orchestration that Kubeflow is designed to own. Until Kubeflow is installed, the training pipeline is run manually against the tracking server (verified in Milestone 15).

---

## Model Serving Approach

### Decision

Deliver serving in two steps: **FastAPI on GKE first (Phase 4a / Milestone 16)**, then **KServe (Phase 4b)**.

### Reason

FastAPI is the shortest path to a working online-inference loop from the Model Registry and validates the end-to-end flow. KServe then adds serverless serving and canary deployments on top of a proven baseline.

---

## KServe Deployment Mode

### Decision

Iteration 1 uses **KServe RawDeployment mode** with a **custom container** (reusing the `loan-api` image). Upgrading to **Serverless mode (Knative)** is deferred to Iteration 2.

### Reason

RawDeployment needs only cert-manager + the KServe controller (no Knative/Istio), which fits the current `e2-standard-2` node pool and reuses the existing ingress-nginx and the proxied MLflow registry loading (no GCS secret). The trade-off is no scale-to-zero and limited canary traffic splitting. Serverless mode adds those capabilities but requires Knative, a network layer, and more node capacity — a natural Iteration 2 hardening step once the platform is fully working.

---

## Workflow Orchestration Platform

### Decision

Iteration 1 uses **Kubeflow Pipelines (KFP) standalone** with a **single-step** training pipeline (reusing the `loan-trainer` image). Full Kubeflow and a multi-step (artifact-passing) pipeline are deferred to Iteration 2.

### Reason

Full Kubeflow (Istio, dashboard, Katib, Notebooks, Profiles) is far too heavy for the `e2-standard-2` node pool; KFP standalone delivers the Phase 5 goals (pipelines, scheduling, MLflow integration) at a fraction of the footprint. A single-step pipeline (preprocess + train + register in one container) proves the orchestration → MLflow → registry loop with minimal code change; decomposing it into `preprocess` and `train` components that pass artifacts is a refinement for Iteration 2.

---

## Monitoring Stack

### Decision

Use the **kube-prometheus-stack** (Prometheus + Grafana + Alertmanager + exporters) and instrument the FastAPI app with `prometheus-fastapi-instrumentator`. Dashboards are provisioned via the Grafana sidecar (ConfigMap). Alert rules and Alertmanager routing are deferred to Iteration 2.

### Reason

The single chart brings the Prometheus Operator, Grafana, Alertmanager, and cluster exporters with ServiceMonitor/PrometheusRule CRDs — the standard, GitOps-friendly path, versus wiring Prometheus and Grafana separately. Instrumenting the app yields real inference metrics (request rate, latency, error rate), not just infra health, and the KServe path is covered since it reuses the same image. GitOps-provisioned dashboards survive Grafana pod restarts. Alerting (rules + receiver routing) is functional-but-not-critical for Iteration 1, so it is deferred to the hardening iteration.

---

## Logging Stack

### Decision

Use **Loki + Promtail** (`loki-stack` chart) in **single-binary mode with filesystem storage**, surfaced in the existing Grafana. Durable GCS-backed storage and a Promtail → Grafana Alloy migration are deferred to Iteration 2.

### Reason

Loki is label-based and Grafana-native, so logs land in the Grafana already used for metrics — one UI for metrics + logs, correlated by shared labels. Single-binary + filesystem is the lightest footprint and adequate for a learning cluster; the trade-off is that logs live on a PVC and are lost if it is deleted. Promtail is the simplest Loki collector (in LTS/maintenance but fully functional). Durable object-store (GCS) backing and the newer Alloy collector are production concerns for Iteration 2.