# Responsibilities:

# Load processed data

# Train baseline model (Random Forest is a good starting point)

# Log to MLflow:

# Parameters

# Metrics

# Model

# Feature importance (optional)

# Metrics to log:

# Accuracy

# Precision

# Recall

# F1 Score

# ROC-AUC


import os
import joblib
import mlflow
import mlflow.sklearn

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

# --------------------------------------------------
# MLflow Configuration
# --------------------------------------------------

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("loan-default-prediction")

# --------------------------------------------------
# Load Processed Data
# --------------------------------------------------

print("Loading processed datasets...")

X_train = joblib.load(os.path.join(PROCESSED_DIR, "X_train.pkl"))
X_test = joblib.load(os.path.join(PROCESSED_DIR, "X_test.pkl"))
y_train = joblib.load(os.path.join(PROCESSED_DIR, "y_train.pkl"))
y_test = joblib.load(os.path.join(PROCESSED_DIR, "y_test.pkl"))

# --------------------------------------------------
# Train Model
# --------------------------------------------------

with mlflow.start_run():

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )

    print("Training model...")

    model.fit(X_train, y_train)

    # --------------------------
    # Predictions
    # --------------------------

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    # --------------------------
    # Metrics
    # --------------------------

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC AUC  : {roc_auc:.4f}")

    # --------------------------
    # MLflow Parameters
    # --------------------------

    mlflow.log_param("model", "RandomForestClassifier")
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("random_state", 42)

    # --------------------------
    # MLflow Metrics
    # --------------------------

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)

    # --------------------------
    # Save Local Model
    # --------------------------

    local_model_path = os.path.join(
        MODEL_DIR,
        "loan_default_model.pkl"
    )

    joblib.dump(model, local_model_path)

    # --------------------------
    # Log Model to MLflow
    # --------------------------

    mlflow.sklearn.log_model(
        sk_model=model,
        name="loan-default-model"
    )

    # --------------------------
    # Confusion Matrix
    # --------------------------

    cm = confusion_matrix(y_test, predictions)

    disp = ConfusionMatrixDisplay(cm)

    disp.plot(cmap="Blues")

    plt.tight_layout()

    cm_path = os.path.join(
        MODEL_DIR,
        "confusion_matrix.png"
    )

    plt.savefig(cm_path)

    plt.close()

    mlflow.log_artifact(cm_path)

print("\nTraining completed successfully.")