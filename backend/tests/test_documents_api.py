from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.document import Document, DocumentStatus, OCRResult
from app.tasks.ocr_tasks import _process_document_sync


@patch("app.tasks.ocr_tasks.get_engine")
@patch("app.tasks.ocr_tasks.preprocess")
@patch("app.tasks.ocr_tasks.load_image_from_path")
def test_process_document_sync_stores_results(
    mock_load: MagicMock,
    mock_preprocess: MagicMock,
    mock_get_engine: MagicMock,
    db_session: Session,
) -> None:
    from pathlib import Path

    mock_load.return_value = np.zeros((20, 20, 3), dtype=np.uint8)
    mock_preprocess.return_value = np.zeros((20, 20), dtype=np.uint8)

    def engine_factory(name: str) -> MagicMock:
        engine = MagicMock()
        engine.name = name
        engine.extract_text.return_value = MagicMock(
            text=f"{name} text",
            processing_time_ms=12.5,
            confidence=0.9,
        )
        return engine

    mock_get_engine.side_effect = engine_factory

    document = Document(
        id="doc-1",
        filename="test.png",
        content_type="image/png",
        file_path=str(Path("test.png")),
        status=DocumentStatus.PENDING,
    )
    db_session.add(document)
    db_session.commit()

    with patch("app.tasks.ocr_tasks.SessionLocal", return_value=db_session):
        _process_document_sync("doc-1")

    db_session.refresh(document)
    assert document.status == DocumentStatus.COMPLETED
    assert len(document.ocr_results) == 3
    engines = {result.engine for result in document.ocr_results}
    assert engines == {"tesseract", "easyocr", "paddleocr"}


def test_upload_document(client: TestClient) -> None:
    import cv2

    image = np.zeros((30, 60, 3), dtype=np.uint8)
    cv2.putText(image, "Hi", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    success, encoded = cv2.imencode(".png", image)
    assert success

    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("sample.png", encoded.tobytes(), "image/png")},
    )

    assert response.status_code == 202
    data = response.json()
    assert data["filename"] == "sample.png"
    assert data["status"] == "pending"


def test_get_document_not_found(client: TestClient) -> None:
    response = client.get("/api/v1/documents/missing-id")
    assert response.status_code == 404


def test_get_document_with_results(client: TestClient, db_session: Session) -> None:
    document = Document(
        id="doc-2",
        filename="report.pdf",
        content_type="application/pdf",
        file_path="/tmp/report.pdf",
        status=DocumentStatus.COMPLETED,
    )
    db_session.add(document)
    db_session.add(
        OCRResult(
            document_id="doc-2",
            engine="tesseract",
            text="Sample",
            processing_time_ms=10.0,
            status="completed",
        )
    )
    db_session.commit()

    response = client.get("/api/v1/documents/doc-2")
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "report.pdf"
    assert len(data["ocr_results"]) == 1
    assert data["ocr_results"][0]["engine"] == "tesseract"
