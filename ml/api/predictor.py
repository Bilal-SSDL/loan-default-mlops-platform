"""Load the model from the MLflow Model Registry and run predictions.

    MLflow Registry -> LoanDefaultModel -> champion (production) version
                    -> loaded into memory -> prediction

The registered model is the end-to-end pipeline (preprocessor + classifier), so
raw records go straight in. We never load loan_default_model.pkl from disk; the
model always comes from the Registry.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

# Make the ml/ package root importable regardless of how the app is launched.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import settings  # noqa: E402

# Alias-based reference: 'champion' points at the promoted (production) version,
# which train.py moves on every successful run. Override with MODEL_URI if needed
# (e.g. a specific version: models:/LoanDefaultModel/3).
MODEL_URI = os.getenv("MODEL_URI", f"models:/{settings.MODEL_NAME}@champion")

_model = None


def load_model():
    """Load and cache the registered model in memory."""
    global _model
    if _model is None:
        mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
        print(f"Loading model from registry: {MODEL_URI}")
        _model = mlflow.sklearn.load_model(MODEL_URI)
    return _model


def predict(features: dict) -> dict:
    """Predict on a single raw loan application.

    ``features`` uses the raw column names (as produced by
    ``LoanRequest.model_dump(by_alias=True)``).
    """
    model = load_model()
    row = pd.DataFrame([features])
    prediction = int(model.predict(row)[0])
    probability = float(model.predict_proba(row)[0][1])
    return {"prediction": prediction, "probability": round(probability, 4)}
