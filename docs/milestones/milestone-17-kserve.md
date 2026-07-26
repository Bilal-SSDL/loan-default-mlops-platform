# Milestone 17 - KServe Model Serving (RawDeployment)

## Objective

Serve the Loan Default Prediction model through a KServe `InferenceService` on GKE,
using **RawDeployment mode** and a **custom container** (the existing `loan-api`
image). This introduces the standard KServe serving abstraction, HPA autoscaling,
and the KServe V1 inference protocol, while keeping the platform lightweight (no
Knative / Istio) so it fits the current node pool.

---

## Architecture

```text
        Client
          │
          ▼
   KServe InferenceService (loan-default)     namespace: application
          │   (RawDeployment: Deployment + Service + HPA)
          ▼
   loan-api custom container
          │
          ▼
   MLflow Tracking Server                     namespace: mlflow
          │
   ┌──────┴───────┐
   ▼              ▼
Model Registry   GCS Artifact Store (proxied)
(champion)
```

The KServe predictor runs the same `loan-api` image built in Milestone 16, so the
model is still loaded from the MLflow Model Registry (`LoanDefaultModel@champion`)
through the tracking-server artifact proxy — no GCS credentials are needed in the
serving pod.

---

## Design Decisions

- **RawDeployment mode** (not Serverless): needs only cert-manager + the KServe
  controller — no Knative, no Istio — which fits the `e2-standard-2` node pool and
  reuses the existing ingress-nginx.
- **Custom container** (reuses `loan-api`): keeps the proxied registry loading and
  avoids a GCS storage-initializer secret.
- **Trade-off accepted for Iteration 1:** no scale-to-zero and no clean canary
  traffic splitting. Upgrading to Serverless (Knative) for those capabilities is
  planned for Iteration 2.

---

## Components

- cert-manager (KServe webhook dependency)
- KServe CRDs
- KServe Controller (RawDeployment default mode)
- `InferenceService` (custom container)
- KServe V1 inference protocol endpoints (added to the FastAPI app)
- HPA autoscaling
- ArgoCD Applications (cert-manager, kserve-crd, kserve, loan-kserve)

---

## Deployment Flow

1. Install cert-manager via ArgoCD (sync-wave 1).
2. Register the KServe OCI Helm repository in ArgoCD.
3. Install KServe CRDs (sync-wave 2), then the KServe controller (sync-wave 3).
4. Add KServe V1 protocol endpoints to the FastAPI app.
5. Rebuild and push the serving image (`loan-api:1.1`).
6. Ensure the `champion` alias exists in the Model Registry.
7. Create the `InferenceService` and its ArgoCD Application (sync-wave 4).
8. Commit to GitHub — ArgoCD syncs each stage.
9. Verify predictions through the KServe V1 endpoint.

---

## Commands

### Register KServe OCI Helm Repo (one-time)

```bash
kubectl apply -n argocd -f - <<'EOF'
apiVersion: v1
kind: Secret
metadata:
  name: kserve-charts
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: helm
  name: kserve-charts
  url: ghcr.io/kserve/charts
  enableOCI: "true"
EOF
```

### Build & Push Serving Image

```bash
docker build -f ml/Dockerfile.api \
-t us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/mlflow-api/loan-api:1.1 \
ml/

docker push \
us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/mlflow-api/loan-api:1.1
```

### Ensure the champion Alias Exists

The predictor loads `models:/LoanDefaultModel@champion`. If training was never run
against this MLflow instance, the alias will be missing and requests fail with
`Registered model alias champion not found`. Run training (which registers the
model and sets the alias) or set the alias manually:

```bash
kubectl port-forward svc/mlflow 5000:5000 -n mlflow

# Option A: run training (registers + sets champion)
cd ml
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/preprocess.py
python src/train.py

# Option B: set the alias on an existing version
python - <<'PY'
import mlflow
from mlflow import MlflowClient
mlflow.set_tracking_uri("http://localhost:5000")
c = MlflowClient()
v = max(c.search_model_versions("name='LoanDefaultModel'"), key=lambda m: int(m.version))
c.set_registered_model_alias("LoanDefaultModel", "champion", v.version)
print("champion ->", v.version)
PY
```

### Commit Changes

```bash
git add kubernetes/applications/cert-manager.yaml \
        kubernetes/applications/kserve-crd.yaml \
        kubernetes/applications/kserve.yaml \
        kubernetes/workloads/kserve/ \
        kubernetes/applications/loan-kserve.yaml \
        ml/api/main.py

git commit -m "Serve loan-default model with KServe (RawDeployment) - Milestone 17"

git push origin main
```

### Verify

```bash
kubectl get pods -n cert-manager
kubectl get pods -n kserve
kubectl get inferenceservice -n application
kubectl get pods,deploy,svc,hpa -n application | grep loan-default

# Confirm the default deployment mode
kubectl -n kserve get cm inferenceservice-config -o jsonpath='{.data.deploy}'; echo
```

### Test Prediction (KServe V1 Protocol)

```bash
kubectl port-forward svc/loan-default-predictor -n application 8080:80

# Readiness
curl http://localhost:8080/v1/models/loan-default

# Predict ("instances" is a list; raw loan-application columns)
curl -X POST http://localhost:8080/v1/models/loan-default:predict \
  -H "Content-Type: application/json" \
  -d '{"instances": [ {
    "year": 2019, "loan_limit": "cf", "Gender": "Sex Not Available",
    "approv_in_adv": "nopre", "loan_type": "type1", "loan_purpose": "p1",
    "Credit_Worthiness": "l1", "open_credit": "nopc", "business_or_commercial": "nob/c",
    "loan_amount": 116500, "term": 360.0, "Neg_ammortization": "not_neg",
    "interest_only": "not_int", "lump_sum_payment": "not_lpsm", "construction_type": "sb",
    "occupancy_type": "pr", "Secured_by": "home", "total_units": "1U", "income": 1740.0,
    "credit_type": "EXP", "Credit_Score": 758, "co-applicant_credit_type": "CIB",
    "age": "25-34", "submission_of_application": "to_inst", "Region": "south",
    "Security_Type": "direct"
  } ]}'
```

---

## Expected Outcome

- cert-manager running (controller, cainjector, webhook)
- KServe CRDs installed and controller Running
- Default deployment mode: `RawDeployment`
- `InferenceService` `loan-default` READY = True
- KServe-managed Deployment, Service, and HPA created in `application`
- `/v1/models/loan-default` returns `{"name":"loan-default","ready":true}`
- `/v1/models/loan-default:predict` returns `{"predictions":[{"prediction":...,"probability":...}]}`
- HPA scales the predictor between `minReplicas` and `maxReplicas` under load

---

## Result

The Loan Default Prediction model is served by a KServe `InferenceService` in
RawDeployment mode, reusing the `loan-api` custom container. Predictions are served
over the KServe V1 inference protocol, the model is loaded from the MLflow Registry
via the `champion` alias, and the predictor autoscales via HPA. The InferenceService
runs alongside the Milestone 16 FastAPI Deployment and is fully GitOps-managed by
ArgoCD.

---

## Notes / Lessons Learned

- **`champion` alias is required.** A `Registered model alias champion not found`
  error means training was not run against this MLflow instance. Run training or
  set the alias manually (see commands above).
- **KServe V1 payload differs from the FastAPI `/predict` payload.** V1 wraps
  records in `{"instances": [...]}` and returns `{"predictions": [...]}`. The
  original `/predict` endpoint (single record) is retained for direct use.
- **CRDs need server-side apply.** cert-manager and KServe CRDs exceed the
  client-side apply annotation size limit; ArgoCD Applications use
  `ServerSideApply=true`.
- **Install ordering matters.** cert-manager must be healthy before the KServe
  controller (webhook certificates). ArgoCD `sync-wave` annotations enforce the
  order: cert-manager (1) -> kserve-crd (2) -> kserve (3) -> loan-kserve (4).
- **OCI Helm repo.** KServe charts are OCI artifacts; the repo must be registered
  in ArgoCD with `enableOCI: "true"` before the Applications can pull the charts.
- **Deployment mode is forced per-service** via the
  `serving.kserve.io/deploymentMode: RawDeployment` annotation, so RawDeployment is
  used even if the global default differs across chart versions.

---

## Next

- **Phase 5 - Kubeflow Pipelines:** orchestrate preprocess -> train -> register.
- **Iteration 2:** upgrade KServe RawDeployment -> Serverless (Knative) for
  scale-to-zero and canary traffic splitting (requires a node-pool capacity bump).
