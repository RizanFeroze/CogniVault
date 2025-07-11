#!/bin/bash

echo "🐍 Installing Python dependencies..."

# Upgrade pip and install requirements (global context for Render)
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "🌐 Installing Uvicorn manually (just in case)..."
python3 -m pip install uvicorn[standard]  # Redundant but forces visibility

echo "🌐 Building React frontend..."
cd frontend
npm install
npm run build
