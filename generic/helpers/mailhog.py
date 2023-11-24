from restclient.restclient import Restclient
from requests import Response
import json
import time


def decorator(fn):

    def wrapper(*args, **kwargs):

        for i in range(5):
            response = fn(*args, **kwargs)
            emails = response.json()['items']

            if len(emails) < 5:
                time.sleep(2)
                continue
            else:
                return response

    return wrapper


class MailhogApi:

    def __init__(self, host='http://5.63.153.31:5025'):
        self.host = host
        self.client = Restclient(host=host)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        response = self.client.get(
            path=f"/api/v2/messages",
            params={
                'limit': limit
            }
        )

        return response

    def get_token_from_last_email(self, reset_password: bool = False) -> str:
        """
        Get user activation token from last email
        :return:
        """
        time.sleep(2)
        email = self.get_api_v2_messages(limit=1).json()
        if reset_password is False:
            token_url = json.loads(email['items'][0]['Content']['Body'])['ConfirmationLinkUrl']
        else:
            token_url = json.loads(email['items'][0]['Content']['Body'])['ConfirmationLinkUri']

        token = token_url.split('/')[-1]

        return token

    def get_token_by_login(self, login: str, attempt: int = 5, reset_password: bool = False):
        """
        Getting a token by login
        :param attempt:
        :param reset_password:
        :param login: login
        :return: token
        """
        if attempt == 0:
            raise AssertionError(f'Не удалось получить письмо с логином {login}')

        emails = self.get_api_v2_messages(limit=100).json()['items']

        for email in emails:
            user_data = json.loads(email['Content']['Body'])
            if login == user_data.get('Login') and reset_password is False:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
                return token
            elif login == user_data.get('Login') and reset_password is True:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
                return token

        time.sleep(2)
        return self.get_token_by_login(login=login, attempt=attempt - 1)

    def delete_all_messages(self):
        response = self.client.delete(path='/api/v1/messages')
        return response
