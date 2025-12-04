# Snappify OCR Model Testing Framework

This framework allows you to test and compare multiple OCR models for the Snappify project:
- **EasyOCR**: Fast and easy-to-use OCR with multi-language support
- **PaddleOCR**: High-performance OCR with excellent accuracy
- **TrOCR**: Transformer-based OCR from Microsoft
- **SwinTextSpotter**: End-to-end text spotting with Swin Transformer backbone

## Installation

### 1. Basic Setup

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install basic requirements
pip install -r requirements.txt
```

### 2. Model-Specific Setup

#### EasyOCR
EasyOCR will automatically download models on first use. No additional setup needed.

#### PaddleOCR
PaddleOCR will automatically download models on first use. Make sure you have the correct CUDA version if using GPU.

#### TrOCR
TrOCR models will be downloaded automatically from HuggingFace on first use.

#### SwinTextSpotter (Advanced Setup)

SwinTextSpotter requires additional setup:

1. **Clone SwinTextSpotter repository:**
```bash
git clone https://github.com/mxin262/SwinTextSpotter.git
cd SwinTextSpotter
```

2. **Install Detectron2:**
   - For CUDA 11.1 and PyTorch 1.8:
   ```bash
   pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.8/index.html
   ```
   - For other CUDA versions, check [Detectron2 installation guide](https://github.com/facebookresearch/detectron2/blob/main/INSTALL.md)

3. **Install SwinTextSpotter:**
```bash
python setup.py build develop
```

4. **Download Model Weights:**
   - Download from the [SwinTextSpotter repository](https://github.com/mxin262/SwinTextSpotter#models)
   - Place weights in the `SwinTextSpotter` directory or specify path in config

5. **Update paths in `test_ocr_models.py`:**
   - Set `config_path` to your SwinTextSpotter config file
   - Set `weights_path` to your downloaded model weights

## Usage

### Basic Testing

Run all OCR models on images in the dataset directory:

```bash
python test_ocr_models.py
```

This will:
- Process all `.jpg`, `.jpeg`, `.png` images in the `dataset/` directory
- Run all available OCR models on each image
- Save results to `ocr_results/` directory
- Generate JSON files with detailed results

### Compare Results

After running tests, compare results from all models:

```bash
python compare_results.py
```

This will:
- Generate a text comparison report
- Create visualization images showing bounding boxes from each model
- Save outputs to `ocr_results/visualizations/`

### Test Single Image

You can modify `test_ocr_models.py` to test a specific image:

```python
tester = OCRTester()
tester.initialize_models()
result = tester.test_all_models("dataset/image.jpg")  # Images are in dataset/ directory
```

### SwinTextSpotter Only

Test SwinTextSpotter on a specific image:

```bash
python swintextspotter_integration.py --image dataset/7.jpg --config path/to/config.yaml --weights path/to/weights.pth
```

## Output Structure

```
ocr_results/
├── all_results.json              # Combined results from all images
├── comparison_report.txt         # Text comparison report
├── visualizations/               # Visualization images
│   ├── 1_comparison.png
│   ├── 2_comparison.png
│   └── ...
├── 1_results.json                # Results for image 1
├── 2_results.json                # Results for image 2
└── ...
```

## Results Format

Each result JSON contains:
```json
{
  "image_path": "path/to/image.jpg",
  "timestamp": "2024-01-01T12:00:00",
  "models": {
    "EasyOCR": {
      "model": "EasyOCR",
      "success": true,
      "texts": [
        {
          "text": "detected text",
          "confidence": 0.95,
          "bbox": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
      ],
      "full_text": "all detected text",
      "num_detections": 5
    },
    ...
  }
}
```

## Model Comparison

### EasyOCR
- **Pros**: Easy setup, multi-language support, good for general use
- **Cons**: Slower inference, may struggle with complex layouts
- **Best for**: Quick prototyping, multi-language documents

### PaddleOCR
- **Pros**: High accuracy, fast inference, good Chinese/Persian support
- **Cons**: Larger model size
- **Best for**: Production use, Asian languages

### TrOCR
- **Pros**: Transformer-based, good for printed text
- **Cons**: Processes full image as single region (no detection)
- **Best for**: Single text region images, printed documents

### SwinTextSpotter
- **Pros**: End-to-end detection + recognition, state-of-the-art accuracy
- **Cons**: Complex setup, requires GPU, larger model
- **Best for**: High-accuracy requirements, research applications

## Troubleshooting

### CUDA/GPU Issues
- Make sure CUDA version matches PyTorch and Detectron2 requirements
- Check GPU availability: `python -c "import torch; print(torch.cuda.is_available())"`

### SwinTextSpotter Not Working
- Verify Detectron2 installation: `python -c "import detectron2; print(detectron2.__version__)"`
- Check that SwinTextSpotter repository is cloned and in the correct location
- Ensure model weights are downloaded and paths are correct

### Memory Issues
- Process images one at a time for large images
- Reduce image resolution if needed
- Use CPU mode if GPU memory is limited

## Performance Tips

1. **For Persian/Farsi text**: PaddleOCR and EasyOCR both support Persian
2. **For speed**: EasyOCR or PaddleOCR are faster than TrOCR/SwinTextSpotter
3. **For accuracy**: SwinTextSpotter > PaddleOCR > EasyOCR > TrOCR (for full images)
4. **For menu/product images**: PaddleOCR or SwinTextSpotter work best

## License

This testing framework is for the Snappify hackathon project. Individual OCR models have their own licenses:
- EasyOCR: Apache 2.0
- PaddleOCR: Apache 2.0
- TrOCR: MIT
- SwinTextSpotter: Check original repository

## References

- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [TrOCR](https://github.com/microsoft/unilm/tree/master/trocr)
- [SwinTextSpotter](https://github.com/mxin262/SwinTextSpotter)

