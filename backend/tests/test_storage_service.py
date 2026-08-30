from backend.app.services.storage_service import save_original_image


def test_save_original_image(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.storage_service.ORIGINAL_DIR",
        tmp_path,
    )

    image_id = "test123"
    image_bytes = b"fake image data"

    result = save_original_image(
        image_bytes,
        image_id,
        ".jpg",
    )

    expected_path = tmp_path / "test123.jpg"

    assert result == str(expected_path)
    assert expected_path.exists()
    assert expected_path.read_bytes() == image_bytes