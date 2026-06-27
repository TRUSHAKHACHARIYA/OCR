from pathlib import Path

import cv2
import fitz
import numpy as np

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/tiff",
}

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def validate_upload(filename: str, content_type: str) -> None:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {extension}")
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"Unsupported content type: {content_type}")


def load_image_from_bytes(data: bytes, content_type: str) -> np.ndarray:
    if content_type == "application/pdf":
        return _load_first_pdf_page(data)

    array = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Unable to decode image file")
    return image


def load_image_from_path(file_path: Path, content_type: str) -> np.ndarray:
    data = file_path.read_bytes()
    return load_image_from_bytes(data, content_type)


def _load_first_pdf_page(data: bytes) -> np.ndarray:
    with fitz.open(stream=data, filetype="pdf") as doc:
        if doc.page_count == 0:
            raise ValueError("PDF has no pages")
        page = doc.load_page(0)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        channels = pixmap.n
        image = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
            pixmap.height, pixmap.width, channels
        )
        if channels == 4:
            return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        if channels == 1:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        return image
