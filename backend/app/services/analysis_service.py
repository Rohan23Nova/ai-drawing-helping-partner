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