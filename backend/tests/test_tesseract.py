from unittest.mock import MagicMock, patch

import numpy as np

from app.ocr.tesseract import TesseractEngine


@patch("app.ocr.tesseract.pytesseract.image_to_string")
def test_tesseract_extract_text(mock_ocr: MagicMock) -> None:
    mock_ocr.return_value = "  Hello OCR  "
    engine = TesseractEngine()
    image = np.zeros((40, 80), dtype=np.uint8)

    result = engine.extract_text(image)

    assert result.text == "Hello OCR"
    assert result.processing_time_ms >= 0
    mock_ocr.assert_called_once()


@patch("app.ocr.tesseract.pytesseract.image_to_string")
def test_tesseract_handles_color_image(mock_ocr: MagicMock) -> None:
    mock_ocr.return_value = "Color text"
    engine = TesseractEngine()
    image = np.zeros((40, 80, 3), dtype=np.uint8)

    result = engine.extract_text(image)

    assert result.text == "Color text"
