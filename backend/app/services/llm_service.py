import os
import json

from openai import OpenAI


SYSTEM_PROMPT = """
You are an AI drawing helping partner.

Your role is to help a person learn and improve drawing
while they work from a reference image.

You are NOT a strict teacher. You are a helpful drawing
partner who gives practical suggestions from your own
analysis.

Rules:

1. Give actionable drawing instructions.
2. Start with large forms, placement, proportions,
   and structure before small details.
3. Encourage light construction lines before darker
   final lines.
4. Use the provided computer-vision analysis as context.
5. Use the provided drawing plan as the main sequence.
6. Respect the learner's current step.
7. Never invent visual information that is not present
   in the supplied analysis.
8. If the analysis is uncertain, explicitly say that
   the learner should verify it against the reference.
9. Keep responses concise unless the learner asks for
   more explanation.
10. If the learner asks a specific question, answer that
    question rather than repeating the entire drawing plan.
11. Be encouraging but do not give meaningless praise.
12. Explain WHY a particular drawing action is useful
    when that would help the learner understand it.

The goal is to help the learner make better drawing
decisions while keeping them in control of the drawing.
"""


def generate_llm_response(
    message: str,
    analysis: dict,
    drawing_plan: dict,
    conversation: list[dict],
    current_step: int,
) -> str:

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:
        return generate_fallback_response(
            message,
            drawing_plan,
            current_step,
            analysis,
        )

    client = OpenAI(
        api_key=api_key
    )

    context = {
        "analysis": analysis,
        "drawing_plan": drawing_plan,
        "current_step": current_step,
    }

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": (
                "Here is the structured information "
                "available about the reference drawing:\n\n"
                + json.dumps(
                    context,
                    indent=2,
                )
            ),
        },
    ]

    messages.extend(
        conversation[-10:]
    )

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    response = client.responses.create(
        model="gpt-5-mini",
        input=messages,
    )

    return response.output_text
 
def generate_fallback_response(
    message: str,
    drawing_plan: dict,
    current_step: int,
    analysis: dict | None = None,
) -> str:

    message_lower = message.lower()
    analysis = analysis or {}

    steps = drawing_plan.get(
        "steps",
        [],
    )

    # User finished the current step
    if (
        "finished" in message_lower
        or "done" in message_lower
    ):
        return (
            "Good. Now compare your drawing with "
            "the reference and check the proportions "
            "and placement before moving to details."
        )

    # User asks about proportions
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
                "Check the proportions of the main "
                f"{largest_shape['type']} form. "
                "Compare its width, height, and "
                "overall size with the reference."
            )

        return (
            "Check the proportions by comparing "
            "the width, height, and relative size "
            "of the major forms with the reference."
        )

    # User asks about lines
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

    # User asks what to do first
    if "first" in message_lower:

        if steps:
            step = steps[0]

            return (
                f"Start with '{step['title']}'. "
                f"{step['instruction']}"
            )

        return (
            "Start by establishing the composition. "
            "Mark the overall placement and proportions "
            "lightly before adding details."
        )

    # User asks what to do next
    if "next" in message_lower:

        next_step_index = current_step

        if next_step_index < len(steps):

            step = steps[next_step_index]

            return (
                f"Next, work on '{step['title']}'. "
                f"{step['instruction']}"
            )

        return (
            "You've reached the final planned step. "
            "Review the drawing against the reference "
            "and refine the important details."
        )

    # General fallback
    return (
        "Start with the major forms and their "
        "placement. Keep your strokes light and "
        "compare your drawing with the reference "
        "as you work."
    )