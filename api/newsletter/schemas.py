from typing import Optional, Dict

from api.schemas import BaseEntitySchema, BaseQueryParams


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
    content: Optional[Dict] = None
