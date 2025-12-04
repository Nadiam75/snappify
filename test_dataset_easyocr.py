"""
Test all images in dataset folder with EasyOCR
"""

import os
import requests
import json
from pathlib import Path
from datetime import datetime

DATASET_DIR = "dataset"
OUTPUT_DIR = "dataset_results"
API_URL = "http://localhost:8000/ocr"


def test_all_images():
    """Test all images in dataset folder with EasyOCR"""

    # Create output directory
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Find all image files
    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".JPG",
        ".JPEG",
        ".PNG",
        ".bmp",
        ".BMP",
    }
    image_files = []

    dataset_path = Path(DATASET_DIR)
    if not dataset_path.exists():
        print(f"Error: {DATASET_DIR} folder not found!")
        return

    for ext in image_extensions:
        image_files.extend(list(dataset_path.glob(f"*{ext}")))

    if not image_files:
        print(f"No images found in {DATASET_DIR} folder!")
        return

    print(f"Found {len(image_files)} images in {DATASET_DIR}")
    print(f"Testing with EasyOCR...")
    print("=" * 60)

    results_summary = {
        "total": len(image_files),
        "successful": 0,
        "failed": 0,
        "results": [],
    }

    for i, img_path in enumerate(image_files, 1):
        filename = img_path.name
        output_file = Path(OUTPUT_DIR) / f"{img_path.stem}_easyocr.json"

        print(f"\n[{i}/{len(image_files)}] Testing: {filename}")

        try:
            # Test with EasyOCR only
            with open(img_path, "rb") as f:
                files = {"file": f}
                params = {"models": "EasyOCR"}
                response = requests.post(API_URL, files=files, params=params)

            result = response.json()

            # Save result
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            if result.get("success"):
                easyocr_result = result.get("models", {}).get("EasyOCR", {})
                if easyocr_result.get("success"):
                    num_detections = easyocr_result.get("num_detections", 0)
                    full_text = easyocr_result.get("full_text", "")[:50]
                    print(f"  ✓ Success - {num_detections} detections")
                    print(f"    Text preview: {full_text}...")
                    results_summary["successful"] += 1
                    results_summary["results"].append(
                        {
                            "image": filename,
                            "status": "success",
                            "detections": num_detections,
                        }
                    )
                else:
                    error = easyocr_result.get("error", "Unknown error")
                    print(f"  ✗ Failed: {error}")
                    results_summary["failed"] += 1
                    results_summary["results"].append(
                        {"image": filename, "status": "failed", "error": error}
                    )
            else:
                error = result.get("error", "Unknown error")
                print(f"  ✗ Failed: {error}")
                results_summary["failed"] += 1
                results_summary["results"].append(
                    {"image": filename, "status": "failed", "error": error}
                )

        except Exception as e:
            print(f"  ✗ Error: {e}")
            results_summary["failed"] += 1
            results_summary["results"].append(
                {"image": filename, "status": "error", "error": str(e)}
            )

    # Save summary
    summary_file = Path(OUTPUT_DIR) / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Total images: {results_summary['total']}")
    print(f"  Successful: {results_summary['successful']}")
    print(f"  Failed: {results_summary['failed']}")
    print(f"  Results saved to: {OUTPUT_DIR}/")
    print(f"  Summary saved to: {summary_file}")
    print("=" * 60)


if __name__ == "__main__":
    test_all_images()
