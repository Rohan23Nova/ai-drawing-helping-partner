from backend.app.core.image_utils import generate_image_id


def test_generate_image_id():
    image_id = generate_image_id()

    assert isinstance(image_id, str)
    assert len(image_id) == 32


def test_generate_unique_image_ids():
    first_id = generate_image_id()
    second_id = generate_image_id()

    assert first_id != second_id