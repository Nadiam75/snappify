# OCR API Usage Guide

FastAPI service for OCR processing with multiple model support.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

### Start the server:
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Endpoints

### 1. Health Check
```bash
GET /health
```

Returns the health status of the service.

### 2. Get Models Status
```bash
GET /models
```

Returns the availability and initialization status of all OCR models.

### 3. Process Single Image
```bash
POST /ocr
```

**Parameters:**
- `file`: Image file (multipart/form-data)
- `models`: (Optional) Comma-separated list of models to use. Options: `EasyOCR`, `PaddleOCR`, `TrOCR`, `SwinTextSpotter`

**Example using curl:**
```bash
# Process with all models
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"

# Process with specific models
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

**Example using Python:**
```python
import requests

url = "http://localhost:8000/ocr"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### 4. Process Multiple Images (Batch)
```bash
POST /ocr/batch
```

**Parameters:**
- `files`: List of image files (multipart/form-data)
- `models`: (Optional) Comma-separated list of models to use

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/ocr/batch" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

## Response Format

### Success Response:
```json
{
  "success": true,
  "image_name": "image.jpg",
  "timestamp": "2025-12-03T12:00:00.000000",
  "processing_time_ms": 1234.56,
  "models": {
    "EasyOCR": {
      "model": "EasyOCR",
      "success": true,
      "texts": [
        {
          "text": "Detected text",
          "confidence": 0.95,
          "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
      ],
      "full_text": "Detected text",
      "num_detections": 1
    },
    "PaddleOCR": { ... },
    "TrOCR": { ... },
    "SwinTextSpotter": { ... }
  }
}
```

### Error Response:
```json
{
  "success": false,
  "image_name": "image.jpg",
  "timestamp": "2025-12-03T12:00:00.000000",
  "models": {},
  "error": "Error message"
}
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

## Notes

- Models are initialized on server startup
- Processing time includes all model inference
- Batch processing is limited to 10 images per request
- All models run in parallel when processing a single image
- Results include bounding boxes, confidence scores, and extracted text

