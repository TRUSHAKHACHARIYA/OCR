import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("UPLOAD_DIR", "test_uploads")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.database import Base, get_db
from app.main import app


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session, tmp_path: Path) -> Generator[TestClient, None, None]:
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()

    os.environ["UPLOAD_DIR"] = str(upload_dir)
    get_settings.cache_clear()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def mock_celery_delay(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.documents.process_document.delay",
        lambda document_id: None,
    )
