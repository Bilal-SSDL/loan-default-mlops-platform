# Milestone 18 - Workflow Orchestration (Kubeflow Pipelines)

## Objective

Orchestrate the model training workflow with **Kubeflow Pipelines (KFP) standalone**
on GKE. The existing preprocess + train code runs as a KFP pipeline that trains the
model, logs the run to MLflow, registers a new `LoanDefaultModel` version, and moves
the `champion` alias — replacing the manual, laptop-driven training run with an
in-cluster, repeatable, schedulable pipeline.

---

## Architecture

```text
        Kubeflow Pipelines (namespace: kubeflow)
        ┌───────────────────────────────────────┐
        │  ml-pipeline API + UI                  │
        │  Argo Workflow Controller              │
        │  MySQL (run metadata)                  │
        │  SeaweedFS / MinIO (step artifacts)    │
        └───────────────────┬───────────────────┘
                            │ runs
                            ▼
        loan-trainer container (single step)
          python src/preprocess.py && python src/train.py
                            │
                            ▼
        MLflow Tracking Server (namespace: mlflow)
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
        Model Registry            GCS Artifact Store
        (champion moved)          (proxied)
```

---

## Design Decisions

- **KFP standalone**, not full Kubeflow. Full Kubeflow (Istio, dashboard, Katib,
  Notebooks, Profiles) is far too heavy for the `e2-standard-2` node pool. KFP
  standalone delivers all Phase 5 goals (pipelines, scheduling, MLflow integration).
  *Full Kubeflow platform is deferred to Iteration 2.*
- **Single-step pipeline** for this iteration: one container runs preprocess +
  train + register. Minimal code change; proves KFP orchestration and MLflow
  integration. *Splitting into multi-step components with artifact passing between
  `preprocess` and `train` is deferred to Iteration 2.*
- **Bundled storage/metadata** (SeaweedFS/MinIO + MySQL) used for KFP's own
  step artifacts and run metadata; MLflow continues to use GCS for model artifacts.

---

## Components

- Kubeflow Pipelines standalone (`kubeflow` namespace)
- Training image (`loan-trainer`) — a new image containing `ml/src`, `ml/config`,
  and the raw dataset (the serving `loan-api` image does not include `src/`)
- KFP SDK v2 pipeline definition (`ml/pipelines/training_pipeline.py`)
- ArgoCD Applications (`kubeflow-cluster`, `kubeflow`)
- Recurring run (scheduled retraining)

---

## Deployment Flow

1. Check node capacity; bump the node pool if needed.
2. Build and push the `loan-trainer` training image.
3. Install KFP standalone via ArgoCD (cluster-scoped resources first, then
   platform-agnostic).
4. Fix the unavailable KFP MinIO image via a kustomize image override.
5. Author the single-step pipeline with the KFP SDK v2 and compile it.
6. Access the KFP UI and submit a run.
7. Verify a new MLflow run, registered version, and `champion` promotion.
8. Create a recurring run for automated retraining.

---

## Commands

### Build & Push Training Image

```bash
docker build -f ml/Dockerfile \
-t us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/mlflow-api/loan-trainer:1.0 \
ml/

docker push \
us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/mlflow-api/loan-trainer:1.0
```

### Install KFP Standalone (via ArgoCD)

Wrapper kustomizations reference the pinned KFP manifests:

```yaml
# kubernetes/platform/kubeflow/cluster-scoped/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=2.2.0
```

```yaml
# kubernetes/platform/kubeflow/platform-agnostic/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=2.2.0
# Image override: the pinned gcr.io minio tag is no longer resolvable.
images:
  - name: gcr.io/ml-pipeline/minio
    newName: minio/minio
    newTag: RELEASE.2019-08-14T20-37-41Z
```

Two ArgoCD Applications install these with sync-waves 1 (cluster-scoped) and 2
(platform-agnostic), both with `ServerSideApply=true`.

### Direct Install Fallback (if ArgoCD will not converge)

```bash
export PIPELINE_VERSION=2.2.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION"
```

### Verify Install

```bash
kubectl get pods -n kubeflow
# ml-pipeline, ml-pipeline-ui, mysql, seaweedfs, metadata-*, workflow-controller ... all Running
```

### Compile the Pipeline

```bash
pip install "kfp==2.*"
python ml/pipelines/training_pipeline.py   # produces training_pipeline.yaml
```

### Access the KFP UI

```bash
kubectl port-forward svc/ml-pipeline-ui -n kubeflow 8080:80
# open http://127.0.0.1:8080   (use http:// and the IP, not https / localhost)
```

Upload `training_pipeline.yaml` -> Create run, or submit via SDK:

```python
from kfp.client import Client
from training_pipeline import training_pipeline
Client(host="http://127.0.0.1:8080").create_run_from_pipeline_func(training_pipeline, arguments={})
```

### Schedule Automated Retraining

Create a **Recurring run** in the KFP UI (e.g. cron `0 2 * * 0`, weekly), or
`client.create_recurring_run(...)`.

---

## Expected Outcome

- All KFP pods Running in the `kubeflow` namespace
- KFP UI reachable via port-forward
- Pipeline run completes successfully (green DAG)
- MLflow: new run under `Loan Default Prediction`, new `LoanDefaultModel` version,
  `champion` alias moved to it
- A recurring run is scheduled for automated retraining

---

## Result

The training workflow is orchestrated by Kubeflow Pipelines. A single-step pipeline
runs preprocessing and training inside the cluster using the `loan-trainer` image,
logs to MLflow, registers a new model version, and promotes the `champion` alias.
Retraining is repeatable and schedulable, removing the dependency on a manual local
run. The install is GitOps-managed by ArgoCD.

---

## Notes / Lessons Learned

- **Unavailable KFP MinIO image.** The KFP manifests pin
  `gcr.io/ml-pipeline/minio:RELEASE.2019-08-14T20-37-41Z-license-compliance`, which
  no longer resolves on the gcr.io mirror (`ErrImagePull: not found`). Fixed with a
  kustomize `images:` override to `minio/minio` at the same release tag. (This KFP
  version actually provisions **SeaweedFS** for object storage; the override still
  applies to any residual minio reference.) For robustness on GKE and to avoid
  Docker Hub rate limits, the image can instead be mirrored into Artifact Registry.
- **KFP UI `ERR_SSL_PROTOCOL_ERROR`.** The `ml-pipeline-ui` serves plain HTTP on
  port 3000; browsers HSTS-upgrade `localhost` to HTTPS and fail. Access via
  `http://127.0.0.1:8080` (IP, explicit http), clear the `localhost` HSTS entry at
  `chrome://net-internals/#hsts`, or use a fresh port. Not a cluster problem.
- **Install ordering / server-side apply.** KFP ships large CRDs and cluster-scoped
  resources; ArgoCD uses `ServerSideApply=true` and sync-waves (cluster-scoped
  before platform-agnostic), plus a retry backoff, because the install briefly goes
  Degraded before self-healing.
- **Separate training image.** The serving image (`loan-api`) contains only `api/`
  and `config/`; training needs `src/` and the raw dataset, so `loan-trainer` is a
  distinct image.
- **Served model does not auto-refresh.** The KServe/FastAPI predictor caches the
  model in memory at load time. After the pipeline promotes a new `champion`, the
  running predictor keeps serving the previous model until restarted:
  `kubectl rollout restart deployment/loan-default-predictor -n application`.
  Automating this on a new `champion` is a Phase 6 (CI/CD) concern.
- **Two artifact stores coexist by design.** KFP uses its bundled object store for
  step-to-step artifacts; MLflow uses GCS for model artifacts. Different purposes.

---

## Next

- **Phase 6 - CI/CD:** GitHub Actions to build/push images and drive ArgoCD
  deployments; automate predictor refresh on new `champion`.
- **Iteration 2:** full Kubeflow platform; split the pipeline into multi-step
  components with artifact passing between `preprocess` and `train`.
