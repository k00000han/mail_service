from fastapi import status, APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from api.auth.auth import current_active_user
from api.pagination import Page
from api.template.query_builder import TemplateQueryBuilder
from api.template.schemas import TemplateSchema, TemplateParams
from api.template.service import TemplateService
from common.db import get_db
from api.schemas import ID

router = APIRouter()


@router.get(
    "/",
    name="get_all_templates",
    dependencies=[Depends(current_active_user)],
    response_model=Page[TemplateSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_templates(
        params: TemplateParams = Depends(TemplateParams),
        qb: TemplateQueryBuilder = Depends(TemplateQueryBuilder),
        db: AsyncSession = Depends(get_db),
        order_by: str = Query(None),
):
    """
    Read All Templates Endpoint

    :param params: QueryParams
    :param qb: QueryBuilder
    :param db: database connection
    :param order_by: Sorting data
    :return: templates from the database
    """

    query = qb.build(params)

    if order_by:
        query = query.order_by(text(f"{order_by} ASC"))

    return await paginate(db, query)


@router.get(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
)
async def get_template(
        pk: ID,
        db_service: TemplateService = Depends(TemplateService),
):
    """
    Read Template Endpoint

    :param pk: ID of template
    :param db_service: database methods
    :return: template
    """

    template = await db_service.get_item(pk)

    return template


@router.post(
    '/',
    dependencies=[Depends(current_active_user)],
    name='new_template',
)
async def create_template(
        object_data: TemplateSchema,
        db_service: TemplateService = Depends(TemplateService),
):
    """
    Create Template Endpoint

    :param object_data: template data
    :param db_service: database methods
    :return: response
    """

    return await db_service.create_item(object_data)


@router.delete(
    '/',
    dependencies=[Depends(current_active_user)],
    name='delete_template',
)
async def delete_template(
        pk: ID,
        db_service: TemplateService = Depends(TemplateService),
):
    """
    Delete Template Endpoint

    :param pk: ID of template
    :param db_service: database methods
    :return: response
    """

    await db_service.delete_item(pk)
