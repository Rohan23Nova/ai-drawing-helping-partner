from backend.app.services.planner_service import (
    generate_drawing_plan,
    create_shape_instruction,
    describe_size,
    describe_position,
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

def test_describe_position():

    center = {
        "x": 0.5,
        "y": 0.2,
    }

    result = describe_position(center)

    assert result == "in the upper-center area"

def test_describe_center_position():

    center = {
        "x": 0.5,
        "y": 0.5,
    }

    result = describe_position(center)

    assert result == "near the center"
def test_describe_size():

    size = {
        "width": 0.5,
        "height": 0.5,
    }

    result = describe_size(size)

    assert result == "medium in width and medium-height"
def test_create_shape_instruction():

    shape = {
        "type": "rectangle",
        "center": {
            "x": 0.5,
            "y": 0.5,
        },
        "size": {
            "width": 0.5,
            "height": 0.5,
        },
        "aspect_ratio": 1.0,
    }

    result = create_shape_instruction(shape)

    assert "rectangle" in result
    assert "near the center" in result
    assert "aspect ratio" in result