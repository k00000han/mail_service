from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, class_mapper


class Base(DeclarativeBase):
    type_annotation_map = {dict[str, Any]: JSONB}

    def get_attrs(self):
        return [key for key in vars(self) if not key.startswith('_')]

    def to_dict(self):
        # Getting the list of column names for the derived class
        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]

        # Creating a dictionary with column names as keys and corresponding object attributes as values
        return {col: getattr(self, col) for col in columns}

    def __repr__(self):
        parts = [f'{key}={repr(getattr(self, key))}' for key in self.get_attrs()]
        return f"<{self.__class__.__name__}({', '.join(parts)})>"
