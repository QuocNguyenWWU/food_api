import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import get_session
from app.main import app
from app.models import Base

test_url = settings.sqlalchemy_test_url
assert test_url is not None, "TEST_DATABASE_URL is missing in .env"
assert "test" in test_url, "Tests must never run on the real database"

engine = create_engine(test_url)
TestSession = sessionmaker(bind=engine)


def override_get_session():
    with TestSession() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return TestClient(app)
