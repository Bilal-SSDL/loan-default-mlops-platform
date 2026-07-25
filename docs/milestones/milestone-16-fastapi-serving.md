# Milestone 16 - FastAPI Model Serving

## Objective

Deploy the Loan Default Prediction model as an online inference service on GKE.
The FastAPI application loads the registered model from the MLflow Model Registry
using the `champion` alias and serves real-time predictions. Deployment is managed
by ArgoCD following the existing GitOps pattern.

---

## Architecture

```text
        Client
          │
          ▼
   FastAPI (loan-api)          namespace: application
          │
          ▼
   MLflow Tracking Server      namespace: mlflow
          │
   ┌──────┴───────┐
   ▼              ▼
Model Registry   GCS Artifact Store (proxied)
(champion)

## Components
FastAPI Inference Service (ml/api)
Serving Docker Image (ml/Dockerfile.api)
Google Artifact Registry
MLflow Model Registry (LoanDefaultModel@champion)
Kubernetes Deployment
Kubernetes Service
ArgoCD Application
Deployment Flow
Pin dependency versions in ml/requirements.txt for reproducible model loading.
Build the FastAPI serving image.
Push the image to Artifact Registry.
Add the Deployment and Service manifests.
Add the ArgoCD Application.
Commit changes to GitHub.
ArgoCD syncs automatically.
The inference service starts on GKE.
Verify online predictions.


## Commands
Build Image

docker build -f ml/Dockerfile.api \
-t us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/loan-api:1.0 \
ml/
Push Image

gcloud auth configure-docker us-central1-docker.pkg.dev

docker push \
us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/loan-api:1.0
Commit Changes

git add ml/Dockerfile.api ml/requirements.txt \
        kubernetes/workloads/serving/ kubernetes/applications/loan-api.yaml

git commit -m "Deploy FastAPI loan-default inference service (Milestone 16)"

git push origin main
Verify

kubectl get applications -n argocd
kubectl get pods -n application
kubectl logs deploy/loan-api -n application

kubectl port-forward svc/loan-api -n application 8000:8000

# Health check
curl http://localhost:8000/health

# Prediction (real dataset row; ID / leakage / target columns removed)
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2019, "loan_limit": "cf", "Gender": "Sex Not Available",
    "approv_in_adv": "nopre", "loan_type": "type1", "loan_purpose": "p1",
    "Credit_Worthiness": "l1", "open_credit": "nopc", "business_or_commercial": "nob/c",
    "loan_amount": 116500, "term": 360.0, "Neg_ammortization": "not_neg",
    "interest_only": "not_int", "lump_sum_payment": "not_lpsm", "construction_type": "sb",
    "occupancy_type": "pr", "Secured_by": "home", "total_units": "1U", "income": 1740.0,
    "credit_type": "EXP", "Credit_Score": 758, "co-applicant_credit_type": "CIB",
    "age": "25-34", "submission_of_application": "to_inst", "Region": "south",
    "Security_Type": "direct"
  }'