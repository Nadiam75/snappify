"""
Quick fix script to check and install missing OCR libraries
"""

import sys
import subprocess

def check_and_install(package_name, import_statement, pip_name=None):
    """Check if package is importable, if not, suggest installation"""
    if pip_name is None:
        pip_name = package_name.lower()
    
    print(f"\nChecking {package_name}...")
    try:
        exec(import_statement)
        print(f"✓ {package_name} is installed and importable")
        return True
    except ImportError as e:
        print(f"✗ {package_name} is NOT importable")
        print(f"  Error: {e}")
        print(f"  Install with: pip install {pip_name}")
        return False
    except Exception as e:
        print(f"✗ {package_name} import failed with unexpected error")
        print(f"  Error: {e}")
        return False

print("=" * 60)
print("OCR Libraries Check and Fix")
print("=" * 60)
print(f"\nPython: {sys.executable}")
print(f"Python version: {sys.version}")

results = {}

# Check EasyOCR
results['EasyOCR'] = check_and_install(
    "EasyOCR",
    "import easyocr",
    "easyocr"
)

# Check PaddleOCR
results['PaddleOCR'] = check_and_install(
    "PaddleOCR",
    "from paddleocr import PaddleOCR",
    "paddleocr"
)

# Check TrOCR
results['TrOCR'] = check_and_install(
    "TrOCR",
    "from transformers import TrOCRProcessor, VisionEncoderDecoderModel",
    "transformers"
)

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

missing = [name for name, status in results.items() if not status]

if missing:
    print(f"\n✗ Missing libraries: {', '.join(missing)}")
    print("\nTo install missing libraries, run:")
    print("  pip install -r requirements.txt")
    print("\nOr install individually:")
    for lib in missing:
        if lib == "EasyOCR":
            print("  pip install easyocr")
        elif lib == "PaddleOCR":
            print("  pip install paddlepaddle paddleocr")
        elif lib == "TrOCR":
            print("  pip install transformers")
else:
    print("\n✓ All libraries are installed and importable!")
    print("\nIf the API still shows 'not initialized', check:")
    print("  1. Make sure you're using the correct virtual environment")
    print("  2. Restart the API server after installing libraries")
    print("  3. Check server logs for initialization errors")

print("\n" + "=" * 60)

