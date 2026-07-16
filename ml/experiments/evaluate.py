# Generate:

# Confusion Matrix

# ROC Curve

# Classification Report

# Log these plots as MLflow artifacts.

import os
import joblib
import mlflow
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    RocCurveDisplay,
    PrecisionRecallDisplay,
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# --------------------------------------------------
# MLflow Configuration
# --------------------------------------------------

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("loan-default-prediction")

# --------------------------------------------------
# Load Model & Data
# --------------------------------------------------

print("Loading model and test dataset...")

model = joblib.load(os.path.join(MODEL_DIR, "loan_default_model.pkl"))

X_test = joblib.load(os.path.join(PROCESSED_DIR, "X_test.pkl"))
y_test = joblib.load(os.path.join(PROCESSED_DIR, "y_test.pkl"))

# --------------------------------------------------
# Predictions
# --------------------------------------------------

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

# --------------------------------------------------
# Metrics
# --------------------------------------------------

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

# --------------------------------------------------
# MLflow Logging
# --------------------------------------------------

with mlflow.start_run(run_name="model-evaluation"):

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("roc_auc", roc_auc)

    # ----------------------------
    # Classification Report
    # ----------------------------

    report = classification_report(y_test, predictions)

    report_path = os.path.join(
        MODEL_DIR,
        "classification_report.txt"
    )

    with open(report_path, "w") as file:
        file.write(report)

    mlflow.log_artifact(report_path)

    # ----------------------------
    # Confusion Matrix
    # ----------------------------

    plt.figure(figsize=(6, 5))

    sns.heatmap(
        confusion_matrix(y_test, predictions),
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    cm_path = os.path.join(
        MODEL_DIR,
        "confusion_matrix.png"
    )

    plt.tight_layout()
    plt.savefig(cm_path)
    plt.close()

    mlflow.log_artifact(cm_path)

    # ----------------------------
    # ROC Curve
    # ----------------------------

    RocCurveDisplay.from_predictions(
        y_test,
        probabilities
    )

    plt.tight_layout()

    roc_path = os.path.join(
        MODEL_DIR,
        "roc_curve.png"
    )

    plt.savefig(roc_path)
    plt.close()

    mlflow.log_artifact(roc_path)

    # ----------------------------
    # Precision Recall Curve
    # ----------------------------

    PrecisionRecallDisplay.from_predictions(
        y_test,
        probabilities
    )

    plt.tight_layout()

    pr_path = os.path.join(
        MODEL_DIR,
        "precision_recall_curve.png"
    )

    plt.savefig(pr_path)
    plt.close()

    mlflow.log_artifact(pr_path)

print("\nEvaluation completed successfully.")