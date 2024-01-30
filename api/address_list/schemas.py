from typing import Optional, List

from api.schemas import BaseEntitySchema, BaseQueryParams


class AddressListParams(BaseQueryParams):
    """
    This is a Pydentic schema that validates the query for the Address list model
    """

    title: Optional[str] = None
    description: Optional[str] = None


class AddressListSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Address list model
    """

    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[List] = None
