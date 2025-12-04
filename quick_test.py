"""
Quick test script - Run a simple test on a single image
Useful for quick verification that everything is working
"""

import sys
from pathlib import Path
from test_ocr_models import OCRTester


def main():
    """Quick test on a single image"""
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Try to find any image in dataset directory
        dataset_path = Path("dataset")
        image_files = []
        if dataset_path.exists():
            image_files = list(dataset_path.glob("*.jpg")) + list(dataset_path.glob("*.png"))
        if not image_files:
            print("No images found in dataset/ directory. Please provide an image path:")
            print("  python quick_test.py <image_path>")
            print("  or place images in the dataset/ directory")
            return
        image_path = str(image_files[0])
        print(f"Using first found image: {image_path}")
    
    if not Path(image_path).exists():
        print(f"Image not found: {image_path}")
        return
    
    print("="*60)
    print("Quick OCR Test")
    print("="*60)
    print(f"Testing: {image_path}\n")
    
    tester = OCRTester()
    tester.initialize_models()
    
    result = tester.test_all_models(image_path)
    
    # Print summary
    print("\n" + "="*60)
    print("Results Summary")
    print("="*60)
    
    for model_name, model_result in result['models'].items():
        print(f"\n{model_name}:")
        if model_result.get('success'):
            num = model_result.get('num_detections', 0)
            text = model_result.get('full_text', '')
            print(f"  ✓ Success - {num} detections")
            print(f"  Text: {text[:100]}..." if len(text) > 100 else f"  Text: {text}")
        else:
            error = model_result.get('error', 'Unknown')
            print(f"  ✗ Failed: {error}")
    
    # Save result
    output_file = Path("ocr_results") / f"{Path(image_path).stem}_quick_test.json"
    output_file.parent.mkdir(exist_ok=True)
    
    import json
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\nFull results saved to: {output_file}")


if __name__ == "__main__":
    main()

