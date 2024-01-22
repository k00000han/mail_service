from fastapi import FastAPI, Depends

from .auth.auth import fastapi_users, auth_backend, current_active_user
from .auth.schemas import UserRead, UserCreate
from .mail.router import router as mail_router

app = FastAPI(title='Mail Service')

app.include_router(mail_router, prefix='/send-mail', tags=['Mails'])


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


@app.get("/", dependencies=[Depends(current_active_user)])
def index():
    return {"status": "ok"}

