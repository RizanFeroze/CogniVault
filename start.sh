#!/bin/bash

echo "🐍 Adjusting PATH so 'uvicorn' can be found"
export PATH="/opt/render/project/src/.local/bin:$PATH"

echo "🚀 Starting Uvicorn..."
uvicorn api_server:app --host 0.0.0.0 --port 10000
