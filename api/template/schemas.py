from services.schemas import BaseEntitySchema


class TemplateSchema(BaseEntitySchema):
    title: str
    description: str
    html_content: str
