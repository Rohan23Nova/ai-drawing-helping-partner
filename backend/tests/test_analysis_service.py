import cv2
import numpy as np

from backend.app.services.analysis_service import (
    find_contours,
    find_largest_contour,
    get_bounding_box,
)
from backend.app.services.analysis_service import (
    analyze_composition,
    analyze_lines,
    calculate_line_length,
    classify_line_orientation,
    detect_lines,
    find_contours,
    find_largest_contour,
    get_bounding_box,
    calculate_line_angle,
    calculate_line_center,
    remove_duplicate_lines,
)

def test_find_contours():
    image = np.zeros((200, 200), dtype=np.uint8)

    cv2.rectangle(
        image,
        (50, 50),
        (150, 150),
        255,
        -1,
    )

    contours = find_contours(image)

    assert len(contours) == 1


def test_find_largest_contour():
    image = np.zeros((200, 200), dtype=np.uint8)

    cv2.rectangle(
        image,
        (20, 20),
        (60, 60),
        255,
        -1,
    )

    cv2.rectangle(
        image,
        (80, 80),
        (180, 180),
        255,
        -1,
    )

    contours = find_contours(image)

    largest = find_largest_contour(contours)

    assert largest is not None
    assert cv2.contourArea(largest) > 5000


def test_find_largest_contour_empty():
    result = find_largest_contour([])

    assert result is None


def test_get_bounding_box():
    image = np.zeros((200, 200), dtype=np.uint8)

    cv2.rectangle(
        image,
        (40, 50),
        (140, 150),
        255,
        -1,
    )

    contours = find_contours(image)

    contour = find_largest_contour(contours)

    box = get_bounding_box(contour)

    assert box["x"] == 40
    assert box["y"] == 50
    assert box["width"] == 101
    assert box["height"] == 101

def test_analyze_composition():
    from backend.app.services.analysis_service import analyze_composition

    image = np.zeros((200, 200), dtype=np.uint8)

    cv2.rectangle(
        image,
        (40, 50),
        (140, 150),
        255,
        -1,
    )

    result = analyze_composition(image)

    assert result["subject_detected"] is True
    assert result["bounding_box"] is not None

def test_analyze_composition_metrics():
    from backend.app.services.analysis_service import analyze_composition

    image = np.zeros((200, 300), dtype=np.uint8)

    cv2.rectangle(
        image,
        (50, 40),
        (150, 140),
        255,
        -1,
    )

    result = analyze_composition(image)

    assert result["subject_detected"] is True

    assert result["center"]["x"] == 100.5
    assert result["center"]["y"] == 90.5

    assert result["size_ratio"]["width"] == round(101 / 300, 4)
    assert result["size_ratio"]["height"] == round(101 / 200, 4)

    assert result["aspect_ratio"] == 1.0
def test_detect_lines():
    image = np.zeros(
        (200, 200),
        dtype=np.uint8,
    )

    cv2.line(
        image,
        (20, 100),
        (180, 100),
        255,
        2,
    )

    lines = detect_lines(image)

    assert len(lines) > 0

def test_calculate_line_length():
    line = {
        "x1": 0,
        "y1": 0,
        "x2": 3,
        "y2": 4,
    }

    length = calculate_line_length(line)

    assert length == 5.0
def test_classify_line_orientation():
    horizontal = {
        "x1": 0,
        "y1": 100,
        "x2": 100,
        "y2": 100,
    }

    vertical = {
        "x1": 100,
        "y1": 0,
        "x2": 100,
        "y2": 100,
    }

    diagonal = {
        "x1": 0,
        "y1": 0,
        "x2": 100,
        "y2": 100,
    }

    assert classify_line_orientation(horizontal) == "horizontal"
    assert classify_line_orientation(vertical) == "vertical"
    assert classify_line_orientation(diagonal) == "diagonal"
def test_analyze_lines():
    image = np.zeros(
        (200, 200),
        dtype=np.uint8,
    )

    cv2.line(
        image,
        (20, 100),
        (180, 100),
        255,
        2,
    )

    result = analyze_lines(image)

    assert result["line_count"] > 0
    assert len(result["lines"]) > 0
def test_analyze_lines_filters_short_lines():
    image = np.zeros(
        (200, 200),
        dtype=np.uint8,
    )

    cv2.line(
        image,
        (20, 100),
        (180, 100),
        255,
        2,
    )

    cv2.line(
        image,
        (20, 20),
        (30, 20),
        255,
        2,
    )

    result = analyze_lines(
        image,
        min_length=50,
    )

    assert result["line_count"] > 0

    for line in result["lines"]:
        assert line["length"] >= 50
def test_analyze_lines_orientation_counts():
    image = np.zeros(
        (200, 200),
        dtype=np.uint8,
    )

    cv2.line(
        image,
        (20, 100),
        (180, 100),
        255,
        2,
    )

    result = analyze_lines(image)

    counts = result["orientation_counts"]

    assert "horizontal" in counts
    assert "vertical" in counts
    assert "diagonal" in counts    

def test_calculate_line_angle():

    horizontal = {
        "x1": 0,
        "y1": 100,
        "x2": 100,
        "y2": 100,
    }

    vertical = {
        "x1": 100,
        "y1": 0,
        "x2": 100,
        "y2": 100,
    }

    assert calculate_line_angle(horizontal) == 0
    assert calculate_line_angle(vertical) == 90

def test_calculate_line_center():

    line = {
        "x1": 20,
        "y1": 40,
        "x2": 100,
        "y2": 120,
    }

    center = calculate_line_center(line)

    assert center == (60, 80)
def test_remove_duplicate_lines():

    lines = [
        {
            "x1": 20,
            "y1": 100,
            "x2": 180,
            "y2": 100,
            "length": 160,
        },
        {
            "x1": 20,
            "y1": 105,
            "x2": 180,
            "y2": 105,
            "length": 160,
        },
    ]

    result = remove_duplicate_lines(lines)

    assert len(result) == 1