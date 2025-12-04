# Dataset Directory - Important Notice

## ⚠️ All Images Must Be in `dataset/` Directory

All images for testing and processing **must be placed in the `dataset/` directory**.

### Directory Structure:
```
hackathon/
├── dataset/              ← PUT ALL IMAGES HERE
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.png
│   └── ...
├── dataset_results/      ← Results from dataset testing
├── ocr_results/          ← Results from other tests
└── ...
```

### All Commands Use `dataset/`:

**✅ Correct:**
```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg"
```

**❌ Incorrect:**
```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@1.jpg"  # Wrong!
```

### Scripts That Use Dataset:

- ✅ `test_ocr_models.py` - Default processes `dataset/` directory
- ✅ `test_dataset_easyocr.py` - Tests all images in `dataset/`
- ✅ `test_api.py` - Looks in `dataset/` first
- ✅ `quick_test.py` - Looks in `dataset/` first
- ✅ All shell scripts - Use `dataset/` paths

### Adding New Images:

```bash
# Copy your images to dataset directory
cp your_image.jpg dataset/
# or move them
mv your_image.jpg dataset/
```

**Remember**: Always use `dataset/` prefix in all commands and scripts!

