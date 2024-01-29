from .base import Base
from .email import WorkEmail
from .adress_list import AddressList
from .newsletter import Newsletter
from .template import MailTemplate
from .user import User

__all__ = [
    "Base",
    "User",
    "WorkEmail",
    "AddressList",
    "Newsletter",
    "MailTemplate",
]
