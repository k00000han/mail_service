from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import httplib2shim

from services.keygen import SCOPES
from tasks import celery_service


@celery_service.task
def send_html_email(token,
                    html_content,
                    recipient_email,
                    subject,
                    sender_email):

    httplib2shim.patch()
    creds = Credentials.from_authorized_user_json(token, SCOPES)
    service = build('gmail', 'v1', credentials=creds)

    sender = sender_email
    to = recipient_email
    message_text = html_content
    msg = create_message(sender, to, subject, message_text)
    send_message(service, "me", msg)


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, "html")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}
