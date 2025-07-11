#!/bin/bash

echo "🐍 Installing Python dependencies in runtime shell..."
python3 -m pip install --upgrade pip --user
python3 -m pip install -r requirements.txt --user
python3 -m pip install 'uvicorn[standard]' --user  # Force to user site

# ✅ Add ~/.local/bin to PATH
export PATH=$PATH:/root/.local/bin

echo "🚀 Starting Uvicorn..."
python3 -m uvicorn api_server:app --host 0.0.0.0 --port 10000
