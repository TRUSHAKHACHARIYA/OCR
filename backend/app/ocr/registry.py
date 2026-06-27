from app.ocr.base import OCREngine
from app.ocr.easyocr import EasyOCREngine
from app.ocr.paddleocr import PaddleOCREngine
from app.ocr.tesseract import TesseractEngine

ENGINE_REGISTRY: dict[str, type[OCREngine]] = {
    "tesseract": TesseractEngine,
    "easyocr": EasyOCREngine,
    "paddleocr": PaddleOCREngine,
}


def get_engine(name: str) -> OCREngine:
    if name not in ENGINE_REGISTRY:
        raise ValueError(f"Unknown OCR engine: {name}")
    return ENGINE_REGISTRY[name]()


def list_engines() -> list[str]:
    return list(ENGINE_REGISTRY.keys())
