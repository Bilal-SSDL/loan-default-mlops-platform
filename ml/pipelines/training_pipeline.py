from kfp import dsl, compiler

IMAGE = "us-central1-docker.pkg.dev/lendo-dr-417012/lendo-app-artifact-repo/mlflow-api/loan-trainer:1.0"
MLFLOW_URI = "http://mlflow.mlflow.svc.cluster.local:5000"


@dsl.container_component
def train_step():
    return dsl.ContainerSpec(
        image=IMAGE,
        command=["sh", "-c", "python src/preprocess.py && python src/train.py"],
    )


@dsl.pipeline(name="loan-default-training", description="Preprocess + train + register to MLflow")
def training_pipeline():
    task = train_step()
    task.set_env_variable("MLFLOW_TRACKING_URI", MLFLOW_URI)
    task.set_caching_options(False)   # always retrain on demand


if __name__ == "__main__":
    compiler.Compiler().compile(training_pipeline, "training_pipeline.yaml")
