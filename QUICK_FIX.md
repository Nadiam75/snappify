# Quick Fix: Server Not Detecting Installed Libraries

## The Problem
The server shows libraries as "not installed" even though they are installed.

## The Solution
**You MUST restart the server** after installing libraries. The import checks happen only when the server starts.

---

## Step-by-Step Fix

### 1. Stop the Current Server
In the terminal where the server is running:
- Press `CTRL+C` to stop it

### 2. Verify Libraries Are Installed
```bash
python fix_imports.py
```

You should see:
```
✓ EasyOCR is installed and importable
✓ PaddleOCR is installed and importable
✓ TrOCR is installed and importable
```

### 3. Restart the Server
```bash
python run_server.py --reload
```

### 4. Wait for Initialization Messages
Look for these messages in the console:
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

### 5. Test Again
```bash
curl http://localhost:8000/models
```

Should now show:
```json
[
  {
    "model": "EasyOCR",
    "available": true,
    "initialized": true,
    "error": null
  },
  {
    "model": "PaddleOCR",
    "available": true,
    "initialized": true,
    "error": null
  }
]
```

---

## Why This Happens

Python modules are imported **once** when the server starts. The flags like `EASYOCR_AVAILABLE` are set at import time:

```python
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False  # This stays False until server restarts
```

Even if you install the library later, the running server still has `EASYOCR_AVAILABLE = False`.

---

## Quick Test After Restart

```bash
# Check models
curl http://localhost:8000/models | python -m json.tool

# Test OCR
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" | python -m json.tool
```

---

## Still Not Working?

1. **Check you're in the right environment:**
   ```bash
   which python  # Should show venv path
   python --version
   ```

2. **Reinstall libraries:**
   ```bash
   pip install easyocr paddlepaddle paddleocr transformers
   ```

3. **Check server logs** for initialization errors

4. **Run diagnostic:**
   ```bash
   python check_models.py
   ```

