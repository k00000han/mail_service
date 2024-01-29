import uuid

from sqlalchemy import UUID, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import mapped_column

from common.models import Base


class AddressList(Base):
    """A model for mailings base"""

    __tablename__ = "address_list"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = mapped_column(String(255))
    description = mapped_column(String(255))
    content = mapped_column(JSON)
