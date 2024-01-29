import json

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from api.auth.auth import current_active_user
from services.keygen import keygen
from api.token.schemas import TokenSchema
from api.token.service import TokenService
from api.schemas import ID

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_active_user)],
)
async def create_email(
        object_data: TokenSchema,
        db_service: TokenService = Depends(TokenService),
):
    """
    Create  New Email Endpoint

    :param object_data: email data
    :param db_service: database methods
    :return: response
    """

    return await db_service.create_item(object_data)


@router.post(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
)
async def create_new_token(
        pk: ID,
        db_service: TokenService = Depends(TokenService),
):
    """
    Create Token Endpoint

    :param pk: ID of template
    :param db_service: database methods
    :return: response
    """

    try:
        token = await keygen(db_service, pk)

        if token is not None:
            token = json.loads(token)
            await db_service.update_token(pk, token)

            return JSONResponse(content={"message": "The token has been generated!"}, status_code=200)

        return JSONResponse(content={"message": "Token already updated!"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
