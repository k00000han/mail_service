from typing import Callable

from sqlalchemy.orm import Query
from sqlalchemy.future import select

from api.newsletter.schemas import NewslatterParams
from api.query_builder import BaseQueryBuilder
from common.models import Newsletter


class NewslatterQueryBuilder(BaseQueryBuilder[NewslatterParams]):
    def __init__(self):
        self._query = select(Newsletter)

    def params(self) -> dict[str, Callable[[str | int, Query], Query]]:
        return {
            "title": self.create_filter(Newsletter.title),
            "description": self.create_filter(Newsletter.description)
        }
