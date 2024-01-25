import uuid

from sqlalchemy import UUID, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import mapped_column

from common.models import Base


class WorkEmail(Base):
    """A model for work emails for mailing"""

    __tablename__ = "work_email"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = mapped_column(String(50), unique=True)
    credentials = mapped_column(JSON)
    token = mapped_column(JSON)
