"""FastAPI inference service.

    Client -> FastAPI -> MLflow Registry -> Prediction

Run locally (with the MLflow port-forward active):
    MLFLOW_TRACKING_URI=http://localhost:5000 uvicorn api.main:app --port 8000
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

# Make the ml/ package root importable regardless of how the app is launched.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from api import predictor  # noqa: E402
from api.schemas import LoanRequest, PredictionResponse  # noqa: E402

app = FastAPI(title="Loan Default Prediction API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "model_uri": predictor.MODEL_URI}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: LoanRequest):
    try:
        # by_alias=True restores the raw column names the pipeline expects.
        return predictor.predict(request.model_dump(by_alias=True))
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Prediction failed: {exc}")
