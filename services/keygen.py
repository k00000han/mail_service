from google.auth.transport.requests import Request

from services.google_auth.process import CustomAppFlow, CustomCredentials

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
        creds = CustomCredentials.from_authorized_user_json(email.token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = CustomAppFlow.from_client_secrets_dict(email.credentials, SCOPES)
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

    flow = CustomAppFlow.from_client_secrets_dict(email.credentials, SCOPES)
    creds = flow.run_token(code)
    token = creds.to_json()

    return token
