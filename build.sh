#!/bin/bash

echo "📦 Installing Python dependencies..."

# Use python3 -m pip to ensure it installs globally (Render installs python globally)
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt || { echo "❌ pip install failed"; exit 1; }

echo "⚛️ Building React frontend..."
cd frontend
npm install
npm run build
