from typing import Optional, Dict


from api.schemas import BaseEntitySchema, BaseQueryParams


class TokenSchemaParams(BaseQueryParams):
    """
    This is a Pydentic schema that validates the query for the Token model
    """
    email: Optional[str] = None


class EmailSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Token model
    """
    email: Optional[str] = None
    credentials: Optional[Dict] = None


class TokenSchema(BaseEntitySchema):
    """
    This is a Pydentic schema that validates the data for the Token model
    """
    email: Optional[str] = None
    credentials: Optional[Dict] = None
    token: Optional[Dict] = None
