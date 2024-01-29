from typing import Optional, Dict

from api.schemas import BaseEntitySchema, BaseQueryParams


class AddressListParams(BaseQueryParams):
    """
    This is a Pydentic schema that validates the query for the Template model
    """

    title: Optional[str] = None
    description: Optional[str] = None


class AddressListSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Template model
    """

    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict] = None
