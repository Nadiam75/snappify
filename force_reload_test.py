"""
Force reload test to check if modules are being cached
"""

import sys
import importlib

print("=" * 60)
print("Module Import Test")
print("=" * 60)
print(f"Python: {sys.executable}")
print()

# Force reload test_ocr_models
if 'test_ocr_models' in sys.modules:
    print("Reloading test_ocr_models module...")
    importlib.reload(sys.modules['test_ocr_models'])
    import test_ocr_models
else:
    import test_ocr_models

print(f"EASYOCR_AVAILABLE: {test_ocr_models.EASYOCR_AVAILABLE}")
print(f"PADDLEOCR_AVAILABLE: {test_ocr_models.PADDLEOCR_AVAILABLE}")
print(f"TROCR_AVAILABLE: {test_ocr_models.TROCR_AVAILABLE}")

# Try direct imports
print()
print("Direct import test:")
try:
    import easyocr
    print("✓ easyocr imported successfully")
except Exception as e:
    print(f"✗ easyocr failed: {e}")

try:
    from paddleocr import PaddleOCR
    print("✓ paddleocr imported successfully")
except Exception as e:
    print(f"✗ paddleocr failed: {e}")

try:
    from transformers import TrOCRProcessor
    print("✓ transformers imported successfully")
except Exception as e:
    print(f"✗ transformers failed: {e}")

print()
print("=" * 60)
print("If flags are True but server shows False, server needs restart!")
print("=" * 60)

