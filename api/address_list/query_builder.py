from typing import Callable

from sqlalchemy.orm import Query
from sqlalchemy.future import select

from api.address_list.schemas import AddressListParams
from api.query_builder import BaseQueryBuilder
from common.models import AddressList


class AddressListQueryBuilder(BaseQueryBuilder[AddressListParams]):
    def __init__(self):
        self._query = select(AddressList)

    def params(self) -> dict[str, Callable[[str | int, Query], Query]]:
        return {
            "title": self.create_filter(AddressList.title),
            "description": self.create_filter(AddressList.description)
        }
