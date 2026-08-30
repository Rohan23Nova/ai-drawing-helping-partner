import cv2
import numpy as np


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def resize_image(
    image: np.ndarray,
    max_width: int = 1000,
) -> np.ndarray:

    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA,
    )


def blur_image(
    image: np.ndarray,
    kernel_size: int = 5,
) -> np.ndarray:

    return cv2.GaussianBlur(
        image,
        (kernel_size, kernel_size),
        0,
    )


def detect_edges(
    image: np.ndarray,
    lower_threshold: int = 50,
    upper_threshold: int = 150,
) -> np.ndarray:

    return cv2.Canny(
        image,
        lower_threshold,
        upper_threshold,
    )
def preprocess_image(image: np.ndarray) -> dict:
    resized = resize_image(image)

    grayscale = convert_to_grayscale(resized)

    blurred = blur_image(grayscale)

    edges = detect_edges(blurred)

    return {
        "resized": resized,
        "grayscale": grayscale,
        "blurred": blurred,
        "edges": edges,
    }