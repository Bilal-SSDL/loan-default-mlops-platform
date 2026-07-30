# Milestone 19 - CI/CD (GitHub Actions)

## Objective

Automate the build and delivery of the platform's images with **GitHub Actions**,
closing the loop with the existing ArgoCD GitOps deployment. On a push to `main`,
CI runs tests, builds and pushes the changed image(s) to Artifact Registry with a
git-SHA tag, then **writes the new tag back into the Kubernetes manifests** so
ArgoCD deploys it. A scheduled in-cluster job refreshes the serving pods when the
model is retrained.

---

## Architecture

```text
   Developer push to main
          │
          ▼
   GitHub Actions
     ├── test         (pytest gate)
     ├── changes      (path filters: api / trainer / mlflow)
     └── build-deploy
            ├── build + push image  (Artifact Registry, tag = sha-XXXXXXX)
            └── write-back tag into k8s manifests + git commit
          │
          ▼
   ArgoCD (auto-sync)  ──►  GKE  (rolling update)

   KFP retrain (weekly) ──► new champion ──► model-refresh CronJob ──► restart serving pods
```

---

## Design Decisions

- **CD via git tag write-back** (not Image Updater, not mutable tags): CI commits the
  new SHA tag into the manifest, ArgoCD syncs it. Pure GitOps — every deploy is an
  auditable commit and the live image is always visible in git.
- **Service-account key auth** for GitHub Actions (stored as the `GCP_SA_KEY`
  secret): consistent with the Iteration 1 "temporary key" stance. *Workload
  Identity Federation (OIDC) is deferred to Iteration 2.*
- **Path-filtered builds:** only the changed image is rebuilt
  (`ml/api/**` → `loan-api`, `ml/src/**` → `loan-trainer`, `platform/mlflow/**` →
  `mlflow`).
- **`champion` refresh via CronJob** (in-cluster, same-namespace RBAC): reliable and
  decoupled. *A strictly event-driven refresh step inside the training pipeline is
  deferred to Iteration 2 with the multi-step pipeline.*

---

## Components

- GitHub Actions workflow (`.github/workflows/cicd.yaml`)
- Test gate (`ml/tests/`)
- `GCP_SA_KEY` GitHub secret + `roles/artifactregistry.writer` on the SA
- Manifest tag write-back (`yq` + git commit via `GITHUB_TOKEN`)
- `model-refresh` CronJob + RBAC (`kubernetes/workloads/model-refresh/`)
- ArgoCD Application (`model-refresh`)

---

## Setup

### IAM + Secret

```bash
gcloud projects add-iam-policy-binding lendo-dr-417012 \
  --member="serviceAccount:lendo-app-service-account@lendo-dr-417012.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

Add the SA key contents as the GitHub Actions secret **`GCP_SA_KEY`**
(Settings → Secrets and variables → Actions).

### Workflow behaviour

- **Trigger:** push to `main` on `ml/**` or `platform/mlflow/**`.
- **Jobs:** `test` (pytest) → `changes` (path filter) → `build-deploy`
  (auth → build/push changed images → `yq` write-back → commit/push).
- **Loop-safe:** the write-back commit only touches `kubernetes/**` (not a trigger
  path), commits made with `GITHUB_TOKEN` do not retrigger workflows, and the commit
  message carries `[skip ci]`.
- **`yq` is pre-installed** on GitHub `ubuntu-latest` runners.
- **`loan-trainer`** is built and pushed but not tag-bumped in a manifest — it is
  consumed by the Kubeflow pipeline, not an ArgoCD workload. Updating the pipeline's
  image reference is manual for now (pipeline-image CD is an Iteration 2 item).

### Manifests updated by write-back

- `loan-api` → `kubernetes/workloads/serving/deployment.yaml`
  (`.spec.template.spec.containers[0].image`) and
  `kubernetes/workloads/kserve/inferenceservice.yaml`
  (`.spec.predictor.containers[0].image`)
- `mlflow` → `kubernetes/platform/mlflow/deployment.yaml`

---

## Model Refresh (champion)

Retraining promotes a new `champion`, but the serving pods cache the model in
memory. The `model-refresh` CronJob restarts both serving deployments shortly after
the weekly retrain, so they reload the new `champion`. RBAC is scoped to `get/list/
patch` on deployments in the `application` namespace via a dedicated
`model-refresher` ServiceAccount.

```bash
# manual test
kubectl create job -n application --from=cronjob/model-refresh model-refresh-manual
kubectl logs -n application job/model-refresh-manual
kubectl rollout status deployment/loan-default-predictor -n application
```

Rolling restarts are zero-downtime (readiness probes gate traffic).

---

## Verify the Loop

1. Make a change under `ml/api/` (e.g. bump the FastAPI `version`), commit, push.
2. **Actions:** `test` passes; `build-deploy` pushes `loan-api:sha-XXXXXXX` and
   commits the manifest bump.
3. **Git:** a `ci: deploy images sha-XXXXXXX [skip ci]` commit edits the serving +
   KServe manifests.
4. **ArgoCD:** syncs the commit and rolls out the new image.

```bash
kubectl get pods -n application -w
kubectl describe pod -n application -l app=loan-api | grep Image:
```

---

## Expected Outcome

- Push to `main` triggers the workflow; the test gate must pass before any build.
- Only the changed image is rebuilt and pushed (SHA-tagged).
- Manifests are updated in git with the new tag; ArgoCD rolls out the change.
- The `model-refresh` CronJob restarts serving pods so retrained models are served.

---

## Result

Image build and delivery are automated end to end: GitHub Actions tests, builds, and
pushes SHA-tagged images, then commits the tag into the manifests, and ArgoCD deploys
them — a fully auditable GitOps CI/CD loop. A scheduled in-cluster job keeps the
served model in sync with the latest `champion` after retraining.

---

## Notes / Lessons Learned

- **pytest exit code 5 = no tests collected.** An empty `ml/tests` (or an uncommitted
  test file) fails the `test` job. Ensure the test file is committed; the job can be
  made tolerant of an empty dir if desired.
- **Loop prevention** relies on three things: path filters, `GITHUB_TOKEN` commits
  not retriggering workflows, and `[skip ci]`.
- **Reused SA + key** (`lendo-app-service-account`) — granted `artifactregistry.writer`.
  This is the Iteration 1 temporary-key approach; OIDC replaces it in Iteration 2.
- **Refresh is scheduled, not event-driven** in Iteration 1. It restarts regardless
  of whether `champion` changed (harmless). A conditional/event-driven refresh pairs
  with the Iteration 2 multi-step pipeline.

---

## Next

- **Phase 7 - Monitoring:** Prometheus + Grafana; Kubernetes, application, MLflow,
  and KServe metrics; alerts.
- **Iteration 2:** GitHub Actions OIDC (keyless) auth; event-driven `champion`
  refresh as a pipeline step; pipeline-image CD.
