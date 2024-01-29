from abc import ABC, abstractmethod
from typing import Type, Generic, Any

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from common.db import get_db
from api.schemas import DbEntity, ID, EntitySchema


class EntityService(ABC, Generic[DbEntity, EntitySchema]):
    """
    Implement CRUD operations with DbEntity
    Cast DBEntity to EntitySchema
    """

    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    @property
    @abstractmethod
    def model(self) -> Type[DbEntity]:
        pass

    @property
    @abstractmethod
    def schema(self) -> Type[EntitySchema]:
        pass

    async def _get_db_item(self, pk: ID) -> DbEntity:
        db_object = await self.db.get(self.model, pk)
        return db_object

    async def _create_db_item(self, data: dict[str, Any]) -> DbEntity:
        db_object = self.model(**data)
        self.db.add(db_object)
        await self.db.commit()
        await self.db.refresh(db_object)
        return db_object

    async def _update_db_item(self, pk: ID, data: dict[str, Any]) -> DbEntity:
        db_object = await self._get_db_item(pk)
        for key, value in data.items():
            if key != 'id':
                setattr(db_object, key, value)
        await self.db.commit()
        await self.db.refresh(db_object)
        return db_object

    async def _delete_db_item(self, pk: ID) -> None:
        db_object = await self._get_db_item(pk=pk)
        await self.db.delete(db_object)
        await self.db.commit()

    async def get_item(self, pk: ID, raise_exception=True) -> EntitySchema:
        db_object = await self._get_db_item(pk)
        if not db_object and raise_exception:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
        return await self.db_to_schema(db_object)

    async def db_to_schema(self, db_object: DbEntity) -> EntitySchema:
        return self.schema.model_validate(db_object.to_dict(), from_attributes=True)

    async def create_item(self, data: BaseModel) -> EntitySchema:
        db_object = await self._create_db_item(data.model_dump())
        return await self.db_to_schema(db_object)

    async def update_item(self, pk: ID, data: BaseModel) -> EntitySchema:
        db_object = await self._update_db_item(pk, data.model_dump())
        return await self.db_to_schema(db_object)

    async def delete_item(self, pk: ID, raise_exception=True):
        item = await self.get_item(pk, raise_exception=raise_exception)
        await self._delete_db_item(item.id)
