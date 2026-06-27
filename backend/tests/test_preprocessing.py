import numpy as np

from app.services.preprocessing import (
    binarize,
    denoise,
    deskew,
    enhance_contrast,
    preprocess,
)


def test_deskew_returns_image_for_blank_input() -> None:
    image = np.zeros((50, 50, 3), dtype=np.uint8)
    result = deskew(image)
    assert result.shape == image.shape


def test_denoise_color_image() -> None:
    image = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    result = denoise(image)
    assert result.shape == image.shape


def test_denoise_grayscale_image() -> None:
    image = np.random.randint(0, 255, (32, 32), dtype=np.uint8)
    result = denoise(image)
    assert result.shape == image.shape


def test_binarize_produces_single_channel() -> None:
    image = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    result = binarize(image)
    assert len(result.shape) == 2


def test_enhance_contrast_grayscale() -> None:
    image = np.random.randint(0, 255, (32, 32), dtype=np.uint8)
    result = enhance_contrast(image)
    assert result.shape == image.shape


def test_preprocess_pipeline() -> None:
    image = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    result = preprocess(image)
    assert len(result.shape) == 2
