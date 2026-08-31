from backend.app.services.planner_service import (
    generate_drawing_plan,
    create_shape_instruction,
    describe_size,
    describe_position,
    create_relationship_instruction,
    get_shape_relationship,
    get_step_category,
    describe_confidence,
    adjust_instruction_for_confidence,

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
def test_create_relationship_instruction():

    shape_a = {
        "type": "circle",
    }

    shape_b = {
        "type": "rectangle",
    }

    result = create_relationship_instruction(
        shape_a,
        shape_b,
        "above",
    )

    assert "circle" in result
    assert "above" in result
    assert "rectangle" in result
def test_get_shape_relationship():

    relationships = [
        {
            "shape_a": 0,
            "shape_b": 1,
            "relationship": "above",
        }
    ]

    result = get_shape_relationship(
        relationships,
        0,
        1,
    )

    assert result == "above"
def test_get_shape_relationship_missing():

    relationships = [
        {
            "shape_a": 0,
            "shape_b": 1,
            "relationship": "above",
        }
    ]

    result = get_shape_relationship(
        relationships,
        1,
        2,
    )

    assert result is None
def test_plan_step_structure():

    analysis = {
        "shapes": {
            "shape_count": 1,
            "shapes": [],
        },
        "proportions": {},
        "lines": {
            "line_count": 0,
        },
    }

    result = generate_drawing_plan(
        analysis
    )

    step = result["steps"][0]

    assert "step" in step
    assert "title" in step
    assert "instruction" in step
    assert "purpose" in step
    assert "difficulty" in step
    assert "confidence" in step

def test_plan_step_category():

    analysis = {
        "shapes": {
            "shape_count": 1,
            "shapes": [],
        },
        "proportions": {},
        "lines": {
            "line_count": 0,
        },
    }

    result = generate_drawing_plan(
        analysis
    )

    first_step = result["steps"][0]

    assert first_step["category"] == "placement"
def test_get_step_category():

    assert (
        get_step_category(
            "Block in the main form"
        )
        == "primary_form"
    )

    assert (
        get_step_category(
            "Refine the drawing"
        )
        == "refinement"
    )
def test_describe_confidence():

    assert describe_confidence(0.95) == "high"
    assert describe_confidence(0.75) == "medium"
    assert describe_confidence(0.40) == "low"
def test_adjust_instruction_high_confidence():

    instruction = "Draw the main rectangle."

    result = adjust_instruction_for_confidence(
        instruction,
        0.95,
    )

    assert result == instruction
def test_adjust_instruction_medium_confidence():

    instruction = "Draw the main rectangle."

    result = adjust_instruction_for_confidence(
        instruction,
        0.70,
    )

    assert "Use this as a guide" in result
def test_adjust_instruction_low_confidence():

    instruction = "Draw the main rectangle."

    result = adjust_instruction_for_confidence(
        instruction,
        0.40,
    )

    assert "uncertain" in result
    assert "verify" in result