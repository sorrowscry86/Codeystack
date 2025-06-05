#!/bin/bash

# Startup script for Studio Lite with Multi-LLM Provider System
echo "Starting Studio Lite with Multi-LLM Provider System..."

# Test the LLM provider system first
echo "Testing LLM Provider System..."
python test_llm_providers.py

echo ""
echo "Available services:"
echo "- Streamlit App: http://localhost:8501"
echo "- LLM API: http://localhost:5000"
echo ""

# Start Flask API in the background
echo "Starting Flask LLM API on port 5000..."
python app.py &

# Wait a moment for Flask to start
sleep 2

# Start Streamlit in the foreground
echo "Starting Streamlit app on port 8501..."
streamlit run studio_lite.py --server.port=8501 --server.address=0.0.0.0
