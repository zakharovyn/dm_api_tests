from dm_api_account.models import LoginCredentials
import allure


class Login:

    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        self.facade.login_api.client.session.headers.update(headers)

    def login_user(self, login: str, password: str, remember_me: bool = True):
        with allure.step('Авторизация пользователя'):
            response = self.facade.login_api.v1_account_login_post(
                login_credentials=LoginCredentials(
                    login=login,
                    password=password,
                    remember_me=remember_me
                )
            )
        return response

    def logout_user(self, **kwargs):
        with allure.step('Выход из учетной записи'):
            response = self.facade.login_api.v1_account_login_delete(**kwargs)
        return response

    def logout_user_from_all_devices(self, **kwargs):
        with allure.step('Выход из учетной записи на всех устройствах'):
            response = self.facade.login_api.v1_account_login_all_delete(**kwargs)
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):

        response = self.login_user(login=login, password=password, remember_me=remember_me)
        token = {'X-Dm-Auth-Token': response.headers['X-Dm-Auth-Token']}

        return token
