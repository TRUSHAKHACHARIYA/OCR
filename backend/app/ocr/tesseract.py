import time

import cv2
import numpy as np
import pytesseract

from app.ocr.base import EngineOutput, OCREngine


class TesseractEngine(OCREngine):
    name = "tesseract"

    def extract_text(self, image: np.ndarray) -> EngineOutput:
        start = time.perf_counter()
        gray = image if len(image.shape) == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return EngineOutput(text=text.strip(), processing_time_ms=elapsed_ms)
