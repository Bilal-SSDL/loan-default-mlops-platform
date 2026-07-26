"""FastAPI inference service.

    Client -> FastAPI -> MLflow Registry -> Prediction

Run locally (with the MLflow port-forward active):
    MLFLOW_TRACKING_URI=http://localhost:5000 uvicorn api.main:app --port 8000
"""

from __future__ import annotations
from pydantic import BaseModel

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

# Make the ml/ package root importable regardless of how the app is launched.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from api import predictor  # noqa: E402
from api.schemas import LoanRequest, PredictionResponse  # noqa: E402

app = FastAPI(title="Loan Default Prediction API", version="1.1.0")


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


# --- KServe V1 inference protocol ---------------------------------------------
# KServe routes external calls to GET /v1/models/{name} (readiness) and
# POST /v1/models/{name}:predict with a {"instances": [...]} body. Each instance
# uses the raw loan-application columns (same shape as /predict, including the
# hyphenated co-applicant_credit_type key).


class InferenceRequest(BaseModel):
    instances: list[dict]


class InferenceResponse(BaseModel):
    predictions: list[dict]


@app.get("/v1/models/{model_name}")
def kserve_ready(model_name: str):
    """KServe V1 readiness endpoint."""
    return {"name": model_name, "ready": True}


@app.post("/v1/models/{model_name}:predict", response_model=InferenceResponse)
def kserve_predict(model_name: str, request: InferenceRequest):
    """KServe V1 predict: run each raw instance through the registered pipeline."""
    try:
        predictions = [predictor.predict(instance) for instance in request.instances]
        return {"predictions": predictions}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Prediction failed: {exc}")
