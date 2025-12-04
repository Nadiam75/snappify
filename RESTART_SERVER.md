# Restart the API Server

The libraries are now installed, but the API server is still running with the old state.

## Steps to Fix:

### 1. Stop the Current Server
Press `CTRL+C` in the terminal where the server is running.

### 2. Restart the Server
```bash
python run_server.py --reload
```

### 3. Wait for Initialization
You should see messages like:
```
Initializing OCR models...
==================================================
Initializing OCR Models...
==================================================
Initializing EasyOCR...
[OK] EasyOCR initialized successfully
Initializing PaddleOCR...
[OK] PaddleOCR initialized successfully
...
OCR models initialized successfully!
```

### 4. Test Again
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

### 5. Check Model Status
```bash
curl http://localhost:8000/models
```

This should now show:
- EasyOCR: `"initialized": true`
- PaddleOCR: `"initialized": true`

## Why This Happened

The API server loads models only once during startup. When you install new libraries while the server is running, it doesn't automatically reload them. You must restart the server for it to:
1. Import the newly installed libraries
2. Initialize the OCR models
3. Make them available for processing

