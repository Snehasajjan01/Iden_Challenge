#!/bin/bash

echo "🚀 Starting Product Dashboard..."
echo ""
echo "The application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 app.py
elif command -v python &> /dev/null; then
    python app.py
else
    echo "❌ Python not found. Please install Python 3.7+ and try again."
    exit 1
fi
