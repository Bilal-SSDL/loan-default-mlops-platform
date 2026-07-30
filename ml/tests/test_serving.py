from unittest.mock import patch
from fastapi.testclient import TestClient

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from api.schemas import LoanRequest

SAMPLE = {
    "year": 2019, "loan_limit": "cf", "Gender": "Sex Not Available",
    "approv_in_adv": "nopre", "loan_type": "type1", "loan_purpose": "p1",
    "Credit_Worthiness": "l1", "open_credit": "nopc", "business_or_commercial": "nob/c",
    "loan_amount": 116500, "term": 360.0, "Neg_ammortization": "not_neg",
    "interest_only": "not_int", "lump_sum_payment": "not_lpsm", "construction_type": "sb",
    "occupancy_type": "pr", "Secured_by": "home", "total_units": "1U", "income": 1740.0,
    "credit_type": "EXP", "Credit_Score": 758, "co-applicant_credit_type": "CIB",
    "age": "25-34", "submission_of_application": "to_inst", "Region": "south",
    "Security_Type": "direct",
}


def test_schema_accepts_sample_with_alias():
    req = LoanRequest(**SAMPLE)
    assert "co-applicant_credit_type" in req.model_dump(by_alias=True)


def test_predict_endpoint_mocked():
    # patch the model so no MLflow/registry is needed in CI
    with patch("api.predictor.predict", return_value={"prediction": 0, "probability": 0.12}):
        from api.main import app
        client = TestClient(app)
        r = client.post("/predict", json=SAMPLE)
        assert r.status_code == 200
        assert set(r.json()) == {"prediction", "probability"}
