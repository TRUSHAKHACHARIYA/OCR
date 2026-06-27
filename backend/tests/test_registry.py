import pytest

from app.ocr.registry import ENGINE_REGISTRY, get_engine, list_engines


def test_list_engines_returns_three_engines() -> None:
    engines = list_engines()
    assert engines == ["tesseract", "easyocr", "paddleocr"]


def test_get_engine_returns_correct_types() -> None:
    for name in list_engines():
        engine = get_engine(name)
        assert engine.name == name


def test_get_engine_unknown_raises() -> None:
    with pytest.raises(ValueError, match="Unknown OCR engine"):
        get_engine("invalid")


def test_registry_contains_all_adapters() -> None:
    assert set(ENGINE_REGISTRY.keys()) == {"tesseract", "easyocr", "paddleocr"}
