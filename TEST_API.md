# Testing the OCR API - Commands Guide

Quick reference for testing the OCR API and checking results.

## Step 1: Start the Server

```bash
# Development mode (with auto-reload)
python run_server.py --reload

# Or using uvicorn directly
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Wait for the message: "OCR models initialized successfully!"

## Step 2: Test the API

### Option A: Using the Test Script (Easiest)

```bash
# In a new terminal, run:
python test_api.py
```

This will automatically:
- Check server health
- Check model status
- Test OCR on available images
- Show results summary

### Option B: Using curl (Command Line)

#### 1. Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Check Models Status
```bash
curl http://localhost:8000/models
```

#### 3. Test OCR on an Image
```bash
# Test with all models (images are in dataset/ directory)
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"

# Test with specific models only
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"

# Save result to file
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o result.json
```

#### 4. View Saved Result
```bash
# Windows PowerShell
Get-Content result.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Windows CMD (if you have jq installed)
type result.json | jq .

# Linux/Mac
cat result.json | jq .
# or
python -m json.tool result.json
```

### Option C: Using Python (Interactive)

```python
import requests
import json

# Test health
response = requests.get("http://localhost:8000/health")
print(json.dumps(response.json(), indent=2))

# Test models status
response = requests.get("http://localhost:8000/models")
print(json.dumps(response.json(), indent=2))

# Test OCR (images are in dataset/ directory)
with open("dataset/1.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/ocr", files=files)
    
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# Print summary
if result.get("success"):
    print(f"\n✓ Success! Processing time: {result.get('processing_time_ms')} ms")
    for model_name, model_result in result.get("models", {}).items():
        if model_result.get("success"):
            print(f"{model_name}: {model_result.get('num_detections', 0)} detections")
            print(f"  Text: {model_result.get('full_text', '')[:100]}")
```

### Option D: Using the Interactive API Docs

1. Start the server
2. Open browser: http://localhost:8000/docs
3. Click on `/ocr` endpoint
4. Click "Try it out"
5. Click "Choose File" and select an image
6. Optionally set `models` parameter (e.g., "EasyOCR,PaddleOCR")
7. Click "Execute"
8. View the response below

## Step 3: Understanding the Results

### Success Response Structure:
```json
{
  "success": true,
  "image_name": "1.jpg",
  "timestamp": "2025-12-03T12:00:00.000000",
  "processing_time_ms": 1234.56,
  "models": {
    "EasyOCR": {
      "model": "EasyOCR",
      "success": true,
      "texts": [
        {
          "text": "Detected text here",
          "confidence": 0.95,
          "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
      ],
      "full_text": "Detected text here",
      "num_detections": 1
    },
    "PaddleOCR": { ... },
    "TrOCR": { ... },
    "SwinTextSpotter": { ... }
  }
}
```

### Error Response Structure:
```json
{
  "success": false,
  "image_name": "1.jpg",
  "timestamp": "2025-12-03T12:00:00.000000",
  "models": {},
  "error": "Error message here"
}
```

## Quick Test Commands (Copy & Paste)

### Windows PowerShell:
```powershell
# Start server (Terminal 1)
python run_server.py --reload

# Test API (Terminal 2)
python test_api.py

# Or test with curl
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Linux/Mac:
```bash
# Start server (Terminal 1)
python run_server.py --reload

# Test API (Terminal 2)
python test_api.py

# Or test with curl
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg" | jq .
```

## Testing Different Scenarios

### Test with All Models (Default)
```bash
# Note: Images are in dataset/ directory
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg"
```

### Test with Only EasyOCR
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR" -F "file=@dataset/1.jpg"
```

### Test with EasyOCR and PaddleOCR
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" -F "file=@dataset/1.jpg"
```

### Test Batch Processing (Multiple Images)
```bash
curl -X POST "http://localhost:8000/ocr/batch" \
  -F "files=@dataset/1.jpg" \
  -F "files=@dataset/2.jpg" \
  -F "files=@dataset/3.jpg"
```

## Viewing Results in a Readable Format

### Save and View JSON:
```bash
# Save result
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg" -o result.json

# View with Python
python -c "import json; print(json.dumps(json.load(open('result.json')), indent=2, ensure_ascii=False))"

# Or use jq (if installed)
cat result.json | jq .
```

### Extract Just the Text:
```python
import requests
import json

with open("1.jpg", "rb") as f:
    response = requests.post("http://localhost:8000/ocr", files={"file": f})
    
result = response.json()
if result.get("success"):
    for model_name, model_result in result["models"].items():
        if model_result.get("success"):
            print(f"{model_name}: {model_result.get('full_text', '')}")
```

## Troubleshooting

### Server not responding?
```bash
# Check if server is running
curl http://localhost:8000/health
```

### Models not initialized?
```bash
# Check model status
curl http://localhost:8000/models
```

### Port already in use?
```bash
# Use different port
python run_server.py --port 8001
# Then test with:
curl -X POST "http://localhost:8001/ocr" -F "file=@dataset/1.jpg"
```

### Image not found?
```bash
# List available images
dir *.jpg
# or
ls *.jpg

# Use correct filename
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/your_image.jpg"
```

