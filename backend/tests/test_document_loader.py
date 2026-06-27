import numpy as np
import pytest

from app.services.document_loader import (
    load_image_from_bytes,
    validate_upload,
)


def test_validate_upload_accepts_png() -> None:
    validate_upload("scan.png", "image/png")


def test_validate_upload_rejects_unknown_extension() -> None:
    with pytest.raises(ValueError, match="Unsupported file extension"):
        validate_upload("scan.gif", "image/gif")


def test_validate_upload_rejects_unknown_content_type() -> None:
    with pytest.raises(ValueError, match="Unsupported content type"):
        validate_upload("scan.png", "image/gif")


def test_load_image_from_png_bytes() -> None:
    import cv2

    image = np.zeros((20, 20, 3), dtype=np.uint8)
  cv2.putText(image, "A", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
  success, encoded = cv2.imencode(".png", image)
  assert success

  loaded = load_image_from_bytes(encoded.tobytes(), "image/png")
  assert loaded.shape[0] == 20
  assert loaded.shape[1] == 20
