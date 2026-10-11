
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from tech_samachar.db.base import Base
from tech_samachar.api.deps import get_db
from tech_samachar.main import app

# Register all models before creating test tables.
import tech_samachar.db.models.article
import tech_samachar.db.models.briefing
import tech_samachar.db.models.preference
import tech_samachar.db.models.processing_job
import tech_samachar.db.models.source


@pytest.fixture(scope="function")
def engine():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=test_engine)

    yield test_engine

    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def isolate_app_database(engine):
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    try:
        yield
    finally:
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as test_client:
        yield test_client