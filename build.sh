#!/bin/bash

echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt || { echo "❌ pip install failed"; exit 1; }

echo "🛠 Building React frontend..."
cd frontend
npm install
npm run build

