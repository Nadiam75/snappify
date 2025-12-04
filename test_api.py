"""
Simple test script for the OCR API
Run this after starting the API server to test the endpoints
"""

import requests
import json
from pathlib import Path


def test_health_check(base_url="http://localhost:8000"):
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{base_url}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_models_status(base_url="http://localhost:8000"):
    """Test models status endpoint"""
    print("Testing models status...")
    response = requests.get(f"{base_url}/models")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_ocr_single_image(image_path, base_url="http://localhost:8000", models=None):
    """Test single image OCR endpoint"""
    print(f"Testing OCR on: {image_path}")
    
    url = f"{base_url}/ocr"
    if models:
        url += f"?models={models}"
    
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"✓ Success! Processing time: {result.get('processing_time_ms', 'N/A')} ms")
        print(f"Models used: {list(result.get('models', {}).keys())}")
        
        # Print summary for each model
        for model_name, model_result in result.get("models", {}).items():
            if model_result.get("success"):
                num_detections = model_result.get("num_detections", 0)
                full_text = model_result.get("full_text", "")[:100]
                print(f"  {model_name}: {num_detections} detections - {full_text}...")
            else:
                error = model_result.get("error", "Unknown error")
                print(f"  {model_name}: Failed - {error}")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    
    print()
    return result


def test_ocr_batch(image_paths, base_url="http://localhost:8000", models=None):
    """Test batch OCR endpoint"""
    print(f"Testing batch OCR on {len(image_paths)} images...")
    
    url = f"{base_url}/ocr/batch"
    if models:
        url += f"?models={models}"
    
    files = []
    for img_path in image_paths:
        files.append(("files", open(img_path, "rb")))
    
    response = requests.post(url, files=files)
    
    # Close file handles
    for _, f in files:
        f.close()
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    if result.get("success"):
        print(f"✓ Success! Processed {result.get('total_images', 0)} images")
        for i, img_result in enumerate(result.get("results", [])):
            print(f"  Image {i+1} ({img_result.get('image_name', 'unknown')}): "
                  f"{'Success' if img_result.get('success') else 'Failed'}")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    
    print()
    return result


def main():
    """Main test function"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("OCR API Test Suite")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    try:
        test_health_check(base_url)
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        print("Make sure the API server is running!")
        return
    
    # Test 2: Models status
    try:
        test_models_status(base_url)
    except Exception as e:
        print(f"✗ Models status check failed: {e}")
        return
    
    # Test 3: Single image OCR
    # Find any image in current directory
    image_files = list(Path(".").glob("*.jpg")) + list(Path(".").glob("*.png"))
    if image_files:
        test_image = str(image_files[0])
        try:
            # Test with all models
            test_ocr_single_image(test_image, base_url)
            
            # Test with specific models
            test_ocr_single_image(test_image, base_url, models="EasyOCR,PaddleOCR")
        except Exception as e:
            print(f"✗ Single image OCR test failed: {e}")
    else:
        print("No images found for testing. Skipping OCR tests.")
    
    print("=" * 60)
    print("Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

