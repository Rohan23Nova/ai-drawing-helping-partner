def generate_chat_response(
    message: str,
    analysis: dict,
    drawing_plan: dict,
) -> str:
    """
    Generate a temporary context-aware response.

    This is intentionally deterministic for now.
    The LLM will be integrated later.
    """

    message_lower = message.lower()

    if "first" in message_lower:
        steps = drawing_plan.get("steps", [])

        if steps:
            first_step = steps[0]

            return (
                f"Start with '{first_step['title']}'. "
                f"{first_step['instruction']}"
            )

    if "proportion" in message_lower:
        proportions = analysis.get(
            "proportions",
            {},
        )

        largest_shape = proportions.get(
            "largest_shape"
        )

        if largest_shape:
            return (
                "Start by checking the proportions of "
                f"the main {largest_shape['type']} form."
            )

    if "line" in message_lower:
        lines = analysis.get(
            "lines",
            {},
        )

        line_count = lines.get(
            "line_count",
            0,
        )

        return (
            f"The analysis detected approximately "
            f"{line_count} structural lines. "
            "Check their direction and placement "
            "before making them darker."
        )

    return (
        "Start with the major forms and their placement. "
        "Keep your strokes light and compare your drawing "
        "with the reference as you work."
    )