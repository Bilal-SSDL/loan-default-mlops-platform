# Milestone 14 - MLflow Deployment

## Objective

Deploy MLflow on Google Kubernetes Engine using ArgoCD with PostgreSQL as the backend store and Google Cloud Storage as the artifact store.

---

## Architecture

```text
                 GitHub
                    │
                    ▼
                 ArgoCD
                    │
                    ▼
          MLflow Deployment
             │          │
             ▼          ▼
       PostgreSQL     GCS Bucket
```

---

## Components

- Custom MLflow Docker Image
- Google Artifact Registry
- PostgreSQL
- Google Cloud Storage
- Kubernetes Deployment
- Kubernetes Service
- Kubernetes Secret
- ArgoCD Application

---

## Deployment Flow

1. Build MLflow Docker image.
2. Push image to Artifact Registry.
3. Create GCP Service Account key.
4. Create Kubernetes Secret.
5. Configure Deployment.
6. Commit changes to GitHub.
7. ArgoCD syncs automatically.
8. MLflow starts on GKE.

---

## Commands

### Build Image

```bash
docker build \
-t us-central1-docker.pkg.dev/<PROJECT_ID>/mlops-images/mlflow:1.1 \
./platform/mlflow
```

### Push Image

```bash
docker push \
us-central1-docker.pkg.dev/<PROJECT_ID>/mlops-images/mlflow:1.1
```

### Create Service Account Key

```bash
gcloud iam service-accounts keys create \
./secrets/mlflow-sa-key.json \
--iam-account=lendo-app-service-account@<PROJECT_ID>.iam.gserviceaccount.com
```

### Create Kubernetes Secret

```bash
kubectl create secret generic gcp-service-account \
--from-file=key.json=./secrets/mlflow-sa-key.json \
-n mlflow
```

### Commit Changes

```bash
git add .

git commit -m "Deploy MLflow"

git push origin main
```

---

## Result

- MLflow deployed successfully on GKE.
- Experiment metadata stored in PostgreSQL.
- Artifacts stored in GCS.
- Deployment managed by ArgoCD.
- Custom image pulled from Artifact Registry.

---

## Notes

Current authentication uses a Google Service Account key stored as a Kubernetes Secret.

In the next iteration, this will be replaced with GKE Workload Identity to eliminate static credentials.