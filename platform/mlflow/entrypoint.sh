#!/bin/sh

mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri "$BACKEND_STORE_URI" \
  --artifacts-destination "$ARTIFACT_ROOT"
