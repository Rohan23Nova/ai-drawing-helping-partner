from backend.app.services.guidance_service import (
    generate_guidance,
    make_guidance_text,
)


def test_make_guidance_text_high_confidence():

    step = {
        "step": 1,
        "title": "Establish the composition",
        "instruction": "Lightly mark the subject position.",
        "purpose": "Establish placement.",
        "difficulty": "beginner",
        "confidence": 0.90,
    }

    result = make_guidance_text(step)

    assert result == (
        "Lightly mark the subject position."
    )


def test_make_guidance_text_medium_confidence():

    step = {
        "step": 1,
        "title": "Establish the composition",
        "instruction": "Lightly mark the subject position.",
        "purpose": "Establish placement.",
        "difficulty": "beginner",
        "confidence": 0.70,
    }

    result = make_guidance_text(step)

    assert "Keep comparing" in result


def test_make_guidance_text_low_confidence():

    step = {
        "step": 1,
        "title": "Establish the composition",
        "instruction": "Lightly mark the subject position.",
        "purpose": "Establish placement.",
        "difficulty": "beginner",
        "confidence": 0.40,
    }

    result = make_guidance_text(step)

    assert "approximate guide" in result


def test_generate_guidance():

    plan = {
        "step_count": 1,
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "instruction": "Lightly mark the subject position.",
                "purpose": "Establish placement.",
                "difficulty": "beginner",
                "confidence": 0.90,
            }
        ],
    }

    result = generate_guidance(plan)

    assert result["step_count"] == 1
    assert len(result["steps"]) == 1
    assert result["steps"][0]["step"] == 1
    assert result["steps"][0]["title"] == (
        "Establish the composition"
    )
    assert result["steps"][0]["purpose"] == (
        "Establish placement."
    )
def test_guidance_preserves_step_information():

    plan = {
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "category": "placement",
                "instruction": "Place the subject lightly.",
                "purpose": "Establish overall placement.",
                "difficulty": "beginner",
                "confidence": 0.90,
                "confidence_level": "high",
            }
        ]
    }

    result = generate_guidance(plan)

    step = result["steps"][0]

    assert step["step"] == 1
    assert step["category"] == "placement"
    assert step["difficulty"] == "beginner"
    assert step["confidence"] == 0.90
    assert step["confidence_level"] == "high"
def test_guidance_contains_category_advice():

    plan = {
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "category": "placement",
                "instruction": "Place the subject lightly.",
                "purpose": "Establish overall placement.",
                "difficulty": "beginner",
                "confidence": 0.90,
                "confidence_level": "high",
            }
        ]
    }

    result = generate_guidance(plan)

    guidance = result["steps"][0]["guidance"]

    assert guidance == "Place the subject lightly."