"""
Example usage of the OCR testing framework
"""

from test_ocr_models import OCRTester
from pathlib import Path

# Example 1: Test a single image
def example_single_image():
    print("Example 1: Testing a single image")
    print("-" * 50)
    
    tester = OCRTester()
    tester.initialize_models()
    
    # Test on image 7.jpg
    result = tester.test_all_models("7.jpg")
    
    # Access results
    for model_name, model_result in result['models'].items():
        if model_result.get('success'):
            print(f"{model_name}: Found {model_result['num_detections']} text regions")
            print(f"  Full text: {model_result['full_text'][:100]}...")
        else:
            print(f"{model_name}: Failed - {model_result.get('error')}")


# Example 2: Test all images in directory
def example_batch_processing():
    print("\nExample 2: Batch processing all images")
    print("-" * 50)
    
    tester = OCRTester()
    tester.initialize_models()
    
    # Process all images
    results = tester.process_images()
    
    print(f"\nProcessed {len(results)} images")
    print("Results saved to ocr_results/")


# Example 3: Compare specific models
def example_model_comparison():
    print("\nExample 3: Comparing EasyOCR vs PaddleOCR")
    print("-" * 50)
    
    tester = OCRTester()
    tester.initialize_models()
    
    image_path = "7.jpg"
    
    # Test only EasyOCR and PaddleOCR
    easyocr_result = tester.test_easyocr(image_path)
    paddleocr_result = tester.test_paddleocr(image_path)
    
    print(f"\nEasyOCR: {easyocr_result.get('num_detections', 0)} detections")
    print(f"PaddleOCR: {paddleocr_result.get('num_detections', 0)} detections")
    
    # Compare texts
    easyocr_texts = set(easyocr_result.get('full_text', '').lower().split())
    paddleocr_texts = set(paddleocr_result.get('full_text', '').lower().split())
    
    common = easyocr_texts & paddleocr_texts
    print(f"\nCommon words: {len(common)}")
    print(f"EasyOCR unique: {len(easyocr_texts - paddleocr_texts)}")
    print(f"PaddleOCR unique: {len(paddleocr_texts - easyocr_texts)}")


# Example 4: Extract structured data (e.g., menu items)
def example_extract_menu_items():
    print("\nExample 4: Extracting menu items from OCR results")
    print("-" * 50)
    
    tester = OCRTester()
    tester.initialize_models()
    
    result = tester.test_all_models("7.jpg")
    
    # Use PaddleOCR results (usually best for structured text)
    if 'PaddleOCR' in result['models']:
        paddle_result = result['models']['PaddleOCR']
        if paddle_result.get('success'):
            texts = paddle_result.get('texts', [])
            
            print("Detected menu items:")
            for i, text_item in enumerate(texts, 1):
                text = text_item.get('text', '')
                confidence = text_item.get('confidence', 0)
                print(f"  {i}. {text} (confidence: {confidence:.2f})")


if __name__ == "__main__":
    # Run examples
    if Path("7.jpg").exists():
        example_single_image()
        example_model_comparison()
        example_extract_menu_items()
    else:
        print("Image 7.jpg not found. Please run examples with your own images.")
    
    # Uncomment to run batch processing
    # example_batch_processing()

