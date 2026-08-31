from backend.app.services.llm_service import (
    generate_llm_response,
)


def generate_chat_response(
    message: str,
    analysis: dict,
    drawing_plan: dict,
    conversation: list[dict] | None = None,
    current_step: int = 1,
) -> str:
    """
    Generate a drawing-partner response.

    The chat service acts as the bridge between
    the API/session layer and the LLM layer.
    """

    return generate_llm_response(
        message=message,
        analysis=analysis,
        drawing_plan=drawing_plan,
        conversation=conversation or [],
        current_step=current_step,
    )