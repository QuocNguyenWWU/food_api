import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from collections.abc import Iterator
from sqlalchemy.orm import Session, sessionmaker


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


load_dotenv()
url = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
