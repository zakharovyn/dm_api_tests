from dm_api_account.models.put_account_password_model import put_v1_account_password_model
from dm_api_account.models.post_account_password_model import post_account_password_model
from dm_api_account.models.put_account_email_model import put_v1_account_email_model
from dm_api_account.models.post_account_model import post_account_model
from restclient.restclient import Restclient
from requests import Response


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)
        # self.client.session.headers.update(headers) if headers else None

    def post_v1_account(self, json: post_account_model, **kwargs) -> Response:
        """
        Register new user

        :param json registration_model
        :return:
        """
        response = self.client.post(
            path=f"/v1/account",
            json=json,
            **kwargs
        )

        return response

    def get_v1_account(self, **kwargs) -> Response:
        """
        Get current user

        :return:
        """
        response = self.client.get(
            path=f"/v1/account",
            **kwargs
        )

        return response

    def put_v1_account_token(self, token: str, **kwargs) -> Response:
        """
        Activate registered user

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/{token}",
            **kwargs
        )

        return response

    def post_v1_account_password(self, json: post_account_password_model, **kwargs) -> Response:
        """
        Reset registered user password

        :return:
        """
        response = self.client.post(
            path=f"/v1/account/password",
            json=json,
            **kwargs
        )

        return response

    def put_v1_account_password(self, json: put_v1_account_password_model, **kwargs) -> Response:
        """
        Change registered user password

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/password",
            json=json,
            **kwargs
        )

        return response

    def put_v1_account_email(self, json: put_v1_account_email_model, **kwargs) -> Response:
        """
        Change registered user email

        :return:
        """
        response = self.client.put(
            path=f"/v1/account/email",
            json=json,
            **kwargs
        )

        return response
