from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate
from starlette import status

from api.auth.auth import current_active_user
from api.newsletter.query_builder import NewslatterQueryBuilder
from api.newsletter.schemas import NewslatterSchema, NewslatterParams
from api.newsletter.service import NewsletterService
from api.pagination import Page
from api.schemas import ID
from common.db import get_db

router = APIRouter()


@router.get(
    "/",
    name="get_all_newsletters",
    dependencies=[Depends(current_active_user)],
    response_model=Page[NewslatterSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_newsletters(
        params: NewslatterParams = Depends(NewslatterParams),
        qb: NewslatterQueryBuilder = Depends(NewslatterQueryBuilder),
        db: AsyncSession = Depends(get_db),
        order_by: str = Query(None),
):
    """
    Read All Newsletters Endpoint

    :param params: QueryParams
    :param qb: QueryBuilder
    :param db: database connection
    :param order_by: Sorting data
    :return: Newsletter from the database
    """

    query = qb.build(params)

    if order_by:
        query = query.order_by(text(f"{order_by} ASC"))

    return await paginate(db, query)


@router.get(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
    name='get_newsletter',
)
async def get_newsletter(
        pk: ID,
        db_service: NewsletterService = Depends(NewsletterService),
):
    """
    Read Newsletter Endpoint

    :param pk: ID of Newsletter
    :param db_service: database methods
    :return: Newsletter
    """

    try:
        return await db_service.get_item(pk)
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")


@router.post(
    '/',
    dependencies=[Depends(current_active_user)],
    name='create_newsletter',
)
async def create_newsletter(
        object_data: NewslatterSchema,
        db_service: NewsletterService = Depends(NewsletterService),
):
    """
    Create Newsletter Endpoint

    :param object_data: Newsletter data
    :param db_service: database methods
    :return: response
    """
    try:
        return await db_service.create_item(object_data)
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")


@router.delete(
    '/',
    dependencies=[Depends(current_active_user)],
    name='delete_newsletter',
)
async def delete_newsletter(
        pk: ID,
        db_service: NewsletterService = Depends(NewsletterService),
):
    """
    Delete Newsletter Endpoint

    :param pk: ID of Newsletter
    :param db_service: database methods
    :return: response
    """
    try:
        await db_service.delete_item(pk)

        return HTTPException(status_code=200, detail=f"Successfully deleted!")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")
