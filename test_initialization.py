"""
Test model initialization exactly like the server does
"""

import sys
from test_ocr_models import OCRTester

print("=" * 60)
print("Testing Model Initialization (Like Server Does)")
print("=" * 60)
print(f"Python: {sys.executable}")
print()

# Create tester and initialize (exactly like server startup)
print("Creating OCRTester...")
tester = OCRTester()

print()
print("Initializing models...")
tester.initialize_models()

print()
print("=" * 60)
print("Initialization Results:")
print("=" * 60)
print(f"EasyOCR reader: {tester.easyocr_reader is not None}")
print(f"PaddleOCR reader: {tester.paddleocr_reader is not None}")
print(f"TrOCR processor: {tester.trocr_processor is not None}")
print(f"TrOCR model: {tester.trocr_model is not None}")

print()
print("Initialization Errors:")
for model, error in tester.init_errors.items():
    if error:
        print(f"  {model}: {error}")
    else:
        print(f"  {model}: OK")

print()
print("=" * 60)
if tester.easyocr_reader and tester.paddleocr_reader:
    print("✓ Models initialized successfully!")
    print("If server still shows errors, the server needs a proper restart.")
else:
    print("✗ Some models failed to initialize")
    print("Check the error messages above")
print("=" * 60)

