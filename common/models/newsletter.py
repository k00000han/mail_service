import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import mapped_column, relationship

from common.models import Base


class Newsletter(Base):
    """A model for mailings base"""

    __tablename__ = "newsletter"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = mapped_column(String(255))
    description = mapped_column(String(255))

    html_template = relationship("template")
    mailing_base = relationship("mailing_base")
