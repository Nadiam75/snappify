# Test All Models - Curl Commands

## Test All Models and Save Output

### Basic Command (Save to file)

```bash
# Note: Images are stored in the dataset/ directory
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o all_models_result.json
```

### With Pretty Print

```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" | python -m json.tool > all_models_result.json
```

### Test Multiple Images

```bash
# Test image 1
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o result_1.json

# Test image 2
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/2.jpg" \
  -o result_2.json

# Test image 3
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/3.png" \
  -o result_3.json
```

### Test All Images in Dataset Directory

```bash
for img in dataset/*.jpg dataset/*.png; do
  if [ -f "$img" ]; then
    filename=$(basename "$img")
    echo "Testing $filename..."
    curl -X POST "http://localhost:8000/ocr" \
      -H "accept: application/json" \
      -H "Content-Type: multipart/form-data" \
      -F "file=@$img" \
      -o "result_${filename%.*}.json"
  fi
done
```

### View Saved Results

```bash
# View result
cat all_models_result.json | python -m json.tool

# Or on Windows PowerShell
Get-Content all_models_result.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Extract Specific Information

```bash
# Extract processing time
python -c "import json; d=json.load(open('all_models_result.json')); print(f\"Processing time: {d.get('processing_time_ms', 'N/A')} ms\")"

# Extract text from each model
python -c "import json; d=json.load(open('all_models_result.json')); [print(f\"{m}: {d['models'][m].get('full_text', 'N/A')[:100]}\") for m in d['models'] if d['models'][m].get('success')]"
```
