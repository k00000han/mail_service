from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse

from api.address_list.router import get_address_list
from api.address_list.service import AddressListService
from api.auth.auth import current_active_user
from api.schemas import ID
from api.template.router import get_template
from api.template.service import TemplateService
from api.token.service import EmailService
from services.mail_sender import send_html_email

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_active_user)],
    name='send_mail',
)
async def send_email(
        address_list_id: ID,
        template_id: ID,
        sender_id: ID,
        subject: str,
        address_list_service: AddressListService = Depends(AddressListService),
        template_service: TemplateService = Depends(TemplateService),
        token_service: EmailService = Depends(EmailService),
):
    """
    This is endpoint which accepts ID of address list and sends mails

    :param address_list_id: list of mail addresses
    :param template_id: template to send
    :param sender_id: id of work email
    :param subject: letter header
    :param address_list_service: address list methods
    :param template_service: template methods
    :param token_service: token methods
    :return: JSONResponse
    """

    try:
        address_list = await get_address_list(address_list_id, address_list_service)
        template = await get_template(template_id, template_service)
        work_email = await token_service.get_item(sender_id)

        for recipient_email in address_list.content:
            send_html_email.delay(work_email.token,
                                  work_email.credentials,
                                  template.html_content,
                                  recipient_email,
                                  subject,
                                  work_email.email)

        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
