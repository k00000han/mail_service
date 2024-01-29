from typing import Optional

from api.schemas import BaseEntitySchema, BaseQueryParams


class TemplateParams(BaseQueryParams):
    """
    This is a Pydentic schema that validates the query for the Template model
    """

    title: Optional[str] = None
    description: Optional[str] = None


class TemplateSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Template model
    """
    title: str
    description: str
    html_content: str
