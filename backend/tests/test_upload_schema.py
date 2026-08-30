from backend.app.schemas.upload_schema import (
    UploadResponse,
)


def test_upload_response():

    response = UploadResponse(
        image_id="abc123",
        filename="test.png",
        original_width=300,
        original_height=200,
        processed_width=300,
        processed_height=200,
        original_path="data/original/abc123.png",
        edge_map_path="data/processed/abc123_edges.png",
        grayscale=True,
        blurred=True,
        edges_detected=True,
        message="Image uploaded successfully.",
        analysis={},
        drawing_plan={
            "step_count": 1,
            "steps": [
                {
                    "step": 1,
                    "title": "Establish the composition",
                    "category": "placement",
                    "instruction": "Mark the overall placement.",
                    "purpose": "Establish the subject position.",
                    "difficulty": "beginner",
                    "confidence": 0.95,
                    "confidence_level": "high",
                }
            ],
        },
    )

    assert response.image_id == "abc123"
    assert response.drawing_plan.step_count == 1
    assert len(response.drawing_plan.steps) == 1