import uuid
from typing import List, Optional
from uuid import UUID

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """
    This is a Pydentic schemas that validates and read the data for the User model
    """

    id: UUID

    user_name: str

    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    """
    This is a Pydentic schemas that validates and create the data for the User model
    """

    user_name: str


class UserUpdate(schemas.BaseUserUpdate):
    """
    This is a Pydentic schemas that validates and update the data for the User model
    """

    user_name: Optional[str]
