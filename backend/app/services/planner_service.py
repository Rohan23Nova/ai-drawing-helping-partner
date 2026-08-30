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
        steps.append(
            {
                "step": 2,
                "title": "Block in the main form",
                "instruction": (
                    f"Start with the main "
                    f"{largest_shape['type']} shape. "
                    f"Use it as the primary construction form."
                ),
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