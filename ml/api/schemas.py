"""Request/response schemas for the inference API.

The model is the end-to-end pipeline registered as LoanDefaultModel, whose
preprocessor was fit on the full raw feature set. ``LoanRequest`` therefore
mirrors those raw columns. Frequently-missing numerics are Optional (the
pipeline's imputer fills them); ``co-applicant_credit_type`` keeps its original
hyphenated name via an alias.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class LoanRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    year: int = 2019
    loan_limit: str
    Gender: str
    approv_in_adv: str
    loan_type: str
    loan_purpose: str
    Credit_Worthiness: str
    open_credit: str
    business_or_commercial: str
    loan_amount: float
    term: float | None = None
    Neg_ammortization: str
    interest_only: str
    lump_sum_payment: str
    construction_type: str
    occupancy_type: str
    Secured_by: str
    total_units: str
    income: float | None = None
    credit_type: str
    Credit_Score: int
    co_applicant_credit_type: str = Field(alias="co-applicant_credit_type")
    age: str
    submission_of_application: str
    Region: str
    Security_Type: str


class PredictionResponse(BaseModel):
    prediction: int
    probability: float
