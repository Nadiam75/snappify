#!/bin/bash
# Test all images in dataset folder with EasyOCR

DATASET_DIR="dataset"
OUTPUT_DIR="dataset_results"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Testing all images in $DATASET_DIR with EasyOCR..."
echo ""

# Counter
count=0
success=0
failed=0

# Loop through all image files
for img in "$DATASET_DIR"/*.{jpg,jpeg,png,JPG,JPEG,PNG} 2>/dev/null; do
    if [ -f "$img" ]; then
        count=$((count + 1))
        filename=$(basename "$img")
        output_file="$OUTPUT_DIR/${filename%.*}_easyocr.json"
        
        echo "[$count] Testing: $filename"
        
        # Test with EasyOCR only
        response=$(curl -s -X POST "http://localhost:8000/ocr?models=EasyOCR" \
          -H "accept: application/json" \
          -H "Content-Type: multipart/form-data" \
          -F "file=@$img" \
          -o "$output_file")
        
        # Check if successful
        if grep -q '"success":true' "$output_file" 2>/dev/null; then
            detections=$(python -c "import json; d=json.load(open('$output_file')); print(d['models']['EasyOCR'].get('num_detections', 0))" 2>/dev/null || echo "0")
            echo "  ✓ Success - $detections detections"
            success=$((success + 1))
        else
            echo "  ✗ Failed"
            failed=$((failed + 1))
        fi
    fi
done

echo ""
echo "=========================================="
echo "Summary:"
echo "  Total images: $count"
echo "  Successful: $success"
echo "  Failed: $failed"
echo "  Results saved to: $OUTPUT_DIR/"
echo "=========================================="

