"""
FastAPI OCR Service
Provides REST API endpoints for OCR processing using multiple models
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the OCR tester
from test_ocr_models import OCRTester

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

# Initialize FastAPI app
app = FastAPI(
    title="OCR API Service",
    description="OCR processing service with multiple model support (EasyOCR, PaddleOCR, TrOCR, SwinTextSpotter)",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global OCR tester instance
ocr_tester: Optional[OCRTester] = None
# Store initialization errors
initialization_errors: dict = {}


class ModelStatus(BaseModel):
    """Model availability status"""

    model: str
    available: bool
    initialized: bool
    error: Optional[str] = None


class OCRResponse(BaseModel):
    """OCR response model"""

    success: bool
    image_name: str
    timestamp: str
    models: dict
    processing_time_ms: Optional[float] = None
    error: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize OCR models on startup"""
    global ocr_tester, initialization_errors
    print("Initializing OCR models...")
    ocr_tester = OCRTester()
    ocr_tester.initialize_models()

    # Capture initialization errors from OCRTester
    initialization_errors = ocr_tester.init_errors.copy()
    initialization_errors["SwinTextSpotter"] = (
        None  # Always available but may fail at runtime
    )

    print("OCR models initialized successfully!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "OCR API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "ocr": "/ocr",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_initialized": ocr_tester is not None,
    }


@app.get("/models", response_model=List[ModelStatus])
async def get_models_status():
    """Get status of all OCR models"""
    if ocr_tester is None:
        raise HTTPException(status_code=503, detail="OCR models not initialized")

    models_status = []

    # Check EasyOCR
    easyocr_initialized = ocr_tester.easyocr_reader is not None
    models_status.append(
        ModelStatus(
            model="EasyOCR",
            available=easyocr_initialized,
            initialized=easyocr_initialized,
            error=(
                initialization_errors.get("EasyOCR")
                if not easyocr_initialized
                else None
            ),
        )
    )

    # Check PaddleOCR
    paddleocr_initialized = ocr_tester.paddleocr_reader is not None
    models_status.append(
        ModelStatus(
            model="PaddleOCR",
            available=paddleocr_initialized,
            initialized=paddleocr_initialized,
            error=(
                initialization_errors.get("PaddleOCR")
                if not paddleocr_initialized
                else None
            ),
        )
    )

    # Check TrOCR
    trocr_initialized = (
        ocr_tester.trocr_processor is not None and ocr_tester.trocr_model is not None
    )
    models_status.append(
        ModelStatus(
            model="TrOCR",
            available=trocr_initialized,
            initialized=trocr_initialized,
            error=initialization_errors.get("TrOCR") if not trocr_initialized else None,
        )
    )

    # Check SwinTextSpotter (always available but may fail at runtime)
    models_status.append(
        ModelStatus(
            model="SwinTextSpotter",
            available=True,  # Available but may fail at runtime
            initialized=True,
            error=None,
        )
    )

    return models_status


@app.post("/ocr", response_model=OCRResponse)
async def process_ocr(
    file: UploadFile = File(...),
    models: Optional[str] = Query(
        None,
        description="Comma-separated list of models to use (EasyOCR, PaddleOCR, TrOCR, SwinTextSpotter). If not specified, all models will be used.",
    ),
):
    """
    Process an image with OCR models

    - **file**: Image file to process (jpg, png, etc.)
    - **models**: Optional comma-separated list of models to use (e.g., "EasyOCR,PaddleOCR")

    Returns OCR results from all specified models.
    """
    if ocr_tester is None:
        raise HTTPException(status_code=503, detail="OCR models not initialized")

    # Validate file type
    allowed_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}",
        )

    # Save uploaded file to temporary location
    import time

    start_time = time.time()

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Parse models parameter
        selected_models = None
        if models:
            selected_models = [m.strip() for m in models.split(",")]
            valid_models = {"EasyOCR", "PaddleOCR", "TrOCR", "SwinTextSpotter"}
            invalid_models = [m for m in selected_models if m not in valid_models]
            if invalid_models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid model names: {', '.join(invalid_models)}. Valid models: {', '.join(valid_models)}",
                )

        # Process with OCR
        if selected_models:
            # Process only selected models
            results = {
                "image_path": file.filename,
                "timestamp": datetime.now().isoformat(),
                "models": {},
            }

            for model_name in selected_models:
                if model_name == "EasyOCR":
                    results["models"]["EasyOCR"] = ocr_tester.test_easyocr(
                        tmp_file_path
                    )
                elif model_name == "PaddleOCR":
                    results["models"]["PaddleOCR"] = ocr_tester.test_paddleocr(
                        tmp_file_path
                    )
                elif model_name == "TrOCR":
                    results["models"]["TrOCR"] = ocr_tester.test_trocr(tmp_file_path)
                elif model_name == "SwinTextSpotter":
                    results["models"]["SwinTextSpotter"] = (
                        ocr_tester.test_swintextspotter(tmp_file_path)
                    )
        else:
            # Process all models
            results = ocr_tester.test_all_models(tmp_file_path)

        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Clean up temporary file
        os.unlink(tmp_file_path)

        return OCRResponse(
            success=True,
            image_name=file.filename,
            timestamp=results["timestamp"],
            models=results["models"],
            processing_time_ms=round(processing_time, 2),
        )

    except HTTPException:
        raise
    except Exception as e:
        # Clean up temporary file if it exists
        if "tmp_file_path" in locals() and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

        return OCRResponse(
            success=False,
            image_name=file.filename,
            timestamp=datetime.now().isoformat(),
            models={},
            error=str(e),
        )


@app.post("/ocr/batch")
async def process_ocr_batch(
    files: List[UploadFile] = File(...),
    models: Optional[str] = Query(
        None, description="Comma-separated list of models to use"
    ),
):
    """
    Process multiple images with OCR models

    - **files**: List of image files to process
    - **models**: Optional comma-separated list of models to use

    Returns OCR results for all images.
    """
    if ocr_tester is None:
        raise HTTPException(status_code=503, detail="OCR models not initialized")

    if len(files) > 10:  # Limit batch size
        raise HTTPException(status_code=400, detail="Maximum 10 files per batch")

    results = []

    for file in files:
        try:
            # Reuse the single OCR endpoint logic
            result = await process_ocr(file, models)
            results.append(result.dict())
        except Exception as e:
            results.append(
                {
                    "success": False,
                    "image_name": file.filename,
                    "timestamp": datetime.now().isoformat(),
                    "models": {},
                    "error": str(e),
                }
            )

    return {"success": True, "total_images": len(files), "results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
