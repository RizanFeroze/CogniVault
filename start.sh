#!/bin/bash

echo "🐍 Installing Python dependencies in runtime shell..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install uvicorn[standard]  # Force it inside start

echo "🚀 Starting Uvicorn..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 10000
