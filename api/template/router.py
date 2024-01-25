from fastapi import APIRouter, Depends

from api.auth.auth import current_active_user
from api.template.schemas import TemplateSchema
from api.template.service import TemplateService
from services.schemas import ID

router = APIRouter()


@router.get(
    '/{pk}/',
    dependencies=[Depends(current_active_user)],
)
async def get_template(
        pk: ID,
        db_service: TemplateService = Depends(TemplateService),
):
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
    return await db_service.create_item(object_data)
