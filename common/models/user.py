import uuid

from sqlalchemy import UUID, String, Boolean
from sqlalchemy.orm import mapped_column

from common.models.base import Base


class User(Base):
    """A model for user's"""

    __tablename__ = "user"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_name = mapped_column(String(255))
    email = mapped_column(String(50), unique=True)

    hashed_password = mapped_column(String(128))

    is_active = mapped_column(Boolean, default=True)
    is_superuser = mapped_column(Boolean, default=False)
    is_verified = mapped_column(Boolean, default=False)
