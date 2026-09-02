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
def create_plan_step(
    step_number: int,
    title: str,
    instruction: str,
    purpose: str,
    confidence: float = 0.75,
    difficulty: str = "beginner",
) -> dict:

    return {
        "step": step_number,
        "title": title,
        "category": get_step_category(title),
        "instruction": instruction,
        "purpose": purpose,
        "difficulty": difficulty,
        "confidence": confidence,
        "confidence_level": describe_confidence(
            confidence
        ),
    }
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
    vision: dict | None = None,
) -> dict:
    """
    Generate a beginner-friendly drawing plan.

    If semantic vision information is available, use it
    to create meaningful drawing stages.

    Otherwise, fall back to the existing OpenCV-based plan.
    """

    if vision:
        return generate_semantic_drawing_plan(vision)

    # Existing OpenCV-based planner
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

    # Step 3: Remaining shapes
    shape_count = shapes.get(
        "shape_count",
        0,
    )

    if shape_count > 1:
        steps.append(
            create_plan_step(
                step_number=len(steps) + 1,
                title="Refine the main forms",
                instruction=(
                    "Check the major shapes and refine "
                    "their outlines lightly. Compare their "
                    "size, position, and proportions with "
                    "the reference."
                ),
                purpose=(
                    "Improve the accuracy of the major forms "
                    "before adding smaller details."
                ),
                confidence=0.75,
            )
        )

    # Relationships
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
            create_plan_step(
                step_number=len(steps) + 1,
                title="Check relative placement",
                instruction=instruction,
                purpose=(
                    "Keep the major forms positioned "
                    "correctly relative to one another."
                ),
                confidence=0.70,
                difficulty="beginner",
            )
        )

    # Lines
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
            create_plan_step(
                step_number=len(steps) + 1,
                title="Refine important lines",
                instruction=(
                    f"Check the approximately "
                    f"{line_count} detected structural "
                    "lines and refine them lightly."
                ),
                purpose=(
                    "Strengthen the structural lines that "
                    "define the major forms."
                ),
                confidence=0.70,
                difficulty="beginner",
            )
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
def generate_semantic_drawing_plan(
    vision: dict,
) -> dict:
    """
    Convert semantic visual understanding into
    a beginner-friendly construction sequence.
    """

    steps = []

    subject = vision.get(
        "subject",
        "subject",
    )

    main_form = vision.get(
        "main_form",
        {},
    )

    components = vision.get(
        "components",
        [],
    )

    construction_order = vision.get(
        "construction_order",
        [],
    )

    # Step 1: Composition
    steps.append(
        create_plan_step(
            step_number=1,
            title="Establish the composition",
            instruction=(
                f"Lightly mark the overall position "
                f"and size of the {subject} on the page."
            ),
            purpose=(
                "Establish the overall placement before "
                "adding internal details."
            ),
            confidence=0.85,
        )
    )

    # Step 2: Main silhouette
    if main_form:
        form_type = main_form.get(
            "type",
            "main form",
        )

        position = main_form.get(
            "position",
            "center",
        )

        steps.append(
            create_plan_step(
                step_number=2,
                title="Block in the main form",
                instruction=(
                    f"Lightly draw the main {form_type} "
                    f"in the {position}. Focus on its "
                    "overall width, height, and silhouette."
                ),
                purpose=(
                    "Build the primary structure of the "
                    "subject before adding smaller forms."
                ),
                confidence=0.85,
            )
        )

    # Step 3+: Components
    for component in components:

        name = component.get(
            "name",
            "secondary form",
        )

        form = component.get(
            "form",
            "simple shape",
        )

        position = component.get(
            "position",
            "appropriate position",
        )

        importance = component.get(
            "importance",
            "medium",
        )

        confidence = (
            0.85
            if importance == "high"
            else 0.75
        )

        steps.append(
            create_plan_step(
                step_number=len(steps) + 1,
                title=f"Add the {name}",
                instruction=(
                    f"Lightly place the {form} "
                    f"{name} in the {position}. "
                    "Check its size and spacing against "
                    "the main form before refining it."
                ),
                purpose=(
                    f"Establish the position and proportion "
                    f"of the {name} relative to the subject."
                ),
                confidence=confidence,
                difficulty="beginner",
            )
        )

    # Final structural step
    steps.append(
        create_plan_step(
            step_number=len(steps) + 1,
            title="Refine the drawing",
            instruction=(
                "Compare the complete construction with "
                "the reference. Correct proportions and "
                "placement before strengthening important "
                "contours and details."
            ),
            purpose=(
                "Correct structural errors before moving "
                "toward darker lines and shading."
            ),
            confidence=0.85,
        )
    )

    return {
        "step_count": len(steps),
        "steps": steps,
    }

def get_step_category(title: str) -> str:
    categories = {
        "Establish the composition": "placement",
        "Block in the main form": "primary_form",
        "Add secondary forms": "secondary_form",
        "Check relative placement": "relationship",
        "Refine important lines": "structure",
        "Refine the drawing": "refinement",
        "Refine the main forms": "secondary_form",
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