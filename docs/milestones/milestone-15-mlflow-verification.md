# Milestone 16 - MLflow Verification

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
cd ml/experiments

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

kubectl port-forward svc/mlflow 5000:5000 -n mlflow

python train.py
```

---

## Expected Outcome

- Experiment created
- Run created
- Parameters logged
- Metrics logged
- Model logged
- Artifacts stored in GCS
- Metadata stored in PostgreSQL

---

## Result

MLflow tracking server successfully manages experiment metadata in PostgreSQL and artifacts in Google Cloud Storage.