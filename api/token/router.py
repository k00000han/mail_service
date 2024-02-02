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
from services.keygen import keygen
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

    :param pk: ID of token
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


@router.delete(
    '/',
    dependencies=[Depends(current_active_user)],
    name='delete_email',
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

    await db_service.delete_item(pk)
