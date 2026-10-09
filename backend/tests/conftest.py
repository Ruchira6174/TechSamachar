import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tech_samachar.db.base import Base

# Use in-memory SQLite for fast, isolated tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # For fully isolated tests, we could use nested transactions here, but for simple tests this is fine.
    try:
        yield db
    finally:
        db.close()
        # Clean tables after each test
        for table in reversed(Base.metadata.sorted_tables):
            engine.execute(table.delete())
