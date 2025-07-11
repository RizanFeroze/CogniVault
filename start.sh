#!/bin/bash

echo "📦 Reinstalling Python dependencies globally..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "🚀 Starting Uvicorn server..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 10000
