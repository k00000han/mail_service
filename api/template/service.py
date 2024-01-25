from abc import ABC


from common.models import MailTemplate
from services.db_service import EntityService
from services.schemas import ID
from .schemas import TemplateSchema


class TemplateService(EntityService[MailTemplate, TemplateSchema], ABC):
    model = MailTemplate
    schema = TemplateSchema

    async def create_or_update_template(self, template_id: ID, template_data: TemplateSchema) -> TemplateSchema:
        template = await self.get_item(template_id, raise_exception=False)
        if template is None:
            template_data.html_content.replace('\n', '')
            return await self.create_item(template_data)
        else:
            await self.update_item(template_id, template_data)
        return template
