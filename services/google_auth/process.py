from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow


class CustomAppFlow(Flow):
    _DEFAULT_AUTH_PROMPT_MESSAGE = (
        "{url}"
    )
    _OOB_REDIRECT_URI = (
        "urn:ietf:wg:oauth:2.0:oob"
    )

    @classmethod
    def from_client_secrets_dict(cls, client_secrets_dict, scopes, **kwargs):
        return cls.from_client_config(client_secrets_dict, scopes=scopes, **kwargs)

    def run_url(
            self,
            authorization_prompt_message=_DEFAULT_AUTH_PROMPT_MESSAGE,
            **kwargs
    ):
        kwargs.setdefault("prompt", "consent")

        self.redirect_uri = self._OOB_REDIRECT_URI

        auth_url, _ = self.authorization_url(**kwargs)

        return authorization_prompt_message.format(url=auth_url)

    def run_token(
            self,
            code,
    ):
        self.redirect_uri = self._OOB_REDIRECT_URI
        self.fetch_token(code=code)

        return self.credentials


class CustomCredentials(Credentials):
    @classmethod
    def from_authorized_user_json(cls, json_data, scopes=None):
        return cls.from_authorized_user_info(json_data, scopes)
