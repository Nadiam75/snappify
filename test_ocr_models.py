"""
OCR Model Testing Script for Snappify
Tests EasyOCR, PaddleOCR, TrOCR, and SwinTextSpotter on input images
"""

# Fix PIL.Image compatibility issue for Pillow 10.0+
# This monkey patch fixes the issue where Image.LINEAR doesn't exist in newer Pillow versions
try:
    from PIL import Image

    # If Image.LINEAR doesn't exist, add it for backward compatibility
    if not hasattr(Image, "LINEAR"):
        if hasattr(Image, "Resampling"):
            # Pillow 10.0+ uses different constant names
            Image.LINEAR = Image.Resampling.BILINEAR  # LINEAR was removed, use BILINEAR
            Image.NEAREST = Image.Resampling.NEAREST
            Image.BILINEAR = Image.Resampling.BILINEAR
            Image.BICUBIC = Image.Resampling.BICUBIC
            Image.LANCZOS = Image.Resampling.LANCZOS
except ImportError:
    pass

import os
import sys
import cv2
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        # Fallback for older Python versions
        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

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
        
        # Store initialization errors
        self.init_errors = {}

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
                print("[OK] EasyOCR initialized successfully")
                self.init_errors["EasyOCR"] = None
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] EasyOCR initialization failed: {error_msg}")
                self.easyocr_reader = None
                self.init_errors["EasyOCR"] = error_msg
        else:
            self.init_errors["EasyOCR"] = "EasyOCR library not installed"

        # Initialize PaddleOCR
        if PADDLEOCR_AVAILABLE:
            print("Initializing PaddleOCR...")
            try:
                # Try different parameter combinations for different PaddleOCR versions
                # Newer versions (3.x) don't support use_gpu or use_angle_cls
                try:
                    # Try with use_gpu and use_angle_cls (older versions)
                    use_gpu = TORCH_AVAILABLE and torch.cuda.is_available()
                    self.paddleocr_reader = PaddleOCR(
                        use_angle_cls=True, lang="en", use_gpu=use_gpu
                    )
                except (TypeError, ValueError, Exception) as e:
                    error_str = str(e)
                    # If error mentions use_gpu or use_angle_cls, try without them
                    if "use_gpu" in error_str or "use_angle_cls" in error_str or "Unknown argument" in error_str:
                        # Try with just lang parameter (newer versions)
                        self.paddleocr_reader = PaddleOCR(lang="en")
                    else:
                        # Re-raise if it's a different error
                        raise
                print("[OK] PaddleOCR initialized successfully")
                self.init_errors["PaddleOCR"] = None
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] PaddleOCR initialization failed: {error_msg}")
                self.paddleocr_reader = None
                self.init_errors["PaddleOCR"] = error_msg
        else:
            self.init_errors["PaddleOCR"] = "PaddleOCR library not installed"

        # Initialize TrOCR
        if TROCR_AVAILABLE:
            print("Initializing TrOCR...")
            try:
                if not TORCH_AVAILABLE or self.device is None:
                    error_msg = "TrOCR requires PyTorch"
                    print(f"✗ {error_msg}")
                    self.trocr_processor = None
                    self.trocr_model = None
                    self.init_errors["TrOCR"] = error_msg
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
                    print("[OK] TrOCR initialized successfully")
                    self.init_errors["TrOCR"] = None
            except Exception as e:
                error_msg = str(e)
                print(f"[ERROR] TrOCR initialization failed: {error_msg}")
                self.trocr_processor = None
                self.trocr_model = None
                self.init_errors["TrOCR"] = error_msg
        else:
            self.init_errors["TrOCR"] = "TrOCR library not installed"

        print("=" * 50 + "\n")

    def test_easyocr(self, image_path: str) -> Dict:
        """Test EasyOCR on an image"""
        if not self.easyocr_reader:
            return {
                "model": "EasyOCR",
                "success": False,
                "error": "EasyOCR not initialized",
            }

        try:
            results = self.easyocr_reader.readtext(image_path)

            extracted_texts = []
            for bbox, text, confidence in results:
                # Convert numpy types to native Python types for JSON serialization
                bbox_list = [[float(x), float(y)] for x, y in bbox]
                extracted_texts.append(
                    {"text": text, "confidence": float(confidence), "bbox": bbox_list}
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
            return {
                "model": "PaddleOCR",
                "success": False,
                "error": "PaddleOCR not initialized",
            }

        try:
            # Try with cls parameter first (older versions), fallback without it (newer versions)
            try:
                results = self.paddleocr_reader.ocr(image_path, cls=True)
            except (TypeError, ValueError) as e:
                # Newer versions don't support cls parameter
                if "cls" in str(e) or "Unknown argument" in str(e):
                    results = self.paddleocr_reader.ocr(image_path)
                else:
                    raise

            extracted_texts = []
            if results and len(results) > 0:
                result = results[0]
                
                # Check if it's the new format (dict with rec_texts, rec_scores, rec_polys)
                if isinstance(result, dict) and 'rec_texts' in result:
                    # New PaddleOCR 3.x format
                    rec_texts = result.get('rec_texts', [])
                    rec_scores = result.get('rec_scores', [])
                    rec_polys = result.get('rec_polys', [])
                    
                    for i, text in enumerate(rec_texts):
                        if text and text.strip():  # Skip empty texts
                            confidence = rec_scores[i] if i < len(rec_scores) else 0.0
                            bbox = rec_polys[i] if i < len(rec_polys) else []
                            
                            # Convert bbox to list format
                            if hasattr(bbox, 'tolist'):
                                bbox_list = bbox.tolist()
                            elif isinstance(bbox, (list, tuple)):
                                bbox_list = [[float(x), float(y)] for x, y in bbox] if len(bbox) > 0 and isinstance(bbox[0], (list, tuple)) else bbox
                            else:
                                bbox_list = []
                            
                            extracted_texts.append({
                                "text": str(text),
                                "confidence": float(confidence),
                                "bbox": bbox_list,
                            })
                else:
                    # Old PaddleOCR format: list of [bbox, (text, confidence)]
                    for line in result if isinstance(result, list) else []:
                        if isinstance(line, list) and len(line) >= 2:
                            bbox = line[0]
                            text_data = line[1]
                            
                            if isinstance(text_data, tuple) and len(text_data) >= 2:
                                text, confidence = text_data[0], text_data[1]
                            else:
                                text, confidence = text_data, 0.0
                            
                            # Convert numpy types to native Python types for JSON serialization
                            bbox_list = (
                                [[float(x), float(y)] for x, y in bbox]
                                if isinstance(bbox[0], (list, tuple))
                                else bbox
                            )
                            extracted_texts.append({
                                "text": str(text),
                                "confidence": float(confidence),
                                "bbox": bbox_list,
                            })

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
            return {
                "model": "TrOCR",
                "success": False,
                "error": "TrOCR not initialized",
            }

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

        # Test all models - always attempt all models (they handle errors internally)
        # Order: PaddleOCR, TrOCR, SwinTextSpotter, EasyOCR
        print("Running PaddleOCR...")
        results["models"]["PaddleOCR"] = self.test_paddleocr(image_path)

        print("Running TrOCR...")
        results["models"]["TrOCR"] = self.test_trocr(image_path)

        print("Running SwinTextSpotter...")
        results["models"]["SwinTextSpotter"] = self.test_swintextspotter(image_path)

        print("Running EasyOCR...")
        results["models"]["EasyOCR"] = self.test_easyocr(image_path)

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

        # Remove duplicates (case-insensitive matching)
        seen = set()
        unique_files = []
        for img_path in image_files:
            key = str(img_path).lower()
            if key not in seen:
                seen.add(key)
                unique_files.append(img_path)

        image_files = unique_files

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
