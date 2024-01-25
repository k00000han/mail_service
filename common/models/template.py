import uuid

from sqlalchemy import UUID, String, TEXT
from sqlalchemy.orm import mapped_column

from common.models import Base


class MailTemplate(Base):
    """A model for templates"""

    __tablename__ = "template"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = mapped_column(String(255))
    description = mapped_column(String(255))

    html_content = mapped_column(TEXT)
