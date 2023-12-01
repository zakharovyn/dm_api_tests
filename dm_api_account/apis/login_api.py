from restclient.restclient import Restclient
from utilites import validate_request_json, validate_status_code
from requests import Response
from ..models import *
import allure


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
            need_json: bool = True,
            **kwargs
    ) -> Response | UserEnvelope:
        """
        Authenticate via credentials
        :return:
        """
        with allure.step(f'POST {self.host}/v1/account/login'):
            response = self.client.post(
                path=f"/v1/account/login",
                json=validate_request_json(json),
                **kwargs
            )
        validate_status_code(response, status_code)

        if response.status_code == 200:
            UserEnvelope(**response.json())

        if need_json is True:
            return response
        else:
            return UserEnvelope(**response.json())

    def delete_v1_account_login(
            self,
            status_code: int = 204,
            **kwargs
    ) -> Response:
        """
        Logout as current user
        :return:
        """
        with allure.step(f'DELETE {self.host}/v1/account/login'):
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
        with allure.step(f'DELETE {self.host}/v1/account/login/all'):
            response = self.client.delete(
                path=f"/v1/account/login/all",
                **kwargs
            )
        validate_status_code(response, status_code)

        return response
