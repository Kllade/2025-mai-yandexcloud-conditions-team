#!/bin/bash
set -e

echo "Waiting for database to be ready..."
python -m scripts.wait_for_db


echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload