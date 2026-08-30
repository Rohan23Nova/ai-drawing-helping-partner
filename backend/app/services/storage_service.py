from pathlib import Path


ORIGINAL_DIR = Path("data/original")
PROCESSED_DIR = Path("data/processed")


def save_original_image(
    image_bytes: bytes,
    image_id: str,
    extension: str,
) -> str:

    ORIGINAL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = ORIGINAL_DIR / f"{image_id}{extension}"

    file_path.write_bytes(image_bytes)

    return str(file_path)