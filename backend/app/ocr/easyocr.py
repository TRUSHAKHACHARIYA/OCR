import time
from functools import lru_cache

import cv2
import numpy as np

from app.ocr.base import EngineOutput, OCREngine


@lru_cache(maxsize=1)
def _get_reader() -> object:
    import easyocr

    return easyocr.Reader(["en"], gpu=False)


class EasyOCREngine(OCREngine):
    name = "easyocr"

    def extract_text(self, image: np.ndarray) -> EngineOutput:
        start = time.perf_counter()
        reader = _get_reader()
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        results = reader.readtext(image)  # type: ignore[attr-defined]
        text = " ".join(item[1] for item in results)
        confidences = [float(item[2]) for item in results if len(item) > 2]
        avg_confidence = sum(confidences) / len(confidences) if confidences else None
        elapsed_ms = (time.perf_counter() - start) * 1000
        return EngineOutput(
            text=text.strip(),
            processing_time_ms=elapsed_ms,
            confidence=avg_confidence,
        )
