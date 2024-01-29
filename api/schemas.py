from typing import TypeVar, Optional
from uuid import UUID

from pydantic import BaseModel

from common.models import Base

DbEntity = TypeVar("DbEntity", bound=Base)
ID = str | UUID


class BaseEntitySchema(BaseModel):
    id: Optional[UUID] = None

    class Config:
        from_attributes = True


EntitySchema = TypeVar("EntitySchema", bound=BaseEntitySchema)


class BaseQueryParams(BaseModel):
    ...


QueryParams = TypeVar("QueryParams", bound=BaseQueryParams)

