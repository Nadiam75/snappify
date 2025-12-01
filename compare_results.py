"""
Compare and visualize OCR results from different models
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
import cv2
import numpy as np
from typing import Dict, List


def load_results(results_file: str = "ocr_results/all_results.json") -> List[Dict]:
    """Load OCR results from JSON file"""
    with open(results_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def visualize_results(image_path: str, results: Dict, output_path: str = None):
    """Visualize OCR results on the image"""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    axes = axes.flatten()
    
    colors = {
        'EasyOCR': 'red',
        'PaddleOCR': 'blue',
        'TrOCR': 'green',
        'SwinTextSpotter': 'purple'
    }
    
    model_idx = 0
    for model_name, model_result in results['models'].items():
        if model_idx >= len(axes):
            break
        
        ax = axes[model_idx]
        ax.imshow(img_rgb)
        ax.set_title(f"{model_name}\n{'Success' if model_result.get('success') else 'Failed'}", 
                     fontsize=14, fontweight='bold')
        ax.axis('off')
        
        if model_result.get('success') and model_result.get('texts'):
            texts = model_result['texts']
            for i, text_item in enumerate(texts):
                bbox = text_item.get('bbox', [])
                text = text_item.get('text', '')
                confidence = text_item.get('confidence', 0)
                
                if bbox:
                    # Handle different bbox formats
                    if isinstance(bbox[0], (list, tuple)):
                        # EasyOCR/PaddleOCR format: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                        bbox_np = np.array(bbox, dtype=np.int32)
                        color = colors.get(model_name, 'black')
                        
                        # Draw bounding box
                        ax.plot([bbox_np[0][0], bbox_np[1][0]], 
                               [bbox_np[0][1], bbox_np[1][1]], 
                               color=color, linewidth=2)
                        ax.plot([bbox_np[1][0], bbox_np[2][0]], 
                               [bbox_np[1][1], bbox_np[2][1]], 
                               color=color, linewidth=2)
                        ax.plot([bbox_np[2][0], bbox_np[3][0]], 
                               [bbox_np[2][1], bbox_np[3][1]], 
                               color=color, linewidth=2)
                        ax.plot([bbox_np[3][0], bbox_np[0][0]], 
                               [bbox_np[3][1], bbox_np[0][1]], 
                               color=color, linewidth=2)
                        
                        # Add text label
                        x_min = min([p[0] for p in bbox])
                        y_min = min([p[1] for p in bbox])
                        ax.text(x_min, y_min - 5, f"{text[:30]}... ({confidence:.2f})", 
                               color=color, fontsize=8, 
                               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        model_idx += 1
    
    # Hide unused subplots
    for idx in range(model_idx, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to {output_path}")
    else:
        plt.show()
    
    plt.close()


def print_comparison_table(results: List[Dict]):
    """Print a comparison table of all results"""
    print("\n" + "="*80)
    print("OCR MODEL COMPARISON")
    print("="*80)
    
    for result in results:
        image_name = Path(result['image_path']).name
        print(f"\n{'='*80}")
        print(f"Image: {image_name}")
        print(f"{'='*80}")
        
        for model_name, model_result in result['models'].items():
            print(f"\n{model_name}:")
            print("-" * 40)
            
            if model_result.get('success'):
                num_detections = model_result.get('num_detections', 0)
                full_text = model_result.get('full_text', '')
                
                print(f"  Status: ✓ Success")
                print(f"  Detections: {num_detections}")
                print(f"  Full Text: {full_text[:200]}..." if len(full_text) > 200 else f"  Full Text: {full_text}")
                
                # Show confidence scores if available
                texts = model_result.get('texts', [])
                if texts and len(texts) > 0:
                    confidences = [t.get('confidence', 0) for t in texts]
                    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                    print(f"  Avg Confidence: {avg_confidence:.3f}")
            else:
                error = model_result.get('error', 'Unknown error')
                print(f"  Status: ✗ Failed")
                print(f"  Error: {error}")


def generate_summary_report(results: List[Dict], output_file: str = "ocr_results/comparison_report.txt"):
    """Generate a text report comparing all models"""
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("OCR MODEL COMPARISON REPORT\n")
        f.write("="*80 + "\n\n")
        
        for result in results:
            image_name = Path(result['image_path']).name
            f.write(f"{'='*80}\n")
            f.write(f"Image: {image_name}\n")
            f.write(f"{'='*80}\n\n")
            
            for model_name, model_result in result['models'].items():
                f.write(f"{model_name}:\n")
                f.write("-" * 40 + "\n")
                
                if model_result.get('success'):
                    num_detections = model_result.get('num_detections', 0)
                    full_text = model_result.get('full_text', '')
                    
                    f.write(f"  Status: ✓ Success\n")
                    f.write(f"  Detections: {num_detections}\n")
                    f.write(f"  Full Text:\n  {full_text}\n\n")
                    
                    texts = model_result.get('texts', [])
                    if texts:
                        f.write(f"  Detected Texts:\n")
                        for i, text_item in enumerate(texts, 1):
                            text = text_item.get('text', '')
                            confidence = text_item.get('confidence', 0)
                            f.write(f"    {i}. {text} (confidence: {confidence:.3f})\n")
                else:
                    error = model_result.get('error', 'Unknown error')
                    f.write(f"  Status: ✗ Failed\n")
                    f.write(f"  Error: {error}\n")
                
                f.write("\n")
    
    print(f"Report saved to {output_path}")


def main():
    """Main function to compare results"""
    results_file = Path("ocr_results/all_results.json")
    
    if not results_file.exists():
        print(f"Results file not found: {results_file}")
        print("Please run test_ocr_models.py first to generate results.")
        return
    
    results = load_results(str(results_file))
    
    # Print comparison table
    print_comparison_table(results)
    
    # Generate text report
    generate_summary_report(results)
    
    # Generate visualizations for each image
    output_dir = Path("ocr_results/visualizations")
    output_dir.mkdir(exist_ok=True)
    
    for result in results:
        image_path = result['image_path']
        if Path(image_path).exists():
            image_name = Path(image_path).stem
            viz_path = output_dir / f"{image_name}_comparison.png"
            visualize_results(image_path, result, str(viz_path))


if __name__ == "__main__":
    main()

