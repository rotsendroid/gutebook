"""
A module responsible for the dependencies
"""

from typing import Generator
from app.db import SessionLocal


def get_db() -> Generator:
    """
    Manages DB sessions
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()