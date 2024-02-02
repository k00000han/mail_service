from typing import Callable

from sqlalchemy.orm import Query
from sqlalchemy.future import select

from api.token.schemas import TokenSchemaParams
from api.query_builder import BaseQueryBuilder
from common.models import WorkEmail


class TokenQueryBuilder(BaseQueryBuilder[TokenSchemaParams]):
    def __init__(self):
        self._query = select(WorkEmail)

    def params(self) -> dict[str, Callable[[str | int, Query], Query]]:
        return {
            "email": self.create_filter(WorkEmail.email),
        }
