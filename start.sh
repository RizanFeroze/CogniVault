#!/bin/bash

echo "🐍 Activating virtualenv and starting uvicorn..."

# Activate venv (created during build)
source venv/bin/activate

# Start the server
uvicorn api_server:app --host 0.0.0.0 --port 10000
