from backend.app.services.storage_service import (
    get_edge_map_path,
    get_original_image_path,
    save_original_image,
)


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


def test_get_original_image_path(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.storage_service.ORIGINAL_DIR",
        tmp_path,
    )

    image_id = "abc123"

    image_path = tmp_path / "abc123.jpg"
    image_path.write_bytes(b"image")

    result = get_original_image_path(image_id)

    assert result == image_path


def test_get_original_image_path_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.storage_service.ORIGINAL_DIR",
        tmp_path,
    )

    result = get_original_image_path("does-not-exist")

    assert result is None


def test_get_edge_map_path(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.storage_service.PROCESSED_DIR",
        tmp_path,
    )

    image_id = "abc123"

    edge_path = tmp_path / "abc123_edges.png"
    edge_path.write_bytes(b"edges")

    result = get_edge_map_path(image_id)

    assert result == edge_path


def test_get_edge_map_path_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backend.app.services.storage_service.PROCESSED_DIR",
        tmp_path,
    )

    result = get_edge_map_path("does-not-exist")

    assert result is None