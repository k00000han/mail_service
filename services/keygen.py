from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


async def keygen(db, pk):
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
            creds = flow.run_local_server(port=0)

        token = creds.to_json()

        return token
