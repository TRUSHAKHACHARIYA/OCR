from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EngineOutput:
    text: str
    processing_time_ms: float
    confidence: float | None = None


class OCREngine:
    name: str = "base"

    def extract_text(self, image: np.ndarray) -> EngineOutput:
        raise NotImplementedError
