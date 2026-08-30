from pydantic import BaseModel

from backend.app.schemas.planner_schema import (
    DrawingPlan,
)


class UploadResponse(BaseModel):
    image_id: str
    filename: str

    original_width: int
    original_height: int

    processed_width: int
    processed_height: int

    original_path: str
    edge_map_path: str

    grayscale: bool
    blurred: bool
    edges_detected: bool

    message: str

    analysis: dict
    drawing_plan: DrawingPlan