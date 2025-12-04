"""
Diagnostic script to check OCR model initialization
Run this to see why models might not be initializing
"""

import sys

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

print("=" * 60)
print("OCR Models Diagnostic Check")
print("=" * 60)
print()

# Check Python version
print(f"Python version: {sys.version}")
print()

# Check PyTorch
print("Checking PyTorch...")
try:
    import torch
    print(f"✓ PyTorch installed: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  GPU device: {torch.cuda.get_device_name(0)}")
    else:
        print("  Using CPU")
except ImportError:
    print("✗ PyTorch not installed")
    print("  Install with: pip install torch torchvision")
print()

# Check EasyOCR
print("Checking EasyOCR...")
try:
    import easyocr
    print(f"✓ EasyOCR installed: {easyocr.__version__ if hasattr(easyocr, '__version__') else 'unknown'}")
    
    # Try to initialize
    print("  Attempting to initialize EasyOCR...")
    try:
        use_gpu = torch.cuda.is_available() if 'torch' in sys.modules else False
        reader = easyocr.Reader(["en", "fa"], gpu=use_gpu)
        print("  ✓ EasyOCR initialized successfully!")
    except Exception as e:
        print(f"  ✗ EasyOCR initialization failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print("  Traceback:")
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                print(f"    {line}")
except ImportError:
    print("✗ EasyOCR not installed")
    print("  Install with: pip install easyocr")
except Exception as e:
    print(f"✗ Error checking EasyOCR: {e}")
print()

# Check PaddleOCR
print("Checking PaddleOCR...")
try:
    from paddleocr import PaddleOCR
    print("✓ PaddleOCR installed")
    
    # Try to initialize
    print("  Attempting to initialize PaddleOCR...")
    try:
        use_gpu = torch.cuda.is_available() if 'torch' in sys.modules else False
        ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=use_gpu)
        print("  ✓ PaddleOCR initialized successfully!")
    except Exception as e:
        print(f"  ✗ PaddleOCR initialization failed: {e}")
        print(f"  Error type: {type(e).__name__}")
        import traceback
        print("  Traceback:")
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                print(f"    {line}")
except ImportError:
    print("✗ PaddleOCR not installed")
    print("  Install with: pip install paddlepaddle paddleocr")
except Exception as e:
    print(f"✗ Error checking PaddleOCR: {e}")
print()

# Check TrOCR
print("Checking TrOCR...")
try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    print("✓ Transformers installed")
    
    if 'torch' not in sys.modules:
        print("  ✗ TrOCR requires PyTorch")
    else:
        print("  Attempting to initialize TrOCR...")
        try:
            processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
            model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")
            print("  ✓ TrOCR initialized successfully!")
        except Exception as e:
            print(f"  ✗ TrOCR initialization failed: {e}")
            print(f"  Error type: {type(e).__name__}")
except ImportError:
    print("✗ Transformers not installed")
    print("  Install with: pip install transformers")
except Exception as e:
    print(f"✗ Error checking TrOCR: {e}")
print()

print("=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print()
print("If models are failing to initialize, check:")
print("1. All dependencies are installed: pip install -r requirements.txt")
print("2. You have sufficient RAM/disk space")
print("3. Internet connection (for downloading models)")
print("4. Check server logs when starting the API for detailed error messages")

