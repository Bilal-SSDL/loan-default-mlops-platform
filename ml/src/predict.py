# Responsibilities:

# Load latest model

# Accept sample input

# Return prediction

# This will later be used by FastAPI inference service.

import os
import joblib
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

# --------------------------------------------------
# Load Model & Preprocessor
# --------------------------------------------------

print("Loading model...")

model = joblib.load(
    os.path.join(MODEL_DIR, "loan_default_model.pkl")
)

preprocessor = joblib.load(
    os.path.join(PROCESSED_DIR, "preprocessor.pkl")
)

# --------------------------------------------------
# Example Input
# --------------------------------------------------
#Dynamic column collection
#df = pd.read_csv("data/raw/Loan_Default.csv")
#sample = df.drop(columns=["Status"]).iloc[[0]].copy()
sample = {
    "year": 2019,
    "loan_limit": "cf",
    "Gender": "Sex Not Available",
    "approv_in_adv": "nopre",
    "loan_type": "type1",
    "loan_purpose": "p1",
    "Credit_Worthiness": "l1",
    "open_credit": "nopc",
    "business_or_commercial": "nob/c",
    "loan_amount": 116500,
    "rate_of_interest": 4.0,
    "Interest_rate_spread": 0.5,
    "Upfront_charges": 1200,
    "term": 360,
    "Neg_ammortization": "not_neg",
    "interest_only": "not_int",
    "lump_sum_payment": "not_lpsm",
    "property_value": 180000,
    "construction_type": "sb",
    "occupancy_type": "pr",
    "Secured_by": "home",
    "total_units": "1U",
    "income": 6000,
    "credit_type": "EXP",
    "Credit_Score": 750,
    "co-applicant_credit_type": "CIB",
    "age": "35-44",
    "submission_of_application": "to_inst",
    "LTV": 65.0,
    "Region": "south",
    "Security_Type": "direct",
    "dtir1": 30
}

# --------------------------------------------------
# Convert to DataFrame
# --------------------------------------------------

input_df = pd.DataFrame([sample])

# --------------------------------------------------
# Apply Preprocessing
# --------------------------------------------------

processed_input = preprocessor.transform(input_df)

# --------------------------------------------------
# Prediction
# --------------------------------------------------

prediction = model.predict(processed_input)[0]

probability = model.predict_proba(processed_input)[0]

confidence = probability.max()

# --------------------------------------------------
# Output
# --------------------------------------------------

label = "Default" if prediction == 1 else "No Default"

print("\nPrediction Result")
print("------------------------")
print(f"Prediction : {label}")
print(f"Confidence : {confidence:.2%}")