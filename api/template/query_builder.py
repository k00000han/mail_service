from typing import Callable

from sqlalchemy.orm import Query
from sqlalchemy.future import select

from api.query_builder import BaseQueryBuilder
from api.template.schemas import TemplateParams
from common.models import MailTemplate


class TemplateQueryBuilder(BaseQueryBuilder[TemplateParams]):
    def __init__(self):
        self._query = select(MailTemplate)

    def params(self) -> dict[str, Callable[[str | int, Query], Query]]:
        return {
            "title": self.create_filter(MailTemplate.title),
            "description": self.create_filter(MailTemplate.description)
        }
