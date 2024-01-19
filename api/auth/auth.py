import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    CookieTransport,
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users.authentication import JWTStrategy

from api.auth.manager import get_user_manager
from common.config import SECRET
from common.models import User

cookie_transport = CookieTransport(cookie_name="real_estate", cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# JWT token generation
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=60 * 60 * 24)


# An instance of the AuthenticationBackend class for configuring authentication
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# An instance of the FastAPIUsers class for authentication
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

# Getting the current user
current_active_user = fastapi_users.current_user(active=True, verified=True)
