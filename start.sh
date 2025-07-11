#!/bin/bash

echo "🚀 Starting Uvicorn without virtualenv..."
uvicorn api_server:app --host 0.0.0.0 --port 10000

