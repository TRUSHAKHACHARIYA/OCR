# OCRDIL Backend

FastAPI application for the OCR Benchmark & Document Intelligence Lab.

## Development

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
celery -A app.tasks.celery_app worker --loglevel=info
pytest -v --cov=app/ocr --cov-fail-under=80
```

For full OCR engine support (EasyOCR + PaddleOCR):

```bash
pip install -e ".[dev,ocr]"
```
