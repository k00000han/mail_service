import uuid
from typing import Optional

from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from common.models import Base


class Newsletter(Base):
    """A model for mailings base"""

    __tablename__ = "newsletter"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = mapped_column(String(255))
    description = mapped_column(String(255))

    html_template_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("template.id"), nullable=True)
    mailing_base_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("address_list.id"), nullable=True)
