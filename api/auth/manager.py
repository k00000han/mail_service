import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from common.config import SECRET
from common.models import User
from common.utils.user_utils import get_user_db, password_helper


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db, password_helper)