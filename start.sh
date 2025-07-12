#!/bin/bash

echo "🐍 Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install --user -r requirements.txt
python3 -m pip install --user 'uvicorn[standard]'

# Export path to where Render installs user binaries
export PATH=$PATH:/root/.local/bin

echo "🚀 Starting Uvicorn..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 10000
