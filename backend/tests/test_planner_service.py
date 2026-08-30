from backend.app.services.planner_service import (
    generate_drawing_plan,
)


def test_generate_drawing_plan():

    analysis = {
        "composition": {},
        "lines": {
            "line_count": 4,
        },
        "shapes": {
            "shape_count": 2,
        },
        "proportions": {
            "largest_shape": {
                "index": 0,
                "type": "rectangle",
                "width": 0.5,
                "height": 0.5,
                "aspect_ratio": 1.0,
            }
        },
    }

    result = generate_drawing_plan(
        analysis
    )

    assert "steps" in result
    assert result["step_count"] > 0

    assert result["steps"][0]["step"] == 1

    assert (
        result["steps"][0]["title"]
        == "Establish the composition"
    )


def test_generate_drawing_plan_empty():

    result = generate_drawing_plan({})

    assert "steps" in result
    assert result["step_count"] > 0
    