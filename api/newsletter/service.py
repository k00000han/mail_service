from abc import ABC


from common.models import Newsletter
from common.db_service import EntityService
from api.schemas import ID
from .schemas import NewslatterSchema


class NewsletterService(EntityService[Newsletter, NewslatterSchema], ABC):
    model = Newsletter
    schema = NewslatterSchema

    async def create_or_update_template(self, newslatter_id: ID,
                                        newslatter_data: NewslatterSchema
                                        ) -> NewslatterSchema:
        newslatter = await self.get_item(newslatter_id, raise_exception=False)
        if newslatter is None:
            return await self.create_item(newslatter_data)
        else:
            await self.update_item(newslatter_id, newslatter_data)
        return newslatter
