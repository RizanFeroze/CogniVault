#!/bin/bash

echo "🐍 Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install 'uvicorn[standard]'

echo "🌐 Building React frontend..."
cd frontend
npm install
npm run build
