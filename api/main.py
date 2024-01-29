from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination

from .auth.auth import fastapi_users, auth_backend, current_active_user
from .auth.schemas import UserRead, UserCreate
from .mail.router import router as mail_router
from .template.router import router as template_router
from .token.router import router as token_router

app = FastAPI(title='Mail Service')

app.include_router(mail_router, prefix='/send-mail', tags=['Mails'])
app.include_router(template_router, prefix='/templates', tags=['Templates'])
app.include_router(token_router, prefix='/tokens', tags=['Tokens'])


app.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

add_pagination(app)


@app.get("/", dependencies=[Depends(current_active_user)])
def index():
    return {"status": "ok"}

