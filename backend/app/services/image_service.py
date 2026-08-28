from pathlib import Path

import cv2
import numpy as np


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def validate_image_extension(filename: str) -> bool:
    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


def read_image(image_bytes: bytes) -> np.ndarray:
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)

    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Unable to decode image.")

    return image