from fastapi import APIRouter, Depends
from starlette import status

from api.auth.auth import current_active_user
from api.users.schemas import User
from common.models import User as DbUser

router = APIRouter()


@router.get("/identity", name="get_user_identity", status_code=status.HTTP_200_OK)
async def read(user: DbUser = Depends(current_active_user)) -> User:
    """
    Read Current User info

    :return: user object
    """

    return User(
        id=str(user.id),
        email=user.email,
        user_name=user.user_name,
    )
