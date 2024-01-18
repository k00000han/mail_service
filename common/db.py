from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from common.config import DB_URI
from common.models.base import Base

_engine = create_async_engine(DB_URI)
_session = sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    The function returning a fresh SQLAlchemy session to interact with the database.
    """
    async with _session() as session:
        yield session


async def save(data: list[Base]) -> None:
    """
    Saves provided data to the DB

    :param data: list of objects of model class
    """
    async with _session() as session:
        session.add_all(data)
        await session.commit()
