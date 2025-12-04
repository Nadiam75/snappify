# Troubleshooting Guide

## EasyOCR Not Initialized Error

If you're getting "EasyOCR not initialized" error, follow these steps:

### Step 1: Check Model Status

```bash
# Check which models are available
curl http://localhost:8000/models
```

This will show you the status of all models and any initialization errors.

### Step 2: Run Diagnostic Script

```bash
python check_models.py
```

This will check:
- Python version
- PyTorch installation and CUDA availability
- EasyOCR installation and initialization
- Other OCR models

### Step 3: Check Server Logs

When you start the server, look for initialization messages:

```bash
python run_server.py --reload
```

Look for lines like:
```
[OK] EasyOCR initialized successfully
[ERROR] EasyOCR initialization failed: <error message>
```

### Common Issues and Solutions

#### 1. EasyOCR Library Not Installed

**Error:** `Warning: EasyOCR not available`

**Solution:**
```bash
pip install easyocr
```

#### 2. EasyOCR Initialization Fails (Memory/Model Download)

**Error:** `[ERROR] EasyOCR initialization failed: ...`

**Common causes:**
- **Out of memory**: EasyOCR needs significant RAM
- **Model download failed**: First run downloads models (~500MB)
- **CUDA/GPU issues**: If trying to use GPU

**Solutions:**
- Ensure you have at least 4GB free RAM
- Check internet connection (models download on first run)
- Try running with CPU only (GPU is optional)
- Clear EasyOCR cache: Delete `~/.EasyOCR/` folder

#### 3. PyTorch Not Installed

**Error:** `PyTorch not available`

**Solution:**
```bash
pip install torch torchvision
```

#### 4. Missing Dependencies

**Solution:**
```bash
pip install -r requirements.txt
```

#### 5. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
python run_server.py --port 8001
```

### Step 4: Test Individual Models

If EasyOCR fails, try other models:

```bash
# Test with PaddleOCR only
curl -X POST "http://localhost:8000/ocr?models=PaddleOCR" -F "file=@1.jpg"

# Test with TrOCR only
curl -X POST "http://localhost:8000/ocr?models=TrOCR" -F "file=@1.jpg"
```

### Step 5: Reinstall EasyOCR

If EasyOCR keeps failing:

```bash
# Uninstall
pip uninstall easyocr

# Clear cache (Windows)
rmdir /s "%USERPROFILE%\.EasyOCR"

# Clear cache (Linux/Mac)
rm -rf ~/.EasyOCR

# Reinstall
pip install easyocr
```

### Getting More Information

#### Check API Model Status Endpoint

```bash
curl http://localhost:8000/models | python -m json.tool
```

This shows detailed status including error messages for each model.

#### Enable Debug Logging

Start server with debug logging:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --log-level debug --reload
```

#### Check System Resources

```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

### Still Having Issues?

1. **Check the server console output** - initialization errors are printed there
2. **Run the diagnostic script**: `python check_models.py`
3. **Check model status endpoint**: `curl http://localhost:8000/models`
4. **Try initializing models manually**: Run `python test_ocr_models.py` to see detailed errors

### Quick Fixes

**If nothing works, try this minimal setup:**

```bash
# 1. Reinstall everything
pip uninstall easyocr paddleocr transformers -y
pip install easyocr

# 2. Test EasyOCR directly
python -c "import easyocr; reader = easyocr.Reader(['en']); print('OK')"

# 3. If that works, restart the API server
python run_server.py --reload
```

