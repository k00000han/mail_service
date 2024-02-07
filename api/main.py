import random
import string
import time

from fastapi import FastAPI, Depends
from fastapi_pagination import add_pagination
from starlette.requests import Request

from common.log import get_logger
from .auth.auth import fastapi_users, auth_backend, current_active_user
from .auth.schemas import UserRead, UserCreate
from .mail.router import router as mail_router
from .template.router import router as template_router
from .token.router import router as token_router
from .address_list.router import router as adddess_list_router
from .newsletter.router import router as newsletter_router
from .users.router import router as users_router

logger = get_logger(__name__)

app = FastAPI(title='Mail Service')

app.include_router(adddess_list_router, prefix='/address_list', tags=['Address List'])
app.include_router(newsletter_router, prefix='/newsletter', tags=['Newsletter'])
app.include_router(template_router, prefix='/templates', tags=['Templates'])
app.include_router(token_router, prefix='/tokens', tags=['Tokens'])
app.include_router(mail_router, prefix='/send-mail', tags=['Mails'])

app.include_router(users_router, prefix="/users", tags=["Users"])


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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.get("/", dependencies=[Depends(current_active_user)])
def index():
    return {"status": "ok"}

