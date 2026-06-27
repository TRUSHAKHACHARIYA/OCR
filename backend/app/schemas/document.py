from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.document import DocumentStatus


class OCRResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    engine: str
    text: str | None
    processing_time_ms: float | None
    status: str
    error_message: str | None
    created_at: datetime


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    content_type: str
    status: DocumentStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    ocr_results: list[OCRResultResponse] = []


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    status: str
    message: str
