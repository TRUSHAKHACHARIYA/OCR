from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.ocr.paddleocr import PaddleOCREngine


@patch("app.ocr.paddleocr._get_ocr")
def test_paddleocr_extract_text(mock_get_ocr: MagicMock) -> None:
    ocr = MagicMock()
    ocr.ocr.return_value = [
        [
            [None, ("Hello", 0.92)],
            [None, ("Paddle", 0.88)],
        ]
    ]
    mock_get_ocr.return_value = ocr

    engine = PaddleOCREngine()
    image = np.zeros((40, 80, 3), dtype=np.uint8)
    result = engine.extract_text(image)

    assert result.text == "Hello Paddle"
    assert result.confidence == pytest.approx(0.90, rel=1e-3)
    assert result.processing_time_ms >= 0


@patch("app.ocr.paddleocr._get_ocr")
def test_paddleocr_handles_empty_result(mock_get_ocr: MagicMock) -> None:
    ocr = MagicMock()
    ocr.ocr.return_value = [None]
    mock_get_ocr.return_value = ocr

    engine = PaddleOCREngine()
    image = np.zeros((40, 80, 3), dtype=np.uint8)
    result = engine.extract_text(image)

    assert result.text == ""
    assert result.confidence is None


@patch("app.ocr.paddleocr._get_ocr")
def test_paddleocr_handles_grayscale(mock_get_ocr: MagicMock) -> None:
    ocr = MagicMock()
    ocr.ocr.return_value = [[ [None, ("Test", 0.85)] ]]
    mock_get_ocr.return_value = ocr

    engine = PaddleOCREngine()
    image = np.zeros((40, 80), dtype=np.uint8)
    result = engine.extract_text(image)

    assert result.text == "Test"
