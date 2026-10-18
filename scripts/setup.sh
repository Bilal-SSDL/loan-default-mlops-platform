#!/usr/bin/env bash
# Setup script for the loan-default MLOps platform (scripted version of docs/Setup-commands).
#
# Usage:
#   ./scripts/setup.sh all              # run steps 1-6 in order
#   ./scripts/setup.sh <step> [step..]  # run specific steps, e.g. ./scripts/setup.sh cluster secrets
#   ./scripts/setup.sh list             # show available steps
#
# Steps are safe to re-run: namespaces, secrets and helm releases are applied idempotently.

set -euo pipefail

PROJECT_ID="lendo-dr-417012"
REGION="us-central1"
CLUSTER="lendo-app-gke-cluster"
SA_EMAIL="lendo-app-service-account@${PROJECT_ID}.iam.gserviceaccount.com"
REGISTRY="${REGION}-docker.pkg.dev/${PROJECT_ID}/lendo-app-artifact-repo"
TF_STATE_BUCKET="gs://lendo-mlops-terraform-state"
GITHUB_REPO="Bilal-SSDL/loan-default-mlops-platform"

MLFLOW_IMAGE="${REGISTRY}/mlflow:1.0"
TRAINER_IMAGE="${REGISTRY}/mlflow-api/loan-trainer:1.0"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

log() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }

require() {
  for cmd in "$@"; do
    command -v "$cmd" >/dev/null 2>&1 || { echo "Missing required tool: $cmd" >&2; exit 1; }
  done
}

# Create or update a resource without failing if it already exists.
apply_namespace() { kubectl create namespace "$1" --dry-run=client -o yaml | kubectl apply -f -; }

# 1: Provision infrastructure with Terraform
step_terraform() {
  require terraform
  log "Terraform init + apply (terraform/environments/dev)"
  terraform -chdir=terraform/environments/dev init
  terraform -chdir=terraform/environments/dev apply
}

# 2: Authenticate, connect to GKE, install ingress-nginx and ArgoCD
step_cluster() {
  require gcloud kubectl helm
  log "GCP authentication"
  # An account can be listed as ACTIVE while its token has expired, so test for a usable token instead.
  if ! gcloud auth print-access-token >/dev/null 2>&1; then
    gcloud auth login
  fi
  gcloud config set project "$PROJECT_ID"
  gcloud container clusters get-credentials "$CLUSTER" --region "$REGION"

  log "Namespaces"
  for ns in ingress-nginx argocd mlflow monitoring application; do
    apply_namespace "$ns"
  done

  log "Helm repositories"
  helm repo add bitnami https://charts.bitnami.com/bitnami --force-update
  helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx --force-update
  helm repo add argo https://argoproj.github.io/argo-helm --force-update
  helm repo update

  log "Ingress NGINX"
  helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --wait

  # Installed with --insecure directly so the ingress in step 5 works without a second upgrade.
  log "ArgoCD"
  helm upgrade --install argocd argo/argo-cd -n argocd \
    --set 'server.extraArgs={--insecure}' --wait
}

# 3: Service-account key, IAM bindings and the MLflow GCP secret
step_secrets() {
  require gcloud kubectl
  mkdir -p secrets
  log "Service-account key"
  # Reuse the local key only if GCP still knows it: recreating the service account (terraform
  # destroy/apply) revokes old keys, and a stale key fails with "invalid_grant: Invalid JWT Signature".
  # Avoid creating keys needlessly, since GCP caps them at 10 per account.
  local key_file=secrets/mlflow-sa-key.json key_id=""
  [[ -f "$key_file" ]] && key_id=$(sed -n 's/.*"private_key_id": *"\([^"]*\)".*/\1/p' "$key_file")
  if [[ -n "$key_id" ]] && gcloud iam service-accounts keys list --iam-account="$SA_EMAIL" \
       --managed-by=user --format='value(name.basename())' | grep -qx "$key_id"; then
    echo "$key_file is still valid (key $key_id), reusing it"
  else
    [[ -f "$key_file" ]] && echo "$key_file is no longer valid for $SA_EMAIL, creating a new key"
    rm -f "$key_file"
    gcloud iam service-accounts keys create "$key_file" --iam-account="$SA_EMAIL"
  fi

  log "IAM bindings"
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" --role="roles/artifactregistry.reader" --condition=None >/dev/null
  gcloud storage buckets add-iam-policy-binding "$TF_STATE_BUCKET" \
    --member="serviceAccount:${SA_EMAIL}" --role="roles/storage.objectUser" >/dev/null

  log "Kubernetes secret gcp-service-account (mlflow)"
  kubectl create secret generic gcp-service-account \
    --from-file=key.json=secrets/mlflow-sa-key.json -n mlflow \
    --dry-run=client -o yaml | kubectl apply -f -

  # A running MLflow keeps the credentials it loaded at startup, so restart it to use the new key.
  if kubectl get deploy/mlflow -n mlflow >/dev/null 2>&1; then
    log "Restart MLflow to load the current key"
    kubectl rollout restart deploy/mlflow -n mlflow
    kubectl rollout status deploy/mlflow -n mlflow --timeout=300s
  fi
}

# 4: Build and push the MLflow server image if image is not already there in registry
step_mlflow_image() {
  require docker gcloud
  log "Build + push $MLFLOW_IMAGE"
  gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
  docker build -t "$MLFLOW_IMAGE" platform/mlflow
  docker push "$MLFLOW_IMAGE"
  # The tag is reused and the pod pulls with imagePullPolicy: Always, so a restart picks up the new image.
  if kubectl get deploy/mlflow -n mlflow >/dev/null 2>&1; then
    log "Restart MLflow to pick up the new image"
    kubectl rollout restart deploy/mlflow -n mlflow
    kubectl rollout status deploy/mlflow -n mlflow --timeout=300s
  fi
}

# 5: ArgoCD ingress + app-of-apps bootstrap
step_argocd() {
  require kubectl
  log "ArgoCD ingress + root application"
  kubectl apply -f kubernetes/infrastructure/ingress/argocd-ingress.yaml
  kubectl apply -f kubernetes/bootstrap/root-application.yaml

  log "ArgoCD initial admin password"
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
  echo
  echo "UI: kubectl port-forward svc/argocd-server -n argocd 8080:443  ->  http://localhost:8080"
}

# 6: Train the model, tracked in the in-cluster MLflow
step_train() {
  require python3 kubectl curl
  # The dataset is gitignored, so it has to be placed manually before training.
  if [[ ! -f "$REPO_ROOT/ml/data/raw/loan_default.csv" ]]; then
    echo "Missing ml/data/raw/loan_default.csv (gitignored). Download Loan_Default.csv from" >&2
    echo "https://www.kaggle.com/datasets/yasserh/loan-default-dataset and save it under that name." >&2
    return 1
  fi
  # Under WSL, a repo on /mnt/c makes pip extremely slow (thousands of small files over the
  # Windows filesystem bridge), so keep the venv on the Linux filesystem there. Override with ML_VENV.
  local venv="${ML_VENV:-}"
  if [[ -z "$venv" ]]; then
    if [[ "$REPO_ROOT" == /mnt/* ]]; then venv="$HOME/.venvs/loan-default-ml"; else venv="$REPO_ROOT/ml/.venv"; fi
  fi
  log "Python environment ($venv)"
  cd "$REPO_ROOT/ml"
  [[ -d "$venv" ]] || python3 -m venv "$venv"
  # Linux/macOS use bin/, Windows Git Bash uses Scripts/
  if [[ -f "$venv/bin/activate" ]]; then source "$venv/bin/activate"; else source "$venv/Scripts/activate"; fi
  # Reinstall only when requirements.txt changed since the last successful install.
  if cmp -s requirements.txt "$venv/.requirements.installed"; then
    echo "Dependencies up to date, skipping pip install"
  else
    echo "Installing dependencies (first install can take several minutes)..."
    pip install --disable-pip-version-check --progress-bar off -r requirements.txt
    cp requirements.txt "$venv/.requirements.installed"
  fi

  log "Port-forward MLflow to localhost:5000 (stopped when the step ends)"
  kubectl rollout status deploy/mlflow -n mlflow --timeout=300s
  # Background jobs ignore Ctrl+C, so an interrupted run can leave a stale forward holding
  # port 5000; clear it so the new forward can bind.
  pkill -f "port-forward svc/mlflow" 2>/dev/null || true
  local pf_log="${TMPDIR:-/tmp}/mlflow-port-forward.log"
  kubectl port-forward svc/mlflow 5000:5000 -n mlflow >"$pf_log" 2>&1 &
  local pf_pid=$!
  trap "kill $pf_pid 2>/dev/null || true" RETURN EXIT

  # Wait until MLflow actually answers through the tunnel before training.
  local ready=false
  for _ in $(seq 1 30); do
    kill -0 "$pf_pid" 2>/dev/null || break
    if curl -sf http://localhost:5000/health >/dev/null; then ready=true; break; fi
    sleep 1
  done
  if [[ "$ready" != true ]]; then
    echo "MLflow is not reachable on localhost:5000. Port-forward log:" >&2
    cat "$pf_log" >&2
    echo "Check the pod: kubectl get pods -n mlflow && kubectl logs deploy/mlflow -n mlflow --tail=50" >&2
    return 1
  fi

  export MLFLOW_TRACKING_URI=http://localhost:5000
  # The model upload goes through the port-forward and can exceed the 120s client default.
  export MLFLOW_HTTP_REQUEST_TIMEOUT=600
  log "Preprocess + train"
  python src/preprocess.py
  python src/train.py
  cd "$REPO_ROOT"
}

# 8: Build and push the Kubeflow trainer image (then follow docs/milestones/milestone-18-kubeflow.md)
step_kfp_image() {
  require docker gcloud
  log "Build + push $TRAINER_IMAGE"
  gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet
  docker build -f ml/Dockerfile.kfp -t "$TRAINER_IMAGE" ml/
  docker push "$TRAINER_IMAGE"
}

# 9: Grant Artifact Registry push permission for CI/CD
step_cicd() {
  require gcloud
  log "Grant roles/artifactregistry.writer to $SA_EMAIL"
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" --role="roles/artifactregistry.writer" --condition=None >/dev/null

  # CI authenticates with the same key (secrets.GCP_SA_KEY in .github/workflows/cicd.yaml); it goes
  # stale whenever the service account is recreated, so push the current one.
  log "Update GitHub secret GCP_SA_KEY"
  if command -v gh >/dev/null 2>&1 && [[ -f secrets/mlflow-sa-key.json ]]; then
    gh secret set GCP_SA_KEY --repo "$GITHUB_REPO" < secrets/mlflow-sa-key.json
  else
    echo "Skipped: needs the gh CLI and secrets/mlflow-sa-key.json (run the 'secrets' step first)." >&2
    echo "Or paste secrets/mlflow-sa-key.json into GitHub > Settings > Secrets > Actions > GCP_SA_KEY." >&2
  fi
}

# 10: Destroy GKE/networking/SA (keeps state bucket and artifact registry)
step_destroy() {
  require terraform
  log "Targeted terraform destroy"
  read -r -p "This destroys the GKE cluster, networking and service account. Type 'destroy' to continue: " answer
  [[ "$answer" == "destroy" ]] || { echo "Aborted."; return 1; }
  terraform -chdir=terraform/environments/dev destroy \
    -target=module.gke \
    -target=module.networking \
    -target=module.service_account \
    -target=google_artifact_registry_repository_iam_member.node_pool_reader
}

list_steps() {
  cat <<'EOF'
Steps (run in this order on a fresh setup):
  terraform     1  terraform init + apply
  cluster       2  gcloud auth, GKE credentials, namespaces, ingress-nginx, ArgoCD
  secrets       3  SA key, IAM bindings, gcp-service-account secret
  mlflow-image  4  build + push MLflow image
  argocd        5  ArgoCD ingress, root app, print admin password
  train         6  venv, port-forward MLflow, preprocess + train
  all              steps 1-6

Optional / separate:
  kfp-image     8  build + push Kubeflow trainer image
  cicd          9  grant artifactregistry.writer + update GitHub secret GCP_SA_KEY
  destroy      10  targeted terraform destroy (asks for confirmation)

Step 7 (KServe) is manual: see docs/milestones/milestone-17-kserve.md
EOF
}

run_step() {
  case "$1" in
    terraform)    step_terraform ;;
    cluster)      step_cluster ;;
    secrets)      step_secrets ;;
    mlflow-image) step_mlflow_image ;;
    argocd)       step_argocd ;;
    train)        step_train ;;
    kfp-image)    step_kfp_image ;;
    cicd)         step_cicd ;;
    destroy)      step_destroy ;;
    all)          for s in terraform cluster secrets mlflow-image argocd train; do run_step "$s"; done ;;
    list|-h|--help) list_steps ;;
    *) echo "Unknown step: $1" >&2; list_steps; exit 1 ;;
  esac
}

[[ $# -gt 0 ]] || { list_steps; exit 0; }
for step in "$@"; do run_step "$step"; done
