import os

# Set before any app imports so pydantic-settings picks it up
os.environ.setdefault("USE_MOCK_DATA", "true")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # noqa: registers all models with Base.metadata
from app.db.base import Base
from app.api.deps import get_db
from app.main import app
from app.core.config import settings

# Patch the singleton directly so service-layer checks see it
settings.USE_MOCK_DATA = True

TEST_DB_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        TEST_DB_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # all threads share same in-memory connection
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def db_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    db = Session()
    # Seed demo user and themes
    from app.models.user import User
    from app.models.theme import Theme
    from app.core.security import hash_password
    import json

    if db.query(User).count() == 0:
        db.add(User(id=1, email="demo@example.com", hashed_password=hash_password("demo1234")))

    if db.query(Theme).count() == 0:
        db.add(Theme(key="ai", name="AI & 빅테크", description="test", tickers=json.dumps(["NVDA", "MSFT"])))

    db.commit()
    yield db
    db.close()


@pytest.fixture(scope="session")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
