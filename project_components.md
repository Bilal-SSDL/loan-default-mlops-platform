# Project Components

Every component used in the loan-default MLOps platform, with a one-line purpose, grouped from cloud infrastructure through deployment, ML lifecycle, serving, observability and CI/CD.

## 1. Cloud foundation (GCP, provisioned by Terraform)

| Component | Purpose |
|---|---|
| **GCP project `lendo-dr-417012`** | The account where all the cloud resources live. |
| **Terraform** | Creates and destroys all GCP infrastructure from code (`terraform/`). |
| **Terraform modules** (`networking`, `gke`, `storage`, `artifact-registry`, `service-account`) | Reusable building blocks for each piece of infrastructure, combined by the environments below. |
| **`environments/dev`** | Creates the full dev stack: network, GKE, bucket, registry and service account. |
| **`environments/persistent`** | Defines only the long-lived resources (bucket, registry, service account), so they can be kept while the cluster is destroyed. |
| **GCS remote backend** (`environment/dev` prefix) | Stores Terraform state in the bucket, so state is shared and versioned. |
| **VPC `lendo-app-vpc`** | Private network that contains the cluster. |
| **Public subnet `10.0.1.0/24`** | Address range for internet-facing resources. |
| **Private subnet `10.0.2.0/24`** | Address range where the GKE nodes run; Private Google Access lets them reach Google APIs. |
| **Cloud Router `lendo-app-router`** | Required control plane for Cloud NAT. |
| **Cloud NAT `lendo-app-nat`** | Lets private nodes reach the internet (pull images, pip install) with no inbound exposure. |
| **GKE cluster `lendo-app-gke-cluster`** | Regional managed Kubernetes cluster (us-central1) that runs every workload; Workload Identity is enabled. |
| **Node pool `lendo-app-primary-node-pool`** (e2-standard-2, autoscaling 1–3) | Worker VMs with shielded secure boot, auto-upgrade and auto-repair. |
| **Service account `lendo-app-service-account`** | Identity used by the nodes, MLflow (GCS access) and CI (image push). |
| **IAM bindings** (`artifactregistry.reader`, `artifactregistry.writer`, `storage.objectUser`) | Let the service account pull and push images and read and write the bucket. |
| **GCS bucket `lendo-mlops-terraform-state`** | Holds Terraform state and MLflow artifacts (`/mlflow`); versioned and protected from deletion. |
| **Artifact Registry `lendo-app-artifact-repo`** | Private Docker registry for the `mlflow`, `loan-api` and `loan-trainer` images. |

## 2. Cluster bootstrap and access

| Component | Purpose |
|---|---|
| **gcloud** | Authenticates to GCP, fetches GKE credentials, manages keys and IAM. |
| **kubectl** | Runs commands against the cluster (apply manifests, logs, port-forward). |
| **Helm** | Installs the ingress-nginx and ArgoCD charts during bootstrap. |
| **`scripts/setup.sh`** | Runs the whole setup step by step: `terraform` → `cluster` → `secrets` → `mlflow-image` → `argocd` → `train`, plus `kfp-image`, `cicd` and `destroy`. |
| **`docs/Setup-commands`** | The original manual command list that `setup.sh` automates. |
| **Namespaces** (`ingress-nginx`, `argocd`, `mlflow`, `monitoring`, `application`, plus `kubeflow`, `kserve`, `cert-manager` created by ArgoCD) | Separate the workloads by concern. |
| **Ingress-NGINX** (Helm) | Single external load balancer that routes HTTP traffic to services by host and path. |
| **GCP Load Balancer** | Created automatically for the ingress-nginx Service; the public entry point into the cluster. |
| **nip.io** (`loan-api.<IP>.nip.io`) | Free wildcard DNS that maps a hostname to the ingress IP, so you don't need a domain. |
| **K8s Secret `gcp-service-account`** | Gives the MLflow pod the service-account key so it can write to GCS. |
| **`secrets/` folder** (gitignored) | Local copy of the service-account key, never committed. |

## 3. GitOps (continuous delivery)

| Component | Purpose |
|---|---|
| **ArgoCD** (Helm, `--insecure` behind the ingress) | Watches the GitHub repo and keeps the cluster matching it, with auto-sync, prune and self-heal. |
| **ArgoCD ingress** (`kubernetes/infrastructure/ingress/argocd-ingress.yaml`) | Serves the ArgoCD UI through ingress-nginx. |
| **`root-application`** (app-of-apps, `kubernetes/bootstrap/`) | One ArgoCD app that deploys every app in `kubernetes/applications/`. |
| **ArgoCD Applications** (`kubernetes/applications/*.yaml`) | One file per deployed component: cert-manager, kserve-crd, kserve, kube-prometheus-stack, kubeflow-cluster, kubeflow, loan-api, loan-kserve, loki-stack, mlflow, monitoring-workloads, postgresql. |
| **Sync waves** (1 → 4) | Install dependencies in order: cert-manager / KFP cluster resources → KServe CRDs / KFP → KServe → InferenceService. |
| **`kubernetes/disabled/minio.yaml`** | Earlier MinIO artifact store, kept for reference. GCS replaced it, so it isn't deployed. |

## 4. Experiment tracking and model registry

| Component | Purpose |
|---|---|
| **MLflow server** (custom image from `platform/mlflow`, v3.1.1) | Tracks runs, params, metrics and artifacts, and hosts the Model Registry. |
| **`platform/mlflow/Dockerfile` + `entrypoint.sh`** | Builds the MLflow server image and starts it with the Postgres backend and GCS artifact destination. |
| **`platform/mlflow/requirements.txt`** | Pins MLflow 3.1.1, SQLAlchemy 2.0.x, psycopg2, google-cloud-storage and gunicorn for the server image. |
| **MLflow artifact proxy** (`--artifacts-destination gs://…/mlflow`) | Clients upload over HTTP and the server writes to GCS, so clients need no GCP credentials. |
| **gunicorn** (`--timeout 600`) | Web server inside the MLflow container; the long timeout allows large model uploads. |
| **MLflow Deployment / Service / ServiceAccount** (`kubernetes/platform/mlflow/`) | Runs MLflow in the `mlflow` namespace and exposes it in-cluster on port 5000. |
| **PostgreSQL** (Bitnami chart) | MLflow's backend store for experiments, runs and registered models. |
| **Experiment `Loan Default Prediction`** | MLflow experiment that groups all training runs. |
| **Registered model `LoanDefaultModel`** | Versioned model in the MLflow Model Registry. |
| **`champion` alias** | Points at the production model version; serving always loads `models:/LoanDefaultModel@champion`. |

## 5. ML lifecycle (code in `ml/`)

| Component | Purpose |
|---|---|
| **Dataset `ml/data/raw/loan_default.csv`** | Kaggle loan-default data (148k rows, 34 columns); gitignored and placed by hand. |
| **`ml/data/processed/`** | Output of preprocessing (train/test splits), regenerated on every run. |
| **`ml/models/` and `ml/artifacts/`** | Local model file and evaluation outputs, also logged to MLflow; gitignored. |
| **`experiments/eda.ipynb`** | Exploratory data analysis that informed the feature and leakage decisions. |
| **`config/settings.py`** | Central paths, MLflow URI, experiment name, model name and random seed. |
| **`src/preprocess.py`** | Drops the ID and leakage columns, splits train/test, fits the preprocessing pipeline and saves the processed data. |
| **`src/train.py`** | Trains a RandomForest, logs to MLflow, registers the model and sets the `champion` alias. |
| **`src/evaluate.py`** | Produces the confusion matrix, ROC curve and classification report as MLflow artifacts. |
| **`src/predict.py`** | Local helper that loads a model and scores a sample; the prototype for the API. |
| **`src/utils.py`** | Shared helper functions. |
| **`ml/requirements.txt`** | Pinned Python dependencies for training, serving and CI. |
| **scikit-learn** | Preprocessing pipeline (ColumnTransformer, imputers, encoders) and the RandomForest model. |
| **pandas / numpy** | Data loading and manipulation. |
| **joblib / cloudpickle** | Model serialization (local file and MLflow model format). |
| **matplotlib / seaborn** | Plotting for the evaluation artifacts. |
| **Local venv** (`~/.venvs/loan-default-ml` under WSL, else `ml/.venv`) | Local training environment used by `setup.sh train`. |
| **kubectl port-forward to MLflow** (`localhost:5000`) | Lets local training reach the in-cluster MLflow server. |

## 6. Training orchestration (Kubeflow)

| Component | Purpose |
|---|---|
| **Kubeflow Pipelines 2.17.0** (`kubeflow-cluster` + `kubeflow` apps) | Runs training as reproducible, schedulable pipelines inside the cluster. |
| **KFP cluster-scoped resources** (`kubernetes/platform/kubeflow/cluster-scoped`) | CRDs and cluster roles KFP needs, installed first. |
| **KFP platform-agnostic install** (`kubernetes/platform/kubeflow/platform-agnostic`) | The KFP services themselves, with the MinIO image overridden. |
| **KFP API server + UI** | Upload pipelines, start runs and view their status. |
| **Argo Workflows** (bundled with KFP) | Execution engine that runs each pipeline step as a pod. |
| **MySQL** (bundled with KFP) | KFP's metadata store for pipelines and runs. |
| **MinIO** (bundled with KFP) | KFP's own artifact store for pipeline outputs, separate from MLflow. |
| **`pipelines/training_pipeline.py`** | KFP DSL definition: one container step that runs preprocess and train. |
| **`training_pipeline.yaml`** | Compiled pipeline spec uploaded to the KFP UI or API. |
| **`Dockerfile.kfp` → `loan-trainer` image** | Container holding `src/`, `config/` and the raw data, used by the pipeline step. |

## 7. Model serving

| Component | Purpose |
|---|---|
| **FastAPI app** (`api/main.py`) | REST inference service: `/health`, `/predict`, plus the KServe V1 routes `/v1/models/{name}` and `/v1/models/{name}:predict`. |
| **`api/schemas.py`** (Pydantic) | Validates the request and response payloads, which mirror the raw feature columns. |
| **`api/predictor.py`** | Loads `models:/LoanDefaultModel@champion` from MLflow once and caches it. |
| **uvicorn** | Web server that runs the FastAPI app on port 8000. |
| **`Dockerfile.api` → `loan-api` image** | Serving container (`api/` and `config/` only). |
| **`loan-api` Deployment** (`application` ns) | Plain Kubernetes serving path with readiness/liveness probes on `/health`. |
| **`loan-api` Service** | In-cluster endpoint on port 8000 (named port `http`). |
| **`loan-api` Ingress** | Exposes the API externally at `loan-api.<IP>.nip.io`. |
| **cert-manager** | Issues the TLS certificates that the KServe webhooks need. |
| **KServe CRDs** (`kserve-crd`, v0.14.1) | Adds the `InferenceService` resource type to the cluster. |
| **KServe controller** (`kserve`, RawDeployment mode) | Turns InferenceServices into plain Deployments + HPA, with no Knative or Istio. |
| **InferenceService `loan-default`** | KServe serving path for the same `loan-api` image, autoscaling 1–3 replicas at 60% CPU. |
| **HPA** (created by KServe) | Scales the InferenceService predictor pods on CPU. |

## 8. Observability

| Component | Purpose |
|---|---|
| **kube-prometheus-stack** (chart 88.1.2) | The whole metrics stack, installed as one chart. |
| **Prometheus Operator** | Turns `ServiceMonitor` and `PrometheusRule` resources into Prometheus configuration. |
| **Prometheus** (7-day retention) | Scrapes and stores metrics. |
| **Alertmanager** | Routes and deduplicates alerts. |
| **node-exporter** | Collects node-level CPU, memory and disk metrics. |
| **kube-state-metrics** | Collects Kubernetes object state (pods, deployments, restarts). |
| **Grafana** (user `admin`) | Dashboards over Prometheus and Loki. |
| **Grafana sidecars** | Auto-load dashboards and datasources from ConfigMaps labelled `grafana_dashboard: "1"` / `grafana_datasource: "1"`. |
| **prometheus-fastapi-instrumentator** | Exposes request count, latency and status metrics on `/metrics` from the API. |
| **ServiceMonitor `loan-api`** | Tells Prometheus to scrape the `loan-api` Service every 15s. |
| **ServiceMonitor `loan-default-predictor-kserve`** | Tells Prometheus to scrape the KServe predictor every 15s. |
| **PrometheusRule** (`kubernetes/workloads/serving/prometheusrule.yaml`) | Placeholder for alert rules; currently empty. |
| **Loki** (loki-stack 2.10.2, 10Gi PVC) | Log store. |
| **Promtail** (DaemonSet) | Tails every pod's logs on every node and ships them to Loki. |
| **`loki-datasource` ConfigMap** | Adds Loki as a Grafana datasource (not the default). |
| **`loan-api-dashboard` ConfigMap** | Grafana dashboard for API request rate, latency and errors. |
| **`loan-api-logs-dashboard` ConfigMap** | Grafana dashboard for the API's logs from Loki. |

## 9. CI/CD

| Component | Purpose |
|---|---|
| **GitHub repo** (`Bilal-SSDL/loan-default-mlops-platform`) | Single source of truth for infrastructure, manifests and code. |
| **GitHub Actions workflow** (`.github/workflows/cicd.yaml`) | Triggered by pushes to `main` that touch `ml/**` or `platform/mlflow/**`. |
| **`test` job** (pytest + `ml/tests/test_serving.py`) | Tests the API with a mocked model before anything is built. |
| **`changes` job** (`dorny/paths-filter`) | Rebuilds only the images whose files changed. |
| **`build-deploy` job** | Builds and pushes the `loan-api`, `loan-trainer` and `mlflow` images, tagged `sha-<commit>`. |
| **`google-github-actions/auth` + `setup-gcloud`** | Authenticate the workflow to GCP and configure Docker for Artifact Registry. |
| **`GCP_SA_KEY` secret** | Service-account key used to push to Artifact Registry. |
| **GitOps write-back** (`yq` + bot commit `[skip ci]`) | Writes the new image tags into the manifests; ArgoCD then rolls them out. |
