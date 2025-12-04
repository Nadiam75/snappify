# API Test Commands - Quick Reference

All commands to test your OCR API. Run these in bash/terminal.

## Prerequisites
Make sure your server is running:
```bash
python run_server.py --reload
```

---

## 1. Health Check
```bash
curl http://localhost:8000/health
```

---

## 2. Check Models Status
```bash
curl http://localhost:8000/models
```

Pretty print:
```bash
curl http://localhost:8000/models | python -m json.tool
```

---

## 3. Test OCR - Single Image (All Models)
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

Pretty print:
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" | python -m json.tool
```

---

## 4. Test OCR - Specific Models Only

### EasyOCR only:
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

### PaddleOCR only:
```bash
curl -X POST "http://localhost:8000/ocr?models=PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

### EasyOCR + PaddleOCR:
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

### All models except one:
```bash
curl -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR,TrOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

---

## 5. Test Different Image Files
```bash
# Test with different images
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@2.jpg"

curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@3.png"
```

---

## 6. Batch Processing (Multiple Images)
```bash
curl -X POST "http://localhost:8000/ocr/batch" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@1.jpg" \
  -F "files=@2.jpg" \
  -F "files=@3.jpg"
```

---

## 7. Save Results to File
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" \
  -o result.json
```

View saved result:
```bash
cat result.json | python -m json.tool
```

---

## 8. Quick Test Script
```bash
# Test all endpoints in sequence
echo "1. Health Check:"
curl -s http://localhost:8000/health | python -m json.tool

echo -e "\n2. Models Status:"
curl -s http://localhost:8000/models | python -m json.tool

echo -e "\n3. OCR Test:"
curl -s -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" | python -m json.tool
```

---

## 9. Test with Different Port (if using custom port)
```bash
# If server is on port 8001
curl http://localhost:8001/health
curl -X POST "http://localhost:8001/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

---

## 10. Extract Just the Text from Results
```bash
# Save result first
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" -o result.json

# Extract EasyOCR text
python -c "import json; data=json.load(open('result.json')); print('EasyOCR:', data['models']['EasyOCR'].get('full_text', 'N/A'))"

# Extract PaddleOCR text
python -c "import json; data=json.load(open('result.json')); print('PaddleOCR:', data['models']['PaddleOCR'].get('full_text', 'N/A'))"
```

---

## 11. Check Processing Time
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" | python -c "import sys, json; d=json.load(sys.stdin); print(f\"Processing time: {d.get('processing_time_ms', 'N/A')} ms\")"
```

---

## 12. Test Error Handling

### Invalid file type:
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@somefile.txt"
```

### Invalid model name:
```bash
curl -X POST "http://localhost:8000/ocr?models=InvalidModel" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg"
```

---

## Quick Copy-Paste Test Suite

Run this to test everything at once:

```bash
#!/bin/bash
echo "=== OCR API Test Suite ==="
echo ""
echo "1. Health Check:"
curl -s http://localhost:8000/health | python -m json.tool
echo ""
echo "2. Models Status:"
curl -s http://localhost:8000/models | python -m json.tool
echo ""
echo "3. OCR Test (EasyOCR + PaddleOCR):"
curl -s -X POST "http://localhost:8000/ocr?models=EasyOCR,PaddleOCR" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@1.jpg" | python -m json.tool
```

Save as `test_api.sh`, make executable, and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## Tips

- **Pretty print JSON**: Add `| python -m json.tool` to any curl command
- **Save results**: Add `-o filename.json` to save output
- **Check specific model**: Use `?models=ModelName` parameter
- **View in browser**: Open http://localhost:8000/docs for interactive testing
- **Check server logs**: Look at the terminal where server is running for initialization messages

