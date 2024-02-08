import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from starlette import status
from starlette.responses import JSONResponse

from api.auth.auth import current_active_user
from api.pagination import Page
from api.token.query_builder import TokenQueryBuilder
from common.db import get_db
from services.keygen import generate_url, generate_token
from api.token.schemas import EmailSchema, TokenSchemaParams
from api.token.service import EmailService, TokenService
from api.schemas import ID

router = APIRouter()


@router.get(
    "/",
    name="get_all_emails",
    dependencies=[Depends(current_active_user)],
    response_model=Page[EmailSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_emails(
        params: TokenSchemaParams = Depends(TokenSchemaParams),
        qb: TokenQueryBuilder = Depends(TokenQueryBuilder),
        db: AsyncSession = Depends(get_db),
        order_by: str = Query(None),
):
    """
    Read All Emails Endpoint

    :param params: QueryParams
    :param qb: QueryBuilder
    :param db: database connection
    :param order_by: Sorting data
    :return: Email from the database
    """

    query = qb.build(params)

    if order_by:
        query = query.order_by(text(f"{order_by} ASC"))

    return await paginate(db, query)


@router.post(
    '/',
    name="create_email",
    dependencies=[Depends(current_active_user)],
)
async def create_email(
        object_data: EmailSchema,
        db_service: EmailService = Depends(EmailService),
):
    """
    Create  New Email Endpoint

    :param object_data: email data
    :param db_service: database methods
    :return: response
    """

    try:
        return await db_service.create_item(object_data)
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")


@router.delete(
    '/',
    name='delete_email',
    dependencies=[Depends(current_active_user)],
)
async def delete_email(
        pk: ID,
        db_service: EmailService = Depends(EmailService),
):
    """
    Delete Work Email Endpoint

    :param pk: ID of Email
    :param db_service: database methods
    :return: response
    """

    try:
        await db_service.delete_item(pk)

        return HTTPException(status_code=200, detail=f"Successfully deleted!")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")


@router.get(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
)
async def get_auth_url(
        pk: ID,
        db_service: TokenService = Depends(TokenService),
):
    """
    Get Auth URL Endpoint

    :param pk: ID of token
    :param db_service: database methods
    :return: response
    """

    try:
        url = await generate_url(db_service, pk)

        return url

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
)
async def create_new_token(
        pk: ID,
        code: str,
        db_service: TokenService = Depends(TokenService),
):
    """
    Create Token Endpoint

    :param pk: ID of token
    :param code: code for generate token
    :param db_service: database methods
    :return: response
    """
    try:
        token = await generate_token(db_service, pk, code)

        if token is not None:
            token = json.loads(token)
            await db_service.update_token(pk, token)

            return JSONResponse(content={"message": "The token has been generated!"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
