#!/bin/sh

# Run Alembic migrations
alembic upgrade head

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 80 --reload

