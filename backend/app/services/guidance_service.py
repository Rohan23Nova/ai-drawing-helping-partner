def generate_guidance(plan: dict) -> dict:
    """
    Convert a structured drawing plan into
    user-friendly drawing guidance.
    """

    steps = plan.get("steps", [])

    guidance_steps = []

    for step in steps:
        guidance_steps.append(
            {
                "step": step["step"],
                "title": step["title"],
                "guidance": make_guidance_text(step),
                "purpose": step["purpose"],
                "difficulty": step["difficulty"],
                "confidence": step["confidence"],
            }
        )

    return {
        "step_count": len(guidance_steps),
        "steps": guidance_steps,
    }


def make_guidance_text(step: dict) -> str:
    """
    Create natural drawing guidance from
    a planner step.
    """

    instruction = step["instruction"]
    confidence = step["confidence"]

    if confidence < 0.60:
        return (
            instruction
            + " Take this as an approximate guide "
            "and rely on the reference for the final placement."
        )

    if confidence < 0.85:
        return (
            instruction
            + " Keep comparing your drawing with "
            "the reference as you work."
        )

    return instruction