from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from services.mail_sender import send_html_email


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/send-mail/', name='send_mail',)
async def send_email(
    body: str = Body(...),
    email: str = Body(...),
    subject: str = Body(...),
    sender: str = Body(...),
):
    try:
        send_html_email.delay(body, email, subject, sender)

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
