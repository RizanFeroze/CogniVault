#!/bin/bash

echo "🐍 Installing Python dependencies in runtime shell..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --user
python3 -m pip install 'uvicorn[standard]' --user

echo "💡 PATH before export: $PATH"
export PATH=$PATH:~/.local/bin
echo "💡 PATH after export: $PATH"

echo "🚀 Starting Uvicorn..."
~/.local/bin/uvicorn api_server:app --host 0.0.0.0 --port 10000
