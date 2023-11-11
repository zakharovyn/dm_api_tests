from restclient.restclient import Restclient
from utilites import validate_request_json, validate_status_code
from requests import Response
from ..models import *


class LoginApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.client = Restclient(host=host, headers=headers)
        if headers:
            self.client.session.headers.update(headers)
        # self.client.session.headers.update(headers) if headers else None

    def post_v1_account_login(
            self,
            json: LoginCredentials,
            status_code: int = 200,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Authenticate via credentials
        :return:
        """

        response = self.client.post(
            path=f"/v1/account/login",
            json=validate_request_json(json),
            **kwargs
        )
        validate_status_code(response, status_code)

        if response.status_code == 200:
            return UserEnvelope(**response.json())

        return response

    def delete_v1_account_login(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        """
        Logout as current user
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login",
            **kwargs
        )
        validate_status_code(response, status_code)

        return response

    def delete_v1_account_login_all(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        """
        Logout from every device
        :return:
        """

        response = self.client.delete(
            path=f"/v1/account/login/all",
            **kwargs
        )
        validate_status_code(response, status_code)

        return response
