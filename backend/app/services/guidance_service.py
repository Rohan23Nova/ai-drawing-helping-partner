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
                "category": step.get(
                    "category",
                    "general",
                ),
                "guidance": make_guidance_text(step),
                "purpose": step["purpose"],
                "difficulty": step["difficulty"],
                "confidence": step["confidence"],
                "confidence_level": step.get(
                    "confidence_level",
                    "medium",
                ),
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
    category = step.get(
        "category",
        "general",
    )

    # High-confidence instructions should remain
    # unchanged.
    if confidence >= 0.85:
        return instruction

    category_guidance = {
        "placement": (
            "Focus on getting the overall placement right "
            "before worrying about details."
        ),
        "primary_form": (
            "Use light strokes and focus on the basic form "
            "rather than making the lines dark immediately."
        ),
        "secondary_form": (
            "Compare this form with the main form to keep "
            "their relative size and position accurate."
        ),
        "relationship": (
            "Pay attention to the space between the forms, "
            "not just the forms themselves."
        ),
        "structure": (
            "Keep these lines light at first and check their "
            "direction against the reference."
        ),
        "refinement": (
            "Only strengthen the lines once the proportions "
            "and placement look correct."
        ),
    }

    extra_guidance = category_guidance.get(
        category,
        "Work gradually and keep comparing your drawing "
        "with the reference."
    )

    if confidence < 0.60:
        confidence_guidance = (
            "The detected information is uncertain, so "
            "treat this as an approximate guide and rely "
            "on the reference for the final placement."
        )
    else:
        confidence_guidance = (
            "Keep comparing your drawing with the reference "
            "as you work."
        )

    return (
        instruction
        + " "
        + extra_guidance
        + " "
        + confidence_guidance
    )