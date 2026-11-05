import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_session
from main import app
from models import Base

load_dotenv()
test_url = os.environ["TEST_DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)
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