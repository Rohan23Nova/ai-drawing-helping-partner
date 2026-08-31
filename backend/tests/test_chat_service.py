from backend.app.services.chat_service import (
    generate_chat_response,
)


def test_chat_response_first_step():

    analysis = {}

    drawing_plan = {
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "instruction": "Lightly mark the subject position.",
            }
        ]
    }

    result = generate_chat_response(
        "What should I do first?",
        analysis,
        drawing_plan,
    )

    assert "Establish the composition" in result
    assert "Lightly mark" in result


def test_chat_response_proportion():

    analysis = {
        "proportions": {
            "largest_shape": {
                "type": "rectangle",
            }
        }
    }

    drawing_plan = {
        "steps": []
    }

    result = generate_chat_response(
        "How should I check the proportions?",
        analysis,
        drawing_plan,
    )

    assert "proportions" in result.lower()
    assert "rectangle" in result.lower()


def test_chat_response_lines():

    analysis = {
        "lines": {
            "line_count": 6,
        }
    }

    drawing_plan = {
        "steps": []
    }

    result = generate_chat_response(
        "What about the lines?",
        analysis,
        drawing_plan,
    )

    assert "6" in result
    assert "lines" in result.lower()