from sqlalchemy import create_engine
from collections.abc import Iterator
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

url = settings.sqlalchemy_url


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
