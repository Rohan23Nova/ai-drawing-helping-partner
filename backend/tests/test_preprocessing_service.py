import cv2
import numpy as np

from backend.app.services.preprocessing_service import (
    convert_to_grayscale,
    detect_edges,
    resize_image,
)
from backend.app.services.preprocessing_service import preprocess_image

def test_convert_to_grayscale():
    image = np.zeros((100, 200, 3), dtype=np.uint8)

    gray = convert_to_grayscale(image)

    assert gray.shape == (100, 200)


def test_resize_image():
    image = np.zeros((2000, 3000, 3), dtype=np.uint8)

    resized = resize_image(image, max_width=1000)

    assert resized.shape[1] == 1000
    assert resized.shape[0] < 2000


def test_resize_does_not_enlarge():
    image = np.zeros((500, 800, 3), dtype=np.uint8)

    resized = resize_image(image, max_width=1000)

    assert resized.shape == image.shape


def test_detect_edges():
    image = np.zeros((100, 100), dtype=np.uint8)

    cv2.rectangle(
        image,
        (20, 20),
        (80, 80),
        255,
        2,
    )

    edges = detect_edges(image)

    assert edges.shape == image.shape
    assert np.count_nonzero(edges) > 0

def test_preprocess_image():
    image = np.zeros((200, 300, 3), dtype=np.uint8)

    result = preprocess_image(image)

    assert "resized" in result
    assert "grayscale" in result
    assert "blurred" in result
    assert "edges" in result

    assert result["grayscale"].ndim == 2
    assert result["blurred"].ndim == 2
    assert result["edges"].ndim == 2