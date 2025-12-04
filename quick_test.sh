#!/bin/bash
# Quick test script for OCR API (Linux/Mac)

echo "=========================================="
echo "OCR API Quick Test"
echo "=========================================="
echo ""

# Check if server is running
echo "1. Checking server health..."
HEALTH=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✓ Server is running"
    echo "$HEALTH" | python -m json.tool
else
    echo "✗ Server is not running!"
    echo "Please start the server first: python run_server.py --reload"
    exit 1
fi

echo ""
echo "2. Checking models status..."
MODELS=$(curl -s http://localhost:8000/models)
echo "$MODELS" | python -m json.tool

echo ""
echo "3. Testing OCR on first available image..."

# Find first image in dataset directory
IMAGE=$(ls dataset/*.jpg dataset/*.png 2>/dev/null | head -1)
if [ -z "$IMAGE" ]; then
    echo "✗ No images found in dataset/ directory"
    exit 1
fi

echo "Using image: $IMAGE"
echo ""

# Test OCR
RESULT=$(curl -s -X POST "http://localhost:8000/ocr" -F "file=@$IMAGE")

# Save result
echo "$RESULT" > test_result.json
echo "Result saved to: test_result.json"
echo ""

# Show summary
echo "Summary:"
echo "$RESULT" | python -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success'):
    print(f\"✓ Success! Processing time: {data.get('processing_time_ms', 'N/A')} ms\")
    for model_name, model_result in data.get('models', {}).items():
        if model_result.get('success'):
            num = model_result.get('num_detections', 0)
            text = model_result.get('full_text', '')[:80]
            print(f\"  {model_name}: {num} detections - {text}...\")
        else:
            print(f\"  {model_name}: Failed\")
else:
    print(f\"✗ Failed: {data.get('error', 'Unknown error')}\")
"

echo ""
echo "Full result available in: test_result.json"
echo "View with: cat test_result.json | python -m json.tool"

