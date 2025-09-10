#!/bin/bash

# LegalMind Backend Startup Script for Railway

echo "🚀 Starting LegalMind Backend..."

# Set default port if not provided
export PORT=${PORT:-5000}

# Activate virtual environment if it exists
if [ -d "/opt/venv" ]; then
    source /opt/venv/bin/activate
fi

# Create necessary directories
mkdir -p src/database
mkdir -p legal_vector_db

# Start the application
echo "🌐 Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 src.main:app