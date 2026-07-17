"""Train the loan-default Random Forest model and log the run to MLflow.

Pipeline (see ``main``):
    load data -> train -> evaluate -> save model -> log everything to MLflow

Everything for a run lives in MLflow: parameters, metrics, the model, and the
artifacts (ROC curve, confusion matrix, classification report, feature
importance). Artifacts are logged straight from in-memory objects via
``mlflow.log_figure`` / ``mlflow.log_text`` -- no manual image files.
"""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")  # headless backend; we never show figures, only log them
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# Make the ml/ package root importable when run as a script (python src/train.py).
sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import settings  # noqa: E402

# Model hyperparameters (RANDOM_STATE comes from the central config).
PARAMS = {
    "n_estimators": 200,
    "max_depth": 10,
    "random_state": settings.RANDOM_STATE,
    "n_jobs": -1,
}

MODEL_PATH = settings.MODEL_DIR / "loan_default_model.pkl"


def load_dataset():
    """Load the processed train/test splits produced by ``preprocess.py``."""
    processed = settings.PROCESSED_DATA_DIR
    X_train = joblib.load(processed / "X_train.pkl")
    X_test = joblib.load(processed / "X_test.pkl")
    y_train = joblib.load(processed / "y_train.pkl")
    y_test = joblib.load(processed / "y_test.pkl")
    print(f"Loaded processed data: {X_train.shape[0]:,} train / {X_test.shape[0]:,} test rows")
    return X_train, X_test, y_train, y_test


def load_feature_names():
    """Return the post-transform feature names from the fitted preprocessor.

    Used to label the feature-importance plot. Returns ``None`` if the
    preprocessor is unavailable so the caller can fall back to generic names.
    """
    try:
        preprocessor = joblib.load(settings.PROCESSED_DATA_DIR / "preprocessor.pkl")
        return list(preprocessor.get_feature_names_out())
    except Exception as exc:  # pragma: no cover - best-effort labelling
        print(f"Could not load feature names from preprocessor: {exc}")
        return None


def train_model(X_train, y_train, params: dict | None = None):
    """Fit a Random Forest classifier on the training split."""
    params = params or PARAMS
    print(f"Training RandomForestClassifier with {params}...")
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test) -> dict:
    """Compute classification metrics on the held-out test set."""
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions),
        "roc_auc": roc_auc_score(y_test, probabilities),
    }

    print("Evaluation metrics:")
    for name, value in metrics.items():
        print(f"  {name:<10}: {value:.4f}")
    return metrics


def save_model(model, path: Path = MODEL_PATH) -> Path:
    """Persist the trained model locally for evaluate.py / predict.py."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    print(f"Saved model to {path}")
    return path


def build_serving_pipeline(model) -> Pipeline:
    """Bundle the fitted preprocessor + trained model into one raw-input pipeline.

    The preprocessor was already fitted in preprocess.py; wrapping the fitted
    steps yields an end-to-end estimator (raw application -> prediction) with no
    refitting. This is what gets registered and served by the FastAPI app, so
    callers send raw records and never touch the preprocessor themselves.
    """
    preprocessor = joblib.load(settings.PROCESSED_DATA_DIR / "preprocessor.pkl")
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def _raw_input_example(pipeline: Pipeline, n: int = 2):
    """A few raw feature rows for the logged model's signature (best effort).

    Columns are taken from the fitted preprocessor so the example always matches
    exactly what the model expects, even as feature selection changes.
    """
    try:
        cols = list(pipeline.named_steps["preprocessor"].feature_names_in_)
        df = pd.read_csv(settings.RAW_DATA_PATH, nrows=n)
        return df[cols]
    except Exception as exc:  # pragma: no cover - signature is best-effort
        print(f"Skipping input_example (raw data unavailable): {exc}")
        return None


def _promote_latest_to_champion() -> None:
    """Point the 'champion' alias at the just-registered version so the API has a
    stable reference: models:/<MODEL_NAME>@champion."""
    client = mlflow.MlflowClient()
    versions = client.search_model_versions(f"name='{settings.MODEL_NAME}'")
    latest = max(versions, key=lambda v: int(v.version))
    client.set_registered_model_alias(settings.MODEL_NAME, "champion", latest.version)
    print(f"Set alias 'champion' -> {settings.MODEL_NAME} v{latest.version}")


def log_to_mlflow(model, params: dict, metrics: dict) -> None:
    """Log params/metrics and register the end-to-end pipeline in the Registry.

    Registers ``settings.MODEL_NAME`` and moves the ``champion`` alias to the new
    version so the FastAPI service always loads the latest promoted model.
    """
    mlflow.log_param("model", type(model).__name__)
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)

    pipeline = build_serving_pipeline(model)
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        name="model",
        registered_model_name=settings.MODEL_NAME,
        input_example=_raw_input_example(pipeline),
        # MLflow 3.x defaults to skops, which rejects the ColumnTransformer's
        # embedded numpy.dtype. cloudpickle serializes the full pipeline reliably.
        serialization_format="cloudpickle",
    )
    _promote_latest_to_champion()


def log_artifacts(model, X_test, y_test, feature_names=None) -> None:
    """Log evaluation artifacts to the active MLflow run without touching disk.

    Artifacts: ROC curve, confusion matrix, classification report, and the
    top-20 feature importances.
    """
    predictions = model.predict(X_test)

    # Confusion matrix
    cm_display = ConfusionMatrixDisplay.from_predictions(y_test, predictions, cmap="Blues")
    cm_display.ax_.set_title("Confusion Matrix")
    mlflow.log_figure(cm_display.figure_, "confusion_matrix.png")
    plt.close(cm_display.figure_)

    # ROC curve
    roc_display = RocCurveDisplay.from_estimator(model, X_test, y_test)
    roc_display.ax_.set_title("ROC Curve")
    mlflow.log_figure(roc_display.figure_, "roc_curve.png")
    plt.close(roc_display.figure_)

    # Classification report
    report = classification_report(y_test, predictions, digits=4)
    mlflow.log_text(report, "classification_report.txt")

    # Feature importance (top 20)
    importances = model.feature_importances_
    if feature_names is None or len(feature_names) != len(importances):
        feature_names = [f"feature_{i}" for i in range(len(importances))]
    top = np.argsort(importances)[::-1][:20][::-1]  # ascending for barh
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh([feature_names[i] for i in top], importances[top])
    ax.set_title("Top 20 Feature Importances")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    mlflow.log_figure(fig, "feature_importance.png")
    plt.close(fig)

    print("Logged artifacts: confusion_matrix, roc_curve, classification_report, feature_importance")


def main() -> None:
    """Run the full training pipeline inside a single MLflow run."""
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.EXPERIMENT_NAME)

    with mlflow.start_run():
        X_train, X_test, y_train, y_test = load_dataset()
        model = train_model(X_train, y_train)
        metrics = evaluate_model(model, X_test, y_test)
        save_model(model)
        log_to_mlflow(model, PARAMS, metrics)
        log_artifacts(model, X_test, y_test, feature_names=load_feature_names())

    print("\nTraining pipeline completed successfully.")


if __name__ == "__main__":
    main()
