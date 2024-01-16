from fastapi import FastAPI

from .mail.router import router as mail_router

app = FastAPI(title='Mail Service')

app.include_router(mail_router, prefix='/send-mail', tags=['Mails'])


@app.get('/')
def index():
    return {"status": "ok"}

