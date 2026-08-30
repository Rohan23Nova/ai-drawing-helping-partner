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
        {
            "step": 1,
            "title": "Establish the composition",
            "instruction": (
                "Lightly mark the overall position "
                "and size of the subject on the page."
            ),
        }
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

        if largest_index < len(shape_list):
            main_shape = shape_list[largest_index]

            instruction = create_shape_instruction(
                main_shape
            )
        else:
            instruction = (
                f"Start with the main "
                f"{largest_shape['type']} shape."
            )

        steps.append(
            {
                "step": 2,
                "title": "Block in the main form",
                "instruction": instruction,
            }
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
        {
            "step": len(steps) + 1,
            "title": "Refine the drawing",
            "instruction": (
                "Check proportions and placement, "
                "then gradually strengthen the "
                "important contours and details."
            ),
        }
    )

    return {
        "step_count": len(steps),
        "steps": steps,
    }