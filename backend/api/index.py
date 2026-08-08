from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from backend.services.gemma_service import analyze_civic_issue


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="CiviSense AI",
    description="AI-powered civic issue monitoring using Gemma 4",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
async def health_check():

    return {
        "status": "ok",
        "service": "CiviSense AI",
        "message": "Backend is running"
    }


# ============================================================
# CIVIC ISSUE ANALYSIS
# ============================================================

@app.post("/api/analyze")
async def analyze_issue(
    image: UploadFile = File(...),
    description: str = Form(""),
    location: str = Form("")
):

    # --------------------------------------------------------
    # Validate image type
    # --------------------------------------------------------

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp"
    }

    if image.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Use JPEG, PNG, or WebP."
            )
        )

    # --------------------------------------------------------
    # Read image
    # --------------------------------------------------------

    try:

        image_bytes = await image.read()

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read uploaded image."
        )

    if not image_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty."
        )

    # --------------------------------------------------------
    # Gemma analysis
    # --------------------------------------------------------

    try:

        analysis = analyze_civic_issue(
            image_bytes=image_bytes,
            mime_type=image.content_type,
            description=description,
            location=location
        )

    except ValueError as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

    except Exception as e:

        print("Unexpected Gemma error:", e)

        raise HTTPException(
            status_code=500,
            detail="Failed to analyze civic issue."
        )

    # --------------------------------------------------------
    # Return structured response
    # --------------------------------------------------------

    return {
        "success": True,
        "filename": image.filename,
        "analysis": analysis.model_dump()
    }