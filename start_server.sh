#!/bin/bash
# Start ValoRPC API Server
# Run this to start the web dashboard on localhost:8000

echo "🎮 Starting ValoRPC API Server..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask not found, installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "✅ Starting server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the API server
python3 api_server.py
