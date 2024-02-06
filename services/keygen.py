from fastapi import HTTPException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


async def generate_url(db, pk):
    """
    Create or Check Token Function

    :param db: database methods
    :param pk: ID of email
    :return: response
    """

    creds = None
    email = await db.get_item(pk)

    if email.token:
        creds = Credentials.from_authorized_user_json(email.token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_dict(email.credentials, SCOPES)
            creds = flow.run_url()

        return creds


async def generate_token(db, pk, code):
    """
    Create Token Function

    :param db: database methods
    :param pk: ID of email
    :param code: code for generate key
    :return: access token
    """

    email = await db.get_item(pk)

    flow = InstalledAppFlow.from_client_secrets_dict(email.credentials, SCOPES)
    creds = flow.run_token(code)
    token = creds.to_json()

    return token
