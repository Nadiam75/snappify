#!/bin/bash
# Test all OCR models and save results

echo "Testing OCR API with all models..."
echo ""

# Test with all models (no models parameter = all models)
# Note: Images are stored in the dataset/ directory
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@dataset/1.jpg" \
  -o all_models_result.json

echo "Result saved to: all_models_result.json"
echo ""
echo "Pretty print result:"
cat all_models_result.json | python -m json.tool

