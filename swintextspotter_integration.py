"""
SwinTextSpotter Integration Script
This script provides integration with SwinTextSpotter for OCR testing.

Note: SwinTextSpotter requires:
1. Detectron2 installation (CUDA-specific)
2. SwinTextSpotter repository cloned
3. Model weights downloaded
4. Proper environment setup

See README.md for detailed setup instructions.
"""

import os
import sys
from pathlib import Path
import cv2
import json
from typing import Dict, Optional


def setup_swintextspotter_path():
    """Add SwinTextSpotter to Python path if it exists"""
    swintextspotter_path = Path("SwinTextSpotter")
    
    if swintextspotter_path.exists():
        sys.path.insert(0, str(swintextspotter_path))
        return True
    return False


def test_swintextspotter(image_path: str, config_path: str = None, weights_path: str = None) -> Dict:
    """
    Test SwinTextSpotter on an image
    
    Args:
        image_path: Path to input image
        config_path: Path to SwinTextSpotter config file
        weights_path: Path to model weights
    
    Returns:
        Dictionary with results
    """
    if not setup_swintextspotter_path():
        return {
            "model": "SwinTextSpotter",
            "success": False,
            "error": "SwinTextSpotter repository not found. Please clone it first.",
            "setup_instructions": [
                "1. Clone SwinTextSpotter: git clone https://github.com/mxin262/SwinTextSpotter.git",
                "2. Install detectron2 (see README)",
                "3. Download model weights",
                "4. Run: python setup.py build develop (in SwinTextSpotter directory)"
            ]
        }
    
    try:
        # Try to import SwinTextSpotter modules
        from detectron2.engine import DefaultPredictor
        from detectron2.config import get_cfg
        from detectron2.utils.visualizer import Visualizer
        from detectron2.data import MetadataCatalog
        
        # Default config path if not provided
        if config_path is None:
            config_path = "SwinTextSpotter/projects/SWINTS/configs/SWINTS-swin-finetune-totaltext.yaml"
        
        if not Path(config_path).exists():
            return {
                "model": "SwinTextSpotter",
                "success": False,
                "error": f"Config file not found: {config_path}",
                "note": "Please download config files from SwinTextSpotter repository"
            }
        
        # Load config
        cfg = get_cfg()
        cfg.merge_from_file(config_path)
        
        if weights_path:
            cfg.MODEL.WEIGHTS = weights_path
        elif not cfg.MODEL.WEIGHTS:
            return {
                "model": "SwinTextSpotter",
                "success": False,
                "error": "Model weights not specified",
                "note": "Please download model weights and specify path"
            }
        
        # Create predictor
        predictor = DefaultPredictor(cfg)
        
        # Read and process image
        image = cv2.imread(image_path)
        if image is None:
            return {
                "model": "SwinTextSpotter",
                "success": False,
                "error": f"Could not load image: {image_path}"
            }
        
        # Run prediction
        outputs = predictor(image)
        
        # Extract text detections and recognitions
        instances = outputs["instances"]
        
        texts = []
        if hasattr(instances, 'pred_boxes') and hasattr(instances, 'rec_texts'):
            boxes = instances.pred_boxes.tensor.cpu().numpy()
            rec_texts = instances.rec_texts if hasattr(instances, 'rec_texts') else []
            scores = instances.scores.cpu().numpy() if hasattr(instances, 'scores') else []
            
            for i, (box, text) in enumerate(zip(boxes, rec_texts)):
                x1, y1, x2, y2 = box
                bbox = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                confidence = float(scores[i]) if len(scores) > i else 1.0
                
                texts.append({
                    "text": text,
                    "confidence": confidence,
                    "bbox": bbox
                })
        
        return {
            "model": "SwinTextSpotter",
            "success": True,
            "texts": texts,
            "full_text": " ".join([t["text"] for t in texts]),
            "num_detections": len(texts)
        }
        
    except ImportError as e:
        return {
            "model": "SwinTextSpotter",
            "success": False,
            "error": f"Import error: {str(e)}",
            "setup_instructions": [
                "1. Install detectron2: pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.8/index.html",
                "2. Make sure SwinTextSpotter is properly installed",
                "3. Check CUDA version compatibility"
            ]
        }
    except Exception as e:
        return {
            "model": "SwinTextSpotter",
            "success": False,
            "error": str(e)
        }


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test SwinTextSpotter on an image")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--weights", type=str, help="Path to model weights")
    
    args = parser.parse_args()
    
    result = test_swintextspotter(args.image, args.config, args.weights)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

