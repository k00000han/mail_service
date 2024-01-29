from abc import ABC, abstractmethod
from typing import Generic, Callable

from sqlalchemy import Select
from sqlalchemy.orm import Query

from api.schemas import QueryParams


class BaseQueryBuilder(ABC, Generic[QueryParams]):
    _query: Query | Select

    @abstractmethod
    def params(self) -> dict[str, Callable[[str | int, Query], Query]]:
        ...

    def create_filter(self, attr):
        def filter(value: str, query: Query) -> Query:
            if value is not None:
                return query.where(attr == value)
            return query

        return filter

    def build(self, params: QueryParams):
        query = self._query
        param_methods = self.params()

        # Validate that keys in param_methods are valid field names for QueryParams
        valid_keys = set(params.model_fields.keys())
        for k in param_methods.keys():
            if k not in valid_keys:
                raise ValueError(f"Invalid key: {k}. Must be one of {', '.join(valid_keys)}.")

        for k, method in param_methods.items():
            value = getattr(params, k)
            if method and value is not None:
                query = method(value, query)
        return query
