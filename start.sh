#!/bin/bash

echo "🐍 Installing Python dependencies in runtime shell..."
python3 -m pip install --upgrade pip --user
python3 -m pip install -r requirements.txt --user
python3 -m pip install 'uvicorn[standard]' --user

# ✅ Add ~/.local/bin to PATH so uvicorn can be found
export PATH="$HOME/.local/bin:$PATH"

echo "🚀 Starting Uvicorn..."
uvicorn api_server:app --host 0.0.0.0 --port 10000
