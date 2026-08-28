import cv2
import numpy as np

from backend.app.services.image_service import (
    read_image,
    validate_image_extension,
)


def test_valid_image_extensions():
    assert validate_image_extension("drawing.jpg")
    assert validate_image_extension("drawing.jpeg")
    assert validate_image_extension("drawing.png")
    assert validate_image_extension("drawing.webp")


def test_invalid_image_extension():
    assert not validate_image_extension("drawing.txt")
    assert not validate_image_extension("drawing.exe")


def test_read_image():
    image = np.zeros((100, 200, 3), dtype=np.uint8)

    success, encoded = cv2.imencode(".png", image)

    assert success

    decoded = read_image(encoded.tobytes())

    assert decoded.shape == (100, 200, 3)