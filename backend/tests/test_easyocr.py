from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.ocr.easyocr import EasyOCREngine


@patch("app.ocr.easyocr._get_reader")
def test_easyocr_extract_text(mock_get_reader: MagicMock) -> None:
    reader = MagicMock()
    reader.readtext.return_value = [
        (None, "Hello", 0.95),
        (None, "World", 0.90),
    ]
    mock_get_reader.return_value = reader

    engine = EasyOCREngine()
    image = np.zeros((40, 80, 3), dtype=np.uint8)
    result = engine.extract_text(image)

    assert result.text == "Hello World"
    assert result.confidence == pytest.approx(0.925, rel=1e-3)
    assert result.processing_time_ms >= 0


@patch("app.ocr.easyocr._get_reader")
def test_easyocr_handles_grayscale(mock_get_reader: MagicMock) -> None:
    reader = MagicMock()
    reader.readtext.return_value = [(None, "Gray", 0.88)]
    mock_get_reader.return_value = reader

    engine = EasyOCREngine()
    image = np.zeros((40, 80), dtype=np.uint8)
    result = engine.extract_text(image)

    assert result.text == "Gray"
