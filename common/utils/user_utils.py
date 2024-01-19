from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import get_db
from common.models import User

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
password_helper = PasswordHelper(pwd_context)


def hash_password(password: str) -> str:
    """
    User Password Setting Functions

    :param password: new password
    """
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(user: User, password: str) -> bool:
    """
    User Password Verification Functions

    :param user: db object
    :param password: user password
    """
    return pwd_context.verify(password, user.hashed_password)


async def get_user_db(
    session: AsyncSession = Depends(get_db),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """
    Adapter for DB connection
    """
    yield SQLAlchemyUserDatabase(session, User)
