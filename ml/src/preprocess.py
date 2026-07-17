"""Preprocess the raw loan-default dataset for model training.

Responsibilities:
    * Load the raw dataset
    * Handle missing values (median for numeric, most-frequent for categorical)
    * Encode categorical features (one-hot)
    * Scale numerical features (optional; off by default since the baseline
      model is a tree ensemble that does not need scaling)
    * Split into stratified train/test sets
    * Persist the processed datasets and the fitted preprocessor

The fitted preprocessor is saved to ``models/preprocessor.joblib`` so that
``predict.py`` / the inference service can apply the exact same transforms to
incoming raw records.

Usage:
    python preprocess.py [--test-size 0.2] [--random-state 42] [--scale-numeric]
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ----------------------------
# Paths
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "loan_default.csv"
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

os.makedirs(PROCESSED_DIR, exist_ok=True)


# ----------------------------
# Load Dataset
# ----------------------------
print("Loading dataset...")

df = pd.read_csv(RAW_DATA_PATH)

print(f"Dataset Shape: {df.shape}")


# ----------------------------
# Drop ID Column
# ----------------------------
if "ID" in df.columns:
    df.drop(columns=["ID"], inplace=True)


# ----------------------------
# Drop Leakage Columns
# ----------------------------
# These fields are missing almost exclusively for defaulted loans (e.g.
# rate_of_interest / property_value / LTV are NaN for ~all Status==1 rows), so
# their missingness (and thus their imputed value) effectively encodes the
# target and yields an unrealistic ~1.0 ROC-AUC. They are also largely known
# only after approval, so they would not be available at scoring time anyway.
LEAKAGE_COLUMNS = [
    "rate_of_interest",
    "Interest_rate_spread",
    "Upfront_charges",
    "property_value",
    "LTV",
    "dtir1",
]
df.drop(columns=[c for c in LEAKAGE_COLUMNS if c in df.columns], inplace=True)


# ----------------------------
# Target Variable
# ----------------------------
TARGET = "Status"

X = df.drop(columns=[TARGET])
y = df[TARGET]


# ----------------------------
# Identify Column Types
# ----------------------------
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

print(f"Numerical Features: {len(numeric_features)}")
print(f"Categorical Features: {len(categorical_features)}")


# ----------------------------
# Numeric Pipeline
# ----------------------------
numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)


# ----------------------------
# Categorical Pipeline
# ----------------------------
categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)


# ----------------------------
# Combine Pipelines
# ----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)


# ----------------------------
# Train/Test Split
# ----------------------------
print("Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ----------------------------
# Fit Preprocessor
# ----------------------------
print("Fitting preprocessing pipeline...")

X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)


# ----------------------------
# Save Processed Data
# ----------------------------
joblib.dump(
    preprocessor,
    os.path.join(PROCESSED_DIR, "preprocessor.pkl")
)

joblib.dump(
    X_train_processed,
    os.path.join(PROCESSED_DIR, "X_train.pkl")
)

joblib.dump(
    X_test_processed,
    os.path.join(PROCESSED_DIR, "X_test.pkl")
)

joblib.dump(
    y_train,
    os.path.join(PROCESSED_DIR, "y_train.pkl")
)

joblib.dump(
    y_test,
    os.path.join(PROCESSED_DIR, "y_test.pkl")
)

print("\nPreprocessing completed successfully!")
print(f"Processed files saved in: {PROCESSED_DIR}")