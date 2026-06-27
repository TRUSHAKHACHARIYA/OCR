from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.document import Document, DocumentStatus, OCRResult
from app.ocr.registry import ENGINE_REGISTRY, get_engine
from app.services.document_loader import load_image_from_path
from app.services.preprocessing import preprocess
from app.tasks.celery_app import celery_app


def _run_engine(engine_name: str, image) -> tuple[str, dict[str, object]]:
    engine = get_engine(engine_name)
    output = engine.extract_text(image)
    return engine_name, {
        "text": output.text,
        "processing_time_ms": output.processing_time_ms,
        "confidence": output.confidence,
        "status": "completed",
        "error_message": None,
    }


def _process_document_sync(document_id: str) -> None:
    db: Session = SessionLocal()
    try:
        document = db.get(Document, document_id)
        if document is None:
            return

        document.status = DocumentStatus.PROCESSING
        document.updated_at = datetime.now(UTC)
        db.commit()

        image = load_image_from_path(
            Path(document.file_path),
            document.content_type,
        )
        processed_image = preprocess(image)

        engine_names = list(ENGINE_REGISTRY.keys())
        results: dict[str, dict[str, object]] = {}

        with ThreadPoolExecutor(max_workers=len(engine_names)) as executor:
            futures = {
                executor.submit(_run_engine, name, processed_image): name
                for name in engine_names
            }
            for future in as_completed(futures):
                engine_name = futures[future]
                try:
                    name, result = future.result()
                    results[name] = result
                except Exception as exc:
                    results[engine_name] = {
                        "text": None,
                        "processing_time_ms": None,
                        "confidence": None,
                        "status": "failed",
                        "error_message": str(exc),
                    }

        for engine_name, result in results.items():
            db.add(
                OCRResult(
                    document_id=document.id,
                    engine=engine_name,
                    text=result["text"],  # type: ignore[arg-type]
                    processing_time_ms=result["processing_time_ms"],  # type: ignore[arg-type]
                    status=str(result["status"]),
                    error_message=result["error_message"],  # type: ignore[arg-type]
                )
            )

        document.status = DocumentStatus.COMPLETED
        document.updated_at = datetime.now(UTC)
        db.commit()
    except Exception as exc:
        db.rollback()
        document = db.get(Document, document_id)
        if document is not None:
            document.status = DocumentStatus.FAILED
            document.error_message = str(exc)
            document.updated_at = datetime.now(UTC)
            db.commit()
        raise
    finally:
        db.close()


@celery_app.task(name="app.tasks.ocr_tasks.process_document")
def process_document(document_id: str) -> str:
    _process_document_sync(document_id)
    return document_id
