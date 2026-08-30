def describe_position(center: dict) -> str:
    x = center["x"]
    y = center["y"]

    if x < 0.33:
        horizontal = "left"
    elif x > 0.66:
        horizontal = "right"
    else:
        horizontal = "center"

    if y < 0.33:
        vertical = "upper"
    elif y > 0.66:
        vertical = "lower"
    else:
        vertical = "middle"

    if horizontal == "center" and vertical == "middle":
        return "near the center"

    return f"in the {vertical}-{horizontal} area"
def describe_size(size: dict) -> str:
    width = size["width"]
    height = size["height"]

    if width < 0.25:
        width_description = "small"
    elif width < 0.60:
        width_description = "medium"
    else:
        width_description = "large"

    if height < 0.25:
        height_description = "short"
    elif height < 0.60:
        height_description = "medium-height"
    else:
        height_description = "tall"

    return (
        f"{width_description} in width "
        f"and {height_description}"
    )
def create_shape_instruction(
    shape: dict,
) -> str:

    shape_type = shape["type"]

    position = describe_position(
        shape["center"]
    )

    size = describe_size(
        shape["size"]
    )

    aspect_ratio = shape["aspect_ratio"]

    return (
        f"Block in the {shape_type} "
        f"{position}. "
        f"Keep it {size}. "
        f"Aim for an aspect ratio of "
        f"approximately {aspect_ratio:.2f}."
    )
def get_shape_relationship(
    relationships: list[dict],
    shape_a: int,
    shape_b: int,
) -> str | None:

    for relationship in relationships:
        if (
            relationship["shape_a"] == shape_a
            and relationship["shape_b"] == shape_b
        ):
            return relationship["relationship"]

    return None
def create_relationship_instruction(
    shape_a: dict,
    shape_b: dict,
    relationship: str,
) -> str:

    type_a = shape_a["type"]
    type_b = shape_b["type"]

    relationship_text = {
        "above": "above",
        "below": "below",
        "left_of": "to the left of",
        "right_of": "to the right of",
    }

    position = relationship_text.get(
        relationship,
        relationship,
    )

    return (
        f"Keep the {type_a} {position} "
        f"the {type_b}, matching the relative "
        f"spacing visible in the reference."
    )
def generate_drawing_plan(
    analysis: dict,
) -> dict:

    steps = []

    composition = analysis.get(
        "composition",
        {},
    )

    shapes = analysis.get(
        "shapes",
        {},
    )

    proportions = analysis.get(
        "proportions",
        {},
    )

    # Step 1: Establish composition
    steps.append(
        create_plan_step(
            step_number=1,
            title="Establish the composition",
            instruction=(
                "Lightly mark the overall position "
                "and size of the subject on the page."
            ),
            purpose=(
                "Create a guide for the overall "
                "placement before adding details."
            ),
        )
    )

    # Step 2: Establish largest form
    largest_shape = proportions.get(
        "largest_shape"
    )

    if largest_shape:
        largest_index = largest_shape["index"]

        shape_list = shapes.get(
            "shapes",
            [],
        )

        confidence = 0.75

        if largest_index < len(shape_list):
            main_shape = shape_list[largest_index]

            confidence = main_shape.get(
                "confidence",
                0.75,
            )

            instruction = create_shape_instruction(
                main_shape
            )

            instruction = adjust_instruction_for_confidence(
                instruction,
                confidence,
            )

        else:
            instruction = (
                f"Start with the main "
                f"{largest_shape['type']} shape."
            )

        steps.append(
            create_plan_step(
                step_number=2,
                title="Block in the main form",
                instruction=instruction,
                purpose=(
                    "Establish the primary structure "
                    "of the drawing."
                ),
                confidence=confidence,
            )
        )
    # Step 3: Add remaining shapes
    shape_count = shapes.get(
        "shape_count",
        0,
    )

    if shape_count > 1:
        steps.append(
            {
                "step": 3,
                "title": "Add secondary forms",
                "instruction": (
                    f"Build the remaining "
                    f"{shape_count - 1} detected "
                    "forms around the main structure."
                ),
            }
        )
    relationships = shapes.get(
        "relationships",
        [],
    )

    shape_list = shapes.get(
        "shapes",
        [],
    )

    for relationship in relationships:

        shape_a_index = relationship["shape_a"]
        shape_b_index = relationship["shape_b"]

        if (
            shape_a_index >= len(shape_list)
            or shape_b_index >= len(shape_list)
        ):
            continue

        shape_a = shape_list[shape_a_index]
        shape_b = shape_list[shape_b_index]

        instruction = create_relationship_instruction(
            shape_a,
            shape_b,
            relationship["relationship"],
        )

        steps.append(
            {
                "step": len(steps) + 1,
                "title": "Check relative placement",
                "instruction": instruction,
            }
        )
    # Step 4: Refine lines
    lines = analysis.get(
        "lines",
        {},
    )

    line_count = lines.get(
        "line_count",
        0,
    )

    if line_count > 0:
        steps.append(
            {
                "step": len(steps) + 1,
                "title": "Refine important lines",
                "instruction": (
                    f"Check the approximately "
                    f"{line_count} detected structural "
                    "lines and refine them lightly."
                ),
            }
        )

    # Final step
    steps.append(
        create_plan_step(
            step_number=len(steps) + 1,
            title="Refine the drawing",
            instruction=(
                "Check proportions and placement, "
                "then gradually strengthen the "
                "important contours and details."
            ),
            purpose=(
                "Correct structural mistakes before "
                "committing to darker lines."
            ),
            difficulty="beginner",
        )
    )

    return {
        "step_count": len(steps),
        "steps": steps,
    }
def create_plan_step(
    step_number: int,
    title: str,
    instruction: str,
    purpose: str,
    difficulty: str = "beginner",
    confidence: float = 1.0,
) -> dict:

    return {
        "step": step_number,
        "title": title,
        "category": get_step_category(title),
        "instruction": instruction,
        "purpose": purpose,
        "difficulty": difficulty,
        "confidence": confidence,
        "confidence": confidence,
        "confidence_level": describe_confidence(
            confidence
        ),
    }
def get_step_category(title: str) -> str:
    categories = {
        "Establish the composition": "placement",
        "Block in the main form": "primary_form",
        "Add secondary forms": "secondary_form",
        "Check relative placement": "relationship",
        "Refine important lines": "structure",
        "Refine the drawing": "refinement",
    }

    return categories.get(
        title,
        "general",
    )
def describe_confidence(confidence: float) -> str:

    if confidence >= 0.85:
        return "high"

    if confidence >= 0.60:
        return "medium"

    return "low"
def adjust_instruction_for_confidence(
    instruction: str,
    confidence: float,
) -> str:

    if confidence >= 0.85:
        return instruction

    if confidence >= 0.60:
        return (
            instruction
            + " Use this as a guide and compare "
            "the placement with the reference."
        )

    return (
        instruction
        + " This detection is uncertain, so "
        "verify the placement visually against "
        "the reference before committing to the line."
    )