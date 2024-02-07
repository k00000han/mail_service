from pydantic import BaseModel


class User(BaseModel):
    """
    This is a Pydentic schema that validates current User
    """
    id: str
    user_name: str
    email: str
