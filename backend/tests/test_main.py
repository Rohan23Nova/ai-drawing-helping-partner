import cv2
import numpy as np
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_image():
    image = np.zeros(
        (200, 200, 3),
        dtype=np.uint8,
    )

    cv2.rectangle(
        image,
        (50, 50),
        (150, 150),
        (255, 255, 255),
        -1,
    )

    success, encoded_image = cv2.imencode(
        ".png",
        image,
    )

    assert success

    response = client.post(
        "/upload",
        files={
            "file": (
                "test.png",
                encoded_image.tobytes(),
                "image/png",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "image_id" in data
    assert data["filename"] == "test.png"

    assert "analysis" in data
    assert data["analysis"] is not None

    assert "composition" in data["analysis"]
    assert data["analysis"]["composition"] is not None
    analysis = data["analysis"]

    assert "proportions" in analysis
    assert analysis["proportions"] is not None
    assert "drawing_plan" in data
    assert data["drawing_plan"] is not None

    assert "steps" in data["drawing_plan"]
    assert data["drawing_plan"]["step_count"] > 0
    assert "guidance" in data
    assert data["guidance"] is not None

    assert "steps" in data["guidance"]
    assert data["guidance"]["step_count"] > 0

    assert (
        len(data["guidance"]["steps"])
        == data["guidance"]["step_count"]
    )
def test_get_original_image():
    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    success, encoded_image = cv2.imencode(
        ".png",
        image,
    )

    assert success

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "test.png",
                encoded_image.tobytes(),
                "image/png",
            )
        },
    )

    assert upload_response.status_code == 200

    image_id = upload_response.json()["image_id"]

    response = client.get(
        f"/images/{image_id}/original"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_get_edge_map():
    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    cv2.rectangle(
        image,
        (20, 20),
        (80, 80),
        (255, 255, 255),
        -1,
    )

    success, encoded_image = cv2.imencode(
        ".png",
        image,
    )

    assert success

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "test.png",
                encoded_image.tobytes(),
                "image/png",
            )
        },
    )

    assert upload_response.status_code == 200

    image_id = upload_response.json()["image_id"]

    response = client.get(
        f"/images/{image_id}/edges"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

def test_get_missing_original_image():
    response = client.get(
        "/images/does-not-exist/original"
    )

    assert response.status_code == 404

def test_get_missing_edge_map():
    response = client.get(
        "/images/does-not-exist/edges"
    )

    assert response.status_code == 404

def test_chat():

    image = np.zeros(
        (200, 200, 3),
        dtype=np.uint8,
    )

    cv2.rectangle(
        image,
        (50, 50),
        (150, 150),
        (255, 255, 255),
        -1,
    )

    success, encoded_image = cv2.imencode(
        ".png",
        image,
    )

    assert success

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "chat_test.png",
                encoded_image.tobytes(),
                "image/png",
            )
        },
    )

    assert upload_response.status_code == 200

    upload_data = upload_response.json()

    image_id = upload_data["image_id"]

    response = client.post(
        "/chat",
        json={
            "image_id": image_id,
            "message": "What should I do first?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["image_id"] == image_id
    assert data["message"] == "What should I do first?"
    assert "response" in data
    assert len(data["response"]) > 0