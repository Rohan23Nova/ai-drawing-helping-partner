from pathlib import Path
from fastapi.responses import FileResponse
from backend.app.core.image_utils import generate_image_id
from backend.app.services.storage_service import (
    get_edge_map_path,
    get_original_image_path,
    save_original_image,
)
from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.app.services.image_service import (
    read_image,
    validate_image_extension,
)

from backend.app.services.preprocessing_service import (
    preprocess_image,
    save_edge_map,
)
from backend.app.services.analysis_service import (
    analyze_reference,
)
from backend.app.services.planner_service import (
    generate_drawing_plan,
)
from backend.app.schemas.planner_schema import (
    DrawingPlan,
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
    image_id = generate_image_id()

    extension = Path(file.filename).suffix.lower()

    original_path = save_original_image(
        image_bytes,
        image_id,
        extension,
    )

    processed = preprocess_image(image)
    analysis = analyze_reference(
        processed["edges"]
    )
    drawing_plan_data = generate_drawing_plan(
        analysis
    )

    drawing_plan = DrawingPlan.model_validate(
        drawing_plan_data
    )

    edge_map_path = save_edge_map(
        processed["edges"],
        f"data/processed/{image_id}_edges.png",
    )

    height, width = processed["resized"].shape[:2]

    return {
        "image_id": image_id,
        "filename": file.filename,
        "original_width": image.shape[1],
        "original_height": image.shape[0],
        "processed_width": width,
        "processed_height": height,
        "original_path": original_path,
        "edge_map_path": edge_map_path,
        "grayscale": True,
        "blurred": True,
        "edges_detected": True,
        "message": "Image uploaded and preprocessed successfully.",
        "analysis": analysis,
        "drawing_plan": drawing_plan,
    }
@app.get("/images/{image_id}/original")
async def get_original_image(image_id: str):
    image_path = get_original_image_path(image_id)

    if image_path is None:
        raise HTTPException(
            status_code=404,
            detail="Original image not found.",
        )

    return FileResponse(image_path)


@app.get("/images/{image_id}/edges")
async def get_edge_map(image_id: str):
    edge_map_path = get_edge_map_path(image_id)

    if edge_map_path is None:
        raise HTTPException(
            status_code=404,
            detail="Edge map not found.",
        )

    return FileResponse(edge_map_path)