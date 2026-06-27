import time
from functools import lru_cache

import cv2
import numpy as np

from app.ocr.base import EngineOutput, OCREngine


@lru_cache(maxsize=1)
def _get_ocr() -> object:
    from paddleocr import PaddleOCR

    return PaddleOCR(use_angle_cls=True, lang="en", show_log=False)


class PaddleOCREngine(OCREngine):
    name = "paddleocr"

    def extract_text(self, image: np.ndarray) -> EngineOutput:
        start = time.perf_counter()
        ocr = _get_ocr()
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        result = ocr.ocr(image, cls=True)  # type: ignore[attr-defined]
        lines: list[str] = []
        confidences: list[float] = []

        if result and result[0]:
            for line in result[0]:
                if line and len(line) >= 2:
                    text_info = line[1]
                    if isinstance(text_info, (list, tuple)) and len(text_info) >= 2:
                        lines.append(str(text_info[0]))
                        confidences.append(float(text_info[1]))

        avg_confidence = sum(confidences) / len(confidences) if confidences else None
        elapsed_ms = (time.perf_counter() - start) * 1000
        return EngineOutput(
            text=" ".join(lines).strip(),
            processing_time_ms=elapsed_ms,
            confidence=avg_confidence,
        )
