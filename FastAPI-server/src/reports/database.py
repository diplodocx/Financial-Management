from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = f"sqlite:///manager.db"

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session