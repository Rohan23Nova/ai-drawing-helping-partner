import uuid


def generate_image_id() -> str:
    return uuid.uuid4().hex