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




import mlflow
import mlflow.sklearn
    
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# MLflow Tracking Server
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("iris-classification")

# Load Dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data,
    iris.target,
    test_size=0.2,
    random_state=42,
)

# Start MLflow Run
with mlflow.start_run():

    # Model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    # Train
    model.fit(X_train, y_train)

    # Predict
    predictions = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, predictions)

    # Log Parameters
    mlflow.log_param("model", "RandomForest")
    mlflow.log_param("n_estimators", 100)

    # Log Metric
    mlflow.log_metric("accuracy", accuracy)

    # Log Model
    mlflow.sklearn.log_model(
        sk_model=model,
        name="iris-model",
    )

    print(f"Accuracy: {accuracy:.4f}")
    print("Run logged successfully!")