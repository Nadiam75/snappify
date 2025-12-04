"""
Verify libraries and provide restart instructions
"""

import sys
import os

print("=" * 60)
print("Server Restart Verification")
print("=" * 60)
print()

# Check Python
print(f"1. Python Path: {sys.executable}")
print(f"   Python Version: {sys.version.split()[0]}")
print()

# Check if in venv
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("✓ Running in virtual environment")
else:
    print("⚠ NOT in virtual environment - this might be the issue!")
print()

# Check libraries
print("2. Checking libraries:")
try:
    import easyocr
    print("   ✓ EasyOCR installed")
except Exception as e:
    print(f"   ✗ EasyOCR: {e}")

try:
    from paddleocr import PaddleOCR
    print("   ✓ PaddleOCR installed")
except Exception as e:
    print(f"   ✗ PaddleOCR: {e}")

try:
    from transformers import TrOCRProcessor
    print("   ✓ Transformers installed")
except Exception as e:
    print(f"   ✗ Transformers: {e}")
print()

# Check test_ocr_models flags
print("3. Checking test_ocr_models flags:")
import test_ocr_models
print(f"   EASYOCR_AVAILABLE: {test_ocr_models.EASYOCR_AVAILABLE}")
print(f"   PADDLEOCR_AVAILABLE: {test_ocr_models.PADDLEOCR_AVAILABLE}")
print(f"   TROCR_AVAILABLE: {test_ocr_models.TROCR_AVAILABLE}")
print()

# Instructions
print("=" * 60)
print("RESTART INSTRUCTIONS:")
print("=" * 60)
print()
print("1. Find the terminal where the server is running")
print("2. Press CTRL+C to stop it")
print("3. Wait 2-3 seconds")
print("4. Run this command:")
print()
print(f"   {sys.executable} run_server.py --reload")
print()
print("5. Look for these messages:")
print("   [OK] EasyOCR initialized successfully")
print("   [OK] PaddleOCR initialized successfully")
print()
print("6. If you see errors, check the full error message")
print("=" * 60)

