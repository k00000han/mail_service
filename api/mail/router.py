from fastapi import APIRouter, HTTPException, File, UploadFile
from starlette.responses import JSONResponse

from services.csv_loader import get_emails
from services.mail_sender import send_html_email
from services.random_template import choose_random_file

router = APIRouter()


@router.post(
    '/send-mail/',
    name='send_mail', )
async def send_email(
        sender_email: str,
        subject: str,
        file: UploadFile = File(...),
):
    try:
        email_list = await get_emails(file)

        for recipient_email in email_list:
            html_file = choose_random_file()
            send_html_email.delay(html_file,
                                  recipient_email,
                                  subject,
                                  sender_email)

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
