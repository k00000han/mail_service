from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from services.mail_sender import send_html_email
from services.random_template import choose_random_file

router = APIRouter()


@router.post('/send-mail/', name='send_mail', )
async def send_email():
    try:
        html_file = choose_random_file()

        send_html_email.delay(html_file,
                              "test17test01test24@gmail.com",
                              'Hi!',
                              "test16test01test24@gmail.com")

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
