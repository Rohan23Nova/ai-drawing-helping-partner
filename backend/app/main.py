from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.app.services.image_service import (
    read_image,
    validate_image_extension,
)


app = FastAPI(
    title="AI Drawing Helping Partner",
    description="An AI-powered drawing assistance API.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Drawing Helping Partner API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    if not validate_image_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format.",
        )

    image_bytes = await file.read()

    try:
        image = read_image(image_bytes)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    height, width = image.shape[:2]

    return {
        "filename": file.filename,
        "width": width,
        "height": height,
        "message": "Image uploaded and successfully read.",
    }