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
def test_chat_uses_conversation_history():

    analysis = {}

    drawing_plan = {
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "instruction": "Mark the subject position.",
            },
            {
                "step": 2,
                "title": "Block in the main form",
                "instruction": "Lightly draw the main form.",
            },
        ]
    }

    conversation = [
        {
            "role": "user",
            "content": "What should I do first?",
        },
        {
            "role": "assistant",
            "content": "Start with the composition.",
        },
    ]

    result = generate_chat_response(
        "What's next?",
        analysis,
        drawing_plan,
        conversation,
    )

    assert "Block in the main form" in result
def test_chat_finished_response():

    result = generate_chat_response(
        "I am done with this step.",
        {},
        {"steps": []},
        [],
    )

    assert "reference" in result.lower()
    assert "proportions" in result.lower()