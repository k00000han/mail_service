from abc import ABC


from common.models import AddressList
from common.db_service import EntityService
from api.schemas import ID
from .schemas import AddressListSchema


class AddressListService(EntityService[AddressList, AddressListSchema], ABC):
    model = AddressList
    schema = AddressListSchema

    async def create_or_update_template(self, adress_list_id: ID,
                                        adress_list_data: AddressListSchema
                                        ) -> AddressListSchema:
        adress_list = await self.get_item(adress_list_id, raise_exception=False)
        if adress_list is None:
            return await self.create_item(adress_list_data)
        else:
            await self.update_item(adress_list_id, adress_list_data)
        return adress_list
