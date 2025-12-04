# Complete List of API Requests Made

**⚠️ Important**: All images are stored in the `dataset/` directory. All commands below use `dataset/` paths.

Based on project files, result files, and test scripts, here are all the API requests that have been made:

## 1. Health Check Requests

### GET /health

```bash
curl http://localhost:8000/health
```

**Purpose**: Check if the API server is running and healthy
**Used in**:

- `test_api.py` - test_health_check()
- `quick_test.sh` - Line 11
- `quick_test.ps1` - Line 11 (PowerShell: Invoke-RestMethod)
- `restart_and_test.sh` - Line 25
- Multiple documentation files

---

## 2. Models Status Requests

### GET /models

```bash
curl http://localhost:8000/models
curl http://localhost:8000/models | python -m json.tool
```

**Purpose**: Check which OCR models are initialized and available
**Used in**:

- `test_api.py` - test_models_status()
- `quick_test.sh` - Line 23
- `quick_test.ps1` - Line 22 (PowerShell: Invoke-RestMethod)
- `restart_and_test.sh` - Line 29
- Troubleshooting and verification scripts

---

## 3. OCR Processing Requests

### 3.1. Single Image - All Models

#### POST /ocr (no model filter)

```bash
# Note: Images are stored in the dataset/ directory
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Process image with all available OCR models
**Result File**: `all_models_result.json` (timestamp: 2025-12-04T10:56:34)
**Used in**:

- `test_api.py` - test_ocr_single_image() with no models parameter
- `quick_test.sh` - Line 40
- `quick_test.ps1` - Line 47
- `test_all_models.sh` - Line 8
- `test_all_models_curl.txt` - Main command

#### With output file:

```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o all_models_result.json
```

---

### 3.2. Single Image - EasyOCR Only

#### POST /ocr?models=EasyOCR

```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Process image with only EasyOCR model
**Result Files**:

- `dataset_results/1_easyocr.json`
- `dataset_results/2_easyocr.json`
- `dataset_results/3_easyocr.json`
- `dataset_results/4_easyocr.json`
- `dataset_results/5_easyocr.json`
- `dataset_results/6_easyocr.json`
- `dataset_results/7_easyocr.json`
- `dataset_results/8_easyocr.json`
- `dataset_results/9_easyocr.json`
  **Used in**:
- `test_dataset_easyocr.py` - Line 59 (18 requests for all dataset images)
- `test_dataset_easyocr.sh` - Line 28
- Dataset testing scripts

**Images Tested** (from dataset_results/summary.json):

1. `3.png` - 102 detections ✓
2. `1.jpg` - 50 detections ✓
3. `2.jpg` - 8 detections ✓
4. `4.jpg` - 63 detections ✓
5. `5.jpg` - 63 detections ✓
6. `6.jpg` - 58 detections ✓
7. `7.jpg` - 55 detections ✓
8. `8.jpg` - 190 detections ✓
9. `9.jpg` - 54 detections ✓
   (Note: Each image was tested twice, total 18 requests)

---

### 3.3. Single Image - EasyOCR + PaddleOCR

#### POST /ocr?models=EasyOCR,PaddleOCR

```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Process image with EasyOCR and PaddleOCR models
**Note**: Images are stored in the `dataset/` directory
**Used in**:

- `test_api.py` - test_ocr_single_image() with models="EasyOCR,PaddleOCR"
- `restart_and_test.sh` - Line 33
- Multiple troubleshooting attempts
- Documentation examples

**Note**: This was used multiple times during troubleshooting when models weren't initializing correctly.

---

### 3.4. Single Image - PaddleOCR Only

#### POST /ocr?models=PaddleOCR

```bash
curl -X POST "http://localhost:8000/ocr?models=PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Test PaddleOCR model individually
**Used in**: Troubleshooting scripts and documentation

---

### 3.5. Single Image - TrOCR Only

#### POST /ocr?models=TrOCR

```bash
curl -X POST "http://localhost:8000/ocr?models=TrOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Test TrOCR model individually
**Used in**: Troubleshooting scripts

---

### 3.6. Single Image - Multiple Models (EasyOCR, PaddleOCR, TrOCR)

#### POST /ocr?models=EasyOCR,PaddleOCR,TrOCR

```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR,TrOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg"
```

**Purpose**: Test multiple models excluding SwinTextSpotter
**Used in**: Documentation and test scripts

---

## 4. Batch Processing Requests

### POST /ocr/batch

```bash
curl -X POST "http://localhost:8000/ocr/batch" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@1.jpg" \
  -F "files=@2.jpg" \
  -F "files=@3.jpg"
```

**Purpose**: Process multiple images in a single request
**Used in**:

- `test_api.py` - test_ocr_batch()
- Documentation examples
- Batch testing scenarios

#### With model filter:

```bash
curl -X POST "http://localhost:8000/ocr/batch?models=EasyOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@dataset/1.jpg" \
  -F "files=@dataset/2.jpg" \
  -F "files=@dataset/3.jpg"
```

---

## Summary of Actual Requests Made

Based on result files and execution:

### Confirmed Executed Requests:

1. **Health Check**: Multiple times (during troubleshooting and testing)
2. **Models Status**: Multiple times (to verify model initialization)
3. **OCR - All Models on dataset/1.jpg**:
   - Result saved in `all_models_result.json`
   - Timestamp: 2025-12-04T10:56:34
   - Models tested: PaddleOCR, TrOCR, SwinTextSpotter, EasyOCR
4. **OCR - EasyOCR Only on Dataset Images**:
   - 18 requests total (9 images × 2 runs)
   - All successful
   - Results saved in `dataset_results/` folder
   - Images from `dataset/`: 1.jpg, 2.jpg, 3.png, 4.jpg, 5.jpg, 6.jpg, 7.jpg, 8.jpg, 9.jpg

### Request Statistics:

- **Total Health Checks**: ~10+ (estimated from troubleshooting)
- **Total Model Status Checks**: ~10+ (estimated from troubleshooting)
- **Total OCR Requests**:
  - All models: 1 (dataset/1.jpg)
  - EasyOCR only: 18 (dataset images)
  - EasyOCR + PaddleOCR: Multiple (troubleshooting)
  - **Total: ~30+ OCR requests**

---

## Request Patterns

### During Initial Setup:

1. Health check to verify server is running
2. Models status to check initialization
3. OCR test with all models
4. Troubleshooting requests when models failed

### During Dataset Testing:

1. Batch EasyOCR requests for all images in dataset folder
2. Results saved individually for each image
3. Summary generated

### During Troubleshooting:

1. Multiple health/model status checks
2. Individual model tests (EasyOCR, PaddleOCR)
3. Combined model tests (EasyOCR + PaddleOCR)
4. Verification after fixes

---

## Files Containing Request Examples

1. **test_api.py** - Python requests library examples
2. **test_dataset_easyocr.py** - Automated dataset testing
3. **quick_test.sh** / **quick_test.ps1** - Quick verification scripts
4. **API_TEST_COMMANDS.md** - Comprehensive command reference
5. **TEST_DATASET_COMMANDS.md** - Dataset-specific commands
6. **test_all_models_curl.txt** - Simple curl command reference

---

## Notes

- All requests were made to `http://localhost:8000`
- Most requests used curl or Python requests library
- Results were saved to JSON files for analysis
- The dataset testing was the most extensive, processing 9 images with EasyOCR
- Troubleshooting phase involved many repeated requests to verify fixes
