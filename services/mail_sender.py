import os
# from . import celery_service
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText
import httplib2shim

from token_gen import SCOPES


# @celery_service.task
def send_html_email(body, email, subject, sender):
    # app = create_celery_app()
    # with app.app_context():

    httplib2shim.patch()
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('/Users/air/PycharmProjects/mail_service/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/air/PycharmProjects/mail_service/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    sender = sender
    to = email
    message_text = body
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
