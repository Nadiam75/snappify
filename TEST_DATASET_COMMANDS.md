# Test All Images in Dataset Folder with EasyOCR

## Option 1: Python Script (Recommended)

```bash
python test_dataset_easyocr.py
```

This will:

- Find all images in the `dataset/` folder
- Test each with EasyOCR
- Save individual results to `dataset_results/`
- Create a summary file

## Option 2: Bash Script (Linux/Mac/Git Bash)

```bash
chmod +x test_dataset_easyocr.sh
./test_dataset_easyocr.sh
```

## Option 3: Manual Loop with curl

### Linux/Mac/Git Bash:

```bash
mkdir -p dataset_results
for img in dataset/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
  if [ -f "$img" ]; then
    filename=$(basename "$img")
    echo "Testing: $filename"
    curl -X POST "http://localhost:8000/ocr?models=EasyOCR" \
      -H "accept: application/json" \
      -H "Content-Type: multipart/form-data" \
      -F "file=@$img" \
      -o "dataset_results/${filename%.*}_easyocr.json"
  fi
done
```

### Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path dataset_results
Get-ChildItem -Path dataset -Include *.jpg,*.jpeg,*.png,*.JPG,*.JPEG,*.PNG -Recurse | ForEach-Object {
    $filename = $_.BaseName
    Write-Host "Testing: $($_.Name)"
    curl.exe -X POST "http://localhost:8000/ocr?models=EasyOCR" `
      -H "accept: application/json" `
      -H "Content-Type: multipart/form-data" `
      -F "file=@$($_.FullName)" `
      -o "dataset_results/${filename}_easyocr.json"
}
```

## Option 4: Single Command (One Image at a Time)

```bash
# Test specific image
curl -X POST "http://localhost:8000/ocr?models=EasyOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o dataset_results/1_easyocr.json
```

## View Results

```bash
# View summary
cat dataset_results/summary.json | python -m json.tool

# View specific result
cat dataset_results/image1_easyocr.json | python -m json.tool

# Count successful tests
python -c "import json; d=json.load(open('dataset_results/summary.json')); print(f\"Successful: {d['successful']}/{d['total']}\")"
```

## Batch Test with All Models

To test with all models (not just EasyOCR), remove `?models=EasyOCR`:

```bash
python test_dataset_easyocr.py
# Then edit the script to change models parameter
```

Or use the batch endpoint:

```bash
# Test multiple images at once (up to 10)
curl -X POST "http://localhost:8000/ocr/batch?models=EasyOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@dataset/1.jpg" \
  -F "files=@dataset/2.jpg" \
  -F "files=@dataset/3.jpg"
```
