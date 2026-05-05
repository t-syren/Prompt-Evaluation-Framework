#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt -q

echo "Starting FastAPI backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait until backend is ready
echo "Waiting for backend..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:8000/docs > /dev/null 2>&1; then
        echo "Backend is up."
        break
    fi
    sleep 1
done

echo "Starting Streamlit frontend on port ${DATABRICKS_APP_PORT:-8501}..."
streamlit run frontend/app.py \
    --server.port "${DATABRICKS_APP_PORT:-8501}" \
    --server.address "0.0.0.0" \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false

# If streamlit exits, kill the backend too
kill $BACKEND_PID
