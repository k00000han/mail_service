from fastapi import FastAPI

from .auth.auth import fastapi_users
from .auth.schemas import UserRead, UserCreate
from .mail.router import router as mail_router

app = FastAPI(title='Mail Service')

app.include_router(mail_router, prefix='/send-mail', tags=['Mails'])


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)


@app.get('/')
def index():
    return {"status": "ok"}

