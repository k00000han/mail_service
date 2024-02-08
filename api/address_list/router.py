from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.address_list.query_builder import AddressListQueryBuilder
from api.address_list.schemas import AddressListParams, AddressListSchema
from api.address_list.service import AddressListService
from api.auth.auth import current_active_user
from api.pagination import Page
from api.schemas import ID
from common.db import get_db

router = APIRouter()


@router.get(
    "/",
    name="get_all_address_lists",
    dependencies=[Depends(current_active_user)],
    response_model=Page[AddressListSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_address_lists(
        params: AddressListParams = Depends(AddressListParams),
        qb: AddressListQueryBuilder = Depends(AddressListQueryBuilder),
        db: AsyncSession = Depends(get_db),
        order_by: str = Query(None),
):
    """
    Read All Address Lists Endpoint

    :param params: QueryParams
    :param qb: QueryBuilder
    :param db: database connection
    :param order_by: Sorting data
    :return: address lists from the database
    """

    query = qb.build(params)

    if order_by:
        query = query.order_by(text(f"{order_by} ASC"))

    return await paginate(db, query)


@router.get(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
    name='get_address_list',
)
async def get_address_list(
        pk: ID,
        db_service: AddressListService = Depends(AddressListService),
):
    """
    Read Address List Endpoint

    :param pk: ID of Adress List
    :param db_service: database methods
    :return: Address List
    """

    try:
        return await db_service.get_item(pk)
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")


@router.post(
    '/',
    dependencies=[Depends(current_active_user)],
    name='create_address_list',
)
async def create_address_list(
        object_data: AddressListSchema,
        db_service: AddressListService = Depends(AddressListService),
):
    """
    Create Address List Endpoint

    :param object_data: Address List data
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
    name='delete_address_list',
)
async def delete_address_list(
        pk: ID,
        db_service: AddressListService = Depends(AddressListService),
):
    """
    Delete Address List Endpoint

    :param pk: ID of Address List
    :param db_service: database methods
    :return: response
    """

    try:
        await db_service.delete_item(pk)

        return HTTPException(status_code=200, detail=f"Successfully deleted!")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Internal Server Error: {str(e)}")
