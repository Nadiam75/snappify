# Dataset Directory Notice

## Important: All Images Are Stored in `dataset/` Directory

All images for testing and processing are stored in the **`dataset/`** directory.

### Directory Structure:
```
hackathon/
├── dataset/          ← All images go here
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.png
│   └── ...
├── dataset_results/  ← Results from dataset testing
├── ocr_results/      ← Results from other tests
└── ...
```

### All Commands Use `dataset/` Path:

**Correct:**
```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@dataset/1.jpg"
```

**Incorrect:**
```bash
curl -X POST "http://localhost:8000/ocr" -F "file=@1.jpg"  # ❌ Wrong - image not in root
```

### Scripts That Use Dataset Directory:

1. **test_dataset_easyocr.py** - Tests all images in `dataset/`
2. **test_api.py** - Looks for images in `dataset/` first
3. **quick_test.py** - Looks for images in `dataset/` first
4. **test_ocr_models.py** - Default `process_images()` uses `dataset/` directory
5. **example_usage.py** - References `dataset/7.jpg`

### Adding New Images:

Place all new test images in the `dataset/` directory:
```bash
# Copy images to dataset directory
cp your_image.jpg dataset/
# or
mv your_image.jpg dataset/
```

### Testing with Images from Dataset:

All test commands and scripts automatically look in or use the `dataset/` directory:
- Python scripts: Check `dataset/` directory first
- curl commands: Use `@dataset/filename.jpg`
- Batch processing: Use `@dataset/image1.jpg`, `@dataset/image2.jpg`, etc.

### Result Files:

- **Dataset test results**: Saved to `dataset_results/` directory
- **Other test results**: Saved to `ocr_results/` directory
- **API test results**: Saved to root directory (e.g., `all_models_result.json`)

---

**Remember**: Always use `dataset/` prefix when referencing images in commands!
