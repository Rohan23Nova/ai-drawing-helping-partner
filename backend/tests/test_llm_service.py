from unittest.mock import patch

from backend.app.services.llm_service import (
    generate_llm_response,
)


def test_llm_fallback_without_api_key():

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

    with patch.dict(
        "os.environ",
        {},
        clear=True,
    ):
        result = generate_llm_response(
            message="How should I check the proportions?",
            analysis=analysis,
            drawing_plan=drawing_plan,
            conversation=[],
            current_step=1,
        )

    assert isinstance(result, str)
    assert "proportions" in result.lower()
def test_llm_response_uses_openai():

    analysis = {
        "proportions": {}
    }

    drawing_plan = {
        "steps": [
            {
                "step": 1,
                "title": "Establish the composition",
                "instruction": "Mark the subject position.",
            }
        ]
    }

    fake_response = type(
        "FakeResponse",
        (),
        {
            "output_text": "Start by marking the composition."
        },
    )()

    with patch(
        "backend.app.services.llm_service.OpenAI"
    ) as mock_openai:

        mock_client = mock_openai.return_value

        mock_client.responses.create.return_value = (
            fake_response
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "test-key"},
        ):

            result = generate_llm_response(
                message="What should I do first?",
                analysis=analysis,
                drawing_plan=drawing_plan,
                conversation=[],
                current_step=1,
            )

    assert result == (
        "Start by marking the composition."
    )

    mock_client.responses.create.assert_called_once()

def test_llm_receives_conversation():

    conversation = [
        {
            "role": "user",
            "content": "I have finished the main form.",
        },
        {
            "role": "assistant",
            "content": "Good. Check the proportions.",
        },
    ]

    fake_response = type(
        "FakeResponse",
        (),
        {
            "output_text": "Now refine the secondary forms."
        },
    )()

    with patch(
        "backend.app.services.llm_service.OpenAI"
    ) as mock_openai:

        mock_client = mock_openai.return_value

        mock_client.responses.create.return_value = (
            fake_response
        )

        with patch.dict(
            "os.environ",
            {"OPENAI_API_KEY": "test-key"},
        ):

            result = generate_llm_response(
                message="What's next?",
                analysis={},
                drawing_plan={
                    "steps": []
                },
                conversation=conversation,
                current_step=2,
            )

    assert result == (
        "Now refine the secondary forms."
    )

    call = (
        mock_client
        .responses
        .create
        .call_args
    )

    assert call is not None

    messages = call.kwargs["input"]

    conversation_contents = [
        message["content"]
        for message in messages
        if message["role"] != "system"
    ]

    assert any(
        "finished the main form"
        in str(content)
        for content in conversation_contents
    )