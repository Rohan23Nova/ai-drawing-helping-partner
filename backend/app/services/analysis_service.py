import cv2
import numpy as np


def find_contours(
    edges: np.ndarray,
) -> list[np.ndarray]:

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    return contours


def find_largest_contour(
    contours: list[np.ndarray],
) -> np.ndarray | None:

    if not contours:
        return None

    return max(
        contours,
        key=cv2.contourArea,
    )


def get_bounding_box(
    contour: np.ndarray,
) -> dict:

    x, y, width, height = cv2.boundingRect(contour)

    return {
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }
def get_position_label(
    normalized_x: float,
    normalized_y: float,
) -> str:

    if normalized_x < 0.33:
        horizontal = "left"
    elif normalized_x > 0.66:
        horizontal = "right"
    else:
        horizontal = "center"

    if normalized_y < 0.33:
        vertical = "top"
    elif normalized_y > 0.66:
        vertical = "bottom"
    else:
        vertical = "center"

    if horizontal == "center" and vertical == "center":
        return "center"

    return f"{vertical}-{horizontal}"
def analyze_image(
    edges: np.ndarray,
) -> dict:

    return {
        "composition": analyze_composition(edges),
        "lines": analyze_lines(edges),
        "shapes": analyze_shapes(edges),
    }
def analyze_composition(
    edges: np.ndarray,
) -> dict:

    contours = find_contours(edges)

    largest_contour = find_largest_contour(contours)

    if largest_contour is None:
        return {
            "subject_detected": False,
            "bounding_box": None,
            "center": None,
            "position": None,
            "size_ratio": None,
            "aspect_ratio": None,
        }

    bounding_box = get_bounding_box(largest_contour)

    image_height, image_width = edges.shape[:2]

    x = bounding_box["x"]
    y = bounding_box["y"]
    width = bounding_box["width"]
    height = bounding_box["height"]

    # Calculate the center of the subject
    center_x = x + width / 2
    center_y = y + height / 2

    # Normalize the center relative to the image dimensions
    normalized_center_x = center_x / image_width
    normalized_center_y = center_y / image_height

    # Calculate how much of the image the subject occupies
    width_ratio = width / image_width
    height_ratio = height / image_height

    # Calculate subject shape ratio
    aspect_ratio = width / height

    # Convert normalized position into a human-readable label
    position_label = get_position_label(
        normalized_center_x,
        normalized_center_y,
    )

    return {
        "subject_detected": True,
        "bounding_box": bounding_box,
        "center": {
            "x": round(center_x, 2),
            "y": round(center_y, 2),
            "normalized_x": round(normalized_center_x, 4),
            "normalized_y": round(normalized_center_y, 4),
        },
        "position": position_label,
        "size_ratio": {
            "width": round(width_ratio, 4),
            "height": round(height_ratio, 4),
        },
        "aspect_ratio": round(aspect_ratio, 4),
    }
def detect_lines(
    edges: np.ndarray,
) -> list[dict]:
    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=50,
        maxLineGap=10,
    )

    if lines is None:
        return []

    detected_lines = []

    for line in lines:
        x1, y1, x2, y2 = line

        detected_lines.append(
            {
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2),
            }
        )

    return detected_lines
def calculate_line_length(
    line: dict,
) -> float:

    dx = line["x2"] - line["x1"]
    dy = line["y2"] - line["y1"]

    return float(
        np.sqrt(dx ** 2 + dy ** 2)
    )
def classify_line_orientation(
    line: dict,
) -> str:

    dx = line["x2"] - line["x1"]
    dy = line["y2"] - line["y1"]

    angle = np.degrees(
        np.arctan2(dy, dx)
    )

    angle = abs(angle)

    if angle > 90:
        angle = 180 - angle

    if angle < 15:
        return "horizontal"

    if angle > 75:
        return "vertical"

    return "diagonal"
def analyze_lines(
    edges: np.ndarray,
    min_length: float = 50,
) -> dict:

    lines = detect_lines(edges)

    valid_lines = []

    for line in lines:
        length = calculate_line_length(line)

        if length < min_length:
            continue

        valid_lines.append(
            {
                **line,
                "length": round(length, 2),
            }
        )

    valid_lines = remove_duplicate_lines(
        valid_lines
    )

    analyzed_lines = []

    for line in valid_lines:

        orientation = classify_line_orientation(
            line
        )

        analyzed_lines.append(
            {
                **line,
                "orientation": orientation,
            }
        )

    horizontal_count = sum(
        1
        for line in analyzed_lines
        if line["orientation"] == "horizontal"
    )

    vertical_count = sum(
        1
        for line in analyzed_lines
        if line["orientation"] == "vertical"
    )

    diagonal_count = sum(
        1
        for line in analyzed_lines
        if line["orientation"] == "diagonal"
    )

    return {
        "line_count": len(analyzed_lines),
        "orientation_counts": {
            "horizontal": horizontal_count,
            "vertical": vertical_count,
            "diagonal": diagonal_count,
        },
        "lines": analyzed_lines,
    }
def calculate_line_angle(
    line: dict,
) -> float:

    dx = line["x2"] - line["x1"]
    dy = line["y2"] - line["y1"]

    angle = np.degrees(
        np.arctan2(dy, dx)
    )

    if angle < 0:
        angle += 180

    return float(angle)
def calculate_line_center(
    line: dict,
) -> tuple[float, float]:

    center_x = (
        line["x1"] + line["x2"]
    ) / 2

    center_y = (
        line["y1"] + line["y2"]
    ) / 2

    return center_x, center_y
def remove_duplicate_lines(
    lines: list[dict],
    angle_threshold: float = 10,
    distance_threshold: float = 20,
) -> list[dict]:

    filtered = []

    for line in lines:

        angle = calculate_line_angle(line)

        center_x, center_y = calculate_line_center(line)

        is_duplicate = False

        for existing in filtered:

            existing_angle = calculate_line_angle(
                existing
            )

            existing_x, existing_y = calculate_line_center(
                existing
            )

            angle_difference = abs(
                angle - existing_angle
            )

            if angle_difference > 90:
                angle_difference = (
                    180 - angle_difference
                )

            center_distance = np.sqrt(
                (center_x - existing_x) ** 2
                + (center_y - existing_y) ** 2
            )

            if (
                angle_difference <= angle_threshold
                and center_distance <= distance_threshold
            ):
                is_duplicate = True
                break

        if not is_duplicate:
            filtered.append(line)

    return filtered
def approximate_contour(
    contour: np.ndarray,
    epsilon_ratio: float = 0.02,
) -> np.ndarray:

    perimeter = cv2.arcLength(
        contour,
        True,
    )

    epsilon = epsilon_ratio * perimeter

    return cv2.approxPolyDP(
        contour,
        epsilon,
        True,
    )
def classify_shape(
    contour: np.ndarray,
) -> str:

    circularity = calculate_circularity(
        contour
    )

    if circularity > 0.80:
        return "circle"

    approximated = approximate_contour(
        contour
    )

    vertices = len(approximated)

    if vertices == 3:
        return "triangle"

    if vertices == 4:
        return "quadrilateral"

    if vertices == 5:
        return "pentagon"

    if vertices == 6:
        return "hexagon"

    return "polygon"
def calculate_circularity(
    contour: np.ndarray,
) -> float:

    area = cv2.contourArea(contour)

    perimeter = cv2.arcLength(
        contour,
        True,
    )

    if perimeter == 0:
        return 0.0

    circularity = (
        4 * np.pi * area
        / (perimeter ** 2)
    )

    return float(circularity)
def analyze_shapes(
    edges: np.ndarray,
    min_area: float = 100,
) -> dict:

    contours = find_contours(edges)

    image_height, image_width = edges.shape[:2]

    shapes = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < min_area:
            continue

        shape_type = classify_shape(contour)

        bounding_box = get_bounding_box(contour)

        metrics = calculate_shape_metrics(
            contour,
            image_width,
            image_height,
        )

        shapes.append(
            {
                "type": shape_type,
                "area": round(float(area), 2),
                "bounding_box": bounding_box,
                **metrics,
            }
        )
    relationships = analyze_shape_relationships(
        shapes
    )

    return {
        "shape_count": len(shapes),
        "shapes": shapes,
        "relationships": relationships,
    }
def calculate_shape_metrics(
    contour: np.ndarray,
    image_width: int,
    image_height: int,
) -> dict:

    x, y, width, height = cv2.boundingRect(contour)

    center_x = x + width / 2
    center_y = y + height / 2

    normalized_center_x = center_x / image_width
    normalized_center_y = center_y / image_height

    normalized_width = width / image_width
    normalized_height = height / image_height

    aspect_ratio = width / height if height != 0 else 0

    return {
        "center": {
            "x": round(float(normalized_center_x), 4),
            "y": round(float(normalized_center_y), 4),
        },
        "size": {
            "width": round(float(normalized_width), 4),
            "height": round(float(normalized_height), 4),
        },
        "aspect_ratio": round(float(aspect_ratio), 4),
    }
def determine_spatial_relationship(
    shape_a: dict,
    shape_b: dict,
) -> str:

    ax = shape_a["center"]["x"]
    ay = shape_a["center"]["y"]

    bx = shape_b["center"]["x"]
    by = shape_b["center"]["y"]

    if abs(ax - bx) > abs(ay - by):
        if ax < bx:
            return "left_of"
        else:
            return "right_of"

    if ay < by:
        return "above"

    return "below"
def analyze_shape_relationships(
    shapes: list[dict],
) -> list[dict]:

    relationships = []

    for i in range(len(shapes)):

        for j in range(len(shapes)):

            if i == j:
                continue

            relationship = determine_spatial_relationship(
                shapes[i],
                shapes[j],
            )

            relationships.append(
                {
                    "shape_a": i,
                    "shape_b": j,
                    "relationship": relationship,
                }
            )

    return relationships
def analyze_reference(
    edges: np.ndarray,
) -> dict:

    composition = analyze_composition(edges)

    lines = analyze_lines(edges)

    shapes = analyze_shapes(edges)

    proportions = calculate_proportions(
        shapes["shapes"]
    )

    return {
        "composition": composition,
        "lines": lines,
        "shapes": shapes,
        "proportions": proportions,
    }
def calculate_proportions(
    shapes: list[dict],
) -> dict:

    if not shapes:
        return {
            "count": 0,
            "largest_shape": None,
        }

    largest_shape = max(
        shapes,
        key=lambda shape: shape.get("area", 0),
    )

    return {
        "count": len(shapes),
        "largest_shape": {
            "index": shapes.index(largest_shape),
            "type": largest_shape["type"],
            "width": largest_shape["size"]["width"],
            "height": largest_shape["size"]["height"],
            "aspect_ratio": largest_shape["aspect_ratio"],
        },
    }
