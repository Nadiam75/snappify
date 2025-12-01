"""
OCR Model Testing Script for Snappify
Tests EasyOCR, PaddleOCR, TrOCR, and SwinTextSpotter on input images
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings("ignore")

# Import torch (required for device detection)
try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: PyTorch not available. Some features may not work.")

# Try importing all OCR libraries
try:
    import easyocr

    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("Warning: EasyOCR not available")

try:
    from paddleocr import PaddleOCR

    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    print("Warning: PaddleOCR not available")

try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    import torch

    TROCR_AVAILABLE = True
except ImportError:
    TROCR_AVAILABLE = False
    print("Warning: TrOCR not available")

try:
    # Try to import SwinTextSpotter integration
    from swintextspotter_integration import (
        test_swintextspotter,
        setup_swintextspotter_path,
    )

    SWINTEXTSPOTTER_AVAILABLE = setup_swintextspotter_path()
except ImportError:
    SWINTEXTSPOTTER_AVAILABLE = False
    print("Warning: SwinTextSpotter requires separate setup (see README)")


class OCRTester:
    """Main class for testing different OCR models"""

    def __init__(self, output_dir: str = "ocr_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize models
        self.easyocr_reader = None
        self.paddleocr_reader = None
        self.trocr_processor = None
        self.trocr_model = None

        # Set device (default to CPU if torch not available)
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = None

        if self.device:
            print(f"Using device: {self.device}")
        else:
            print("Using CPU (PyTorch not available)")

    def initialize_models(self):
        """Initialize all available OCR models"""
        print("\n" + "=" * 50)
        print("Initializing OCR Models...")
        print("=" * 50)

        # Initialize EasyOCR
        if EASYOCR_AVAILABLE:
            print("Initializing EasyOCR...")
            try:
                use_gpu = TORCH_AVAILABLE and torch.cuda.is_available()
                self.easyocr_reader = easyocr.Reader(["en", "fa"], gpu=use_gpu)
                print("✓ EasyOCR initialized successfully")
            except Exception as e:
                print(f"✗ EasyOCR initialization failed: {e}")
                self.easyocr_reader = None

        # Initialize PaddleOCR
        if PADDLEOCR_AVAILABLE:
            print("Initializing PaddleOCR...")
            try:
                use_gpu = TORCH_AVAILABLE and torch.cuda.is_available()
                self.paddleocr_reader = PaddleOCR(
                    use_angle_cls=True, lang="en", use_gpu=use_gpu
                )
                print("✓ PaddleOCR initialized successfully")
            except Exception as e:
                print(f"✗ PaddleOCR initialization failed: {e}")
                self.paddleocr_reader = None

        # Initialize TrOCR
        if TROCR_AVAILABLE:
            print("Initializing TrOCR...")
            try:
                if not TORCH_AVAILABLE or self.device is None:
                    print("✗ TrOCR requires PyTorch")
                    self.trocr_processor = None
                    self.trocr_model = None
                else:
                    processor_name = "microsoft/trocr-base-printed"
                    model_name = "microsoft/trocr-base-printed"

                    self.trocr_processor = TrOCRProcessor.from_pretrained(
                        processor_name
                    )
                    self.trocr_model = VisionEncoderDecoderModel.from_pretrained(
                        model_name
                    )
                    self.trocr_model.to(self.device)
                    self.trocr_model.eval()
                    print("✓ TrOCR initialized successfully")
            except Exception as e:
                print(f"✗ TrOCR initialization failed: {e}")
                self.trocr_processor = None
                self.trocr_model = None

        print("=" * 50 + "\n")

    def test_easyocr(self, image_path: str) -> Dict:
        """Test EasyOCR on an image"""
        if not self.easyocr_reader:
            return {"error": "EasyOCR not initialized"}

        try:
            results = self.easyocr_reader.readtext(image_path)

            extracted_texts = []
            for bbox, text, confidence in results:
                extracted_texts.append(
                    {"text": text, "confidence": float(confidence), "bbox": bbox}
                )

            return {
                "model": "EasyOCR",
                "success": True,
                "texts": extracted_texts,
                "full_text": " ".join([item["text"] for item in extracted_texts]),
                "num_detections": len(extracted_texts),
            }
        except Exception as e:
            return {"model": "EasyOCR", "success": False, "error": str(e)}

    def test_paddleocr(self, image_path: str) -> Dict:
        """Test PaddleOCR on an image"""
        if not self.paddleocr_reader:
            return {"error": "PaddleOCR not initialized"}

        try:
            results = self.paddleocr_reader.ocr(image_path, cls=True)

            extracted_texts = []
            if results and results[0]:
                for line in results[0]:
                    bbox, (text, confidence) = line
                    extracted_texts.append(
                        {"text": text, "confidence": float(confidence), "bbox": bbox}
                    )

            return {
                "model": "PaddleOCR",
                "success": True,
                "texts": extracted_texts,
                "full_text": " ".join([item["text"] for item in extracted_texts]),
                "num_detections": len(extracted_texts),
            }
        except Exception as e:
            return {"model": "PaddleOCR", "success": False, "error": str(e)}

    def test_trocr(self, image_path: str) -> Dict:
        """Test TrOCR on an image"""
        if not self.trocr_processor or not self.trocr_model:
            return {"error": "TrOCR not initialized"}

        try:
            if not TORCH_AVAILABLE or self.device is None:
                return {
                    "model": "TrOCR",
                    "success": False,
                    "error": "PyTorch not available. TrOCR requires PyTorch.",
                }

            from PIL import Image

            image = Image.open(image_path).convert("RGB")

            # TrOCR works best on cropped text regions
            # For full image, we'll use the entire image
            pixel_values = self.trocr_processor(image, return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)

            with torch.no_grad():
                generated_ids = self.trocr_model.generate(pixel_values)
                generated_text = self.trocr_processor.batch_decode(
                    generated_ids, skip_special_tokens=True
                )[0]

            return {
                "model": "TrOCR",
                "success": True,
                "texts": [{"text": generated_text, "confidence": 1.0}],
                "full_text": generated_text,
                "num_detections": 1,
                "note": "TrOCR processes full image as single text region",
            }
        except Exception as e:
            return {"model": "TrOCR", "success": False, "error": str(e)}

    def test_swintextspotter(
        self, image_path: str, config_path: str = None, weights_path: str = None
    ) -> Dict:
        """Test SwinTextSpotter on an image"""
        try:
            from swintextspotter_integration import test_swintextspotter

            return test_swintextspotter(image_path, config_path, weights_path)
        except ImportError:
            return {
                "model": "SwinTextSpotter",
                "success": False,
                "error": "SwinTextSpotter requires separate setup. See README for installation instructions.",
                "note": "SwinTextSpotter needs detectron2 and model weights. Check SwinTextSpotter repository for setup.",
            }

    def test_all_models(self, image_path: str) -> Dict:
        """Test all available models on a single image"""
        print(f"\nTesting image: {image_path}")
        print("-" * 50)

        results = {
            "image_path": str(image_path),
            "timestamp": datetime.now().isoformat(),
            "models": {},
        }

        # Test each model
        if EASYOCR_AVAILABLE and self.easyocr_reader:
            print("Running EasyOCR...")
            results["models"]["EasyOCR"] = self.test_easyocr(image_path)

        if PADDLEOCR_AVAILABLE and self.paddleocr_reader:
            print("Running PaddleOCR...")
            results["models"]["PaddleOCR"] = self.test_paddleocr(image_path)

        if TROCR_AVAILABLE and self.trocr_processor:
            print("Running TrOCR...")
            results["models"]["TrOCR"] = self.test_trocr(image_path)

        if SWINTEXTSPOTTER_AVAILABLE:
            print("Running SwinTextSpotter...")
            results["models"]["SwinTextSpotter"] = self.test_swintextspotter(image_path)
        else:
            results["models"]["SwinTextSpotter"] = self.test_swintextspotter(image_path)

        return results

    def process_images(
        self,
        image_dir: str = ".",
        extensions: List[str] = [".jpg", ".jpeg", ".png", ".JPG", ".PNG"],
    ):
        """Process all images in a directory"""
        image_dir = Path(image_dir)
        image_files = []

        for ext in extensions:
            image_files.extend(list(image_dir.glob(f"*{ext}")))

        if not image_files:
            print(f"No images found in {image_dir}")
            return

        print(f"\nFound {len(image_files)} images to process")

        all_results = []
        for img_path in sorted(image_files):
            results = self.test_all_models(str(img_path))
            all_results.append(results)

            # Save individual results
            output_file = self.output_dir / f"{img_path.stem}_results.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"Results saved to {output_file}")

        # Save combined results
        combined_file = self.output_dir / "all_results.json"
        with open(combined_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)

        print(f"\nAll results saved to {combined_file}")
        return all_results


def main():
    """Main function to run OCR tests"""
    print("=" * 60)
    print("Snappify OCR Model Testing Framework")
    print("=" * 60)

    tester = OCRTester()
    tester.initialize_models()

    # Process all images in current directory
    results = tester.process_images()

    # Print summary
    print("\n" + "=" * 60)
    print("Testing Summary")
    print("=" * 60)

    if results:
        for result in results:
            print(f"\nImage: {Path(result['image_path']).name}")
            for model_name, model_result in result["models"].items():
                if model_result.get("success"):
                    num_detections = model_result.get("num_detections", 0)
                    print(f"  {model_name}: {num_detections} detections")
                else:
                    error = model_result.get("error", "Unknown error")
                    print(f"  {model_name}: Failed - {error}")


if __name__ == "__main__":
    main()
