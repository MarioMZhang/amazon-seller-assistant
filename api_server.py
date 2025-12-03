#!/usr/bin/env python3
"""
FastAPI Server for Amazon Content Generator

Provides REST API endpoints for uploading XLSX files and generating
Amazon product listing content using the single_content_agent.
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.single_content_agent import create_single_content_agent

app = FastAPI(
    title="Amazon Content Generator API",
    description="API for generating optimized Amazon product listings from XLSX files",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Amazon Content Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "POST - Upload XLSX files and generate content",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/generate")
async def generate_content(
    seller_elf: UploadFile = File(..., description="seller_elf.xlsx file"),
    sif: UploadFile = File(..., description="sif.xlsx file"),
    brand_name: str = Form(..., description="Brand name (required)"),
    product_type: str = Form(..., description="Product type (required)"),
    top_n: int = Form(default=50, description="Number of top keywords to use"),
    model: str = Form(default="gemini-2.5-flash-lite", description="Model to use")
):
    """
    Generate Amazon product listing content from uploaded XLSX files.

    Args:
        seller_elf: The seller_elf.xlsx file
        sif: The sif.xlsx file
        brand_name: Brand name for the product
        product_type: Product type/category
        top_n: Number of top keywords to use
        model: AI model to use for generation

    Returns:
        JSON response with generated content
    """
    # Create temporary directory for file uploads
    temp_dir = None

    try:
        # Validate file extensions
        if not seller_elf.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="seller_elf file must be an XLSX file")
        if not sif.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="sif file must be an XLSX file")

        # Validate required text fields
        if not brand_name or not brand_name.strip():
            raise HTTPException(status_code=400, detail="brand_name is required and cannot be empty")
        if not product_type or not product_type.strip():
            raise HTTPException(status_code=400, detail="product_type is required and cannot be empty")

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()

        # Save uploaded files to temporary directory
        seller_elf_path = os.path.join(temp_dir, "seller_elf.xlsx")
        sif_path = os.path.join(temp_dir, "sif.xlsx")

        with open(seller_elf_path, "wb") as f:
            shutil.copyfileobj(seller_elf.file, f)

        with open(sif_path, "wb") as f:
            shutil.copyfileobj(sif.file, f)

        print(f"\n{'='*70}")
        print(f"Processing request:")
        print(f"  Brand: {brand_name}")
        print(f"  Product: {product_type}")
        print(f"  Top Keywords: {top_n}")
        print(f"  Model: {model}")
        print(f"{'='*70}\n")

        # Create agent and generate content
        agent = create_single_content_agent(model=model)

        start_time = datetime.now()
        result = agent.generate_content(
            file_seller_elf=seller_elf_path,
            file_sif=sif_path,
            brand_name=brand_name,
            product_type=product_type,
            top_n=top_n
        )
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Add metadata
        result["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": duration,
            "model": model,
            "parameters": {
                "brand_name": brand_name,
                "product_type": product_type,
                "top_n": top_n
            }
        }

        print(f"\n✓ Content generation completed in {duration:.2f} seconds")
        print(f"  Quality Status: {result.get('quality_check_results', {}).get('overall_status', 'N/A')}\n")

        return JSONResponse(content=result)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up temporary files
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def main():
    """Main function to start the API server."""
    import uvicorn

    print("="*70)
    print("Amazon Content Generator API Server")
    print("="*70)
    print("Starting server on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("="*70)
    print()

    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
