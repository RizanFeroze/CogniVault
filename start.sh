#!/bin/bash

echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install 'uvicorn[standard]'

echo "🔧 Setting PATH for uvicorn..."
export PATH="$HOME/.local/bin:$PATH"

echo "🚀 Starting Uvicorn..."
exec ~/.local/bin/uvicorn api_server:app --host 0.0.0.0 --port 10000
