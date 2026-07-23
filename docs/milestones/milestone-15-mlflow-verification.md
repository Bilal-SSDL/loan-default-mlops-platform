# Milestone 15 - MLflow Verification

## Objective

MLflow is an open-source MLOps platform that manages the entire machine learning lifecycle. You should use it to centralize experiment tracking, enforce reproducibility across teams, and streamline model deployment. It eliminates the chaos of scattered spreadsheets and lost code by automatically logging parameters, metrics, and model artifacts

---

## Steps

1. Create Python virtual environment.
2. Install dependencies.
3. Configure MLflow Tracking URI.
4. Train a sample model.
5. Log experiment data.
6. Verify metadata in PostgreSQL.
7. Verify artifacts in GCS.

---

## Commands

```bash
cd ml

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

# Expose the in-cluster MLflow tracking server locally
kubectl port-forward svc/mlflow 5000:5000 -n mlflow

# Point the pipeline at the forwarded tracking server, then run it
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/preprocess.py
python src/train.py
```

---

## Expected Outcome

- Experiment created
- Run created
- Parameters logged
- Metrics logged
- Model logged and registered as `LoanDefaultModel`
- `champion` alias pointed at the new version
- Artifacts stored in GCS
- Metadata stored in PostgreSQL

---

## Result

MLflow tracking server successfully manages experiment metadata in PostgreSQL and artifacts in Google Cloud Storage.