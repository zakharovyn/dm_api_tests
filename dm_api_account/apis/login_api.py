from dm_api_account.models.post_account_login_model import post_account_login_model
from requests import Response, session


class LoginApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.session = session()
        if headers:
            self.session.headers.update(headers)
        # self.session.headers.update(headers) if headers else None

    def post_v1_account_login(self, json: post_account_login_model, **kwargs) -> Response:
        """
        Authenticate via credentials
        :return:
        """

        response = self.session.post(
            url=f"{self.host}/v1/account/login",
            json=json,
            **kwargs
        )

        return response

    def delete_v1_account_login(self, **kwargs) -> Response:
        """
        Logout as current user
        :return:
        """

        response = self.session.delete(
            url=f"{self.host}/v1/account/login",
            **kwargs
        )

        return response

    def delete_v1_account_login_all(self, **kwargs) -> Response:
        """
        Logout from every device
        :return:
        """

        response = self.session.delete(
            url=f"{self.host}/v1/account/login/all",
            **kwargs
        )

        return response
