# """Central configuration for the ML pipeline.

# Import these constants instead of hard-coding paths / hyperparameters in the
# individual scripts, e.g.::

#     from config.settings import PROCESSED_DIR, MLFLOW_TRACKING_URI
# """

# from pathlib import Path

# # ml/ directory (this file lives in ml/config/settings.py).
# BASE_DIR = Path(__file__).resolve().parents[1]

# # ---- Paths ----
# DATA_DIR = BASE_DIR / "data"
# RAW_DIR = DATA_DIR / "raw"
# PROCESSED_DIR = DATA_DIR / "processed"
# MODELS_DIR = BASE_DIR / "models"
# ARTIFACTS_DIR = BASE_DIR / "artifacts"

# RAW_DATA_PATH = RAW_DIR / "loan_default.csv"
# PREPROCESSOR_PATH = PROCESSED_DIR / "preprocessor.pkl"
# MODEL_PATH = MODELS_DIR / "loan_default_model.pkl"

# # ---- Dataset ----
# TARGET = "Status"
# ID_COLUMN = "ID"

# # ---- Train/test split ----
# TEST_SIZE = 0.2
# RANDOM_STATE = 42

# # ---- MLflow ----
# MLFLOW_TRACKING_URI = "http://localhost:5000"
# MLFLOW_EXPERIMENT = "loan-default-prediction"

# # ---- Model hyperparameters ----
# RF_PARAMS = {
#     "n_estimators": 200,
#     "max_depth": 10,
#     "random_state": RANDOM_STATE,
#     "n_jobs": -1,
# }

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "loan_default.csv"

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = BASE_DIR / "models"

ARTIFACT_DIR = BASE_DIR / "artifacts"

# Static, internal MLflow endpoint. The Kubernetes service DNS
# (<service>.<namespace>.svc.cluster.local) is stable across infra rebuilds and
# never exposed publicly. Training therefore runs inside the cluster (K8s Job).
# Overridable via the MLFLOW_TRACKING_URI env var.
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://mlflow.mlflow.svc.cluster.local:5000",
)

EXPERIMENT_NAME = "Loan Default Prediction"

MODEL_NAME = "LoanDefaultModel"

RANDOM_STATE = 42
