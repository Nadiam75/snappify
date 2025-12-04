#!/bin/bash
# Script to restart server and test API

echo "=========================================="
echo "OCR API Restart and Test"
echo "=========================================="
echo ""
echo "IMPORTANT: Make sure to stop the current server first!"
echo "Press CTRL+C in the server terminal, then press Enter here to continue..."
read

echo ""
echo "Starting server in background..."
python run_server.py &
SERVER_PID=$!

echo "Waiting for server to start (5 seconds)..."
sleep 5

echo ""
echo "Testing API..."
echo ""

echo "1. Health Check:"
curl -s http://localhost:8000/health | python -m json.tool

echo ""
echo "2. Models Status:"
curl -s http://localhost:8000/models | python -m json.tool

echo ""
echo "3. OCR Test:"
curl -s -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" | python -m json.tool

echo ""
echo "=========================================="
echo "Test complete!"
echo "To stop the server, run: kill $SERVER_PID"
echo "=========================================="

