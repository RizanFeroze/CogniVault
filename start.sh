#!/bin/bash

echo "🚀 Starting Uvicorn..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 10000
