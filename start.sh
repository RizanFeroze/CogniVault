#!/bin/bash

which uvicorn
uvicorn --version

echo "🚀 Starting Uvicorn..."
uvicorn api_server:app --host 0.0.0.0 --port 10000
