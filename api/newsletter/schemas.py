from typing import Optional, Dict

from api.schemas import BaseEntitySchema, BaseQueryParams, ID


class NewslatterParams(BaseQueryParams):
    """
    This is a Pydentic schema that validates the query for the Newslatter model
    """

    title: Optional[str] = None
    description: Optional[str] = None


class NewslatterSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Newslatter model
    """

    title: Optional[str] = None
    description: Optional[str] = None
    html_template_id: ID
    mailing_base_id: ID
